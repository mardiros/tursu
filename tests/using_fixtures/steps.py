from tursu import given, then, when

from .conftest import DummyApp


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
