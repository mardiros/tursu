import pytest
from pydantic import BaseModel

from tursu import given, then, when


class DummyApp:
    """Represent a tested application."""

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


@given("a user {username} with password {password}")
def give_user(app: DummyApp, username: str, password: str):
    app.users[username] = password


@when("{username} signs in with password {password}")
def login(app: DummyApp, username: str, password: str):
    app.login(username, password)


@then("the user {username} is connected")
def assert_connected(app: DummyApp, username: str):
    assert app.connected_user == username


@then("the user is not connected")
def assert_not_connected(app: DummyApp):
    assert app.connected_user is None


@then("I see the docstring")
def assert_docstring(app: DummyApp, doc_string: dict[str, str]):
    assert doc_string == {"nick": app.connected_user}


class ParsedDocstring(BaseModel):
    nick: str


@then("I can parse the docstring")
def assert_parsed_docstring(app: DummyApp, doc_string: ParsedDocstring):
    assert doc_string.nick == app.connected_user


@then("I see the data_table")
def assert_data_table(app: DummyApp, data_table: list[dict[str, str]]):
    records = [{"username": key, "password": val} for key, val in app.users.items()]
    assert records == data_table, records
