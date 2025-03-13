import contextlib

import pytest
from typing_extensions import Generator

from tursu import Tursu
from tursu.runner import ScenarioFailed, TursuRunner
from unittests.fixtures.steps import DummyApp


class CapsysMock(pytest.CaptureFixture[str]):
    @contextlib.contextmanager
    def disabled(self) -> Generator[None]:
        yield


class TursuRunnerNoLog(TursuRunner):
    def __init__(
        self,
        request: pytest.FixtureRequest,
        capsys: pytest.CaptureFixture[str],
        tursu: Tursu,
    ) -> None:
        self.logged_lines: list[str] = []
        super().__init__(request, capsys, tursu, ["📄 Document: ..."])

    def log(
        self, text: str, remove_previous_line: bool = False, end: str = "\n"
    ) -> None:
        if remove_previous_line:
            self.logged_lines.append("<UP>")
        self.logged_lines.append(f"{text}{end}")


@pytest.fixture()
def tursu_runner(
    tursu: Tursu, request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str]
) -> TursuRunnerNoLog:
    request.config.option.verbose = 1
    with TursuRunnerNoLog(request, capsys, tursu) as runner:
        return runner


def test_remove_ansi_escape_sequences(tursu_runner: TursuRunner):
    assert tursu_runner.remove_ansi_escape_sequences("\033[91m│\033[0m") == "│"


def test_log(tursu_runner: TursuRunnerNoLog):
    assert tursu_runner.logged_lines == [
        # remove the python file name when verbose
        # emit line up
        "<UP>",
        # write white space instead
        "                                          \n",
        # write the scenario here
        # remove the python file name when verbose
        "📄 Document: ...\n",
        "                                          ",
    ]


def test_fancy_no_step_runned(tursu_runner: TursuRunner):
    assert (
        tursu_runner.fancy()
        == """
\x1b[91m┌───────────────────┐\033[0m
\033[91m│\033[0m 📄 Document: ...  \033[91m│\033[0m
\033[91m│\033[0m 🔥 no step runned \033[91m│\033[0m
\033[91m└───────────────────┘\033[0m
"""
    )


def test_fancy_scenario(tursu_runner: TursuRunner):
    tursu_runner.runned = ["Given a user bob"]
    assert (
        tursu_runner.fancy()
        == """
\x1b[91m┌───────────────────┐\033[0m
\033[91m│\033[0m 📄 Document: ...  \033[91m│\033[0m
\033[91m│\033[0m Given a user bob \033[91m│\033[0m
\033[91m└───────────────────┘\033[0m
"""
    )


def test_run_step(tursu_runner: TursuRunner, dummy_app: DummyApp):
    tursu_runner.verbose = False
    tursu_runner.run_step("given", "a user Bob", dummy_app=dummy_app)
    assert tursu_runner.runned == [
        "\x1b[92m✅ Given a user \x1b[36mBob\x1b[0m\x1b[0m",
    ]


def test_run_step_error(tursu_runner: TursuRunner, dummy_app: DummyApp):
    tursu_runner.verbose = False
    with pytest.raises(ScenarioFailed):
        tursu_runner.run_step("then", "I see a mailbox X for X", dummy_app=dummy_app)
    assert tursu_runner.runned == [
        "\x1b[91m❌ Then I see a mailbox \x1b[36mX\x1b[0m for \x1b[36mX\x1b[0m\x1b[0m",
    ]


def test_format_example_step(tursu_runner: TursuRunner):
    assert (
        tursu_runner.format_example_step(
            "a username <user1> and a username <user2>", user1="Alice", user2="Bob"
        )
        == "a username Alice and a username Bob"
    )


@pytest.mark.parametrize(
    "verbose",
    [
        pytest.param(False, id="false"),
        pytest.param(True, id="true"),
    ],
)
def test_emit_running(
    verbose: bool,
    tursu_runner: TursuRunner,
    tursu: Tursu,
):
    tursu_runner.verbose = verbose
    tursu_runner.emit_running(
        "given", tursu._handlers["given"][0], matches={"username": "bob"}
    )
    assert tursu_runner.runned == [
        "\x1b[90m⏳ Given a user \x1b[36mbob\x1b[0m\x1b[0m",
    ]


@pytest.mark.parametrize(
    "verbose",
    [
        pytest.param(False, id="false"),
        pytest.param(True, id="true"),
    ],
)
def test_emit_error(
    verbose: bool,
    tursu_runner: TursuRunner,
    tursu: Tursu,
):
    tursu_runner.runned.append("⏳")
    tursu_runner.verbose = verbose
    tursu_runner.emit_error(
        "given", tursu._handlers["given"][0], matches={"username": "bob"}
    )
    assert tursu_runner.runned == [
        "\x1b[91m❌ Given a user \x1b[36mbob\x1b[0m\x1b[0m",
    ]


@pytest.mark.parametrize(
    "verbose",
    [
        pytest.param(False, id="false"),
        pytest.param(True, id="true"),
    ],
)
def test_emit_success(
    verbose: bool,
    tursu_runner: TursuRunner,
    tursu: Tursu,
):
    tursu_runner.runned.append("⏳")
    tursu_runner.verbose = verbose
    tursu_runner.emit_success(
        "given", tursu._handlers["given"][0], matches={"username": "bob"}
    )
    assert tursu_runner.runned == [
        "\x1b[92m✅ Given a user \x1b[36mbob\x1b[0m\x1b[0m",
    ]
