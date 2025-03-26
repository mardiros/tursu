from pathlib import Path

import pytest

from tursu.domain.model.gherkin import GherkinDocument
from tursu.runtime.registry import Tursu


@pytest.fixture
def docs_dir():
    return Path(__file__).parent / "runtime" / "fixtures"


@pytest.fixture
def doc(docs_dir: Path):
    return GherkinDocument.from_file(docs_dir / "scenario.feature")


@pytest.fixture
def outline_doc(docs_dir: Path):
    return GherkinDocument.from_file(docs_dir / "scenario_outline.feature")


@pytest.fixture(scope="session")
def registry():
    import tests.unittests.runtime.fixtures

    return Tursu().scan(tests.unittests.runtime.fixtures)
