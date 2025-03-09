import importlib
from typing import Callable

import venusian

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


class StepRegitry:
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

    def run_step(self, step: StepKeyword, text: str) -> None:
        handlers = self._handlers[step]
        for handler in handlers:
            matches = handler.pattern.get_matches(text)
            if matches is not None:
                handler(**matches)
                break
        else:
            raise Unregistered(f"{step.capitalize()} {text}")

    def scan(
        self,
        *mods: str,
    ) -> None:
        """
        Scan the module (or modules) containing service handlers.

        when a message is handled by the bus, the bus propagate the message
        to hook functions, called :term:`Service Handler` that receive the message,
        and a :term:`Unit Of Work` to process it has a business transaction.
        """
        scanner = venusian.Scanner(registry=self)
        for modname in mods:
            if modname.startswith("."):
                raise ValueError(
                    f"scan error: relative package unsupported for {modname}"
                )
            mod = importlib.import_module(modname)
            scanner.scan(mod, categories=[VENUSIAN_CATEGORY])  # type: ignore
