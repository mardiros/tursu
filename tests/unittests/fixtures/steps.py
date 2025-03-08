from tursu import given, when, then


@given("a user {username}")
def give_user(username: str): ...


@when("I create a mailbox {email}")
def create_mailbox(email: str): ...


@then("I see a mailbox {email} for {username}")
def assert_user_has_mailbox(email: str): ...


@then("the mailbox {email} contains {subject}")
def assert_mailbox_contains(email: str, subject: str): ...
