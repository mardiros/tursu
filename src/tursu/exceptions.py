from typing import TYPE_CHECKING

from tursu.steps import StepKeyword

if TYPE_CHECKING:
    from .registry import Tursu


class Unregistered(RuntimeError):
    def __init__(self, registry: "Tursu", step: StepKeyword, text: str):
        registered_list = [
            f"{step.capitalize()} {hdl.pattern.pattern}"
            for hdl in registry._handlers[step]
        ]
        super().__init__(
            f"Unregister step:\n  - {step.capitalize()} {text}\nAvailable steps:\n"
            f"  - {'\n  - '.join(registered_list)}"
        )
