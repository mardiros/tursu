import textwrap

import pytest

from tests.unittests.conftest import DummyApp, DummyMail
from tests.unittests.fixtures.steps import (
    assert_api_response,
    assert_dataset,
    assert_mailbox_contains,
    assert_user_has_mailbox,
    create_mailbox,
    give_user,
)
from tursu.registry import Tursu, Unregistered
from tursu.runner import TursuRunner
from tursu.steps import Step


@pytest.fixture()
def tursu_runner(
    registry: Tursu, request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str]
) -> TursuRunner:
    return TursuRunner(request, capsys, registry, ["📄 Document: ..."])


def test_registry_handler(registry: Tursu):
    assert registry._handlers == {
        "Given": [Step("a user {username}", give_user)],
        "When": [
            Step("{username} create a mailbox {email}", create_mailbox),
        ],
        "Then": [
            Step("the API for {username} respond", assert_api_response),
            Step("the users dataset is", assert_dataset),
            Step('the mailbox {email} "{subject}" message is', assert_mailbox_contains),
            Step("{username} see a mailbox {email}", assert_user_has_mailbox),
        ],
    }


def test_registry_step(tursu_runner: TursuRunner, dummy_app: DummyApp, registry: Tursu):
    registry.run_step(tursu_runner, "Given", "a user Bob", dummy_app=dummy_app)
    registry.run_step(
        tursu_runner, "When", "Bob create a mailbox bob@alice.net", dummy_app=dummy_app
    )
    registry.run_step(
        tursu_runner,
        "Then",
        "Bob see a mailbox bob@alice.net",
        dummy_app=dummy_app,
    )

    registry.run_step(
        tursu_runner,
        "Then",
        "the API for Bob respond",
        dummy_app=dummy_app,
        doc_string=[
            {"email": "bob@alice.net", "subject": "Welcome Bob", "body": "..."}
        ],
    )

    assert dummy_app.mailboxes == {
        "Bob": [
            DummyMail(email="bob@alice.net", subject="Welcome Bob", body="..."),
        ],
    }

    with pytest.raises(Unregistered) as ctx:
        registry.run_step(tursu_runner, "When", "Bob see a mailbox bob@alice.net")

    assert str(ctx.value) == (
        """\
Unregister step:
  - When Bob see a mailbox bob@alice.net
Available steps:
  - When {username} create a mailbox {email}
""".strip()
    )

    assert (
        tursu_runner.remove_ansi_escape_sequences(tursu_runner.fancy())
        == """
┌────────────────────────────────────────────┐
│ 📄 Document: ...                           │
│ ✅ Given a user Bob                        │
│ ✅ When Bob create a mailbox bob@alice.net │
│ ✅ Then Bob see a mailbox bob@alice.net    │
│ ✅ Then the API for Bob respond            │
└────────────────────────────────────────────┘
"""
    )


def test_registry_step_unregistered_extract_fixtures(
    tursu_runner: TursuRunner, dummy_app: DummyApp, registry: Tursu
):
    with pytest.raises(Unregistered) as ctx:
        registry.extract_fixtures("Given", "a nickname Bob", dummy_app=dummy_app)
    assert (
        str(ctx.value)
        == textwrap.dedent("""
            Unregister step:
              - Given a nickname Bob
            Available steps:
              - Given a user {username}
            """).strip()
    )
