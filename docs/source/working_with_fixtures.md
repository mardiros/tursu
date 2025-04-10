# Working with pytest fixtures

Using Turşu is using pytest, with tests structured in the Gherkin style.

Any step definition can utilize a pytest fixture, and a fixture scoped to function
remains the same instance for a scenario.

And, a module scope fixture, persists across an entire Gherkin feature.

Every step definition works in the same way at the runtime, they just
serve different purpose.

In gherkin, a [@given](#tursu.given) is made to provide context for a test,
which could be a fixtures in pytest, but this is not the case and it will
never be for the reason of simplicity and tracability of the tests.

But, another approach is possible, a context can be created by having
a fixture parameter which act as a factory and the [@given](#tursu.given)
method will consume the fixture to setup the context.

So imagine we have this dummy application, below that don't use any
database but it could, and we just have a user database and a login method.

## The application

```python
class DummyApp:
    """Represent a tested application."""

    def __init__(self):
        self.users = {}
        self.connected_user: str | None = None

    def login(self, username: str, password: str) -> None:
        if username in self.users and self.users[username] == password:
            self.connected_user = username
```

## A testing scenario with hardcoded value.

So, we can create a simple gherkin scenario for the login:

```Gherkin
Feature: User sign in with their own password

  Scenario: User Bob can login
    Given a user Bob signs in with password dumbsecret
    When Bob signs in with password dumbsecret
    Then the user is connected with username Bob

```

## Step definitions for hardcoded values

```python
import pytest
from tursu import given, then, when


class DummyApp:
    """Represent a tested application."""

    def __init__(self):
        self.users = {}
        self.connected_user: str | None = None

    def login(self, username: str, password: str) -> None:
        if username in self.users and self.users[username] == password:
            self.connected_user = username


@pytest.fixture()
def app() -> DummyApp:
    return DummyApp()


@given("a user {username} signs in with password {password}")
def setup_user(app: DummyApp, username: str, password: str):
    app.users[username] = password


@when("{username} signs in with password {password}")
def login(app: DummyApp, username: str, password: str):
    app.login(username, password)


@then("the user is connected with username {username}")
def assert_connected(app: DummyApp, username: str):
    assert app.connected_user == username

```

All step definition works in the same way but they serve different purpose,

the **Given** will setup the application, the **When** will perform the tested action,

and the **Then** will ensure that the action behave properly.

And, everything happen in the fixture `app` that represent the context of the application.

```{note}
In normal situation, the DummyApp does not live in a step definition module,
it is imported from the codebase of the project that is going to be tested.
```

## A testing scenario with faked values

Now lets move on and add a scenario where the username is not predictable.

Here is my scenario:

```Gherkin
Feature: User sign in with their own password

  Scenario: Random user can login
    Given a user
    When user login
    Then the user is connected
```

And I am going to reuse the same step definition for this scenario.

```{literalinclude} ../../tests/using_fixtures/steps.py

```

As you can see, the gherkin pattern matcher will not have username and password
parametrized, but the function still have them, they have to be provision by
a fixture.

Ant that's all. Turşu will use the fixture to fill the username and the password.
Ant it will be the same set of data for the tests. If another test is added,
it will be new values.

Note that the data extracted by the pattern matcher from the Gherkin step
**will always take precedence over the pytest fixture**.

```{important}
The pytest.fixture() can be created in a conftest.py file or in a step definition
module.

At the moment, there is a limitation with fixtures created in step definition files,
**they cannot have duplicate names**.

You can't have two fixtures names `username` in two step definition files,
they will overlap in the Turşu fixture registry.

You may use two gherkin step that match two step definitions in two distinct modules,
and at the end, pytest test function can only have one fixture for both if they have
the same name.
```

Everything about the pytest fixtures usage has been written here.

## conclusion

- pytest function scope is gherkin scenario scope.
- Every step definition can received pytest fixtures, in the same way.
- In case of conflict, matched value for the gherkin scenario will always take precedence.
