import pytest

from tests.unittests.entrypoints.fixtures.steps import DummyApp
from tursu.domain.model.gherkin import GherkinDocument
from tursu.entrypoints.plugin import GherkinTestModule, _tursu, tursu_collect_file
from tursu.runtime.registry import Tursu


@pytest.fixture
def dummy_app():
    return DummyApp()


@pytest.fixture()
def gherkin_test_module(doc: GherkinDocument, request: pytest.FixtureRequest):
    import tests.unittests.entrypoints.fixtures.steps

    tursu = Tursu()
    tursu.scan(tests.unittests.entrypoints.fixtures.steps)
    return GherkinTestModule.from_parent(
        request.session, path=doc.filepath, tursu=tursu
    )


def test_fixture(tursu: Tursu):
    assert tursu is _tursu


def test_tursu_collect_file(
    tursu: Tursu, doc: GherkinDocument, request: pytest.FixtureRequest
):
    old_handlers = tursu._handlers
    tursu._handlers = {"Given": [], "Then": [], "When": []}
    tursu_collect_file()
    assert "pytest_collect_file" in globals()
    pkg = pytest.Package.from_parent(request.session, path=doc.filepath.parent)
    globals()["pytest_collect_file"](pkg, doc.filepath)
    repr_handlers = {
        "Given": [repr(h) for h in tursu._handlers["Given"]],
        "Then": [repr(h) for h in tursu._handlers["Then"]],
        "When": [repr(h) for h in tursu._handlers["When"]],
    }
    assert repr_handlers == {
        "Given": [
            'Step("a set of users:", a_set_of_users)',
        ],
        "Then": [
            'Step("the user is connected with username {username}", assert_connected)',
            'Step("the user is not connected", assert_not_connected)',
        ],
        "When": [
            'Step("{username} login with password {password}", login)',
        ],
    }

    # we restore the tursu global registry has its previous step.
    tursu._handlers = old_handlers


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
    fns[0].obj(request, capsys, tursu, dummy_app)  # type: ignore
