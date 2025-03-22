from tursu import given, then, when

from .conftest import DummyApp


@given("a user {username} with password {password}")
def give_user(app: DummyApp, username: str, password: str):
    app.users[username] = password


@when("{username} login with password {password}")
def login(app: DummyApp, username: str, password: str):
    app.login(username, password)


@then("the user {username} is connected")
def assert_connected(app: DummyApp, username: str):
    assert app.connected_user == username


@then("I am not connected")
def assert_not_connected(app: DummyApp):
    assert app.connected_user is None


@then("I see the docstring")
def assert_docstring(app: DummyApp, doc_string: dict[str, str]):
    assert doc_string == {"nick": app.connected_user}


@then("I see the data_table")
def assert_data_table(app: DummyApp, data_table: list[dict[str, str]]):
    records = [{"username": key, "password": val} for key, val in app.users.items()]
    assert records == data_table, records
