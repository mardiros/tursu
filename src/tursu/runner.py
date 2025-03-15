import logging
import re
from collections.abc import Mapping
from types import TracebackType
from typing import Self

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
        request: pytest.FixtureRequest,
        capsys: pytest.CaptureFixture[str],
        tursu: Tursu,
        scenario: list[str],
    ) -> None:
        self.name = request.node.nodeid
        self.verbose = request.config.option.verbose
        self.tursu = tursu
        self.capsys = capsys
        self.runned: list[str] = []
        self.scenario = scenario
        if self.verbose:
            self.log("", replace_previous_line=True)
            for step in self.scenario:
                self.log(step)

    def remove_ansi_escape_sequences(self, text: str) -> str:
        return re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", text)

    def fancy(self) -> str:
        lines: list[str] = self.runned or ["🔥 no step runned"]
        lines = self.scenario + lines
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

    def log(
        self, text: str, replace_previous_line: bool = False, end: str = "\n"
    ) -> None:
        if self.verbose:  # coverage: ignore
            with self.capsys.disabled():  # coverage: ignore
                if replace_previous_line and self.verbose == 1:  # coverage: ignore
                    print("\033[F", end="")  # coverage: ignore
                print(f"{text}\033[K", end=end)  # coverage: ignore

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
        self.log("-" * (len(self.name) + 2), end="")

    def emit_success(
        self, keyword: StepKeyword, step: Step, matches: Mapping[str, Any]
    ) -> None:
        text = f"\033[92m✅ {keyword.capitalize()} {step.highlight(matches)}\033[0m"
        self.runned.pop()
        self.runned.append(text)
        self.log(text, True)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.log(" " * (len(self.name) + 2), end="")
