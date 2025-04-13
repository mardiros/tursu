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

## Use the trace artefact

While doing continuous integration, always activate the option
`--tracing retain-on-failure` from pytest-playright, it will generate a `trace.zip`
file in a `test-results` directory to configured as a build artefact.

Afterwhat you can see all step of the scenario using the show-trace command:

```bash
$ uv run playwright show-trace trace.zip
```

While running locally, you can stop on the first error and then show the trace.

```bash
$ rm -rf test-results
$ uv run pytest -sxv --tracing retain-on-failure tests/functionals
$ uv run playwright show-trace test-results/**/trace.zip
```

## Asyncio

pytest-playwright does not works well with pytest-asyncio, both plugins conflicts
on the asyncio loop.

To start an async application, like a FastAPI app, you can start the app in a separated
thread.

Example with uvicorn:

```python
import socket
import threading
import time
from collections.abc import Iterator

from fastapi import FastAPI
import pytest
import uvicorn


def wait_for_socket(host: str, port: int, timeout: int = 5):
    """Wait until the socket is open before proceeding."""
    for _ in range(timeout * 10):  # Check every 0.1s for `timeout` seconds
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                return  # Socket is open
        time.sleep(0.1)
    raise RuntimeError(f"Server on {host}:{port} did not start in time.")


@pytest.fixture(autouse=True)
def fastapi_endpoint(app: FastAPI) -> Iterator[str]:
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8888,
        loop="asyncio",
        lifespan="off",
        log_level="info",
    )
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    wait_for_socket("127.0.0.1", 8888)
    yield "http://127.0.0.1:8888"
    server.should_exit = True
    thread.join()
```
