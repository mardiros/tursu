import pytest

from tursu import given, then, when


class DummyApp:
    def __init__(self):
        self.mailboxes: dict[str, dict[str, list[str]]] = {}

    def create_user(self, username: str) -> None:
        assert username not in self.mailboxes
        self.mailboxes[username] = {}

    def add_mailbox(self, username: str, mailbox: str) -> None:
        assert username in self.mailboxes
        self.mailboxes[username][mailbox] = [f"Welcome {username}"]


@given("a user {username}")
def give_user(dummy_app: DummyApp, username: str):
    dummy_app.create_user(username)


@when("{username} create a mailbox {email}")
def create_mailbox(dummy_app: DummyApp, username: str, email: str):
    dummy_app.add_mailbox(username, email)


@then("I see a mailbox {email} for {username}")
def assert_user_has_mailbox(dummy_app: DummyApp, email: str, username: str):
    assert username in dummy_app.mailboxes
    assert email in dummy_app.mailboxes[username]


@then('the mailbox {email} contains "{subject}"')
def assert_mailbox_contains(dummy_app: DummyApp, email: str, subject: str):
    for mailbox in dummy_app.mailboxes.values():
        if email in mailbox:
            assert subject in mailbox[email]
            break
    else:
        pytest.fail(f"mailbox {email} not found or not contains {subject}")
