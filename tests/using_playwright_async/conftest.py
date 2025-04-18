import asyncio
import socket

import pytest
import uvicorn
from playwright.async_api import async_playwright
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Route

from tursu import tursu_collect_file

tursu_collect_file()


async def homepage(request: Request):
    return HTMLResponse("<body>Hello, World!</body>")


app = Starlette(routes=[Route("/", homepage)])


async def wait_for_socket(
    host: str, port: int, timeout: int = 5, poll_time: float = 0.1
):
    """Wait until the socket is open, or raise an error if the timeout is exceeded."""
    for _ in range(timeout * int(1 / poll_time)):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                break
        await asyncio.sleep(poll_time)
    else:
        raise RuntimeError(f"Server on {host}:{port} did not start in time.")


@pytest.fixture(autouse=True)
async def http_server():
    """Start the service in an asyncio task."""
    host, port = "127.0.0.1", 8888
    config = uvicorn.Config(
        app, host=host, port=port, log_level="error", loop="asyncio"
    )
    server = uvicorn.Server(config)

    task = asyncio.create_task(server.serve())
    await wait_for_socket(host, port)

    yield f"http://{host}:{port}"

    server.should_exit = True
    await task


@pytest.fixture()
async def page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        yield page
        await browser.close()
