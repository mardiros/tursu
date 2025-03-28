import pytest

from tests.functionals.conftest import DummyApp
from tursu import RegEx, given, then, when


@given(RegEx(r"a user (?P<username>[^\s]+) using a regex"))
def give_user_with_fixture(app: DummyApp, username: str):
    app.create_user(username)


@when(RegEx(r"(?P<username>[^\s]+) create a mailbox (?P<email>[^\s]+) using a regex"))
def create_mailbox_with_fixture(app: DummyApp, username: str, email: str):
    app.add_mailbox(username, email)


@then(RegEx(r"(?P<username>[^\s]+) see a mailbox (?P<email>[^\s]+) using a regex"))
def assert_user_has_mailbox_with_fixture(app: DummyApp, email: str, username: str):
    assert username in app.mailboxes
    assert email in app.mailboxes[username]


@then(
    RegEx(r'the mailbox (?P<email>[^\s]+) contains "(?P<subject>[^\"]+)" using a regex')
)
def assert_mailbox_contains_with_fixture(app: DummyApp, email: str, subject: str):
    for mailbox in app.mailboxes.values():
        if email in mailbox:
            assert subject in mailbox[email]
            break
    else:
        pytest.fail(f"mailbox {email} not found or not contains {subject}")
