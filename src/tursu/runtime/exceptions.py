"""Runtime exception"""
from typing import TYPE_CHECKING

from tursu.domain.model.steps import StepKeyword

if TYPE_CHECKING:
    from .registry import Tursu


class Unregistered(RuntimeError):
    """
    Raised when no step definition are found from a gherkin step.

    :param registry: the tursu registry.
    :param step: Keyworkd of the step.
    :param text: the text that did not match any step definition.
    """
    def __init__(self, registry: "Tursu", step: StepKeyword, text: str):
        registered_list = [
            f"{step} {hdl.pattern.pattern}" for hdl in registry._handlers[step]
        ]
        CR = "\n"
        registered_list_str = "\n  - ".join(registered_list)
        super().__init__(
            f"Unregister step:{CR}"
            f"  - {step} {text}{CR}Available steps:{CR}"
            f"  - {registered_list_str}"
        )
