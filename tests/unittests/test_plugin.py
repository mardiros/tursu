from pathlib import Path

import pytest

from tests.unittests.fixtures.steps import DummyApp
from tursu.plugin import GherkinTestModule, _tursu
from tursu.registry import Tursu


def test_fixture(tursu: Tursu):
    assert tursu is _tursu


@pytest.fixture()
def gherkin_test_module(request: pytest.FixtureRequest, docs_dir: Path):
    import tests.unittests.fixtures.steps

    tursu = Tursu()
    tursu.scan(tests.unittests.fixtures.steps)
    return GherkinTestModule.from_parent(
        request.session, path=docs_dir / "scenario.feature", tursu=tursu
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
        "<Function test_10_I_can_find_scenario_based_on_tag>"
    ]
    tursu = Tursu()
    import tests.unittests.fixtures

    tursu.scan(tests.unittests.fixtures)
    fns[0].obj(request, capsys, tursu, dummy_app)  # type: ignore
