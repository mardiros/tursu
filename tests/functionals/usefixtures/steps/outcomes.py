import pytest

from tests.functionals.steps import DummyApp
from tursu import then


@then("{username} sees a mailbox {email}")
def assert_user_has_mailbox_with_fixture(app: DummyApp, email: str, username: str):
    assert username in app.mailboxes
    assert email in app.mailboxes[username]


@then('the mailbox {email} contains "{subject}"')
def assert_mailbox_contains_with_fixture(app: DummyApp, email: str, subject: str):
    for mailbox in app.mailboxes.values():
        if email in mailbox:
            assert subject in mailbox[email]
            break
    else:
        pytest.fail(f"mailbox {email} not found or not contains {subject}")
