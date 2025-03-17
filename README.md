# Turşu

[![Documentation](https://github.com/mardiros/tursu/actions/workflows/release.yml/badge.svg)](https://mardiros.github.io/tursu/)
[![Continuous Integration](https://github.com/mardiros/tursu/actions/workflows/tests.yml/badge.svg)](https://github.com/mardiros/tursu/actions/workflows/tests.yml)
[![Coverage Report](https://codecov.io/gh/mardiros/tursu/graph/badge.svg?token=DTpi73d7mf)](https://codecov.io/gh/mardiros/tursu)


This project allows you to write **Gherkin**-based behavior-driven development (BDD) tests
and execute them using **pytest**.

It compiles Gherkin syntax into Python code using **Abstract Syntax Tree (AST)** manipulation,
enabling seamless integration with pytest for running your tests.

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

The simplest way to initialize a test suite is to run the tursu cli.

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
  <Dir tests>
    <Package functionals>
      <GherkinDocument login.feature>
        <Function test_3_I_properly_logged_in>
        <Function test_7_I_hit_the_wrong_password>
        <Function test_14_I_user_another_login>

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
🥒 Feature: As a user I logged in with my password
🎬 Scenario: I properly logged in
✅ Given a user Bob with password dumbsecret
✅ When Bob login with password dumbsecret
✅ Then I am connected with username Bob

📄 Document: login.feature
🥒 Feature: As a user I logged in with my password
🎬 Scenario: I hit the wrong password
✅ Given a user Bob with password dumbsecret
✅ When Bob login with password notthat
✅ Then I am not connected

📄 Document: login.feature
🥒 Feature: As a user I logged in with my password
🎬 Scenario: I user another login
✅ Given a user Bob with password dumbsecret
✅ Given a user Alice with password anothersecret
✅ When Alice login with password dumbsecret
✅ Then I am not connected
✅ When Bob login with password dumbsecret
✅ Then I am connected with username Bob
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

tests/tests2/login.feature::test_3_I_properly_logged_in <- tests/tests2/test_login.py
📄 Document: login.feature
🥒 Feature: As a user I logged in with my password
🎬 Scenario: I properly logged in
⏳ Given a user Bob with password dumbsecret
✅ Given a user Bob with password dumbsecret
⏳ When Bob login with password dumbsecret
✅ When Bob login with password dumbsecret
⏳ Then I am connected with username Bob
✅ Then I am connected with username Bob
                                                         PASSED [ 33%]
tests/tests2/login.feature::test_7_I_hit_the_wrong_password <- tests/tests2/test_login.py
📄 Document: login.feature
🥒 Feature: As a user I logged in with my password
🎬 Scenario: I hit the wrong password
⏳ Given a user Bob with password dumbsecret
✅ Given a user Bob with password dumbsecret
⏳ When Bob login with password notthat
✅ When Bob login with password notthat
⏳ Then I am not connected
✅ Then I am not connected
                                                             PASSED [ 66%]
tests/tests2/login.feature::test_14_I_user_another_login <- tests/tests2/test_login.py
📄 Document: login.feature
🥒 Feature: As a user I logged in with my password
🎬 Scenario: I user another login
⏳ Given a user Bob with password dumbsecret
✅ Given a user Bob with password dumbsecret
⏳ Given a user Alice with password anothersecret
✅ Given a user Alice with password anothersecret
⏳ When Alice login with password dumbsecret
✅ When Alice login with password dumbsecret
⏳ Then I am not connected
✅ Then I am not connected
⏳ When Bob login with password dumbsecret
✅ When Bob login with password dumbsecret
⏳ Then I am connected with username Bob
✅ Then I am connected with username Bob
                                                          PASSED [100%]

=========================== 3 passed in 0.02s ===========================
```

```{note}

You can choose the test name ( tests/tests2/login.feature::test_3_I_properly_logged_in )
or even decorate with tag and use pytest markers (`pytest -m <tag>`).

```


## Get errors context

```bash
$ uv run pytest tests/functionals
============================ test session starts ==============================
platform linux -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0
configfile: pyproject.toml
plugins: cov-6.0.0, base-url-2.1.0, playwright-0.7.0, tursu-0.10.1
collected 3 items

tests/functionals/test_login.py F..                                      [100%]

================================== FAILURES ===================================
_________________________ test_3_I_properly_logged_in _________________________

self = <tursu.runner.TursuRunner object at 0x775de9b49e80>, step = 'then'
text = 'I am connected with username Bobby'
kwargs = {'app': <tests.functionals.conftest.DummyApp object at 0x775de9b49be0>}

    def run_step(
        self,
        step: StepKeyword,
        text: str,
        **kwargs: Any,
    ) -> None:
        try:
>           self.tursu.run_step(self, step, text, **kwargs)

src/tursu/runner.py:79:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src/tursu/registry.py:98: in run_step
    handler(**matches)
src/tursu/steps.py:36: in __call__
    self.hook(**kwargs)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

app = <tests.functionals.conftest.DummyApp object at 0x775de9b49be0>, username = 'Bobby'

    @then("I am connected with username {username}")
    def assert_connected(app: DummyApp, username: str):
>       assert app.connected_user == username
E       AssertionError

tests/functionals/steps.py:18: AssertionError

The above exception was the direct cause of the following exception:

request = <FixtureRequest for <Function test_3_I_properly_logged_in>>
capsys = <_pytest.capture.CaptureFixture object at 0x775de9b4a510>
tursu = <tursu.registry.Tursu object at 0x775dea9ffb60>
app = <tests.functionals.conftest.DummyApp object at 0x775de9b49be0>

    def test_3_I_properly_logged_in(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu, app: Any):
        """I properly logged in"""
        with TursuRunner(request, capsys, tursu, ['📄 Document: login.feature', '🥒 Feature: As a user I logged in with my password', '🎬 Scenario: I properly logged in']) as tursu_runner:
            tursu_runner.run_step('given', 'a user Bob with password dumbsecret', app=app)
            tursu_runner.run_step('when', 'Bob login with password dumbsecret', app=app)
>           tursu_runner.run_step('then', 'I am connected with username Bobby', app=app)

tests/functionals/test_login.py:12:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <tursu.runner.TursuRunner object at 0x775de9b49e80>, step = 'then'
text = 'I am connected with username Bobby'
kwargs = {'app': <tests.functionals.conftest.DummyApp object at 0x775de9b49be0>}

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
E           │ 🥒 Feature: As a user I logged in with my password │
E           │ 🎬 Scenario: I properly logged in                  │
E           │ ✅ Given a user Bob with password dumbsecret       │
E           │ ✅ When Bob login with password dumbsecret         │
E           │ ❌ Then I am connected with username Bobby         │
E           └────────────────────────────────────────────────────┘

src/tursu/runner.py:81: ScenarioFailed
=========================== short test summary info ===========================
FAILED tests/functionals/test_login.py::test_3_I_properly_logged_in - tursu.runner.ScenarioFailed:
========================= 1 failed, 2 passed in 0.07s =========================
```


### All Gherkin features are support.

tursu use the gherkin-official package to parse scenario, however,
they must be compiled to pytest tests function, implementation in development.

- ✅ Scenario
- ✅ Scenario Outlines / Examples
- ✅ Background
- ✅ Rule
- ✅ Feature
- ✅ Steps (Given, When, Then, And, But)
- ✅ Tags  (converted as pytest marker)
- ✅ Doc String
- ✅ Datatables
