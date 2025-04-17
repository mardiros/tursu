from playwright.sync_api import Page, expect

from tursu import given, then, when


@given("anonymous user on {path}")
@when("I visit {path}")
def i_visit(page: Page, http_server: str, path: str):
    page.goto(f"{http_server}{path}")


@then('the user sees the text "{text}"')
def assert_text(page: Page, text: str):
    loc = page.get_by_text(text)
    expect(loc).to_be_visible()
