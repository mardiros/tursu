"""Command line interface."""

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
from tursu import tursu_collect_file

tursu_collect_file()
"""

DEFAULT_CONFTEST_WITH_DUMMIES = f'''\
import pytest

{DEFAULT_CONFTEST}

class DummyApp:
    """Represent a tested application."""
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
from dataclasses import dataclass

from tursu import given, then, when

from .conftest import DummyApp


@dataclass
class User:
    username: str
    password: str


@given("a set of users:")
def a_set_of_users(app: DummyApp, data_table: list[User]):
    for user in data_table:
        app.users[user.username] = user.password


@when("{username} login with password {password}")
def login(app: DummyApp, username: str, password: str):
    app.login(username, password)


@then("the user is connected with username {username}")
def assert_connected(app: DummyApp, username: str):
    assert app.connected_user == username


@then("the user is not connected")
def assert_not_connected(app: DummyApp):
    assert app.connected_user is None

"""

DEFAULT_FEATURE = """\
Feature: User login with their own password

  Background:
    Given a set of users:
      | username | password      |
      | Bob      | dumbsecret    |
      | Alice    | anothersecret |

  Scenario: User can login
    When Bob login with password dumbsecret
    Then the user is connected with username Bob

  Scenario: User can't login with wrong password
    When Bob login with password notthat
    Then the user is not connected

  Scenario Outline: User can't login with someone else username
    When <username> login with password <password>
    Then the user is not connected

    Examples:
      | username | password      |
      | Bob      | anothersecret |
      | Alice    | dumbsecret    |

"""


def init(outdir: str, overwrite: bool, no_dummies: bool) -> None:
    """
    Will write a functional tests directory.

    :param outdir: destination
    :param overwrite: overwrite existing file.
    :param no_dummies: do not write dummy fixtures and tests.
    """
    with_dummies = not no_dummies
    outpath = Path(outdir)
    if outpath.exists() and not overwrite:
        print(f"{outdir} already exists")
        sys.exit(1)

    if outpath.is_file():
        outpath.unlink()

    outpath.mkdir(exist_ok=True, parents=True)
    (outpath / "__init__.py").write_text(DEFAULT_INIT)
    (outpath / "conftest.py").write_text(
        DEFAULT_CONFTEST_WITH_DUMMIES if with_dummies else DEFAULT_CONFTEST
    )

    if with_dummies:
        (outpath / "steps.py").write_text(DEFAULT_STEPS)
        (outpath / "login.feature").write_text(DEFAULT_FEATURE)


def main(args: Sequence[str] = sys.argv) -> None:
    """Entrypoint of the CLI."""
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
