from tursu.registry import Command, CommandRegitry


def test_registry():
    registry = CommandRegitry()
    registry.scan("unittests.fixtures")

    from unittests.fixtures.steps import give_user

    assert registry._handlers == {
        "given": [Command("a user {username}", give_user)],
        "when": [],
        "then": [],
    }
