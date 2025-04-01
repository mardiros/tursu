import pytest
from faker import Faker

from tursu import given, then, when

faker = Faker()


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


@pytest.fixture()
def username():
    return faker.user_name


@pytest.fixture()
def password():
    return faker.random_letters(24)


@given("a user")
@given("a user {username} login with password {password}")
def setup_user(app: DummyApp, username: str, password: str):
    app.users[username] = password


@when("user login")
@when("{username} login with password {password}")
def login(app: DummyApp, username: str, password: str):
    app.login(username, password)


@then("the user is connected")
@then("the user is connected with username {username}")
def assert_connected(app: DummyApp, username: str):
    assert app.connected_user == username


@then("the user is not connected")
def assert_not_connected(app: DummyApp):
    assert app.connected_user is None
