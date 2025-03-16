# Migrate from behave

This framework is a modern, type-safe alternative to Behave, designed to bring type hints,
better IDE support, and static analysis to Behavior-Driven Development (BDD) in Python 3.

It improves upon Behave by eliminating dynamic attribute issues and enhancing maintainability.

The cherry on top is that you can run the debugger without pain.

## Step 1 - Install tursu and configure it.

Installation:

```bash
uv add --group dev tursu
```

Add the Tursu Gherkin compiler to AST generate the tests suite:

- Ensure the `__init__.py` file exists in the functionals tests suite.

```bash
touch tests/functionals/__init__.py
```

- create a minimal conftest.py

```bash
cat << 'EOF' > tests/functionals/conftest.py
from tursu.plugin import tursu_collect_file

tursu_collect_file()
EOF
```

## Step 2 - Replace context with fixtures in all decorators

Tursu simplifies BDD by replacing Behave’s dynamic context with pytest fixtures,
making it more maintainable and test-friendly.

Example:

### Behave

```python
from behave import given

@given("A user with username {username} and password {password}")
def step_create_user(context, username, password):
    context.user = {"username": username, "password": password}


@when("they log in")
def step_login(context):
    user = context.user
    context.logged_in = user["username"] == "john" and user["password"] == "secret"

@then("they should see a welcome message")
def step_welcome_message(context):
    assert context.logged_in, "Login failed!"
```

### Tursu


```python
from dataclasses import dataclass

import pytest
from tursu import given


@dataclass
class User:
    username: str
    password: str
    logged_in: bool = False


@pytest.fixture
def user() -> User:
    return User(username="", password="")


@given("a user with username {username} and password {password}")
def step_create_user(username: str, password: str, user: User):
    user.username = username
    user.password = password


@when("they log in")
def step_login(user: User):
    user.logged_in = user.username == "john" and user.password == "secret"


@then("they should see a welcome message")
def step_welcome_message(user: User):
    assert user.logged_in, "Login failed!"
```

```{note}
- **context.text** has to be replaced by doc_string
- **context.table** has to be replaced by data_table
```

### Behave

```
@given('a set of specific users')
def step_impl(context):
    for row in context.table:
        context.model.add_user(name=row['name'], department=row['department'])

@then('I will see the account details')
def step_impl(context):
    assert context.text == ...
```

### Tursu

```
@given('a set of specific users')
def step_impl(model: MyModelFixture, data_dable: list[dict[str, str]]):
    for row in data_dable:
        model.add_user(name=row['name'], department=row['department'])

@then('I will see the account details')
def step_impl(doc_string: text):
    assert doc_string == ...
```


## Step 3 - Replace Behave Fixtures with Pytest autouse Fixtures

Behave allows using fixtures through before_scenario and after_scenario.
In Tursu, we achieve the same behavior using pytest’s autouse fixtures.

Example:

### Behave

```python
from behave import fixture, use_fixture

from my_dummy_app.entrypoint import main

from .utils import wait_for_url


@fixture
def start_webapp(context, **kwargs):
    proc = Process(target=main, daemon=True)
    proc.start()
    wait_for_url("http://localhost:8888")
    yield
    proc.kill()

def before_scenario(context, scenario):
    use_fixture(start_webapp, context)
```


### Tursu

```python
import pytest

from my_dummy_app.entrypoint import main

from .utils import wait_for_url

@pytest.fixture(autouse=True, scope="function")  # adapt the scope for your needs
def start_webapp():
    proc = Process(target=main, daemon=True)
    proc.start()
    wait_for_url("http://localhost:8888")
    yield
    proc.kill()
```


## Step 4 - Remove code that launch a browser, use pytest-playwright

Example:

### Behave

```
@fixture
def browser(context: Any, **kwargs: Any) -> Iterator[None]:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=50)
        context.browser = browser.new_page(base_url="http://localhost:8888")
        yield
        browser.close()

```


### Tursu

```python

# you can configure the browser context in a fixture
# https://playwright.dev/python/docs/test-runners#use-custom-viewport-size

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }
```

## Step 5 - Declare your gherkin tag into your pytest marker.

This is highly recommended, to avoid warnings from pytest.

```toml
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "dev: experiment with some background context.",
    "openapi: open api tests.",
    "wip: work in progress.",
]
```

## Step 6 - Run the test, enable tracing, if necessary

It's hard to run a debugger in behave, remote debugging is mandatory,
in pytest, you can use start a debugger in your test by a

```bash
uv run pytest \
  -m "wip" \
  --base-url http://localhost:8888 \
  --headed \
  --browser chromium \
  --trace \
  -sxv \
  tests/functionals/
```

-m "wip" :  only run the @wip Gherkin tag

--base-url http://localhost:8888 :  configure a base url, may be in the code

--headed :  start a real browser to see what happen

--browser chromium :  choose the browser you want

--trace :  start the test by a breakpoint

-sv :  donc capture stdout, and choose your vebosity level


```
$ uv run pytest \
  -m "wip" \
  --base-url http://localhost:8888 \
  --headed \
  --browser chromium \
  --trace \
  -sxv \
  tests/using_playwright
================================= test session starts =================================
baseurl: http://localhost:8888
configfile: pyproject.toml
plugins: cov-6.0.0, playwright-0.7.0, base-url-2.1.0
collected 1 item

tests/using_playwright/test_1_Basic_Test.py::test_2_Hello_world[chromium]
>>>>>>>>>>>>>> PDB runcall (IO-capturing turned off for fixture capsys) >>>>>>>>>>>>>>>
> ~/git/tursu/tests/using_playwright/test_1_Basic_Test.py(10)test_2_Hello_world()
-> with TursuRunner(request, capsys, tursu, ['📄 Document: 01_basic.feature', '🥒 Feature: Basic Test', '🎬 Scenario: Hello world']) as tursu_runner:

📄 Document: 01_basic.feature
🥒 Feature: Basic Test
🎬 Scenario: Hello world
> ~/git/tursu/tests/using_playwright/test_1_Basic_Test.py(11)test_2_Hello_world()
-> tursu_runner.run_step('given', 'anonymous user on /', page=page)
(Pdb) c

>>>>>>>>>>>>>>> PDB continue (IO-capturing resumed for fixture capsys) >>>>>>>>>>>>>>>>
✅ Given anonymous user on /
✅ Then I see the text "Hello, World!"
127.0.0.1 - - [14/Mar/2025 21:51:08] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [14/Mar/2025 21:51:08] "GET /favicon.ico HTTP/1.1" 200 -
                                                                           PASSED

================================== 1 passed in 6.52s ==================================
```
