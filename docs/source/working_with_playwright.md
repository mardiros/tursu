# Working with playwright

Turşu does not provice playwright option, but you can works with both
playwright and Turşu for testing your web application.

Actually, it has been develop for that!

## Installation

```bash
uv add tursu pytest-playwright
uv run playwright install chromium
uv tursu init --no-dummies -o tests/functionals-playwright/
```

- playwright requires to download its own browsers,
  refer to the playwright documentation for more options.
- The `--no-dummies` does not create dummy scenario.

## Create a step

```{literalinclude} ../../tests/using_playwright/steps.py

```

That's it. You can just use the "Page" fixture provided by pytest-playwright directly.

## Create a scenario

```{literalinclude} ../../tests/using_playwright/01_basic.feature

```

## Run the test

```bash
uv run pytest --base-url http://localhost:8888 --browser chromium -v tests/using_playwright/
```

Sure this tests will fail, this is BDD :)

## Adding a fixture


```{literalinclude} ../../tests/using_playwright/conftest.py

```


### Run the test

```bash
$ uv run pytest --base-url http://localhost:8888 --browser chromium -v tests/using_playwright/
================================= test session starts =================================
baseurl: http://localhost:8888
configfile: pyproject.toml
plugins: cov-6.0.0, playwright-0.7.0, base-url-2.1.0
collected 1 item

📄 Document: 01_basic.feature_Basic_Test.py::test_2_Hello_world[chromium]
🥒 Feature: Basic Test
🎬 Scenario: Hello world
✅ Given anonymous user on /
✅ Then I see the text "Hello, World!"
                                                                           PASSED [100%]

================================== 1 passed in 0.94s ==================================
```


````{tip}
While doing continuous integration, always activate the option `--tracing on`
from pytest-playright, it will generate a `trace.zip` file in a `test-results`
directory to configured as a build artefact.

Afterwhat you can see all step of the scenario using the show-trace command:

```bash
$ uv run playwright show-trace test-results/**/trace.zip
```

````
