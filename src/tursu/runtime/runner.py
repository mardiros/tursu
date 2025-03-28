"""Run a gherkin scenario."""

import logging
import re
from collections.abc import Mapping
from types import TracebackType
from typing import Self

import pytest
from typing_extensions import Any

from tursu.domain.model.steps import Step, StepKeyword
from tursu.runtime.registry import Tursu

# Set up the logger
logger = logging.getLogger("tursu")
logger.setLevel(logging.DEBUG)


class ScenarioFailed(Exception):
    """Scenario failure error."""


class TursuRunner:
    """
    Run the scenario in a context manager.

    :param request: the pytest request fixture.
    :param capsys: the pytest capsys fixture.
    :param tursu: the tursu registry.
    :param scenario: the stack list of gherkin sentence run for display purpose.
    """

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
        """
        Sanitize text of terminal decoration.

        :param text: the text to cleanup.
        """
        return re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", text)

    def fancy(self) -> str:
        """Terminal fancy representation of the current state of the runner."""
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
        """Helper method to log line."""
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
        """
        Will run the given step using the tursu registry, raised an error if its fail.

        :param step: gherkin keyword.
        :param text: text that should match a step definition.

        :raises ScenarioFailed: if the step did not run properly.
        """
        try:
            self.tursu.run_step(self, step, text, **kwargs)
        # FIXME this should be a spacial cases
        # except Unregistered as exc:
        #     raise ScenarioFailed(self.fancy()) from exc
        except Exception as exc:
            raise ScenarioFailed(self.fancy()) from exc

    def format_example_step(self, text: str, **kwargs: Any) -> str:
        """
        Format the scenario outline with args that comes from the parametrized mark.

        :param text: gherkin step from scenario file.
        :param **kwargs: example line for the Examples of the scenario outline.
        """
        for key, val in kwargs.items():
            text = text.replace(f"<{key}>", val)
        return text

    def emit_running(
        self, keyword: StepKeyword, step: Step, matches: Mapping[str, Any]
    ) -> None:
        """
        Update state when a step is marked as running.

        :param keyword: gherkin step keyword.
        :param step: matched step for the tursu registry.
        :param matches: parameters that match for highlighting purpose.
        """
        text = f"\033[90m⏳ {keyword} {step.highlight(matches)}\033[0m"
        self.runned.append(text)
        self.log(text)

    def emit_error(
        self,
        keyword: StepKeyword,
        step: Step,
        matches: Mapping[str, Any],
    ) -> None:
        """
        Update state when a step is marked as error.

        :param keyword: gherkin step keyword.
        :param step: matched step for the tursu registry.
        :param matches: parameters that match for highlighting purpose.
        """
        text = f"\033[91m❌ {keyword} {step.highlight(matches)}\033[0m"
        self.runned.pop()
        self.runned.append(text)
        self.log(text, True)
        self.log("-" * (len(self.name) + 2), end="")

    def emit_success(
        self, keyword: StepKeyword, step: Step, matches: Mapping[str, Any]
    ) -> None:
        """
        Update state when a step is marked as success.

        :param keyword: gherkin step keyword.
        :param step: matched step for the tursu registry.
        :param matches: parameters that match for highlighting purpose.
        """
        text = f"\033[92m✅ {keyword} {step.highlight(matches)}\033[0m"
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
