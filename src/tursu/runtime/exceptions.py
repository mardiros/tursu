"""Runtime exception"""

import textwrap
from typing import TYPE_CHECKING

from tursu.domain.model.steps import StepKeyword

if TYPE_CHECKING:
    from .registry import Tursu

TEMPLATE_WITH_MATCHED_STEPS = """
Unregistered step:

    {step} {text}

Maybe you look for:

    {registered_list_str}

Otherwise, to register this new step:
{create_step}
"""

TEMPLATE_WITHOUT_MATCHED_STEPS = """
Unregistered step:

    {step} {text}

To register this new step:
{create_step}
"""


class Unregistered(RuntimeError):
    """
    Raised when no step definition are found from a gherkin step.

    :param module_name: the test module where the step definition is not registered.
    :param registry: the tursu registry.
    :param step: Keyworkd of the step.
    :param text: the text that did not match any step definition.
    """

    def __init__(
        self, module_name: str, registry: "Tursu", step: StepKeyword, text: str
    ):
        registered_list: list[str] = registry.get_best_matches(module_name, text)

        registered_list_str = "\n    ".join(registered_list)
        safe_text = text.replace('"', '\\"')
        create_step = textwrap.indent(
            textwrap.dedent(
                f"""
                @{step.lower()}("{safe_text}")
                def step_definition(): ...
                """
            ),
            prefix="    ",
        )

        template = (
            TEMPLATE_WITH_MATCHED_STEPS
            if registered_list
            else TEMPLATE_WITHOUT_MATCHED_STEPS
        )
        super().__init__(
            template.format(
                step=step,
                text=text,
                registered_list_str=registered_list_str,
                create_step=create_step,
            )
        )
