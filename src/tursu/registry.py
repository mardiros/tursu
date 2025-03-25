import sys
from collections.abc import Mapping
from types import ModuleType
from typing import TYPE_CHECKING, Annotated, Callable, get_args, get_origin

import venusian
from typing_extensions import Any

from tursu.pattern_matcher import AbstractPattern

if TYPE_CHECKING:
    from tursu.runner import TursuRunner

from tursu.domain.model.steps import Handler, Step, StepKeyword

from .exceptions import Unregistered

VENUSIAN_CATEGORY = "tursu"


def _step(
    step_name: str, step_pattern: str | AbstractPattern
) -> Callable[[Handler], Handler]:
    def wrapper(wrapped: Handler) -> Handler:
        def callback(scanner: venusian.Scanner, name: str, ob: Handler) -> None:
            if not hasattr(scanner, "registry"):
                return  # coverage: ignore

            scanner.registry.register_handler(  # type: ignore
                step_name, step_pattern, wrapped
            )

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)
        return wrapped

    return wrapper


def given(pattern: str | AbstractPattern) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the `Given` Gherkin keyword.

    :param pattern: a pattern to extract parameter.
                    Refer to the [pattern matcher documentation](#pattern-matcher)
                    for the syntax.
    :return: the decorate function that have any parameter coming from
             the pattern matcher or pytest fixtures.
    """
    return _step("Given", pattern)


def when(pattern: str | AbstractPattern) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the `When` gherkin keyword.

    :param pattern: a pattern to extract parameter.
                    Refer to the [pattern matcher documentation](#pattern-matcher)
                    for the syntax.
    :return: the decorate function that have any parameter coming from
             the pattern matcher or pytest fixtures.
    """
    return _step("When", pattern)


def then(pattern: str | AbstractPattern) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the `Then` gherkin keyword.

    :param pattern: a pattern to extract parameter.
                    Refer to the [pattern matcher documentation](#pattern-matcher)
                    for the syntax.
    :return: the decorate function that have any parameter coming from
             the pattern matcher or pytest fixtures.
    """
    return _step("Then", pattern)


class Tursu:
    """Store all the handlers for gherkin action."""

    DATA_TABLE_EMPTY_CELL = ""
    """
    This value is used only in case of data_table types usage.
    If the table contains this value, then, it is ommited by the constructor in order
    to let the type default value works.

    In case of list[dict[str,str]], then this is ignored, empty cells exists with
    an empty string value.
    """

    def __init__(self) -> None:
        self.scanned: set[ModuleType] = set()
        self._handlers: dict[StepKeyword, list[Step]] = {
            "Given": [],
            "When": [],
            "Then": [],
        }
        self._data_tables: dict[type, str] = {}

    @property
    def data_tables_types(self) -> dict[type, str]:
        """ "Registered data types, used in order to build imports on tests."""
        return self._data_tables

    def register_handler(
        self, type: StepKeyword, pattern: str | AbstractPattern, handler: Handler
    ) -> None:
        step = Step(pattern, handler)
        self._handlers[type].append(step)
        self.register_data_table(step)

    def register_data_table(self, step: Step) -> None:
        parameter = step.pattern.signature.parameters.get("data_table")
        if parameter and parameter.annotation:
            typ = get_args(parameter.annotation)[0]
            orig = get_origin(typ)
            if orig is not dict:
                if orig is Annotated:
                    typ = get_args(typ)[-1]
                if typ not in self._data_tables:
                    self._data_tables[typ] = f"{typ.__name__}{len(self._data_tables)}"

    def get_step(self, step: StepKeyword, text: str, **kwargs: Any) -> Step | None:
        handlers = self._handlers[step]
        for handler in handlers:
            if handler.pattern.match(text):
                return handler
        return None

    def run_step(
        self, tursu_runner: "TursuRunner", step: StepKeyword, text: str, **kwargs: Any
    ) -> None:
        handlers = self._handlers[step]
        for handler in handlers:
            matches = handler.pattern.get_matches(text, kwargs)
            if matches is not None:
                tursu_runner.emit_running(step, handler, matches)
                try:
                    handler(**matches)
                except Exception:
                    tursu_runner.emit_error(step, handler, matches)
                    raise
                else:
                    tursu_runner.emit_success(step, handler, matches)
                break
        else:
            raise Unregistered(self, step, text)

    def extract_fixtures(
        self, step: StepKeyword, text: str, **kwargs: Any
    ) -> Mapping[str, Any]:
        handlers = self._handlers[step]
        for handler in handlers:
            fixtures = handler.pattern.extract_fixtures(text)
            if fixtures is not None:
                return fixtures
                break
        else:
            raise Unregistered(self, step, text)

    def scan(self, mod: ModuleType | None = None) -> "Tursu":
        """
        Scan the module (or modules) containing steps.
        """
        if mod is None:
            import inspect

            mod = inspect.getmodule(inspect.stack()[1][0])
            assert mod
            module_name = mod.__name__
            if "." in module_name:  # Check if it's a submodule
                parent_name = module_name.rsplit(".", 1)[0]  # Remove the last part
                mod = sys.modules.get(parent_name)

        assert mod
        if mod not in self.scanned:
            self.scanned.add(mod)
            scanner = venusian.Scanner(registry=self)
            scanner.scan(mod, categories=[VENUSIAN_CATEGORY])
        return self
