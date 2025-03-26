from collections.abc import Iterator

import pytest
from pydantic import BaseModel


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


@pytest.fixture()
def dummy_app() -> Iterator[DummyApp]:
    yield DummyApp()
