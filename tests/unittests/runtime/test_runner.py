import time
from collections.abc import Iterator

import pytest

from tests.unittests.runtime.fixtures.steps import DummyApp
from tursu.runtime.registry import ModRegistry, Tursu
from tursu.runtime.runner import ScenarioFailed, TursuRunner


@pytest.fixture()
def dummy_app() -> DummyApp:
    return DummyApp()


class TursuRunnerNoLog(TursuRunner):
    def __init__(
        self,
        request: pytest.FixtureRequest,
        capsys: pytest.CaptureFixture[str],
        registry: Tursu,
    ) -> None:
        self.logged_lines: list[str] = []
        super().__init__(request, capsys, registry, ["📄 Document: ..."])

    def log(
        self, text: str, replace_previous_line: bool = False, end: str = "\n"
    ) -> None:
        if replace_previous_line:
            self.logged_lines.append("<UP>")
        self.logged_lines.append(f"{text}{end}")


@pytest.fixture()
def tursu_runner(
    registry: Tursu,
    request: pytest.FixtureRequest,
    capsys: pytest.CaptureFixture[str],
    gherkin_test_module: pytest.Package,
) -> Iterator[TursuRunnerNoLog]:
    oldparent, request.node.parent = request.node.parent, gherkin_test_module
    old_verbose = request.config.option.verbose
    request.config.option.verbose = max(request.config.option.verbose, 1)
    with TursuRunnerNoLog(request, capsys, registry) as runner:
        yield runner
    request.config.option.verbose = old_verbose
    request.node.parent = oldparent


def test_remove_ansi_escape_sequences(tursu_runner: TursuRunner):
    assert tursu_runner.remove_ansi_escape_sequences("\033[91m│\033[0m") == "│"


def test_log(tursu_runner: TursuRunnerNoLog):
    assert tursu_runner.logged_lines == [
        "<UP>",
        "\n",
        "📄 Document: ...\n",
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
    tursu_runner.start_time = time.perf_counter()
    tursu_runner.run_step("Given", "a user Bob", dummy_app=dummy_app)

    assert tursu_runner.runned == [
        "\x1b[92m✅ Given a user \x1b[36mBob\x1b[92m\x1b[0m",
    ]


def test_run_step_error(tursu_runner: TursuRunner, dummy_app: DummyApp):
    tursu_runner.verbose = False
    tursu_runner.start_time = time.perf_counter()
    with pytest.raises(ScenarioFailed):
        tursu_runner.run_step("Then", "X sees a mailbox X", dummy_app=dummy_app)

    assert tursu_runner.runned == [
        "\x1b[91m❌ Then\x1b[0m \x1b[36mX\x1b[91m sees a mailbox "
        "\x1b[36mX\x1b[91m\x1b[0m",
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
    verbose: bool, tursu_runner: TursuRunner, mod_registry: ModRegistry
):
    tursu_runner.verbose = verbose
    tursu_runner.emit_running(
        "Given", mod_registry._step_defs["Given"][1], matches={"username": "bob"}
    )
    assert tursu_runner.runned == [
        "\x1b[90m⏳ Given a user \x1b[36mbob\x1b[90m\x1b[0m",
    ]


@pytest.mark.parametrize(
    "verbose",
    [
        pytest.param(False, id="false"),
        pytest.param(True, id="true"),
    ],
)
def test_emit_error(
    verbose: bool, tursu_runner: TursuRunner, mod_registry: ModRegistry
):
    tursu_runner.runned.append("⏳")
    tursu_runner.verbose = verbose
    tursu_runner.start_time = time.perf_counter()
    tursu_runner.emit_error(
        "Given", mod_registry._step_defs["Given"][1], matches={"username": "bob"}
    )
    assert tursu_runner.runned == [
        "\x1b[91m❌ Given\x1b[0m a user \x1b[36mbob\x1b[91m\x1b[0m",
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
    mod_registry: ModRegistry,
):
    tursu_runner.runned.append("⏳")
    tursu_runner.verbose = verbose
    tursu_runner.start_time = time.perf_counter()
    tursu_runner.emit_success(
        "Given", mod_registry._step_defs["Given"][1], matches={"username": "bob"}
    )
    assert tursu_runner.runned == [
        "\x1b[92m✅ Given a user \x1b[36mbob\x1b[92m\x1b[0m",
    ]


@pytest.mark.parametrize(
    "start_shift,expected",
    [
        pytest.param(TursuRunner.OK_TIMING_MS - 100, "\x1b[92m[600", id="ok"),
        pytest.param(TursuRunner.OK_TIMING_MS + 100, "\x1b[93m[800", id="warn"),
        pytest.param(TursuRunner.WARN_TIMING_MS + 100, "\x1b[91m[2200", id="error"),
    ],
)
def test_emit_success_color(
    start_shift: int,
    expected: str,
    tursu_runner: TursuRunner,
    mod_registry: ModRegistry,
):
    tursu_runner.runned.append("⏳")
    tursu_runner.verbose = 1
    tursu_runner.start_time = time.perf_counter() - start_shift / 1000
    tursu_runner.emit_success(
        "Given", mod_registry._step_defs["Given"][1], matches={"username": "bob"}
    )
    assert expected in tursu_runner.runned[0]
