import pytest

from tursu.registry import StepRegitry, Unregistered
from tursu.steps import Step
from unittests.fixtures.steps import DummyApp


def test_registry_handler(registry: StepRegitry):
    from unittests.fixtures.steps import (
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
            Step("the mailbox {email} contains {subject}", assert_mailbox_contains),
            Step("I see a mailbox {email} for {username}", assert_user_has_mailbox),
        ],
    }


def test_registry_step(dummy_app: DummyApp, registry: StepRegitry):
    registry.run_step("given", "a user Bob")
    registry.run_step("when", "Bob create a mailbox bob@alice.net")
    registry.run_step("then", "I see a mailbox bob@alice.net for Bob")

    assert dummy_app.mailboxes == {
        "Bob": {
            "bob@alice.net": [
                "Welcome Bob",
            ],
        },
    }

    with pytest.raises(Unregistered) as ctx:
        registry.run_step("when", "I see a mailbox bob@alice.net for Bob")

    assert str(ctx.value) == "When I see a mailbox bob@alice.net for Bob"
