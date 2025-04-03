from typing import Annotated

import factory
from pydantic import BaseModel

from tursu import given

from ..steps import DummyApp


class User(BaseModel):
    username: str
    password: str


class UserFactory(factory.Factory[User]):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.Faker("password")


@given("a set of users:")
def a_set_of_users(app: DummyApp, data_table: list[Annotated[User, UserFactory]]):
    for user in data_table:
        app.users[user.username] = user.password


@given("a user with the following properties:")
def on_user(app: DummyApp, data_table: User):
    app.users[data_table.username] = data_table.password
