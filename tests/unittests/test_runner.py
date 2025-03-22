from collections.abc import Iterator

import pytest

from tests.unittests.fixtures.steps import DummyApp
from tursu.domain.model.gherkin import GherkinDocument
from tursu.plugin import tursu_collect_file
from tursu.registry import Tursu
from tursu.runner import ScenarioFailed, TursuRunner


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
    registry: Tursu, request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str]
) -> Iterator[TursuRunnerNoLog]:
    old_verbose = request.config.option.verbose
    request.config.option.verbose = max(request.config.option.verbose, 1)
    with TursuRunnerNoLog(request, capsys, registry) as runner:
        yield runner
    request.config.option.verbose = old_verbose


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
    tursu_runner.run_step("Given", "a user Bob", dummy_app=dummy_app)
    assert tursu_runner.runned == [
        "\x1b[92m✅ Given a user \x1b[36mBob\x1b[0m\x1b[0m",
    ]


def test_run_step_error(tursu_runner: TursuRunner, dummy_app: DummyApp):
    tursu_runner.verbose = False
    with pytest.raises(ScenarioFailed):
        tursu_runner.run_step("Then", "X see a mailbox X", dummy_app=dummy_app)
    assert tursu_runner.runned == [
        "\x1b[91m❌ Then \x1b[36mX\x1b[0m see a mailbox \x1b[36mX\x1b[0m\x1b[0m",
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
    registry: Tursu,
):
    tursu_runner.verbose = verbose
    tursu_runner.emit_running(
        "Given", registry._handlers["Given"][0], matches={"username": "bob"}
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
    registry: Tursu,
):
    tursu_runner.runned.append("⏳")
    tursu_runner.verbose = verbose
    tursu_runner.emit_error(
        "Given", registry._handlers["Given"][0], matches={"username": "bob"}
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
    registry: Tursu,
):
    tursu_runner.runned.append("⏳")
    tursu_runner.verbose = verbose
    tursu_runner.emit_success(
        "Given", registry._handlers["Given"][0], matches={"username": "bob"}
    )
    assert tursu_runner.runned == [
        "\x1b[92m✅ Given a user \x1b[36mbob\x1b[0m\x1b[0m",
    ]


def test_tursu_collect_file(
    tursu: Tursu, doc: GherkinDocument, request: pytest.FixtureRequest
):
    old_handlers = tursu._handlers
    tursu._handlers = {"Given": [], "Then": [], "When": []}
    tursu_collect_file()
    assert "pytest_collect_file" in globals()
    pkg = pytest.Package.from_parent(request.session, path=doc.filepath.parent)
    globals()["pytest_collect_file"](pkg, doc.filepath)
    repr_handlers = {
        "Given": [repr(h) for h in tursu._handlers["Given"]],
        "Then": [repr(h) for h in tursu._handlers["Then"]],
        "When": [repr(h) for h in tursu._handlers["When"]],
    }
    assert repr_handlers == {
        "Given": [
            'Step("a user {username}", give_user)',
        ],
        "Then": [
            'Step("the API for {username} respond", assert_api_response)',
            'Step("the users dataset is", assert_dataset)',
            'Step("the mailbox {email} "{subject}" message is", '
            "assert_mailbox_contains)",
            'Step("{username} see a mailbox {email}", assert_user_has_mailbox)',
        ],
        "When": [
            'Step("{username} create a mailbox {email}", create_mailbox)',
        ],
    }

    # we restore the tursu global registry has its previous step.
    tursu._handlers = old_handlers
