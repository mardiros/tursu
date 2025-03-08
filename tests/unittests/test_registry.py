from tursu.registry import Command, CommandRegitry


def test_registry():
    registry = CommandRegitry()
    registry.scan("unittests.fixtures")

    from unittests.fixtures.steps import (
        assert_mailbox_contains,
        assert_user_has_mailbox,
        create_mailbox,
        give_user,
    )

    assert registry._handlers == {
        "given": [Command("a user {username}", give_user)],
        "then": [
            Command("the mailbox {email} contains {subject}", assert_mailbox_contains),
            Command("I see a mailbox {email} for {username}", assert_user_has_mailbox),
        ],
        "when": [
            Command("I create a mailbox {email}", create_mailbox),
        ],
    }
