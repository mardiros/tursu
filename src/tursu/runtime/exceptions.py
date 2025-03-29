"""Runtime exception"""

import difflib
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


def get_best_matches(
    text: str,
    possibilities: list[str],
    n: int = 5,
    cutoff: float = 0.3,
    lgtm_threshold: float = 0.4,
    sure_threshold: float = 0.5,
) -> list[str]:
    matches = difflib.get_close_matches(text, possibilities, n=n, cutoff=cutoff)
    if len(matches) <= 1:
        return matches

    scored_matches = [
        (difflib.SequenceMatcher(None, text, match).ratio(), match) for match in matches
    ]
    scored_matches.sort(reverse=True)

    if scored_matches[0][0] >= sure_threshold:
        return [scored_matches[0][1]]
    return [match for score, match in scored_matches if score > lgtm_threshold]


class Unregistered(RuntimeError):
    """
    Raised when no step definition are found from a gherkin step.

    :param registry: the tursu registry.
    :param step: Keyworkd of the step.
    :param text: the text that did not match any step definition.
    """

    def __init__(self, registry: "Tursu", step: StepKeyword, text: str):
        registered_list = get_best_matches(
            text,
            [f"Given {hdl.pattern.pattern}" for hdl in registry._handlers["Given"]]
            + [f"When {hdl.pattern.pattern}" for hdl in registry._handlers["When"]]
            + [f"Then {hdl.pattern.pattern}" for hdl in registry._handlers["Then"]],
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
