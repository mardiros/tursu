# Introduction

## Behavior-Driven Development (BDD)

Behavior-Driven Development (BDD) is a software development approach
that focuses on defining the behavior of an application through simple,
natural language descriptions.

It bridges the gap between developers, testers, and non-technical stakeholders.

Test scenarios are written in plain English following a specification in
the Gherkin language, where each step corresponds to a function that is executed
during test execution.

## Gherkin Introduction

All you need to know at the moment is that the most important keyword
of gherkin are:

- **Given** (setup or context)
- **When** (action or event)
- **Then** (expected outcome)

The full reference of the language is hosted at: https://cucumber.io/docs/gherkin/reference/

[cucumber.io](https://cucumber.io/docs/gherkin/reference/)

and is you're new to gherkin, we will reintroduce it in the next chapter.

## Bind code function to gherkin keyword

Using Turşu, those keywords are bound to python decorators that will match the phrase.

While running the following command

```bash
uv run tursu init
```

An example will be written:

```gherkin
# tests/functionals/login.feature
Feature: User signs in with the right password

  Scenario: Successful sign-in with valid credentials

    Given a user Bob with password dumbsecret
    When Bob signs in with password dumbsecret
    Then the user Bob is connected
```

We can match it in a python method:

```python
# tests/functionals/steps.py
from tursu import given, then, when

from .conftest import DummyApp


@given("a user {username} with password {password}")
def give_user(app: DummyApp, username: str, password: str):
    app.users[username] = password


@when("{username} signs in with password {password}")
def login(app: DummyApp, username: str, password: str):
    app.login(username, password)


@then("the user {username} is connected")
def assert_connected(app: DummyApp, username: str):
    assert app.connected_user == username
```

Every `Feature` keyword will be transformed to a python module.

Every `Scenario keyword` keyword will be transformed to a python function.

The steps keywords, `Given`, `When` and `Then` will match the decoverator above
from those function.

Everything whill be generated automatically using Python AST.

The generated file will look like this:

```python
def test_3_I_properly_logged_in(
    request: pytest.FixtureRequest,
    capsys: pytest.CaptureFixture[str],
    tursu: Tursu,
    app: Any,
):
    """Successful sign-in with valid credentials"""
    with TursuRunner(
        request,
        capsys,
        tursu,
        [
            "📄 Document: login.feature",
            "🥒 Feature: User signs in with the right password",
            "🎬 Scenario: Successful sign-in with valid credentials",
        ],
    ) as tursu_runner:
        tursu_runner.run_step("Given", "a user Bob with password dumbsecret", app=app)
        tursu_runner.run_step("When", "Bob signs in with password dumbsecret", app=app)
        tursu_runner.run_step("Then", "the user Bob is connected", app=app)
```

```{note}
Functions are written before run, then deleted from the disk.

While running `pdb` in a test run, using `--trace` in the pytest command, you can see
those functions on the disk.

async statement are not supported.
```

## Pytest Fixtures

`@given`, `@when` and `@then` decorators can received many parameters,
which are a mix of:

- the matched element from the decorator text.
- any pytest fixtures available.

But those parameters named are reserved

- `doc_string` which is reserved for the associated Gherkin feature, seen later.
- `data_table` which is reserved for the associated Gherkin feature, seen later.
- `example_row` which is reserved for scenario outline example.
- `tursu` an instance of `Tursu` used as a step registry.
- `request`, the pytest request fixture object.
- `capsys`, the pytest fixture capture fixture.

You should probably not used other native pytest fixture as keyword for extensibility.

In our example, we have an `app` that represent a configured app from a fixture.

You may also use the `page` fixture while using `pytest-playwright` or
`pytest-playwright-asyncio`.

## Running the tests

```bash
uv run pytest tests/functionals
```

You can use `-v` to have the scenario displayed while testing.

You can use `-vv` to have more info in the scenario displayed while testing.

You can use `--lf` to run the last failed tests or any feature you are used too!

You can use `--trace` to start a debugger in the tested scenario.

You can use any pytest options you are used to use while doing unit testing.
