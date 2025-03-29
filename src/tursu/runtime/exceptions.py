"""Runtime exception"""

import textwrap
from difflib import get_close_matches
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
        registered_list = get_close_matches(
            text,
            [f"Given {hdl.pattern.pattern}" for hdl in registry._handlers["Given"]]
            + [f"When {hdl.pattern.pattern}" for hdl in registry._handlers["When"]]
            + [f"Then {hdl.pattern.pattern}" for hdl in registry._handlers["Then"]],
            cutoff=0.3,
        )
        registered_list_str = "\n    ".join(registered_list)

        create_step = textwrap.indent(
            textwrap.dedent(
                f"""
                @{step.lower()}("{text.replace('"', '\\"')}")
                def step_definition(): ...
                """
            ),
            prefix="    ",
        )

        super().__init__(
            textwrap.dedent(
                f"""
                Unregistered step:

                    {step} {text}

                Maybe you look for:

                    {{registered_list_str}}

                Or you want to register a new step:
                {{create_step}}
                """
            ).format(registered_list_str=registered_list_str, create_step=create_step)
        )
