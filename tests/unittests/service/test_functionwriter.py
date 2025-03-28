import ast
import textwrap
from collections.abc import Sequence
from pathlib import Path
from typing import Annotated, cast

import pytest
from pydantic.main import BaseModel
from typing_extensions import Any

from tests.unittests.service.fixtures.conftest import DummyApp
from tursu.domain.model.gherkin import (
    GherkinCell,
    GherkinDataTable,
    GherkinDocString,
    GherkinFeature,
    GherkinLocation,
    GherkinScenario,
    GherkinStep,
    GherkinTableRow,
    GherkinTag,
)
from tursu.domain.model.steps import StepKeyword
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


@pytest.mark.parametrize(
    "steps,expected_keywords",
    [
        pytest.param([], [], id="empty"),
        pytest.param(
            [
                GherkinStep(
                    id="1",
                    location=GherkinLocation(line=1, column=1),
                    keyword="Given",
                    text="a set of users:",
                    keywordType="Context",
                ),
                GherkinStep(
                    id="1",
                    location=GherkinLocation(line=1, column=1),
                    keyword="And",
                    text="a set of users:",
                    keywordType="Conjunction",
                ),
                GherkinStep(
                    id="1",
                    location=GherkinLocation(line=1, column=1),
                    keyword="When",
                    text="Alice login with password pwd",
                    keywordType="Action",
                ),
                GherkinStep(
                    id="1",
                    location=GherkinLocation(line=1, column=1),
                    keyword="Then",
                    text="the user is not connected",
                    keywordType="Outcome",
                ),
            ],
            [
                "Given",
                "Given",
                "When",
                "Then",
            ],
            id="And becomes Given",
        ),
    ],
)
def test_get_keyword(
    registry: Tursu,
    scenario: GherkinScenario,
    steps: Sequence[GherkinStep],
    expected_keywords: Sequence[StepKeyword],
):
    fn = TestFunctionWriter(scenario, registry, stack=[], steps=[])
    keywords = [fn.get_keyword(step) for step in steps]
    assert keywords == expected_keywords


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
                ),
            ],
            'Using "And" keyword without context',
            id="And",
        ),
    ],
)
def test_get_keyword_error(
    registry: Tursu,
    scenario: GherkinScenario,
    steps: Sequence[GherkinStep],
    expected_error: str,
):
    fn = TestFunctionWriter(scenario, registry, stack=[], steps=[])
    with pytest.raises(ValueError) as ctx:
        fn.get_keyword(steps[0])
    assert str(ctx.value) == expected_error


def given_username(username: str): ...


def given_username_fixture(username: str, fixture: str): ...


def given_raw_data_table(data_table: list[dict[str, str]]): ...


def given_doc_string(doc_string: dict[str, str]): ...


class User(BaseModel):
    username: str


def given_parsed_data_table(data_table: list[User]): ...


def load_user(username: str): ...


def given_parsed_annotated_data_table(data_table: list[Annotated[User, load_user]]): ...


@pytest.mark.parametrize(
    "steps,step,handler,expected_result",
    [
        pytest.param(
            [],
            GherkinStep(
                id="1",
                location=GherkinLocation(line=1, column=1),
                keyword="Given",
                text="a user {username}",
                keywordType="Context",
            ),
            given_username,
            textwrap.dedent(
                """
                def test_dummy():
                    step()
                """
            ).strip(),
            id="no-fixture",
        ),
        pytest.param(
            [],
            GherkinStep(
                id="1",
                location=GherkinLocation(line=1, column=1),
                keyword="Given",
                text="a user {username}",
                keywordType="Context",
            ),
            given_username_fixture,
            textwrap.dedent(
                """
                def test_dummy():
                    step(fixture=fixture)
                """
            ).strip(),
            id="fixture",
        ),
        pytest.param(
            [],
            GherkinStep(
                id="1",
                location=GherkinLocation(line=1, column=1),
                keyword="Given",
                text="a set of users:",
                keywordType="Context",
                dataTable=GherkinDataTable(
                    location=GherkinLocation(line=1, column=1),
                    rows=[
                        GherkinTableRow(
                            id="header",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="username",
                                )
                            ],
                        ),
                        GherkinTableRow(
                            id="row1",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="alice",
                                )
                            ],
                        ),
                        GherkinTableRow(
                            id="row2",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="bob",
                                )
                            ],
                        ),
                    ],
                ),
            ),
            given_raw_data_table,
            textwrap.dedent(
                """
                def test_dummy():
                    step(data_table=[{'username': 'alice'}, {'username': 'bob'}])
                """
            ).strip(),
            id="raw data_table",
        ),
        pytest.param(
            [],
            GherkinStep(
                id="1",
                location=GherkinLocation(line=1, column=1),
                keyword="Given",
                text="a set of users:",
                keywordType="Context",
                dataTable=GherkinDataTable(
                    location=GherkinLocation(line=1, column=1),
                    rows=[
                        GherkinTableRow(
                            id="header",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="username",
                                )
                            ],
                        ),
                        GherkinTableRow(
                            id="row1",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="alice",
                                )
                            ],
                        ),
                        GherkinTableRow(
                            id="row2",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="bob",
                                )
                            ],
                        ),
                        GherkinTableRow(
                            id="row3",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="",
                                )
                            ],
                        ),
                    ],
                ),
            ),
            given_parsed_data_table,
            textwrap.dedent(
                """
                def test_dummy():
                    step(data_table=[User0(username='alice'), User0(username='bob'), User0()])
                """
            ).strip(),
            id="parsed data_table",
        ),
        pytest.param(
            [],
            GherkinStep(
                id="1",
                location=GherkinLocation(line=1, column=1),
                keyword="Given",
                text="a set of users:",
                keywordType="Context",
                dataTable=GherkinDataTable(
                    location=GherkinLocation(line=1, column=1),
                    rows=[
                        GherkinTableRow(
                            id="header",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="username",
                                )
                            ],
                        ),
                        GherkinTableRow(
                            id="row1",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="alice",
                                )
                            ],
                        ),
                        GherkinTableRow(
                            id="row2",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="bob",
                                )
                            ],
                        ),
                        GherkinTableRow(
                            id="row3",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="",
                                )
                            ],
                        ),
                    ],
                ),
            ),
            given_parsed_annotated_data_table,
            textwrap.dedent(
                """
                def test_dummy():
                    step(data_table=[load_user0(username='alice'), load_user0(username='bob'), load_user0()])
                """
            ).strip(),
            id="parsed given_parsed_annotated_data_table",
        ),
        pytest.param(
            [],
            GherkinStep(
                id="1",
                location=GherkinLocation(line=1, column=1),
                keyword="Given",
                text="a set of users:",
                keywordType="Context",
                docString=GherkinDocString(
                    location=GherkinLocation(line=1, column=1),
                    content="username\nbob\nalice",
                    delimiter="",
                    mediaType="csv",
                ),
            ),
            given_doc_string,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string='username\\nbob\\nalice')
                """
            ).strip(),
            id="docstring",
        ),
        pytest.param(
            [],
            GherkinStep(
                id="1",
                location=GherkinLocation(line=1, column=1),
                keyword="Given",
                text="a set of users:",
                keywordType="Context",
                docString=GherkinDocString(
                    location=GherkinLocation(line=1, column=1),
                    content='[{"username": "alice"}, {"username": "bob"}]',
                    delimiter="",
                    mediaType="json",
                ),
            ),
            given_doc_string,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string=[{'username': 'alice'}, {'username': 'bob'}])
                """
            ).strip(),
            id="docstring json",
        ),
    ],
)
def test_build_step_kwargs(
    scenario: GherkinScenario,
    steps: Sequence[GherkinStep],
    step: GherkinStep,
    handler: Any,
    expected_result: str,
    tmpdir: Path,
):
    registry = Tursu()
    step_keyword = cast(StepKeyword, step.keyword)
    registry.register_handler(step_keyword, step.text, handler)
    fn = TestFunctionWriter(scenario, registry, stack=[], steps=[])
    kwargs = fn.build_step_kwargs(step_keyword, step)

    module = ast.Module(
        body=[
            ast.FunctionDef(
                name="test_dummy",
                args=ast.arguments(
                    args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None
                ),
                body=[
                    ast.Expr(
                        ast.Call(
                            func=ast.Name(id="step", ctx=ast.Load()),
                            args=[],
                            keywords=kwargs,
                        )
                    )
                ],
                decorator_list=[],
                lineno=1,
            )
        ]
    )
    tmod = TestModule("dummy", module)
    tmod.write_temporary(tmpdir)
    assert (tmpdir / tmod.filename).read_text(encoding="utf-8") == expected_result
