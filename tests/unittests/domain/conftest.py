from pathlib import Path

import pytest

from tursu.domain.model.gherkin import GherkinDocument
from tursu.runtime.runner import Tursu


@pytest.fixture
def doc():
    return GherkinDocument.from_file(
        Path(__file__).parent / "fixtures" / "login.feature"
    )


@pytest.fixture
def registry() -> Tursu:
    import tests.unittests.domain.fixtures

    return Tursu().scan(tests.unittests.domain.fixtures)
