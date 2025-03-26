from pathlib import Path

import pytest

from tursu.domain.model.gherkin import GherkinDocument


@pytest.fixture
def doc() -> GherkinDocument:
    return GherkinDocument.from_file(
        Path(__file__).parent / "fixtures" / "login.feature"
    )
