from pathlib import Path

import pytest

from tests.unittests.runtime.fixtures.steps import DummyApp
from tursu.domain.model.gherkin import GherkinDocument
from tursu.plugin import GherkinTestModule, _tursu, tursu_collect_file
from tursu.runtime.registry import Tursu


@pytest.fixture
def dummy_app():
    return DummyApp()


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
            'Step("a user {username}", give_user)',
            'Step("a set of users:", a_set_of_users)',
        ],
        "Then": [
            'Step("the users dataset is", assert_dataset)',
            'Step("the API for {username} respond", assert_api_response)',
            'Step("the users raw dataset is", assert_dataset_raw)',
            'Step("the mailbox {email} "{subject}" message is", '
            "assert_mailbox_contains)",
            'Step("{username} see a mailbox {email}", assert_user_has_mailbox)',
            'Step("the user is connected with username {username}", assert_connected)',
            'Step("the user is not connected", assert_not_connected)',
        ],
        "When": [
            'Step("{username} create a mailbox {email}", create_mailbox)',
            'Step("{username} login with password {password}", login)',
        ],
    }

    # we restore the tursu global registry has its previous step.
    tursu._handlers = old_handlers


@pytest.fixture()
def gherkin_test_module(request: pytest.FixtureRequest, docs_dir: Path):
    import tests.unittests.runtime.fixtures.dataset_factory
    import tests.unittests.runtime.fixtures.steps

    tursu = Tursu()
    tursu.scan(tests.unittests.runtime.fixtures.dataset_factory)
    tursu.scan(tests.unittests.runtime.fixtures.steps)
    return GherkinTestModule.from_parent(
        request.session, path=docs_dir / "scenario.feature", tursu=tursu
    )


@pytest.fixture()
def gherkin_test_module_dataset(request: pytest.FixtureRequest, docs_dir: Path):
    import tests.unittests.runtime.fixtures.dataset_factory
    import tests.unittests.runtime.fixtures.steps

    tursu = Tursu()
    tursu.scan(tests.unittests.runtime.fixtures.dataset_factory)
    tursu.scan(tests.unittests.runtime.fixtures.steps)
    return GherkinTestModule.from_parent(
        request.session, path=docs_dir / "scenario_datatable.feature", tursu=tursu
    )


def test_repr(gherkin_test_module: GherkinTestModule):
    assert repr(gherkin_test_module) == "<GherkinDocument scenario.feature>"


def test_collect_and_run(
    gherkin_test_module: GherkinTestModule,
    request: pytest.FixtureRequest,
    capsys: pytest.CaptureFixture[str],
    dummy_app: DummyApp,
):
    fns = [fn for fn in gherkin_test_module.collect()]
    assert [repr(fn) for fn in fns] == [
        # should be <Scenario ...>
        "<Function test_13_I_can_find_scenario_based_on_tag>"
    ]
    tursu = Tursu()
    import tests.unittests.runtime.fixtures

    tursu.scan(tests.unittests.runtime.fixtures)
    fns[0].obj(request, capsys, tursu, dummy_app)  # type: ignore


def test_collect_and_run_datatable(
    gherkin_test_module_dataset: GherkinTestModule,
    request: pytest.FixtureRequest,
    capsys: pytest.CaptureFixture[str],
    dummy_app: DummyApp,
):
    fns = [fn for fn in gherkin_test_module_dataset.collect()]
    assert [repr(fn) for fn in fns] == [
        # should be <Scenario ...>
        "<Function test_8_Fill_a_dataset_with_a_factory>"
    ]
    tursu = Tursu()
    import tests.unittests.runtime.fixtures

    tursu.scan(tests.unittests.runtime.fixtures)
    fns[0].obj(request, capsys, tursu, dummy_app)  # type: ignore
