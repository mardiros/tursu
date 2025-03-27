import ast
import textwrap
from collections.abc import Sequence
from pathlib import Path

import pytest
from typing_extensions import Any

from tests.unittests.service.fixtures.conftest import DummyApp
from tursu.domain.model.gherkin import (
    GherkinFeature,
    GherkinLocation,
    GherkinScenario,
    GherkinStep,
    GherkinTag,
)
from tursu.domain.model.testmod import TestModule
from tursu.runtime.registry import Tursu
from tursu.service.ast.astfunction import TestFunctionWriter


@pytest.fixture()
def scenario(steps: Sequence[GherkinStep]) -> GherkinScenario:
    return GherkinScenario(
        id="1",
        location=GherkinLocation(line=1, column=1),
        name="dummy",
        description="",
        keyword="Scenario",
        steps=steps,
        tags=[],
    )


@pytest.mark.parametrize(
    "steps,expected_fixtures",
    [
        pytest.param([], {}, id="empty"),
        pytest.param(
            [
                GherkinStep(
                    id="1",
                    location=GherkinLocation(line=1, column=1),
                    keyword="Given",
                    text="a set of users:",
                    keywordType="Context",
                )
            ],
            {
                "app": DummyApp,
            },
            id="fixture",
        ),
    ],
)
def test_fixtures(
    registry: Tursu,
    scenario: GherkinScenario,
    steps: Sequence[GherkinStep],
    expected_fixtures: dict[str, type],
):
    fn = TestFunctionWriter(scenario, registry, stack=[], steps=[])
    fixtures = fn.build_fixtures(steps, registry)
    assert fixtures == expected_fixtures


@pytest.mark.parametrize(
    "steps,expected_error",
    [
        pytest.param(
            [
                GherkinStep(
                    id="1",
                    location=GherkinLocation(line=1, column=1),
                    keyword="And",
                    text="a set of users:",
                    keywordType="Conjunction",
                )
            ],
            'Using "And" keyword without context',
            id="fixture",
        ),
    ],
)
def test_fixtures_invalid(
    registry: Tursu,
    scenario: GherkinScenario,
    steps: Sequence[GherkinStep],
    expected_error: str,
):
    fn = TestFunctionWriter(scenario, registry, stack=[], steps=[])
    with pytest.raises(ValueError) as ctx:
        fn.build_fixtures(steps, registry)
    assert str(ctx.value) == expected_error


@pytest.mark.parametrize(
    "steps,stack,expected_result",
    [
        pytest.param(
            [],
            [
                GherkinFeature(
                    children=[],
                    description="",
                    keyword="Feature",
                    language="",
                    location=GherkinLocation(line=1, column=1),
                    name="",
                    tags=[
                        GherkinTag(
                            id="",
                            name="tik",
                            location=GherkinLocation(line=1, column=1),
                        )
                    ],
                )
            ],
            textwrap.dedent(
                """\
                @pytest.mark.tik
                def test_dummy():
                    ...
                """
            ).strip(),
            id="fixture",
        ),
    ],
)
def test_build_tags_decorators(
    tmpdir: Path,
    registry: Tursu,
    scenario: GherkinScenario,
    stack: Sequence[Any],
    expected_result: str,
):
    fn = TestFunctionWriter(scenario, registry, stack=[], steps=[])
    decorators = fn.build_tags_decorators(stack)

    module = ast.Module(
        body=[
            ast.FunctionDef(
                name="test_dummy",
                args=ast.arguments(
                    args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None
                ),
                body=[ast.Expr(value=ast.Constant(value=Ellipsis))],
                decorator_list=decorators,
                lineno=1,
            )
        ]
    )
    tmod = TestModule("dummy", module)
    tmod.write_temporary(tmpdir)
    assert (tmpdir / tmod.filename).read_text(encoding="utf-8") == expected_result
