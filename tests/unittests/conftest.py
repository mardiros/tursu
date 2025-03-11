from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from tursu.domain.model.gherkin import GherkinDocument
from tursu.registry import Tursu

docs_dir = Path(__file__).parent / "fixtures"


@pytest.fixture
def doc():
    return GherkinDocument.from_file(docs_dir / "scenario.feature")


@pytest.fixture
def outline_doc():
    return GherkinDocument.from_file(docs_dir / "scenario_outline.feature")


@pytest.fixture(scope="session")
def tursu():
    return Tursu().scan()


@pytest.fixture()
def dummy_app() -> Iterator[Any]:
    from unittests.fixtures.steps import DummyApp

    yield DummyApp()
