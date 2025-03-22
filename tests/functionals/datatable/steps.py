from datetime import datetime

from pydantic import BaseModel, Field

from tursu import given

from ..conftest import DummyApp


class User(BaseModel):
    username: str
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


@given("a set of users:")
def a_set_of_users(app: DummyApp, data_table: list[User]):
    for user in data_table:
        app.users[user.username] = user.password
