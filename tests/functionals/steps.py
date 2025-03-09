from tursu import given, then, when

from .conftest import DummyApp


@given("a user {username} with password {password}")
def give_user(app: DummyApp, username: str, password: str):
    app.users[username] = password


@when("{username} login with password {password}")
def login(app: DummyApp, username: str, password: str):
    app.login(username, password)


@then("I am connected with username {username}")
def assert_connected(app: DummyApp, username: str):
    assert app.connected_user == username


@then("I am not connected")
def assert_not_connected(app: DummyApp):
    assert app.connected_user is None
