from typing import Annotated

import factory
from pydantic import BaseModel

from tursu import given, then

from ..conftest import DummyApp


class User(BaseModel):
    username: str
    mailbox: str


class UserFactory(factory.Factory[User]):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    mailbox = factory.Faker("email")


class Dataset(BaseModel):
    username: str
    mailbox: str


@then("the users dataset is")
def assert_dataset(dummy_app: DummyApp, data_table: list[Dataset]): ...


@given("a set of users:")
def a_set_of_users(dummy_app: DummyApp, data_table: list[Annotated[User, UserFactory]]):
    for user in data_table:
        dummy_app.create_user(user.username)
        dummy_app.add_mailbox(user.username, user.mailbox)
