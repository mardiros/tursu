import pytest

from tursu.entrypoints.plugin import tursu_collect_file

tursu_collect_file()


class DummyApp:
    """Represent a tested application"""

    def __init__(self):
        self.users = {}
        self.connected_user: str | None = None

    def login(self, username: str, password: str) -> None:
        if username in self.users and self.users[username] == password:
            self.connected_user = username


@pytest.fixture()
def app() -> DummyApp:
    return DummyApp()
