from pathlib import Path

import pytest

from tests.unittests.entrypoints.fixtures.steps import DummyApp
from tursu.domain.model.gherkin import GherkinDocument
from tursu.entrypoints.plugin import GherkinTestModule, _tursu, tursu_collect_file
from tursu.runtime.registry import Registry, Tursu


@pytest.fixture
def dummy_app():
    return DummyApp()


@pytest.fixture()
def gherkin_test_package(root_dir: Path, request: pytest.FixtureRequest):
    dir = pytest.Dir.from_parent(request.session, path=root_dir)
    pkg = pytest.Package.from_parent(dir, path=root_dir / "tests")
    pkg = pytest.Package.from_parent(pkg, path=root_dir / "tests" / "unittests")
    pkg = pytest.Package.from_parent(
        pkg, path=root_dir / "tests" / "unittests" / "entrypoints"
    )
    pkg = pytest.Package.from_parent(
        pkg, path=root_dir / "tests" / "unittests" / "entrypoints" / "fixtures"
    )
    return pkg


@pytest.fixture()
def gherkin_test_module(gherkin_test_package: pytest.Package, doc: GherkinDocument):
    import tests.unittests.entrypoints.fixtures.steps

    tursu = Tursu()
    tursu.scan(tests.unittests.entrypoints.fixtures.steps)
    return GherkinTestModule.from_parent(
        gherkin_test_package, path=doc.filepath, tursu=tursu
    )


def test_fixture(tursu: Tursu):
    assert tursu is _tursu


def test_tursu_collect_file(
    tursu: Tursu,
    doc: GherkinDocument,
    request: pytest.FixtureRequest,
    gherkin_test_package: pytest.Package,
):
    old_regitry = tursu._registry
    tursu._registry = Registry()
    tursu_collect_file()
    assert "pytest_collect_file" in globals()
    globals()["pytest_collect_file"](gherkin_test_package, doc.filepath)
    repr_handlers = {
        mod: {
            "Given": [repr(h) for h in r._handlers["Given"]],
            "Then": [repr(h) for h in r._handlers["Then"]],
            "When": [repr(h) for h in r._handlers["When"]],
        }
        for mod, r in tursu._registry._handlers.items()
    }
    assert repr_handlers == {
        "tests.unittests.entrypoints.fixtures": {
            "Given": [
                'StepDefinition("a set of users:", a_set_of_users)',
            ],
            "Then": [
                'StepDefinition("the user is connected with username {username}", assert_connected)',
                'StepDefinition("the user is not connected", assert_not_connected)',
            ],
            "When": [
                'StepDefinition("{username} login with password {password}", login)',
            ],
        }
    }

    # we restore the tursu global registry has its previous step.
    tursu._registry = old_regitry


def test_repr(gherkin_test_module: GherkinTestModule):
    assert repr(gherkin_test_module) == "<GherkinDocument login.feature>"


def test_collect_and_run(
    gherkin_test_module: GherkinTestModule,
    request: pytest.FixtureRequest,
    capsys: pytest.CaptureFixture[str],
    dummy_app: DummyApp,
):
    fns = [fn for fn in gherkin_test_module.collect()]
    assert [repr(fn) for fn in fns] == [
        "<Function test_7_User_can_login>",
        "<Function test_10_User_can_t_login_with_wrong_password>",
        "<Function test_17_User_can_t_login_with_someone_else_username[Examples0]>",
        "<Function test_17_User_can_t_login_with_someone_else_username[Examples1]>",
    ]
    tursu = Tursu()
    import tests.unittests.entrypoints.fixtures

    tursu.scan(tests.unittests.entrypoints.fixtures)
    oldparent, request.node.parent = request.node.parent, gherkin_test_module
    fns[0].obj(request, capsys, tursu, dummy_app)  # type: ignore
    request.node.parent = oldparent
