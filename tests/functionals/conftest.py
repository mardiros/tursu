import pytest

from tursu.registry import StepRegistry


@pytest.fixture()
def registry() -> StepRegistry:
    return StepRegistry().scan()


class DummyApp:
    """Represent a tested application"""

    def __init__(self):
        self.mailboxes: dict[str, dict[str, list[str]]] = {}
        self.users = {}
        self.connected_user: str | None = None

    def login(self, username: str, password: str) -> None:
        if username in self.users and self.users[username] == password:
            self.connected_user = username

    def create_user(self, username: str) -> None:
        assert username not in self.mailboxes
        self.mailboxes[username] = {}

    def add_mailbox(self, username: str, mailbox: str) -> None:
        assert username in self.mailboxes
        self.mailboxes[username][mailbox] = [f"Welcome {username}"]


@pytest.fixture
def app():
    return DummyApp()
