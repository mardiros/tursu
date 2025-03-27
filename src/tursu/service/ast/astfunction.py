import ast
import re
from collections.abc import Sequence
from typing import Annotated, Any, TypeGuard, get_args, get_origin

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


def repr_stack(stack: list[Any]) -> list[str]:
    ret = []
    for el in stack:
        ret.append(repr(el))
    return ret


def is_step_keyword(value: GherkinKeyword) -> TypeGuard[StepKeyword]:
    return value in get_args(StepKeyword)


def sanitize(name: str) -> str:
    return re.sub(r"\W+", "_", name)[:100]


class TestFunctionWriter:
    def __init__(
        self,
        scenario: GherkinScenario | GherkinScenarioOutline,
        registry: Tursu,
        steps: Sequence[GherkinStep],
        stack: list[Any],
    ) -> None:
        self.registry = registry
        self.gherkin_keyword: StepKeyword | None = None

        fixtures = self.build_fixtures(steps, registry)
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

        args = self.build_args(fixtures, examples_keys)
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
        self, fixtures: dict[str, Any], examples_keys: Sequence[Any] | None = None
    ) -> list[ast.arg]:
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
        fixtures: dict[str, type] = {}
        step_last_keyword = None
        for step in steps:
            if step.keyword_type == "Conjunction":
                assert step_last_keyword is not None, (
                    f"Using {step.keyword} without context"
                )
            else:
                step_last_keyword = step.keyword
            assert is_step_keyword(step_last_keyword)

            fixtures.update(registry.extract_fixtures(step_last_keyword, step.text))
        return fixtures

    def build_tags_decorators(self, stack: Sequence[Any]) -> list[ast.expr]:
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
        keyword = stp.keyword
        if stp.keyword_type == "Conjunction":
            assert self.gherkin_keyword is not None, (
                f"Using {stp.keyword} without context"
            )
            keyword = self.gherkin_keyword
        assert is_step_keyword(keyword)
        self.gherkin_keyword = keyword
        return keyword

    def add_step(
        self,
        stp: GherkinStep,
        stack: list[Any],
        examples: Sequence[GherkinExamples] | None = None,
    ) -> None:
        step_keyword = self.get_keyword(stp)

        py_kwargs = []
        step_fixtures = self.registry.extract_fixtures(step_keyword, stp.text)
        for key, _val in step_fixtures.items():
            py_kwargs.append(
                ast.keyword(arg=key, value=ast.Name(id=key, ctx=ast.Load()))
            )

        if stp.doc_string:
            py_kwargs.append(
                ast.keyword(
                    arg="doc_string", value=ast.Constant(value=stp.doc_string.content)
                )
            )

        if stp.data_table:
            registry_step = self.registry.get_step(step_keyword, stp.text)

            assert registry_step, "Step not found"
            typ: type | None = None
            anon = registry_step.pattern.signature.parameters["data_table"].annotation
            if anon:
                typ = get_args(anon)[0]
                orig = get_origin(typ)
                if orig is dict:
                    typ = None
                elif orig is Annotated:
                    typ = get_args(typ)[-1]

            if typ is None:
                tabl = []
                hdr = [c.value for c in stp.data_table.rows[0].cells]
                for row in stp.data_table.rows[1:]:
                    vals = [c.value for c in row.cells]
                    tabl.append(dict(zip(hdr, vals)))

                py_kwargs.append(
                    ast.keyword(arg="data_table", value=ast.Constant(value=tabl))
                )
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
                                id=self.registry.data_tables_types[typ],
                                ctx=ast.Load(),
                            ),
                            keywords=datatable_keywords,
                        )
                    )
                py_kwargs.append(
                    ast.keyword(
                        arg="data_table",
                        value=ast.List(elts=call_datatable_node, ctx=ast.Load()),
                    )
                )

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

        call_node = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="tursu_runner", ctx=ast.Load()),
                attr="run_step",
                ctx=ast.Load(),
            ),  # tursu.run_step
            args=[
                ast.Constant(value=step_keyword),
                call_format_node if call_format_node else text,
            ],
            keywords=py_kwargs,
        )

        # Add the call node to the body of the function
        self.step_list.append(ast.Expr(value=call_node, lineno=stp.location.line))

    def to_ast(self) -> ast.FunctionDef:
        return self.funcdef
