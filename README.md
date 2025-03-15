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
rootdir: /home/guillaume/workspace/git/tursu
configfile: pyproject.toml
plugins: cov-6.0.0
collected 3 items

tests/functionals3/test_1_As_a_user_I_logged_in_with_my_password.py . [ 33%]
..                                                                [100%]

=========================== 3 passed in 0.02s ===========================
```

```bash
𝝿 uv run pytest tests/functionals3

### Gherkin keywords support.

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
