from typing import Any

import pytest

from tursu.registry import StepRegistry, Unregistered
from tursu.steps import Step
from unittests.fixtures.steps import DummyApp, DummyMail


def test_registry_handler(registry: StepRegistry):
    from unittests.fixtures.steps import (
        assert_api_response,
        assert_dataset,
        assert_mailbox_contains,
        assert_user_has_mailbox,
        create_mailbox,
        give_user,
    )

    assert registry._handlers == {
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


def test_registry_step(request: Any, dummy_app: DummyApp, registry: StepRegistry):
    registry.run_step(request, "given", "a user Bob", dummy_app=dummy_app)
    registry.run_step(
        request, "when", "Bob create a mailbox bob@alice.net", dummy_app=dummy_app
    )
    registry.run_step(
        request, "then", "I see a mailbox bob@alice.net for Bob", dummy_app=dummy_app
    )

    registry.run_step(
        request,
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
        registry.run_step(request, "when", "I see a mailbox bob@alice.net for Bob")

    assert str(ctx.value) == "When I see a mailbox bob@alice.net for Bob"
