import ast
import textwrap
from collections.abc import Mapping, Sequence
from typing import Annotated, Any, cast

import pytest
from pydantic.main import BaseModel

from tests.unittests.service.fixtures.steps import DummyApp
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


@pytest.fixture()
def async_scenario(steps: Sequence[GherkinStep]) -> GherkinScenario:
    return GherkinScenario(
        id="1",
        location=GherkinLocation(line=1, column=1),
        name="dummy",
        description="",
        keyword="Scenario",
        steps=steps,
        tags=[
            GherkinTag(
                name="asyncio",
                id="1",
                location=GherkinLocation(line=1, column=1),
            )
        ],
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
    fn = TestFunctionWriter(
        scenario,
        registry,
        stack=[],
        steps=[],
        package_name="tests.unittests.service.fixtures",
    )
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
    fn = TestFunctionWriter(
        scenario,
        registry,
        stack=[],
        steps=[],
        package_name="tests.unittests.service.fixtures",
    )
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
    registry: Tursu,
    scenario: GherkinScenario,
    stack: Sequence[Any],
    expected_result: str,
):
    fn = TestFunctionWriter(
        scenario,
        registry,
        stack=[],
        steps=[],
        package_name="tests.unittests.service.fixtures",
    )
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
    assert str(tmod) == expected_result


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
                    text="Alice signs in with password pwd",
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
    fn = TestFunctionWriter(
        scenario,
        registry,
        stack=[],
        steps=[],
        package_name="tests.unittests.service.fixtures",
    )
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
    fn = TestFunctionWriter(
        scenario,
        registry,
        stack=[],
        steps=[],
        package_name="tests.unittests.service.fixtures",
    )
    with pytest.raises(ValueError) as ctx:
        fn.get_keyword(steps[0])
    assert str(ctx.value) == expected_error


def given_username(username: str): ...


def given_username_fixture(username: str, fixture: str): ...


def given_username_request_fixture(username: str, request: pytest.FixtureRequest): ...


def given_raw_data_table(data_table: list[dict[str, str]]): ...


def given_raw_revesed_data_table(data_table: dict[str, str]): ...


def given_raw_doc_string(doc_string: str): ...


def given_doc_string(doc_string: dict[str, str]): ...


def given_doc_string_seq(doc_string: list[dict[str, str]]): ...


def given_ast_doc_string(doc_string: set[str]): ...


class User(BaseModel):
    username: str


def given_parsed_doc_string(doc_string: User): ...


def given_parsed_doc_string_seq(doc_string: list[User]): ...


def given_parsed_data_table(data_table: list[User]): ...


def given_parsed_rev_data_table(data_table: User): ...


def load_user(username: str): ...


def given_parsed_annotated_data_table(data_table: list[Annotated[User, load_user]]): ...


def given_parsed_annotated_rev_data_table(data_table: Annotated[User, load_user]): ...


def given_parsed_annotated_doc_string(doc_string: Annotated[User, load_user]): ...


def given_parsed_annotated_doc_string_seq(
    doc_string: list[Annotated[User, load_user]],
): ...


@pytest.mark.parametrize(
    "steps,fixtures,examples_keys,expected_result",
    [
        pytest.param(
            [],
            {},
            [],
            textwrap.dedent(
                """
                def test_dummy(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu):
                    ...
                """
            ).strip(),
            id="no-fixture",
        ),
        pytest.param(
            [],
            {"fixture1": ...},
            [],
            textwrap.dedent(
                """
                def test_dummy(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu, fixture1: Any):
                    ...
                """
            ).strip(),
            id="fixture",
        ),
        pytest.param(
            [],
            {"request": ..., "capsys": ..., "tursu": ...},
            [],
            textwrap.dedent(
                """
                def test_dummy(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu):
                    ...
                """
            ).strip(),
            id="existing fixtures",
        ),
        pytest.param(
            [],
            {"request": ..., "fixture1": ...},
            [],
            textwrap.dedent(
                """
                def test_dummy(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu, fixture1: Any):
                    ...
                """
            ).strip(),
            id="mix",
        ),
    ],
)
def test_build_args(
    scenario: GherkinScenario,
    steps: Sequence[GherkinStep],
    fixtures: Mapping[str, Any],
    examples_keys: Sequence[Any],
    expected_result: str,
):
    registry = Tursu()
    fn = TestFunctionWriter(
        scenario,
        registry,
        stack=[],
        steps=[],
        package_name="tests.unittests.service.fixtures",
    )
    args = fn.build_args(fixtures, examples_keys)

    module = ast.Module(
        body=[
            ast.FunctionDef(
                name="test_dummy",
                args=ast.arguments(
                    args=args, vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None
                ),
                body=[
                    ast.Expr(value=ast.Constant(Ellipsis)),
                ],
                decorator_list=[],
                lineno=1,
            )
        ]
    )
    tmod = TestModule("dummy", module)
    assert str(tmod) == expected_result


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
                text="a user {username}",
                keywordType="Context",
            ),
            given_username_request_fixture,
            textwrap.dedent(
                """
                def test_dummy():
                    step(request=request)
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
                docString=GherkinDocString(
                    location=GherkinLocation(line=1, column=1),
                    content="username\nbob\nalice",
                    delimiter="",
                    mediaType="csv",
                ),
            ),
            given_raw_doc_string,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string='username\\nbob\\nalice')
                """
            ).strip(),
            id="docstring",
        ),
    ],
)
def test_build_step_kwargs(
    scenario: GherkinScenario,
    steps: Sequence[GherkinStep],
    step: GherkinStep,
    handler: Any,
    expected_result: str,
):
    registry = Tursu()
    step_keyword = cast(StepKeyword, step.keyword)
    registry.register_step_definition(
        "tests.unittests.service.fixtures", step_keyword, step.text, handler
    )
    fn = TestFunctionWriter(
        scenario,
        registry,
        stack=[],
        steps=[],
        package_name="tests.unittests.service.fixtures",
    )
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
    assert str(tmod) == expected_result


@pytest.mark.parametrize(
    "steps,step,handler,expected_result",
    [
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
                text="a user:",
                keywordType="Context",
                dataTable=GherkinDataTable(
                    location=GherkinLocation(line=1, column=1),
                    rows=[
                        GherkinTableRow(
                            id="row1",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="username",
                                ),
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="alice",
                                ),
                            ],
                        ),
                        GherkinTableRow(
                            id="row2",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="password",
                                ),
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="secret",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
            given_raw_revesed_data_table,
            textwrap.dedent(
                """
                def test_dummy():
                    step(data_table={'username': 'alice', 'password': 'secret'})
                """
            ).strip(),
            id="raw reversed data_table",
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
            id="parsed annotated data_table",
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
                            id="row1",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="username",
                                ),
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="alice",
                                ),
                            ],
                        ),
                        GherkinTableRow(
                            id="row2",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="password",
                                ),
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="secret",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
            given_parsed_rev_data_table,
            textwrap.dedent(
                """
                def test_dummy():
                    step(data_table=User0(username='alice', password='secret'))
                """
            ).strip(),
            id="parsed reverse data_table",
        ),
        pytest.param(
            [],
            GherkinStep(
                id="1",
                location=GherkinLocation(line=1, column=1),
                keyword="Given",
                text="a user with a random password:",
                keywordType="Context",
                dataTable=GherkinDataTable(
                    location=GherkinLocation(line=1, column=1),
                    rows=[
                        GherkinTableRow(
                            id="row1",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="username",
                                ),
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="alice",
                                ),
                            ],
                        ),
                        GherkinTableRow(
                            id="row2",
                            location=GherkinLocation(line=1, column=1),
                            cells=[
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="password",
                                ),
                                GherkinCell(
                                    location=GherkinLocation(line=1, column=1),
                                    value="",
                                ),
                            ],
                        ),
                    ],
                ),
            ),
            given_parsed_annotated_rev_data_table,
            textwrap.dedent(
                """
                def test_dummy():
                    step(data_table=load_user0(username='alice'))
                """
            ).strip(),
            id="parsed annotated reverved data_table",
        ),
    ],
)
def test_parse_data_table(
    scenario: GherkinScenario,
    steps: Sequence[GherkinStep],
    step: GherkinStep,
    handler: Any,
    expected_result: str,
):
    registry = Tursu()
    step_keyword = cast(StepKeyword, step.keyword)
    registry.register_step_definition(
        "tests.unittests.service.fixtures", step_keyword, step.text, handler
    )
    fn = TestFunctionWriter(
        scenario,
        registry,
        stack=[],
        steps=[],
        package_name="tests.unittests.service.fixtures",
    )
    kwargs = fn.parse_data_table(step_keyword, step)

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
                            keywords=[kwargs],
                        )
                    )
                ],
                decorator_list=[],
                lineno=1,
            )
        ]
    )
    tmod = TestModule("dummy", module)
    assert str(tmod) == expected_result


@pytest.mark.parametrize(
    "steps,step,handler,expected_result",
    [
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
            given_raw_doc_string,
            textwrap.dedent(
                """
            def test_dummy():
                step(doc_string='username\\nbob\\nalice')
            """
            ).strip(),
            id="raw",
        ),
        pytest.param(
            [],
            GherkinStep(
                id="1",
                location=GherkinLocation(line=1, column=1),
                keyword="Given",
                text="a user:",
                keywordType="Context",
                docString=GherkinDocString(
                    location=GherkinLocation(line=1, column=1),
                    content='{"username": "alice"}',
                    delimiter="",
                    mediaType="json",
                ),
            ),
            given_doc_string,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string={'username': 'alice'})
                """
            ).strip(),
            id="dict",
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
            given_doc_string_seq,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string=[{'username': 'alice'}, {'username': 'bob'}])
                """
            ).strip(),
            id="list",
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
                    content='{"alice"}',
                    delimiter="",
                    mediaType="python",
                ),
            ),
            given_ast_doc_string,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string={'alice'})
                """
            ).strip(),
            id="ast set",
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
                    content='{"username": "alice"}',
                    delimiter="",
                    mediaType="json",
                ),
            ),
            given_parsed_doc_string,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string=User0(username='alice'))
                """
            ).strip(),
            id="model",
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
                    content='{"username": "alice"}',
                    delimiter="",
                    mediaType="",
                ),
            ),
            given_parsed_doc_string,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string=User0(username='alice'))
                """
            ).strip(),
            id="model without media_type",
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
            given_parsed_doc_string_seq,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string=[User0(username='alice'), User0(username='bob')])
                """
            ).strip(),
            id="list[model]",
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
                    content='{"username": "alice"}',
                    delimiter="",
                    mediaType="json",
                ),
            ),
            given_parsed_annotated_doc_string,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string=load_user0(username='alice'))
                """
            ).strip(),
            id="Annotated[model]",
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
            given_parsed_annotated_doc_string_seq,
            textwrap.dedent(
                """
                def test_dummy():
                    step(doc_string=[load_user0(username='alice'), load_user0(username='bob')])
                """
            ).strip(),
            id="list[Annotated[model, factory]",
        ),
    ],
)
def test_parse_docstring(
    scenario: GherkinScenario,
    steps: Sequence[GherkinStep],
    step: GherkinStep,
    handler: Any,
    expected_result: str,
):
    registry = Tursu()
    step_keyword = cast(StepKeyword, step.keyword)
    registry.register_step_definition(
        "tests.unittests.service.fixtures", step_keyword, step.text, handler
    )
    fn = TestFunctionWriter(
        scenario,
        registry,
        stack=[],
        steps=[],
        package_name="tests.unittests.service.fixtures",
    )
    kwargs = fn.parse_doc_string(step_keyword, step)

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
                            keywords=[kwargs],
                        )
                    )
                ],
                decorator_list=[],
                lineno=1,
            )
        ]
    )
    tmod = TestModule("dummy", module)
    assert str(tmod) == expected_result


@pytest.mark.parametrize(
    "steps,step,handler,expected_result",
    [
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
                    content="username",
                    delimiter="",
                    mediaType="csv",
                ),
            ),
            given_raw_doc_string,
            textwrap.dedent(
                '''
def test_1_dummy(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu):
    """dummy"""
    with TursuRunner(request, capsys, tursu, ['🎬 Scenario: dummy']) as tursu_runner:
        tursu_runner.run_step('Given', 'a set of users:', doc_string='username')
                '''
            ).strip(),
            id="raw",
        ),
    ],
)
def test_build_function(
    scenario: GherkinScenario,
    step: GherkinStep,
    handler: Any,
    expected_result: str,
):
    registry = Tursu()
    step_keyword = cast(StepKeyword, step.keyword)
    registry.register_step_definition(
        "tests.unittests.service.fixtures", step_keyword, step.text, handler
    )
    fn = TestFunctionWriter(
        scenario,
        registry,
        stack=[scenario],
        steps=[step],
        package_name="tests.unittests.service.fixtures",
    )
    fn.add_step(step, [scenario, step])

    module = ast.Module(body=[fn.to_ast()])
    tmod = TestModule("dummy", module)
    assert str(tmod) == expected_result


@pytest.mark.parametrize(
    "steps,step,handler,expected_result",
    [
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
                    content="username",
                    delimiter="",
                    mediaType="csv",
                ),
            ),
            given_raw_doc_string,
            textwrap.dedent(
                '''
@pytest.mark.asyncio
async def test_1_dummy(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu):
    """dummy"""
    with TursuRunner(request, capsys, tursu, ['🎬 Scenario: dummy']) as tursu_runner:
        await tursu_runner.run_step_async('Given', 'a set of users:', doc_string='username')
                '''
            ).strip(),
            id="raw",
        ),
    ],
)
def test_build_async_function(
    async_scenario: GherkinScenario,
    step: GherkinStep,
    handler: Any,
    expected_result: str,
):
    registry = Tursu()
    step_keyword = cast(StepKeyword, step.keyword)
    registry.register_step_definition(
        "tests.unittests.service.fixtures", step_keyword, step.text, handler
    )
    fn = TestFunctionWriter(
        async_scenario,
        registry,
        stack=[async_scenario],
        steps=[step],
        package_name="tests.unittests.service.fixtures",
    )
    fn.add_step(step, [async_scenario, step])

    module = ast.Module(body=[fn.to_ast()])
    tmod = TestModule("dummy", module)
    assert str(tmod) == expected_result
