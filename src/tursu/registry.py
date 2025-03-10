import sys
from collections.abc import Mapping
from types import ModuleType
from typing import Callable

import venusian
from typing_extensions import Any

from .exceptions import Unregistered
from .steps import Handler, Step, StepKeyword

VENUSIAN_CATEGORY = "tursu"


def _step(step_name: str, step_pattern: str) -> Callable[[Handler], Handler]:
    def wrapper(wrapped: Handler) -> Handler:
        def callback(scanner: venusian.Scanner, name: str, ob: Handler) -> None:
            if not hasattr(scanner, "registry"):
                return  # coverage: ignore
            scanner.registry.register_handler(step_name, step_pattern, wrapped)  # type: ignore

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)  # type: ignore
        return wrapped

    return wrapper


def given(pattern: str) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the given gherkin keyword.
    """
    return _step("given", pattern)


def when(pattern: str) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the when gherkin keyword.
    """
    return _step("when", pattern)


def then(pattern: str) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the then gherkin keyword.
    """
    return _step("then", pattern)


class StepRegistry:
    """Store all the handlers for gherkin action."""

    def __init__(self) -> None:
        self._handlers: dict[StepKeyword, list[Step]] = {
            "given": [],
            "when": [],
            "then": [],
        }

    def register_handler(
        self, type: StepKeyword, pattern: str, handler: Handler
    ) -> None:
        self._handlers[type].append(Step(pattern, handler))

    def run_step(self, step: StepKeyword, text: str, **kwargs: Any) -> None:
        handlers = self._handlers[step]
        for handler in handlers:
            matches = handler.pattern.get_matches(text, kwargs)
            if matches is not None:
                handler(**matches)
                break
        else:
            raise Unregistered(f"{step.capitalize()} {text}")

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
            raise Unregistered(f"{step.capitalize()} {text}")

    def scan(self, mod: ModuleType | None = None) -> "StepRegistry":
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

        scanner = venusian.Scanner(registry=self)
        scanner.scan(mod, categories=[VENUSIAN_CATEGORY])  # type: ignore
        return self
