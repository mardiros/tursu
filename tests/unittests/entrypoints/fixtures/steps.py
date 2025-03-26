from dataclasses import dataclass

from tursu import given, then, when

from .conftest import DummyApp


@dataclass
class User:
    username: str
    password: str


@given("a set of users:")
def a_set_of_users(app: DummyApp, data_table: list[User]):
    for user in data_table:
        app.users[user.username] = user.password


@when("{username} login with password {password}")
def login(app: DummyApp, username: str, password: str):
    app.login(username, password)


@then("the user is connected with username {username}")
def assert_connected(app: DummyApp, username: str):
    assert app.connected_user == username


@then("the user is not connected")
def assert_not_connected(app: DummyApp):
    assert app.connected_user is None
