import pytest

from tursu.registry import StepRegistry


@pytest.fixture()
def registry():
    return StepRegistry().scan()


class DummyApp:
    def __init__(self):
        self.mailboxes: dict[str, dict[str, list[str]]] = {}

    def create_user(self, username: str) -> None:
        assert username not in self.mailboxes
        self.mailboxes[username] = {}

    def add_mailbox(self, username: str, mailbox: str) -> None:
        assert username in self.mailboxes
        self.mailboxes[username][mailbox] = [f"Welcome {username}"]


@pytest.fixture()
def app():
    return DummyApp()
