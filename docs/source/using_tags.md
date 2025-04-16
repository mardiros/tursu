(using-tags)=

# Gherkin tag as pytest tag

Gherkin support tags on multiple keywords, such as `Feature`, `Rule`, `Scenario`
and `Scenario Outline`.

All of them can be used to set a pytest mark and use the `-m` option of pytest.

## Skipping tests

```gherkin
Feature: Discover Gherkin tag

  @skip
  Scenario: I can skip a test
    Given a user Bob

```

This test will be skipped because of the `@skip` tag:

```bash
uv run pytest -v
========================== test session starts ==========================
platform linux -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0
configfile: pyproject.toml
plugins: cov-6.0.0
collected 1 item

tests/functionals/test_1_Discover_Gherkin_tag.py::test_2_I_can_skip_a_test SKIPPED (unconditional skip)        [100%]

========================== 1 skipped in 0.01s ===========================
```

## Asyncio support

```gherkin
@asyncio
Feature: A feature where steps use asyncio

  Scenario: I can run tests with pytest-asyncio
    Given a user Bob

```

This test will be marked with `@pytest.mark.asyncio` and steps definition
can be coroutine.


## Writing a wip tag

```gherkin
Feature: Discover Gherkin tag

  @wip
  Scenario: I work on this test
    Given a user Alice

  Scenario: This test is not runned
    Given a user Bob
```

Now to avoid warning, markers have to be registered in pytest options, in pyproject.toml:

```toml
[tool.pytest.ini_options]
markers = ["wip: work in progress."]
```

```bash
𝝿 uv run pytest tests/functionals2 -m wip
========================== test session starts ==========================
platform linux -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0
configfile: pyproject.toml
plugins: cov-6.0.0
collected 2 items / 1 deselected / 1 selected

tests/functionals/test_1_Discover_Gherkin_tag.py                   [100%]

=================== 1 passed, 1 deselected in 0.01s =====================
```

## Write your own tags dependings on your need.

Depending on the what you are working on, you have different needs, if
you are working.

You may have `@smoke`, `@regression`, `@critical` or even `@mobile` if you ware working
on a responsive design.

Also note that the marks are available in your step definition using
the pytest request fixture, and you can access to it by declaring the dependency.

```python
import time
import pytest

from tursu import given, then, when


@given("example")
def example(request: pytest.FixtureRequest):
    if request.node.get_closest_marker("slow_down") is not None:
        time.sleep(1)
```
