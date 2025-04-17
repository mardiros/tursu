from playwright.async_api import Page, expect

from tursu import given, then, when


@given("anonymous user on {path}")
@when("I visit {path}")
async def i_visit(page: Page, http_server: str, path: str):
    await page.goto(f"{http_server}{path}")


@then('the user sees the text "{text}"')
async def assert_text(page: Page, text: str):
    loc = page.get_by_text(text)
    await expect(loc).to_be_visible()
