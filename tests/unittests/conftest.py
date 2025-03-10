from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from tursu.domain.model.gherkin import GherkinDocument
from tursu.registry import StepRegistry

path = Path(__file__).parent / "fixtures" / "scenario.feature"


@pytest.fixture
def doc():
    return GherkinDocument.from_file(path)


@pytest.fixture(scope="session")
def registry():
    return StepRegistry().scan()


@pytest.fixture()
def dummy_app() -> Iterator[Any]:
    from unittests.fixtures.steps import DummyApp

    yield DummyApp()
