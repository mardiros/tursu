from tests.functionals.steps import DummyApp
from tursu import when


@when("{username} creates a mailbox {email}")
def create_mailbox_with_fixture(app: DummyApp, username: str, email: str):
    app.add_mailbox(username, email)
