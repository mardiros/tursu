"""AST helpers at the test function level."""

import ast
import json
import re
from collections.abc import Mapping, Sequence
from typing import Annotated, Any, TypeGuard, cast, get_args, get_origin

from tursu.domain.model.gherkin import (
    GherkinExamples,
    GherkinFeature,
    GherkinKeyword,
    GherkinRule,
    GherkinScenario,
    GherkinScenarioOutline,
    GherkinStep,
)
from tursu.domain.model.steps import StepKeyword
from tursu.runtime.registry import Tursu
from tursu.shared.utils import is_mapping, is_sequence, is_union


def repr_stack(stack: Sequence[Any]) -> Sequence[str]:
    """Helper to get a stack representation to display fancy tests results."""
    ret = []
    for el in stack:
        ret.append(repr(el))
    return ret


def is_step_keyword(value: GherkinKeyword) -> TypeGuard[StepKeyword]:
    """
    Typeguard for step keyword only.

    :param value: any gherkin keyword input
    """
    return value in get_args(StepKeyword)


def sanitize(name: str) -> str:
    """Used to generate valid python identifiers."""
    return re.sub(r"\W+", "_", name)[:100]


class TestFunctionWriter:
    """
    Helper to write a test function for a given scenario.

    :param scenario: scenario to compile to ast code.
    :param registry: tursu registry containing steps definition.
    :param steps: steps to include, including the one from the background.
    :param stack: tursu compilation current stack.
    :param package_name: package name where the scenario lives in.
    """

    def __init__(
        self,
        scenario: GherkinScenario | GherkinScenarioOutline,
        registry: Tursu,
        steps: Sequence[GherkinStep],
        stack: Sequence[Any],
        package_name: str,
    ) -> None:
        self.registry = registry
        self.gherkin_keyword: StepKeyword | None = None
        self.package_name = package_name

        self.fixtures = self.build_fixtures(steps, registry)
        decorator_list = self.build_tags_decorators(stack)
        examples_keys = None
        if isinstance(scenario, GherkinScenarioOutline) and scenario.examples:
            examples_keys = [c.value for c in scenario.examples[0].table_header.cells]
            params = ",".join(examples_keys)
            params_name = ast.Constant(params)
            data: list[ast.expr] = []
            for ex in scenario.examples:
                id_ = ex.name or ex.keyword
                for row in ex.table_body:
                    parametrized_set = ast.Attribute(
                        value=ast.Name(id="pytest", ctx=ast.Load()),
                        attr="param",
                        ctx=ast.Load(),
                    )
                    dataset: list[ast.expr] = [ast.Constant(c.value) for c in row.cells]
                    data.append(
                        ast.Call(
                            func=parametrized_set,
                            args=dataset,
                            keywords=[ast.keyword("id", ast.Constant(id_))],
                        )
                    )
            ex_args: list[ast.expr] = [
                params_name,
                ast.List(elts=data, ctx=ast.Load()),
            ]

            decorator = ast.Attribute(
                value=ast.Name(id="pytest", ctx=ast.Load()),
                attr="mark",
                ctx=ast.Load(),
            )

            parametrize_decorator = ast.Attribute(
                value=decorator, attr="parametrize", ctx=ast.Load()
            )

            decorator_list.append(
                ast.Call(func=parametrize_decorator, args=ex_args, keywords=[])
            )

        self.step_list: list[ast.stmt] = []
        runner_instance = ast.With(
            items=[
                ast.withitem(
                    context_expr=ast.Call(
                        func=ast.Name(id="TursuRunner", ctx=ast.Load()),
                        args=[
                            ast.Name(id="request", ctx=ast.Load()),
                            ast.Name(id="capsys", ctx=ast.Load()),
                            ast.Name(id="tursu", ctx=ast.Load()),
                            ast.Constant(value=repr_stack(stack)),
                        ],
                        keywords=[],
                    ),
                    optional_vars=ast.Name(id="tursu_runner", ctx=ast.Store()),
                )
            ],
            body=self.step_list,
            lineno=scenario.location.line + 2,
        )

        docstring = f"{scenario.name}\n\n    {scenario.description}".strip()

        args = self.build_args(self.fixtures, examples_keys)
        self.funcdef = ast.FunctionDef(
            name=f"test_{scenario.id}_{sanitize(scenario.name)}",
            args=ast.arguments(
                args=args,
                posonlyargs=[],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                ast.Expr(
                    value=ast.Constant(docstring),
                    lineno=scenario.location.line + 1,
                ),
                runner_instance,
            ],
            decorator_list=decorator_list,
            lineno=scenario.location.line,
        )

    def build_args(
        self, fixtures: Mapping[str, Any], examples_keys: Sequence[Any] | None = None
    ) -> list[ast.arg]:
        """Build the args for the test functions."""
        args = [
            ast.arg(
                arg="request",
                annotation=ast.Name(id="pytest.FixtureRequest", ctx=ast.Load()),
            ),
            ast.arg(
                arg="capsys",
                annotation=ast.Name(id="pytest.CaptureFixture[str]", ctx=ast.Load()),
            ),
            ast.arg(
                arg="tursu",
                annotation=ast.Name(id="Tursu", ctx=ast.Load()),
            ),
        ]
        for key, _val in fixtures.items():
            if key in ("request", "capsys", "tursu"):
                continue
            args.append(
                ast.arg(
                    arg=key,
                    annotation=ast.Name(id="Any", ctx=ast.Load()),
                )
            )
        if examples_keys:
            for exkeys in examples_keys:
                args.append(
                    ast.arg(
                        arg=exkeys,
                        annotation=ast.Name(id="str", ctx=ast.Load()),
                    )
                )
        return args

    def build_fixtures(
        self, steps: Sequence[GherkinStep], registry: Tursu
    ) -> dict[str, type]:
        """
        Get the fixture for the given step.

        :param steps: steps to include, including the one from the background.
        :param registry: tursu registry containing steps definition.
        :return: the fixtures to include for all the steps of the scenario.
        """
        fixtures: dict[str, type] = {}
        step_last_keyword = None
        for step in steps:
            if step.keyword_type == "Conjunction":
                if step_last_keyword is None:
                    raise ValueError(f'Using "{step.keyword}" keyword without context')
            else:
                step_last_keyword = step.keyword
            assert is_step_keyword(step_last_keyword)

            fixtures.update(
                registry.extract_fixtures(
                    self.package_name, step_last_keyword, step.text
                )
            )
        return fixtures

    def build_tags_decorators(self, stack: Sequence[Any]) -> list[ast.expr]:
        """
        Generate pytest markers for the function.
        It will traverse the stack to get all the gherkin tags in order to generate
        pytest markers with them.

        :param stack: current compiler stack.
        """
        decorator_list = []
        tags = self.get_tags(stack)
        if tags:
            for tag in tags:
                decorator = ast.Attribute(
                    value=ast.Name(id="pytest", ctx=ast.Load()),
                    attr="mark",
                    ctx=ast.Load(),
                )
                tag_decorator = ast.Attribute(value=decorator, attr=tag, ctx=ast.Load())
                decorator_list.append(tag_decorator)
        return decorator_list  # type: ignore

    def get_tags(self, stack: Sequence[Any]) -> set[str]:
        """
        Get the all the gherkin tags from the stack.

        :param stack: current compiler stack.
        """
        ret = set()
        for el in stack:
            match el:
                case (
                    GherkinFeature(tags=tags)
                    | GherkinRule(tags=tags)
                    | GherkinScenario(tags=tags)
                    | GherkinScenarioOutline(tags=tags)
                    | GherkinExamples(tags=tags)
                ):
                    for tag in tags:
                        ret.add(tag.name)
                case _:
                    ...
        return ret

    def get_keyword(self, stp: GherkinStep) -> StepKeyword:
        """
        Get the step keyword from the current step.
        If the step is a conjunction (`And`, `But`), the step keyword come from
        the previous step.

        :param stp: the step to analyse.
        :return: proper keyword for the step.
        :raises ValueError: if a conjunction has been used to start a scenario.
        """
        keyword = stp.keyword
        if stp.keyword_type == "Conjunction":
            if self.gherkin_keyword is None:
                raise ValueError(f'Using "{stp.keyword}" keyword without context')
            keyword = self.gherkin_keyword
        assert is_step_keyword(keyword)
        self.gherkin_keyword = keyword
        return keyword

    def build_step_args(
        self,
        step_keyword: StepKeyword,
        stp: GherkinStep,
        examples: Sequence[GherkinExamples] | None = None,
    ) -> list[ast.expr]:
        """
        Get a step ast argument.

        :param step_keyword: the step definition keyword.
        :param stp: the step to analyse.
        :param examples: in cases of scenario outline, its associated examples.
            In this case, the chevron-enclosed placeholders (e.g. `<value>`) are
            replaced by parametrized value during the call.
        :return: ast values for the step argument.
        :raises ValueError: if a conjunction has been used to start a scenario.
        """
        call_format_node = None
        text = ast.Constant(value=stp.text)
        if examples:
            format_keywords = []
            ex = examples[0]
            for cell in ex.table_header.cells:
                format_keywords.append(
                    ast.keyword(
                        arg=cell.value, value=ast.Name(id=cell.value, ctx=ast.Load())
                    )
                )
            call_format_node = ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="tursu_runner", ctx=ast.Load()),
                    attr="format_example_step",
                    ctx=ast.Load(),
                ),  # tursu.run_step
                args=[
                    text,
                ],
                keywords=format_keywords,
            )
        return [
            ast.Constant(value=step_keyword),
            call_format_node if call_format_node else text,
        ]

    def parse_doc_string(
        self, step_keyword: StepKeyword, stp: GherkinStep
    ) -> ast.keyword:
        step_def = self.registry.get_step(self.package_name, step_keyword, stp.text)

        assert step_def, "Step not found"
        assert stp.doc_string, "Step has not doc_string"

        typ = None
        is_list = False
        anon = step_def.pattern.signature.parameters["doc_string"].annotation
        if anon:
            param_origin = get_origin(anon)
            if is_union(anon):
                typ = None
            elif param_origin is Annotated:
                # we are in a factory
                typ = get_args(anon)[-1]
            elif is_sequence(param_origin):
                is_list = True
                typ = get_args(anon)[0]
                orig = get_origin(typ)
                if is_mapping(orig):
                    typ = None
                elif orig is Annotated:
                    typ = get_args(typ)[-1]
            else:
                orig = get_origin(anon)
                if is_mapping(orig):
                    typ = None
                else:
                    typ = anon

        if typ and typ is not str and stp.doc_string.media_type != "python":
            doc_string_keywords = []
            call_doc_string_node: ast.expr
            if isinstance(stp.doc_string.content, str):
                data = json.loads(stp.doc_string.content)
            else:
                data = stp.doc_string.content
            if is_list:
                doc_string_models: list[ast.expr] = []
                for model in cast(Sequence[Mapping[str, Any]], data):
                    doc_string_keywords = [
                        ast.keyword(
                            arg=key,
                            value=ast.Constant(value=val),
                        )
                        for key, val in model.items()
                    ]

                    param_origin = get_origin(anon)
                    doc_string_models.append(
                        ast.Call(
                            func=ast.Name(
                                id=self.registry.get_models_type(
                                    self.package_name, typ
                                ),
                                ctx=ast.Load(),
                            ),
                            keywords=doc_string_keywords,
                        )
                    )

                call_doc_string_node = ast.List(elts=doc_string_models, ctx=ast.Load())
            else:
                doc_string_keywords = [
                    ast.keyword(
                        arg=key,
                        value=ast.Constant(value=val),
                    )
                    for key, val in cast(Mapping[str, Any], data).items()
                ]

                param_origin = get_origin(anon)
                call_doc_string_node = ast.Call(
                    func=ast.Name(
                        id=self.registry.get_models_type(self.package_name, typ),
                        ctx=ast.Load(),
                    ),
                    keywords=doc_string_keywords,
                )
            return ast.keyword(arg="doc_string", value=call_doc_string_node)

        return ast.keyword(
            arg="doc_string", value=ast.Constant(value=stp.doc_string.content)
        )

    def parse_data_table(
        self, step_keyword: StepKeyword, stp: GherkinStep
    ) -> ast.keyword:
        """
        Parse the data table to its step definition signature.

        :param step_keyword: the step definition keyword.
        :param stp: the step to analyse.
            the step must have a definved data_table.
        """
        step_def = self.registry.get_step(self.package_name, step_keyword, stp.text)

        assert step_def, "Step not found"
        assert stp.data_table, "Step has no data_table"
        typ: type | None = None
        is_reversed = False
        anon = step_def.pattern.signature.parameters["data_table"].annotation
        if anon:
            param_origin = get_origin(anon)
            if param_origin is Annotated:
                # we are in a factory
                is_reversed = True
                typ = get_args(anon)[-1]
            elif is_sequence(param_origin):
                typ = get_args(anon)[0]
                orig = get_origin(typ)
                if is_mapping(orig):
                    typ = None
                elif orig is Annotated:
                    typ = get_args(typ)[-1]
            else:
                is_reversed = True
                orig = get_origin(anon)
                if is_mapping(orig):
                    typ = None
                else:
                    typ = anon

        if typ is None:
            if is_reversed:
                rev_tabl = {
                    row.cells[0].value: row.cells[1].value
                    for row in stp.data_table.rows
                }
                return ast.keyword(arg="data_table", value=ast.Constant(value=rev_tabl))
            else:
                tabl = []
                hdr = [c.value for c in stp.data_table.rows[0].cells]
                for row in stp.data_table.rows[1:]:
                    vals = [c.value for c in row.cells]
                    tabl.append(dict(zip(hdr, vals)))

                return ast.keyword(arg="data_table", value=ast.Constant(value=tabl))

        if is_reversed:
            datatable_keywords = [
                ast.keyword(
                    arg=row.cells[0].value,
                    value=ast.Constant(value=row.cells[1].value),
                )
                for row in stp.data_table.rows
                if row.cells[1].value != self.registry.DATA_TABLE_EMPTY_CELL
            ]
            call_rev_datatable_node = ast.Call(
                func=ast.Name(
                    id=self.registry.get_models_type(self.package_name, typ),
                    ctx=ast.Load(),
                ),
                keywords=datatable_keywords,
            )
            return ast.keyword(arg="data_table", value=call_rev_datatable_node)
        else:
            # we have to parse the value
            tabl = []
            hdr = [c.value for c in stp.data_table.rows[0].cells]
            call_datatable_node: list[ast.expr] = []
            for row in stp.data_table.rows[1:]:
                vals = [c.value for c in row.cells]
                datatable_keywords = []
                for key, val in zip(hdr, vals):
                    if val == self.registry.DATA_TABLE_EMPTY_CELL:
                        # empty string are our null value
                        continue
                    datatable_keywords.append(
                        ast.keyword(arg=key, value=ast.Constant(value=val))
                    )

                call_datatable_node.append(
                    ast.Call(
                        func=ast.Name(
                            id=self.registry.get_models_type(self.package_name, typ),
                            ctx=ast.Load(),
                        ),
                        keywords=datatable_keywords,
                    )
                )
            return ast.keyword(
                arg="data_table",
                value=ast.List(elts=call_datatable_node, ctx=ast.Load()),
            )

    def build_step_kwargs(
        self, step_keyword: StepKeyword, stp: GherkinStep
    ) -> list[ast.keyword]:
        """
        Get the step kwargs, e.g. pytest fixtures for the given step.

        :param step_keyword: the step definition keyword.
        :param stp: the step to analyse.

        :return: ast values for the step keyword argument.
        """
        py_kwargs = []
        step_fixtures = self.registry.extract_fixtures(
            self.package_name, step_keyword, stp.text
        )
        for key, _val in step_fixtures.items():
            py_kwargs.append(
                ast.keyword(arg=key, value=ast.Name(id=key, ctx=ast.Load()))
            )

        if stp.doc_string:
            py_kwargs.append(self.parse_doc_string(step_keyword, stp))

        if stp.data_table:
            py_kwargs.append(self.parse_data_table(step_keyword, stp))

        return py_kwargs

    def add_step(
        self,
        stp: GherkinStep,
        stack: list[Any],
        examples: Sequence[GherkinExamples] | None = None,
    ) -> None:
        """
        Appened the given step to the test function.

        :param stp: the step to add.
        :param stack: current compiler stack.
        :param examples: in cases of scenario outline, its associated examples.
        """
        step_keyword = self.get_keyword(stp)
        py_args = self.build_step_args(step_keyword, stp, examples)
        py_kwargs = self.build_step_kwargs(step_keyword, stp)

        call_node = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="tursu_runner", ctx=ast.Load()),
                attr="run_step",
                ctx=ast.Load(),
            ),
            args=py_args,
            keywords=py_kwargs,
        )

        # Add the call node to the body of the function
        self.step_list.append(ast.Expr(value=call_node, lineno=stp.location.line))

    def to_ast(self) -> ast.FunctionDef:
        """Convert the current state to ast code."""
        return self.funcdef
