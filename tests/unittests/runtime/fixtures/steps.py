import asyncio

from tursu import given, then, when

from .conftest import DummyApp, DummyMail


@given("a user {username}")
def give_user(dummy_app: DummyApp, username: str):
    dummy_app.create_user(username)


@when("{username} creates a mailbox {email}")
def create_mailbox(dummy_app: DummyApp, username: str, email: str):
    dummy_app.add_mailbox(username, email)


@then("{username} sees a mailbox {email}")
def assert_user_has_mailbox(dummy_app: DummyApp, email: str, username: str):
    assert username in dummy_app.mailboxes


@then('the mailbox {email} "{subject}" message is')
def assert_mailbox_contains(
    dummy_app: DummyApp, email: str, subject: str, doc_string: str
): ...


@then("the API for {username} is responding")
def assert_api_response(
    dummy_app: DummyApp, username: str, doc_string: list[DummyMail]
):
    assert doc_string == dummy_app.mailboxes[username]


@then("the async API for {username} is responding")
async def assert_async_api_response(
    dummy_app: DummyApp, username: str, doc_string: list[DummyMail]
):
    await asyncio.sleep(0)
    assert doc_string == dummy_app.mailboxes[username]


@then("the users raw dataset is")
def assert_dataset_raw(dummy_app: DummyApp, data_table: list[dict[str, str]]): ...


@then("the raw API for {username} is responding")
def assert_api_response_json_as_any(
    dummy_app: DummyApp,
    username: str,
    doc_string: list[dict[str, str]] | dict[str, str],
):
    assert doc_string == dummy_app.mailboxes[username]
