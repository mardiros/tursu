from pathlib import Path

import pytest

from tursu.domain.model.gherkin import GherkinDocument


@pytest.fixture
def doc() -> GherkinDocument:
    return GherkinDocument.from_file(
        Path(__file__).parent / "fixtures" / "login.feature"
    )


@pytest.fixture
def registry() -> Tursu:
    import tests.unittests.domain.fixtures

    return Tursu().scan(tests.unittests.domain.fixtures)
