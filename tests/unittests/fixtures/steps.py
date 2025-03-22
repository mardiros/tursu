from typing import Any

from tests.unittests.conftest import DummyApp
from tursu import given, then, when


@given("a user {username}")
def give_user(dummy_app: DummyApp, username: str):
    dummy_app.create_user(username)


@when("{username} create a mailbox {email}")
def create_mailbox(dummy_app: DummyApp, username: str, email: str):
    dummy_app.add_mailbox(username, email)


@then("{username} see a mailbox {email}")
def assert_user_has_mailbox(dummy_app: DummyApp, email: str, username: str):
    assert username in dummy_app.mailboxes


@then('the mailbox {email} "{subject}" message is')
def assert_mailbox_contains(
    dummy_app: DummyApp, email: str, subject: str, doc_string: str
): ...


@then("the API for {username} respond")
def assert_api_response(
    dummy_app: DummyApp, username: str, doc_string: list[dict[str, Any]]
):
    assert [m.model_dump() for m in dummy_app.mailboxes[username]] == doc_string


@then("the users dataset is")
def assert_dataset(dummy_app: DummyApp, data_table: list[dict[str, str]]): ...
