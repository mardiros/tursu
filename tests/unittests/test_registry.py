import pytest

from tursu.registry import StepRegistry, Unregistered
from tursu.steps import Step
from unittests.fixtures.steps import DummyApp, DummyMail


def test_registry_handler(registry: StepRegistry):
    from unittests.fixtures.steps import (
        assert_api_response,
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
            Step('the mailbox {email} "{subject}" message is', assert_mailbox_contains),
            Step("I see a mailbox {email} for {username}", assert_user_has_mailbox),
        ],
    }


async def test_registry_step(dummy_app: DummyApp, registry: StepRegistry):
    await registry.run_step("given", "a user Bob", dummy_app=dummy_app)
    await registry.run_step("when", "Bob create a mailbox bob@alice.net", dummy_app=dummy_app)
    await registry.run_step(
        "then", "I see a mailbox bob@alice.net for Bob", dummy_app=dummy_app
    )

    await registry.run_step(
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
        await registry.run_step("when", "I see a mailbox bob@alice.net for Bob")

    assert str(ctx.value) == "When I see a mailbox bob@alice.net for Bob"
