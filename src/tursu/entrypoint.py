import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

DEFAULT_INIT = '''\
"""
Functional tests suite based on Turşu.

Documentation: https://mardiros.github.io/tursu/
"""
'''

DEFAULT_CONFTEST = """\
from tursu.plugin import tursu_collect_file

tursu_collect_file()
"""

DEFAULT_CONFTEST_WITH_DUMMIES = f'''\
import pytest

{DEFAULT_CONFTEST}

class DummyApp:
    """Represent a tested application"""
    def __init__(self):
        self.users = {{}}
        self.connected_user: str | None = None

    def login(self, username: str, password: str) -> None:
        if username in self.users and self.users[username] == password:
            self.connected_user = username


@pytest.fixture()
def app() -> DummyApp:
    return DummyApp()
'''

DEFAULT_STEPS = """\
from tursu import given, then, when

from .conftest import DummyApp


@given("a user {username} with password {password}")
def give_user(app: DummyApp, username: str, password: str):
    app.users[username] = password


@when("{username} login with password {password}")
def login(app: DummyApp, username: str, password: str):
    app.login(username, password)


@then("I am connected with username {username}")
def assert_connected(app: DummyApp, username: str):
    assert app.connected_user == username

@then("I am not connected")
def assert_not_connected(app: DummyApp):
    assert app.connected_user is None
"""

DEFAULT_FEATURE = """\
Feature: As a user I logged in with my password

  Scenario: I properly logged in
    Given a user Bob with password dumbsecret
    When Bob login with password dumbsecret
    Then I am connected with username Bob

  Scenario: I hit the wrong password
    Given a user Bob with password dumbsecret
    When Bob login with password notthat
    Then I am not connected

  Scenario: I user another login
    Given a user Bob with password dumbsecret
    And a user Alice with password anothersecret
    When Alice login with password dumbsecret
    Then I am not connected
    When Bob login with password dumbsecret
    Then I am connected with username Bob
"""


def init(outdir: str, overwrite: bool, no_dummies: bool) -> None:
    with_dummies = not no_dummies
    outpath = Path(outdir)
    if outpath.exists() and not overwrite:
        print(f"{outdir} already exists")
        sys.exit(1)

    if outpath.is_file():
        outpath.unlink()

    outpath.mkdir(exist_ok=True)
    (outpath / "__init__.py").write_text(DEFAULT_INIT)
    (outpath / "conftest.py").write_text(
        DEFAULT_CONFTEST_WITH_DUMMIES if with_dummies else DEFAULT_CONFTEST
    )

    if with_dummies:
        (outpath / "steps.py").write_text(DEFAULT_STEPS)
        (outpath / "login.feature").write_text(DEFAULT_FEATURE)


def main(args: Sequence[str] = sys.argv) -> None:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="action", required=True)

    sp_action = subparsers.add_parser("init")
    sp_action.add_argument(
        "-o",
        "--out-dir",
        dest="outdir",
        default="tests/functionals",
        help="Directory where the handlers will be generated",
    )
    sp_action.add_argument(
        "--overwrite", action="store_true", dest="overwrite", default=False
    )
    sp_action.add_argument(
        "--no-dummies", action="store_true", dest="no_dummies", default=False
    )

    sp_action.set_defaults(handler=init)
    kwargs = parser.parse_args(args[1:])
    kwargs_dict = vars(kwargs)

    handler = kwargs_dict.pop("handler")
    handler(**kwargs_dict)
