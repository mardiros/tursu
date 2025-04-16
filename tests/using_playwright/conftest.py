import socket
import threading
import time
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from tursu import tursu_collect_file

tursu_collect_file()


class HelloWorldHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<body>Hello, World!</body>")


def wait_for_socket(host: str, port: int, timeout: int = 5):
    """Wait until the socket is open before proceeding."""
    for _ in range(timeout * 10):  # Check every 0.1s for `timeout` seconds
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                return  # Socket is open
        time.sleep(0.1)
    raise RuntimeError(f"Server on {host}:{port} did not start in time.")


@pytest.fixture(autouse=True)
def http_server() -> Iterator[str]:
    """Start the service I test in a thread."""
    server_address = ("127.0.0.1", 8888)
    httpd = HTTPServer(server_address, HelloWorldHandler)

    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    wait_for_socket(*server_address)
    yield "http://127.0.0.1:8888"

    httpd.shutdown()
    thread.join()
