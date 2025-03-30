# Turşu

[![PyPI](https://github.com/mardiros/tursu/actions/workflows/release.yml/badge.svg)](https://pypi.org/project/tursu/)
[![Doc](https://github.com/mardiros/tursu/actions/workflows/publish-doc.yml/badge.svg)](https://mardiros.github.io/tursu/)
[![Continuous Integration](https://github.com/mardiros/tursu/actions/workflows/tests.yml/badge.svg)](https://github.com/mardiros/tursu/actions/workflows/tests.yml)
[![Coverage Report](https://codecov.io/gh/mardiros/tursu/graph/badge.svg?token=DTpi73d7mf)](https://codecov.io/gh/mardiros/tursu)


This project allows you to write **Gherkin**-based behavior-driven development (BDD) tests
and execute them using **pytest**.

It compiles Gherkin syntax into Python code using **Abstract Syntax Tree (AST)** manipulation,
enabling seamless integration with pytest for running your tests.

Enjoy practicing BDD in modern Python (3.10+), type hinting, dataclasses or Pydantic, pytest,
playwright.

## Features

- Write tests using **Gherkin syntax**.
- Write **step definitions** in Python for with type hinting to cast Gherkin parameters.
- Execute tests directly with **pytest**.
- Compile Gherkin scenarios to Python code using **AST**.

## Getting started

### Installation using uv

```bash
uv add --group dev tursu
```

### Creating a new test suite

The simplest way to initialize a test suite is to run the Turşu cli.

```
uv run tursu init
```

### Discover your tests.

```bash
𝝿 uv run pytest --collect-only tests/functionals
========================== test session starts ==========================
platform linux -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0
configfile: pyproject.toml
plugins: cov-6.0.0
collected 3 items

<Dir tursu>
  <Package tests>
    <Package functionals>
      <GherkinDocument login.feature>
        <Function test_3_User_can_login>
        <Function test_7_User_can_t_login_with_wrong_password>
        <Function test_12_User_can_t_login_with_someone_else_username>

====================== 3 tests collected in 0.01s =======================
```

### Run the tests.

## All the suite
```bash
𝝿 uv run pytest tests/functionals
========================== test session starts ==========================
platform linux -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0
configfile: pyproject.toml
collected 3 items

tests/functionals/test_login.py ...                               [ 33%]
..                                                                [100%]

=========================== 3 passed in 0.02s ===========================
```

## All the suite with details:

```bash
𝝿 uv run pytest -v tests/functionals
============================= test session starts =============================
platform linux -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0
configfile: pyproject.toml
collected 3 items


📄 Document: login.feature
🥒 Feature: User login with their own password
🎬 Scenario: User can login
✅ Given a user Bob with password dumbsecret
✅ When Bob login with password dumbsecret
✅ Then the user is connected with username Bob

📄 Document: login.feature
🥒 Feature: User login with their own password
🎬 Scenario: User can't login with wrong password
✅ Given a user Bob with password dumbsecret
✅ When Bob login with password notthat
✅ Then the user is not connected

📄 Document: login.feature
🥒 Feature: User login with their own password
🎬 Scenario: User can't login with someone else username
✅ Given a user Bob with password bobsecret
✅ Given a user Alice with password alicesecret
✅ When Alice login with password bobsecret
✅ Then the user is not connected
                                                                         PASSED

============================== 3 passed in 0.02s ==============================
```

## Choose your scenario file to test:

```bash
𝝿 uv run pytest -vv tests/tests2/login.feature
========================== test session starts ==========================
platform linux -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0
configfile: pyproject.toml
plugins: cov-6.0.0, tursu-0.11.1
collected 3 items

tests/functionals/login.feature::test_3_User_can_login <- test_login.py
📄 Document: login.feature
🥒 Feature: User login with their own password
🎬 Scenario: User can login
⏳ Given a user Bob with password dumbsecret
✅ Given a user Bob with password dumbsecret
⏳ When Bob login with password dumbsecret
✅ When Bob login with password dumbsecret
⏳ Then the user is connected with username Bob
✅ Then the user is connected with username Bob
                                                            PASSED [ 33%]
tests/functionals/login.feature::test_7_User_can_t_login_with_wrong_password <- test_login.py
📄 Document: login.feature
🥒 Feature: User login with their own password
🎬 Scenario: User can't login with wrong password
⏳ Given a user Bob with password dumbsecret
✅ Given a user Bob with password dumbsecret
⏳ When Bob login with password notthat
✅ When Bob login with password notthat
⏳ Then the user is not connected
✅ Then the user is not connected
                                                            PASSED [ 66%]
tests/functionals/login.feature::test_12_User_can_t_login_with_someone_else_username <- test_login.py
📄 Document: login.feature
🥒 Feature: User login with their own password
🎬 Scenario: User can't login with someone else username
⏳ Given a user Bob with password bobsecret
✅ Given a user Bob with password bobsecret
⏳ Given a user Alice with password alicesecret
✅ Given a user Alice with password alicesecret
⏳ When Alice login with password bobsecret
✅ When Alice login with password bobsecret
⏳ Then the user is not connected
✅ Then the user is not connected

                                                            PASSED [100%]
=========================== 3 passed in 0.02s ===========================
```

```{note}

You can choose the test name ( tests/tests2/login.feature::test_3_User_can_login )
or even decorate with tag and use pytest markers (`pytest -m <tag>`).

```

## Get errors context

```bash
𝝿 uv run pytest tests/functionals
========================== test session starts ===========================
platform linux -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0
rootdir: /home/guillaume/workspace/git/tursu
configfile: pyproject.toml
plugins: cov-6.0.0, tursu-0.12.4, playwright-0.7.0, base-url-2.1.0
collected 3 items

tests/functionals/login.feature F..                                      [100%]

================================ FAILURES ================================
_________________________ test_3_User_can_login __________________________

self = <tursu.runner.TursuRunner object at 0x76103daadbe0>, step = 'Then'
text = 'the user is connected with username Bobby'
kwargs = {'app': <tests.functionals.conftest.DummyApp object at 0x76103daad940>}

    def run_step(
        self,
        step: StepKeyword,
        text: str,
        **kwargs: Any,
    ) -> None:
        try:
>           self.tursu.run_step(self, step, text, **kwargs)

src/tursu/runner.py:79:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src/tursu/registry.py:102: in run_step
    handler(**matches)
src/tursu/steps.py:38: in __call__
    self.hook(**kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

app = <tests.functionals.conftest.DummyApp object at 0x76103daad940>
username = 'Bobby'

    @then("the user is connected with username {username}")
    def assert_connected(app: DummyApp, username: str):
>       assert app.connected_user == username
E       AssertionError

tests/functionals/steps.py:18: AssertionError

The above exception was the direct cause of the following exception:

request = <FixtureRequest for <Function test_3_User_can_login>>
capsys = <_pytest.capture.CaptureFixture object at 0x76103daae270>
tursu = <tursu.runtime.registry.Tursu object at 0x76103f107230>
app = <tests.functionals.conftest.DummyApp object at 0x76103daad940>

>   ???

test_login.py:12:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <tursu.runner.TursuRunner object at 0x76103daadbe0>, step = 'Then'
text = 'the user is connected with username Bobby'
kwargs = {'app': <tests.functionals.conftest.DummyApp object at 0x76103daad940>}

    def run_step(
        self,
        step: StepKeyword,
        text: str,
        **kwargs: Any,
    ) -> None:
        try:
            self.tursu.run_step(self, step, text, **kwargs)
        except Exception as exc:
>           raise ScenarioFailed(self.fancy()) from exc
E           tursu.runner.ScenarioFailed:
E           ┌────────────────────────────────────────────────────┐
E           │ 📄 Document: login.feature                         │
E           │ 🥒 Feature: User login with their own password     │
E           │ 🎬 Scenario: User can login                        │
E           │ ✅ Given a user Bob with password dumbsecret       │
E           │ ✅ When Bob login with password dumbsecret         │
E           │ ❌ Then the user is connected with username Bobby  │
E           └────────────────────────────────────────────────────┘

src/tursu/runner.py:81: ScenarioFailed
======================== short test summary info =========================
FAILED tests/functionals/login.feature::test_3_User_can_login - tursu.runner.ScenarioFailed:
```

```{note}

If --trace is used, or -vvv, the tests files are written on the disk, and
the `???` in the context are replaced by the generated python test function.

This my be usefull in case of hard time debugging.
```

### All Gherkin features are support.

Turşu use the [gherkin-official](https://pypi.org/project/gherkin-official/)
package to parse Gherkin Scenario beeing compiled to python.

- ✅ Feature  *(converted to python module)*
- ✅ Scenario *(converted to python test functions)*
- ✅ Scenario Outlines / Examples *(converted to @pytest.mark.parametrized test function)*
- ✅ Background *(Step copied to all the function of the scenario)*
- ✅ Rule
- ✅ Steps *(Given, When, Then, And, But, bound to the step definition provided.)*
- ✅ Tags *(converted as pytest marker on Feature, Scenario, Scenario Outline and Rule)*
- ✅ Doc String *(support casting of json to python model with the lib of your choice: pydantic, dataclasses,...)*
- ✅ Data Table *(support casting to python model with the lib of your choice: pydantic, dataclasses,...)*


### Great support of playwright.

Combining Turşu and [pytest-playwright](https://pypi.org/project/pytest-playwright/)
is a great experience.
See the [example in the documentation](https://mardiros.github.io/tursu/working_with_playwright.html)

### Great support of pytest fixtures and faker.

See the [example in the documentation](https://mardiros.github.io/tursu/working_with_fixtures.html)
