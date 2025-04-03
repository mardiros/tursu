"""Run a gherkin scenario."""

import logging
import re
import time
from collections.abc import Mapping
from types import TracebackType
from typing import Self

import pytest
from typing_extensions import Any

from tursu.domain.model.steps import StepDefinition, StepKeyword
from tursu.runtime.registry import Tursu

# Set up the logger
logger = logging.getLogger("tursu")
logger.setLevel(logging.DEBUG)


# ANSI color codes
GREEN = "\033[92m"
GREY = "\033[90m"
ORANGE = "\033[93m"
RED = "\033[91m"
CYAN = "\033[36m"

RESET = "\033[0m"  # Reset color
UP = "\033[F"  # Cursor Previous Line
EL = "\033[K"  # Erase in line


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

    IGNORE_TIMING_MS = 200
    OK_TIMING_MS = 700
    WARN_TIMING_MS = 2100

    def __init__(
        self,
        request: pytest.FixtureRequest,
        capsys: pytest.CaptureFixture[str],
        tursu: Tursu,
        scenario: list[str],
    ) -> None:
        self.module_name = request.node.parent.module_name
        self.name = request.node.nodeid
        self.verbose = request.config.option.verbose
        self.tursu = tursu
        self.capsys = capsys
        self.runned: list[str] = []
        self.scenario = scenario
        self.start_time = time.perf_counter()
        self.end_time = time.perf_counter()

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
        top_border = f"{RED}┌" + "─" * (max_line_length + 3) + f"┐{RESET}"
        bottom_border = f"{RED}└" + "─" * (max_line_length + 3) + f"┘{RESET}"

        middle_lines = []
        sep = f"{RED}│{RESET}"
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
                    print(UP, end="")  # coverage: ignore
                print(f"{text}{EL}", end=end)  # coverage: ignore

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
        self,
        keyword: StepKeyword,
        step: StepDefinition,
        matches: Mapping[str, Any],
    ) -> None:
        """
        Update state when a step is marked as running.

        :param keyword: gherkin step keyword.
        :param step: matched step for the tursu registry.
        :param matches: parameters that match for highlighting purpose.
        """
        text = f"{GREY}⏳ {keyword} {step.highlight(matches, CYAN, GREY)}{RESET}"
        self.runned.append(text)
        self.log(text)
        self.start_time = time.perf_counter()

    def emit_error(
        self,
        keyword: StepKeyword,
        step: StepDefinition,
        matches: Mapping[str, Any],
        *,
        unregistered: bool = False,
    ) -> None:
        """
        Update state when a step is marked as error.

        :param keyword: gherkin step keyword.
        :param step: matched step for the tursu registry.
        :param matches: parameters that match for highlighting purpose.
        """
        self.end_time = time.perf_counter()
        elapsed_ms = (self.end_time - self.start_time) * 1000

        timelog = (
            f" {RED}[{elapsed_ms:.2f}ms]"
            if elapsed_ms > self.IGNORE_TIMING_MS or self.verbose > 1
            else ""
        )

        steplog = step.highlight(matches, CYAN, RED)
        text = f"{RED}❌ {keyword}{RESET} {steplog}{timelog}{RESET}"
        if not unregistered:
            self.runned.pop()
        self.runned.append(text)
        self.log(text, True)
        self.log("-" * (len(self.name) + 2), end="")

    def emit_success(
        self, keyword: StepKeyword, step: StepDefinition, matches: Mapping[str, Any]
    ) -> None:
        """
        Update state when a step is marked as success.

        :param keyword: gherkin step keyword.
        :param step: matched step for the tursu registry.
        :param matches: parameters that match for highlighting purpose.
        """

        self.end_time = time.perf_counter()
        elapsed_ms = (self.end_time - self.start_time) * 1000

        if elapsed_ms < self.OK_TIMING_MS:
            color = GREEN
        elif elapsed_ms < self.WARN_TIMING_MS:
            color = ORANGE
        else:
            color = RED

        timelog = (
            f" {color}[{elapsed_ms:.2f}ms]"
            if elapsed_ms > self.IGNORE_TIMING_MS or self.verbose > 1
            else ""
        )

        steplog = step.highlight(matches, CYAN, GREEN)
        text = f"{GREEN}✅ {keyword} {steplog}{timelog}{RESET}"
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
