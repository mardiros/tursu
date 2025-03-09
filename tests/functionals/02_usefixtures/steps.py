import pytest

from tursu import given, then, when

from .conftest import DummyApp


@given("a user {username} using a fixture")
def give_user_with_fixture(app: DummyApp, username: str):
    app.create_user(username)


@when("{username} create a mailbox {email} using a fixture")
def create_mailbox_with_fixture(app: DummyApp, username: str, email: str):
    app.add_mailbox(username, email)


@then("I see a mailbox {email} for {username} using a fixture")
def assert_user_has_mailbox_with_fixture(app: DummyApp, email: str, username: str):
    assert username in app.mailboxes
    assert email in app.mailboxes[username]


@then('the mailbox {email} contains "{subject}" using a fixture')
def assert_mailbox_contains_with_fixture(app: DummyApp, email: str, subject: str):
    for mailbox in app.mailboxes.values():
        if email in mailbox:
            assert subject in mailbox[email]
            break
    else:
        pytest.fail(f"mailbox {email} not found or not contains {subject}")
