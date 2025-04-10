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

    def clear(self):
        self.mailboxes.clear()


app = DummyApp()


@given("a user {username}")
def give_user(username: str):
    app.create_user(username)


@when("{username} creates a mailbox {email}")
def create_mailbox(username: str, email: str):
    app.add_mailbox(username, email)


@then("{username} sees a mailbox {email}")
def assert_user_has_mailbox(email: str, username: str):
    assert username in app.mailboxes
    assert email in app.mailboxes[username]


@then('the mailbox {email} contains "{subject}"')
def assert_mailbox_contains(email: str, subject: str):
    for mailbox in app.mailboxes.values():
        if email in mailbox:
            assert subject in mailbox[email]
            break
    else:
        pytest.fail(f"mailbox {email} not found or not contains {subject}")
