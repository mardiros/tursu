import logging
import re
from collections.abc import Mapping

import pytest
from typing_extensions import Any

from tursu.registry import Tursu
from tursu.steps import Step, StepKeyword

# Set up the logger
logger = logging.getLogger("tursu")
logger.setLevel(logging.DEBUG)


class ScenarioFailed(Exception): ...


class TursuRunner:
    def __init__(
        self,
        tursu: Tursu,
        request: pytest.FixtureRequest,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        self.verbose = request.config.option.verbose
        self.tursu = tursu
        self.capsys = capsys
        self.runned: list[str] = []

    def remove_ansi_escape_sequences(self, text: str) -> str:
        return re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", text)

    def fancy(self) -> str:
        lines: list[str] = self.runned or ["🔥 TursuRunner: no step runned"]
        line_lengthes = [len(self.remove_ansi_escape_sequences(line)) for line in lines]
        max_line_length = max(line_lengthes)

        # Create the border based on the longest line
        top_border = "\033[91m┌" + "─" * (max_line_length + 3) + "┐\033[0m"
        bottom_border = "\033[91m└" + "─" * (max_line_length + 3) + "┘\033[0m"

        middle_lines = []
        sep = "\033[91m│\033[0m"
        for line, length in zip(lines, line_lengthes):
            middle_lines.append(
                f"{sep} {line + ' ' * (max_line_length - length)} {sep}"
            )

        middle_lines_str = "\n".join(middle_lines)
        return f"\n{top_border}\n{middle_lines_str}\n{bottom_border}\n"

    def log(self, text: str, remove_previous_line: bool = False) -> None:
        if self.verbose:
            with self.capsys.disabled():
                if remove_previous_line and self.verbose == 1:
                    print("\033[F", end="")
                    print("\033[K", end="")
                print(text)

    def run_step(
        self,
        step: StepKeyword,
        text: str,
        **kwargs: Any,
    ) -> None:
        try:
            self.tursu.run_step(self, step, text, **kwargs)
        except Exception as exc:
            raise ScenarioFailed(self.fancy()) from exc

    def format_example_step(self, text: str, **kwargs: Any) -> str:
        for key, val in kwargs.items():
            text = text.replace(f"<{key}>", val)
        return text

    def emit_running(
        self, keyword: StepKeyword, step: Step, matches: Mapping[str, Any]
    ) -> None:
        text = f"\033[90m⏳ {keyword.capitalize()} {step.highlight(matches)}\033[0m"
        self.runned.append(text)
        self.log(text)

    def emit_error(
        self,
        keyword: StepKeyword,
        step: Step,
        matches: Mapping[str, Any],
    ) -> None:
        text = f"\033[91m❌ {keyword.capitalize()} {step.highlight(matches)}\033[0m"
        self.runned.pop()
        self.runned.append(text)
        self.log(text, True)

    def emit_success(
        self, keyword: StepKeyword, step: Step, matches: Mapping[str, Any]
    ) -> None:
        text = f"\033[92m✅ {keyword.capitalize()} {step.highlight(matches)}\033[0m"
        self.runned.pop()
        self.runned.append(text)
        self.log(text, True)


@pytest.fixture()
def tursu_runner(
    tursu: Tursu, request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str]
) -> TursuRunner:
    return TursuRunner(tursu, request, capsys)
