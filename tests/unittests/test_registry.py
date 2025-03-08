from tursu.registry import StepRegitry
from tursu.steps import Step


def test_registry():
    registry = StepRegitry()
    registry.scan("unittests.fixtures")

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
