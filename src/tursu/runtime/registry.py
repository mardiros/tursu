"""Registry of step definition."""

import difflib
import sys
from collections.abc import Mapping, Sequence
from inspect import Parameter
from types import ModuleType
from typing import TYPE_CHECKING, Annotated, Callable, get_args, get_origin

import venusian
from typing_extensions import Any

from tursu.domain.model.steps import Handler, Step, StepKeyword
from tursu.runtime.pattern_matcher import AbstractPattern

if TYPE_CHECKING:
    from tursu.runtime.runner import TursuRunner

from tursu.runtime.exceptions import Unregistered

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
                    Refer to the [step definition documentation](#step-definition)
                    for the syntax.
    :return: the decorate function that have any parameter coming from
             the pattern matcher or pytest fixtures.
    """
    return _step("Given", pattern)


def when(pattern: str | AbstractPattern) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the `When` gherkin keyword.

    :param pattern: a pattern to extract parameter.
                    Refer to the [step definition documentation](#step-definition)
                    for the syntax.
    :return: the decorate function that have any parameter coming from
             the pattern matcher or pytest fixtures.
    """
    return _step("When", pattern)


def then(pattern: str | AbstractPattern) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the `Then` gherkin keyword.

    :param pattern: a pattern to extract parameter.
                    Refer to the [step definition documentation](#step-definition)
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
        self._models_types: dict[type, str] = {}

    def get_fixtures(self) -> Mapping[str, type]:
        fixtures: dict[str, type] = {}
        for handlers in self._handlers.values():
            for handler in handlers:
                fixtures.update(handler.fixtures)
        return fixtures

    @property
    def models_types(self) -> dict[type, str]:
        """
        Registered data types, used in order to build imports on tests.
        The type are aliased during registration to avoid conflict name at import time
        during the ast generation.

        :return: type as key, alias as value.
        """

        return self._models_types

    def register_handler(
        self, type: StepKeyword, pattern: str | AbstractPattern, handler: Handler
    ) -> None:
        """
        Register a step handler for a step definition.

        This method is the primitive for [@given](#tursu.given),
        [@when](#tursu.when) and [@then](#tursu.then) decorators.

        :param type: gherkin keyword for the definition.
        :param pattern: pattern to match the definition.
        :param handler: function called when a step in a scenario match the pattern.
        """
        step = Step(pattern, handler)
        self._handlers[type].append(step)
        self.register_data_table(step)
        self.register_doc_string(step)

    def register_model(self, parameter: Parameter | None) -> None:
        """
        Register the model in the parameter of a signature for data_table or doc_string.
        """
        if parameter and parameter.annotation:
            param_origin = get_origin(parameter.annotation)
            if param_origin is Annotated:
                # we are in a factory
                typ = get_args(parameter.annotation)[-1]
            elif param_origin and issubclass(param_origin, Sequence):
                # we are in a list
                typ = get_args(parameter.annotation)[0]
                item_orig = get_origin(typ)
                if item_orig is not dict:
                    if item_orig is Annotated:
                        # the list has a factory
                        typ = get_args(typ)[-1]
            else:
                # this is a reversed data_table, there should be two column
                typ = parameter.annotation

            if typ.__module__ != "builtins" and typ not in self._models_types:
                self._models_types[typ] = f"{typ.__name__}{len(self._models_types)}"

    def register_data_table(self, step: Step) -> None:
        """
        This method register the data table as a model.

        :param step: The step containing a data_table parameter.
        """
        self.register_model(step.pattern.signature.parameters.get("data_table"))

    def register_doc_string(self, step: Step) -> None:
        """
        This method register the doc string as a model.

        :param step: The step containing a doc_string parameter.
        """
        self.register_model(step.pattern.signature.parameters.get("doc_string"))

    def get_step(self, step: StepKeyword, text: str) -> Step | None:
        """
        Get the first registered step that match the text.

        :param type: gherkin keyword for the definition.
        :param text: text to match the definition.
        :return: the register step if exists otherwise None.
        """
        handlers = self._handlers[step]
        for handler in handlers:
            if handler.pattern.match(text):
                return handler
        return None

    def get_best_matches(
        self,
        text: str,
        n: int = 5,
        cutoff: float = 0.3,
        lgtm_threshold: float = 0.4,
        sure_threshold: float = 0.7,
    ) -> Sequence[str]:
        """
        Return the gherkin steps from the registry that look like the given text.
        This method is called if no step definition matches to build a proper hint
        for the user.

        :param text: text to match the definition.
        """
        possibilities = [
            *[f"Given {hdl.pattern.pattern}" for hdl in self._handlers["Given"]],
            *[f"When {hdl.pattern.pattern}" for hdl in self._handlers["When"]],
            *[f"Then {hdl.pattern.pattern}" for hdl in self._handlers["Then"]],
        ]
        matches = difflib.get_close_matches(text, possibilities, n=n, cutoff=cutoff)
        if len(matches) <= 1:
            return matches

        scored_matches = [
            (difflib.SequenceMatcher(None, text, match).ratio(), match)
            for match in matches
        ]
        scored_matches.sort(reverse=True)

        if scored_matches[0][0] >= sure_threshold:
            return [match for score, match in scored_matches if score > sure_threshold]
        return [match for score, match in scored_matches if score > lgtm_threshold]

    def run_step(
        self, tursu_runner: "TursuRunner", step: StepKeyword, text: str, **kwargs: Any
    ) -> None:
        """
        Run the step that match the parameter and emit information to the runner.

        :param tursu_runner: the fixtures pytest fixtures from the test function.
        :param step: gherkin step to match.
        :param text: text to match the definition.
        :param kwargs: the fixtures pytest fixtures from the test function.
        """
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
            tursu_runner.emit_error(
                step, Step(text, lambda: None), {}, unregistered=True
            )
            raise Unregistered(self, step, text)

    def extract_fixtures(
        self, step: StepKeyword, text: str, **kwargs: Any
    ) -> Mapping[str, Any]:
        """
        Extract fixture for a step from the given pytest fixtures of the test function.

        :param step: gherkin step to match.
        :param text: text to match the definition.
        :param kwargs: the fixtures pytest fixtures from the test function.
        :return: the fixtures for the step handler.
        """
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

        :return: the current tursu registry for multiple scan purpose.
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
