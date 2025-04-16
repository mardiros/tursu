(playwright-asyncio)=

# Working with async playwright

While using pytest-asyncio, pytest-playwright may not works fine.
The package [pytest-playwright-asyncio](https://pypi.org/project/pytest-playwright-asyncio/)
will include the async version that can also be used instead.

In that case, feature has to be tagged `@asyncio` in order to generate coroutine
instead of function.

## Create a scenario

```{literalinclude} ../../tests/using_playwright_async/01_basic.feature

```

## Step definitions

```{literalinclude} ../../tests/using_playwright_async/steps.py

```

## Example of application as a pytest fixture

```{literalinclude} ../../tests/using_playwright_async/conftest.py

```

```{note}
In this test, a page fixture has been created instead of using `pytest-playwright-asyncio`.
```
