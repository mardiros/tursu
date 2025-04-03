from pathlib import Path

import pytest

from tursu.domain.model.gherkin import GherkinDocument
from tursu.entrypoints.plugin import GherkinTestModule
from tursu.runtime.registry import ModRegistry, Tursu


@pytest.fixture()
def registry():
    import tests.unittests.runtime.fixtures

    return Tursu().scan(tests.unittests.runtime.fixtures)


@pytest.fixture()
def gherkin_test_package(root_dir: Path, request: pytest.FixtureRequest):
    dir = pytest.Dir.from_parent(request.session, path=root_dir)
    pkg = pytest.Package.from_parent(dir, path=root_dir / "tests")
    pkg = pytest.Package.from_parent(pkg, path=root_dir / "tests" / "unittests")
    pkg = pytest.Package.from_parent(
        pkg, path=root_dir / "tests" / "unittests" / "runtime"
    )
    pkg = pytest.Package.from_parent(
        pkg, path=root_dir / "tests" / "unittests" / "runtime" / "fixtures"
    )
    return pkg


@pytest.fixture()
def doc() -> GherkinDocument:
    return GherkinDocument.from_file(
        Path(__file__).parent / "fixtures" / "scenario.feature"
    )


@pytest.fixture()
def gherkin_test_module(
    registry: Tursu, gherkin_test_package: pytest.Package, doc: GherkinDocument
):
    return GherkinTestModule.from_parent(
        gherkin_test_package, path=doc.filepath, tursu=registry
    )


@pytest.fixture()
def mod_registry(registry: Tursu) -> ModRegistry:
    return registry._registry._step_defs["tests.unittests.runtime.fixtures"]
