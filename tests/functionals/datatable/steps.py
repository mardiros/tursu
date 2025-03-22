from pydantic import BaseModel

from tursu import given

from ..conftest import DummyApp


class User(BaseModel):
    username: str
    password: str


@given("a set of users:")
def a_set_of_users(app: DummyApp, data_table: list[User]):
    for user in data_table:
        app.users[user.username] = user.password
