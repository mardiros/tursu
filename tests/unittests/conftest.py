from pathlib import Path

import pytest

from tursu.domain.model.gherkin import GherkinDocument

path = Path(__file__).parent / "fixtures" / "scenario.feature"


@pytest.fixture
def doc():
    return GherkinDocument.from_file(path)
