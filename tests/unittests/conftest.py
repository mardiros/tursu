from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel

from tursu.domain.model.gherkin import GherkinDocument
from tursu.registry import Tursu


class DummyMail(BaseModel):
    email: str
    subject: str
    body: str


class DummyApp:
    def __init__(self):
        self.mailboxes: dict[str, list[DummyMail]] = {}

    def create_user(self, username: str) -> None:
        assert username not in self.mailboxes
        self.mailboxes[username] = []

    def add_mailbox(self, username: str, mailbox: str) -> None:
        assert username in self.mailboxes
        self.mailboxes[username] = [
            DummyMail(email=mailbox, subject=f"Welcome {username}", body="...")
        ]


@pytest.fixture
def docs_dir():
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def doc(docs_dir: Path):
    return GherkinDocument.from_file(docs_dir / "scenario.feature")


@pytest.fixture
def outline_doc(docs_dir: Path):
    return GherkinDocument.from_file(docs_dir / "scenario_outline.feature")


@pytest.fixture(scope="session")
def registry():
    return Tursu().scan()


@pytest.fixture()
def dummy_app() -> Iterator[Any]:
    from tests.unittests.fixtures.steps import DummyApp

    yield DummyApp()
