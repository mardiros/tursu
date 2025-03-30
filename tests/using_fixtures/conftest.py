import pytest
from faker import Faker

from tursu import tursu_collect_file

tursu_collect_file()


faker = Faker()


@pytest.fixture()
def username():
    return faker.user_name


@pytest.fixture()
def password():
    return faker.random_letters(24)


class DummyApp:
    """Represent a tested application"""

    def __init__(self):
        self.users = {}
        self.connected_user: str | None = None

    def login(self, username: str, password: str) -> None:
        if username in self.users and self.users[username] == password:
            self.connected_user = username


@pytest.fixture()
def app() -> DummyApp:
    return DummyApp()
