from typing import Any

import pytest
from pydantic import BaseModel

from tursu import given, then, when


class DummyMail(BaseModel):
    email: str
    subject: str
    body: str


class DummyApp:
    def __init__(self):
        self.mailboxes: dict[str, list[DummyMail]] = {}

    def create_user(self, username: str) -> None:
        assert username not in self.mailboxes
        self.mailboxes[username] = []

    def add_mailbox(self, username: str, mailbox: str) -> None:
        assert username in self.mailboxes
        self.mailboxes[username] = [
            DummyMail(email=mailbox, subject=f"Welcome {username}", body="...")
        ]


@given("a user {username}")
def give_user(dummy_app: DummyApp, username: str):
    dummy_app.create_user(username)


@when("{username} create a mailbox {email}")
def create_mailbox(dummy_app: DummyApp, username: str, email: str):
    dummy_app.add_mailbox(username, email)


@then("I see a mailbox {email} for {username}")
def assert_user_has_mailbox(dummy_app: DummyApp, email: str, username: str):
    assert username in dummy_app.mailboxes


@then('the mailbox {email} "{subject}" message is')
def assert_mailbox_contains(
    dummy_app: DummyApp, email: str, subject: str, doc_string: str
):
    for mailboxes in dummy_app.mailboxes.values():
        for mailbox in mailboxes:
            if mailbox.email == email and mailbox.subject in subject:
                assert mailbox.body == doc_string
    else:
        pytest.fail(f"mailbox {email} not found or not contains {subject}")


@then("the API for {username} respond")
def assert_api_response(
    dummy_app: DummyApp, username: str, doc_string: list[dict[str, Any]]
):
    assert [m.model_dump() for m in dummy_app.mailboxes[username]] == doc_string


@then("the users dataset is")
def assert_dataset(dummy_app: DummyApp, data_table: list[dict[str, str]]):
    assert [
        {"username": username, "email": m.email}
        for username in dummy_app.mailboxes
        for m in dummy_app.mailboxes[username]
    ]
