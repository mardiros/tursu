from tests.functionals.steps import DummyApp
from tursu import given


@given("a user {username}")
def give_user_with_fixture(app: DummyApp, username: str):
    app.create_user(username)
