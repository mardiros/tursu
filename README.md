# Turşu

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
      <Module test_1_As_a_user_I_logged_in_with_my_password.py>
        <Function test_3_I_properly_logged_in>
        <Function test_7_I_hit_the_wrong_password>
        <Function test_14_I_user_another_login>

====================== 3 tests collected in 0.01s =======================
```

### Run the tests.

```bash
𝝿 uv run pytest tests/functionals
========================== test session starts ==========================
platform linux -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0
configfile: pyproject.toml
collected 3 items

tests/functionals/test_1_As_a_user_I_logged_in_with_my_password.py . [ 33%]
..                                                                [100%]

=========================== 3 passed in 0.02s ===========================
```

Or run it with the details:

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
                                                                         PASSED

📄 Document: login.feature
🥒 Feature: As a user I logged in with my password
🎬 Scenario: I hit the wrong password
✅ Given a user Bob with password dumbsecret
✅ When Bob login with password notthat
✅ Then I am not connected
                                                                         PASSED

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
