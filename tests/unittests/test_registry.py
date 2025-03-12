import pytest

from tursu.registry import Tursu, Unregistered
from tursu.runner import TursuRunner, tursu_runner
from tursu.steps import Step
from unittests.fixtures.steps import DummyApp, DummyMail

tursu_runner = tursu_runner  # ignore import error for the imported and used fixture


def test_registry_handler(tursu: Tursu):
    from unittests.fixtures.steps import (
        assert_api_response,
        assert_dataset,
        assert_mailbox_contains,
        assert_user_has_mailbox,
        create_mailbox,
        give_user,
    )

    assert tursu._handlers == {
        "given": [Step("a user {username}", give_user)],
        "when": [
            Step("{username} create a mailbox {email}", create_mailbox),
        ],
        "then": [
            Step("the API for {username} respond", assert_api_response),
            Step("the users dataset is", assert_dataset),
            Step('the mailbox {email} "{subject}" message is', assert_mailbox_contains),
            Step("I see a mailbox {email} for {username}", assert_user_has_mailbox),
        ],
    }


def test_registry_step(tursu_runner: TursuRunner, dummy_app: DummyApp, tursu: Tursu):
    tursu.run_step(tursu_runner, "given", "a user Bob", dummy_app=dummy_app)
    tursu.run_step(
        tursu_runner, "when", "Bob create a mailbox bob@alice.net", dummy_app=dummy_app
    )
    tursu.run_step(
        tursu_runner,
        "then",
        "I see a mailbox bob@alice.net for Bob",
        dummy_app=dummy_app,
    )

    tursu.run_step(
        tursu_runner,
        "then",
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
        tursu.run_step(tursu_runner, "when", "I see a mailbox bob@alice.net for Bob")

    assert str(ctx.value) == "When I see a mailbox bob@alice.net for Bob"

    assert (
        tursu_runner.remove_ansi_escape_sequences(tursu_runner.fancy())
        == """
┌───────────────────────────────────────────────┐
│ ✅ Given a user Bob                           │
│ ✅ When Bob create a mailbox bob@alice.net    │
│ ✅ Then I see a mailbox bob@alice.net for Bob │
│ ✅ Then the API for Bob respond               │
└───────────────────────────────────────────────┘
"""
    )
