from dataclasses import dataclass

from tursu import given, then, when

from .conftest import DummyApp


@dataclass
class User:
    username: str
    password: str


@given("a set of users:")
def a_set_of_users(app: DummyApp, data_table: list[User]): ...


@when("{username} login with password {password}")
def login(app: DummyApp, username: str, password: str): ...


@then("the user is connected with username {username}")
def assert_connected(app: DummyApp, username: str): ...


@then("the user is not connected")
def assert_not_connected(app: DummyApp): ...
