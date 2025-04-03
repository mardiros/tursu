from tests.functionals.steps import DummyApp
from tursu import when


@when("{username} create a mailbox {email} using a fixture")
def create_mailbox_with_fixture(app: DummyApp, username: str, email: str):
    app.add_mailbox(username, email)
