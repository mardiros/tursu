from pathlib import Path

import pytest

from tursu.domain.model.gherkin import GherkinDocument
from tursu.runtime.runner import Tursu


@pytest.fixture()
def gherkin_test_package(root_dir: Path, request: pytest.FixtureRequest):
    dir = pytest.Dir.from_parent(request.session, path=root_dir)
    pkg = pytest.Package.from_parent(dir, path=root_dir / "tests")
    pkg = pytest.Package.from_parent(pkg, path=root_dir / "tests" / "unittests")
    pkg = pytest.Package.from_parent(
        pkg, path=root_dir / "tests" / "unittests" / "service"
    )
    pkg = pytest.Package.from_parent(
        pkg, path=root_dir / "tests" / "unittests" / "service" / "fixtures"
    )
    return pkg


@pytest.fixture
def doc():
    return GherkinDocument.from_file(
        Path(__file__).parent / "fixtures" / "login.feature"
    )


@pytest.fixture
def doc_tagged_example():
    return GherkinDocument.from_file(
        Path(__file__).parent / "fixtures" / "tagged_example.feature"
    )


@pytest.fixture
def registry() -> Tursu:
    import tests.unittests.service.fixtures

    return Tursu().scan(tests.unittests.service.fixtures)
