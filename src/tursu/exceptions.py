from typing import TYPE_CHECKING

from tursu.steps import StepKeyword

if TYPE_CHECKING:
    from .registry import Tursu


class Unregistered(RuntimeError):
    def __init__(self, registry: "Tursu", step: StepKeyword, text: str):
        registered_list = [
            f"{step} {hdl.pattern.pattern}"
            for hdl in registry._handlers[step]
        ]
        CR = "\n"
        registered_list_str = '\n  - '.join(registered_list)
        super().__init__(
            f"Unregister step:{CR}"
            f"  - {step} {text}{CR}Available steps:{CR}"
            f"  - {registered_list_str}"
        )
