import importlib
from typing import Callable, Literal

import venusian
from typing_extensions import Any

VENUSIAN_CATEGORY = "tursu"

Keyword = Literal["given", "when", "then"]
Handler = Callable[..., None]


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


class Command:
    def __init__(self, pattern: str, hook: Handler):
        self.pattern = pattern
        self.hook = hook

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Command):
            return False
        return self.pattern == other.pattern and self.hook == other.hook

    def __repr__(self):
        return f'Command("{self.pattern}", {self.hook.__qualname__})'

class CommandRegitry:
    """Store all the handlers for gherkin action."""

    def __init__(self) -> None:
        self._handlers: dict[Keyword, list[Command]] = {
            "given": [],
            "when": [],
            "then": [],
        }

    def register_handler(self, type: Keyword, pattern: str, handler: Handler) -> None:
        self._handlers[type].append(Command(pattern, handler))

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
