import pytest

from tursu import Tursu
from tursu.runner import ScenarioFailed, TursuRunner, tursu_runner
from unittests.fixtures.steps import DummyApp

tursu_runner = tursu_runner


def test_remove_ansi_escape_sequences(tursu_runner: TursuRunner):
    assert tursu_runner.remove_ansi_escape_sequences("\033[91m│\033[0m") == "│"


def test_fancy_no_step_runned(tursu_runner: TursuRunner):
    assert (
        tursu_runner.fancy()
        == """
\x1b[91m┌────────────────────────────────┐\033[0m
\033[91m│\033[0m 🔥 TursuRunner: no step runned \033[91m│\033[0m
\033[91m└────────────────────────────────┘\033[0m
"""
    )


def test_fancy_scenario(tursu_runner: TursuRunner):
    tursu_runner.runned = ["Given a user bob"]
    assert (
        tursu_runner.fancy()
        == """
\x1b[91m┌───────────────────┐\033[0m
\033[91m│\033[0m Given a user bob \033[91m│\033[0m
\033[91m└───────────────────┘\033[0m
"""
    )


def test_run_step(tursu_runner: TursuRunner, dummy_app: DummyApp):
    tursu_runner.verbose = False
    tursu_runner.run_step("given", "a user Bob", dummy_app=dummy_app)
    assert tursu_runner.runned == ["\x1b[92m✅ Given a user \x1b[36mBob\x1b[0m\x1b[0m"]


def test_run_step_error(tursu_runner: TursuRunner, dummy_app: DummyApp):
    tursu_runner.verbose = False
    with pytest.raises(ScenarioFailed):
        tursu_runner.run_step("then", "I see a mailbox X for X", dummy_app=dummy_app)
    assert tursu_runner.runned == [
        "\x1b[91m❌ Then I see a mailbox \x1b[36mX\x1b[0m for \x1b[36mX\x1b[0m\x1b[0m"
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
    assert tursu_runner.runned == ["\x1b[90m⏳ Given a user \x1b[36mbob\x1b[0m\x1b[0m"]


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
    assert tursu_runner.runned == ["\x1b[91m❌ Given a user \x1b[36mbob\x1b[0m\x1b[0m"]


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
    assert tursu_runner.runned == ["\x1b[92m✅ Given a user \x1b[36mbob\x1b[0m\x1b[0m"]
