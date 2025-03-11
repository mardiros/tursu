import ast
import re
from collections.abc import Iterator, Sequence
from typing import Any, TypeGuard, get_args

from tursu.domain.model.gherkin import (
    GherkinBackground,
    GherkinBackgroundEnvelope,
    GherkinDocument,
    GherkinEnvelope,
    GherkinExamples,
    GherkinFeature,
    GherkinKeyword,
    GherkinRule,
    GherkinRuleEnvelope,
    GherkinScenario,
    GherkinScenarioEnvelope,
    GherkinScenarioOutline,
    GherkinStep,
)
from tursu.domain.model.testmod import TestModule
from tursu.registry import StepRegistry
from tursu.steps import StepKeyword


class GherkinIterator:
    def __init__(self, doc: GherkinDocument) -> None:
        self.doc = doc
        self.stack: list[Any] = []

    def emit(self) -> Iterator[Any]:
        self.stack.append(self.doc)
        yield self.stack
        for _ in self.emit_feature(self.doc.feature):
            yield self.stack
        self.stack.pop()

    def emit_feature_from_enveloppe(
        self, enveloppe: Sequence[GherkinEnvelope]
    ) -> Iterator[Any]:
        for child in enveloppe:
            match child:
                case GherkinBackgroundEnvelope(background=background):
                    self.stack.append(background)
                    yield self.stack
                    self.stack.pop()
                case GherkinScenarioEnvelope(scenario=scenario):
                    self.stack.append(scenario)
                    yield self.stack
                    for _ in self.emit_scenario(scenario):
                        yield self.stack
                    self.stack.pop()
                case GherkinRuleEnvelope(rule=rule):
                    self.stack.append(rule)
                    yield self.stack
                    for child in self.emit_feature_from_enveloppe(rule.children):
                        yield child
                    self.stack.pop()

    def emit_feature(self, feature: GherkinFeature) -> Iterator[Any]:
        self.stack.append(feature)
        yield self.stack
        yield from self.emit_feature_from_enveloppe(self.doc.feature.children)
        self.stack.pop()

    def emit_scenario(
        self, scenario: GherkinScenario | GherkinScenarioOutline
    ) -> Iterator[Any]:
        for step in scenario.steps:
            self.stack.append(step)
            yield self.stack
            self.stack.pop()


def is_step_keyword(value: GherkinKeyword) -> TypeGuard[StepKeyword]:
    return value in get_args(StepKeyword)


def sanitize(name: str) -> str:
    return re.sub(r"\W+", "_", name)[:100]


class GherkinCompiler:
    feat_idx = 1

    def __init__(self, doc: GherkinDocument, registry: StepRegistry) -> None:
        self.emmiter = GherkinIterator(doc)
        self.registry = registry

    def get_tags(self, stack: list[Any]) -> set[str]:
        ret = set()
        for el in stack:
            match el:
                case (
                    GherkinFeature(
                        location=_,
                        tags=tags,
                        language=_,
                        keyword=_,
                        name=_,
                        description=_,
                        children=_,
                    )
                    | GherkinRule(
                        id=_,
                        location=_,
                        tags=tags,
                        keyword=_,
                        name=_,
                        description=_,
                        children=_,
                    )
                    | GherkinScenario(
                        id=_,
                        location=_,
                        tags=tags,
                        keyword=_,
                        name=_,
                        description=_,
                        steps=_,
                    )
                    | GherkinScenarioOutline(
                        id=_,
                        location=_,
                        tags=tags,
                        keyword=_,
                        name=_,
                        description=_,
                        steps=_,
                        examples=_,
                    )
                    | GherkinExamples(
                        id=_,
                        location=_,
                        tags=tags,
                        keyword=_,
                        name=_,
                        description=_,
                        table_header=_,
                        table_body=_,
                    )
                ):
                    for tag in tags:
                        ret.add(tag.name)
                case _:
                    ...
        return ret

    def _handle_step(
        self,
        test_function: ast.FunctionDef,
        stp: GherkinStep,
        last_keyword: StepKeyword | None,
        examples: Sequence[GherkinExamples] | None = None,
    ) -> StepKeyword:
        keyword = stp.keyword
        if stp.keyword_type == "Conjunction":
            assert last_keyword is not None, f"Using {stp.keyword} without context"
            keyword = last_keyword
        assert is_step_keyword(keyword)
        last_keyword = keyword

        keywords = []
        step_fixtures = self.registry.extract_fixtures(last_keyword, stp.text)
        for key, _val in step_fixtures.items():
            keywords.append(
                ast.keyword(arg=key, value=ast.Name(id=key, ctx=ast.Load()))
            )

        if stp.doc_string:
            keywords.append(
                ast.keyword(
                    arg="doc_string", value=ast.Constant(value=stp.doc_string.content)
                )
            )

        if stp.data_table:
            tabl = []
            hdr = [c.value for c in stp.data_table.rows[0].cells]
            for row in stp.data_table.rows[1:]:
                vals = [c.value for c in row.cells]
                tabl.append(dict(zip(hdr, vals)))

            keywords.append(
                ast.keyword(arg="data_table", value=ast.Constant(value=tabl))
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
                    value=ast.Name(id="registry", ctx=ast.Load()),
                    attr="format_example_step",
                    ctx=ast.Load(),
                ),  # registry.run_step
                args=[
                    text,
                ],
                keywords=format_keywords,
            )

        call_node = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id="registry", ctx=ast.Load()),
                attr="run_step",
                ctx=ast.Load(),
            ),  # registry.run_step
            args=[
                ast.Constant(value=last_keyword),
                call_format_node if call_format_node else text,
            ],
            keywords=keywords,
        )

        # Add the call node to the body of the function
        test_function.body.append(ast.Expr(value=call_node, lineno=stp.location.line))
        return last_keyword

    def build_fixtures(self, steps: list[GherkinStep]) -> dict[str, type]:
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

            fixtures.update(
                self.registry.extract_fixtures(step_last_keyword, step.text)
            )
        return fixtures

    def to_module(self) -> TestModule:
        module_name = None
        module_node = None
        test_function = None
        args: Any = None
        last_keyword: StepKeyword | None = None
        background_steps: Sequence[GherkinStep] = []

        for stack in self.emmiter.emit():
            el = stack[-1]
            match el:
                case GherkinFeature(
                    location=_,
                    tags=_,
                    language=_,
                    keyword=_,
                    name=name,
                    description=description,
                    children=_,
                ):
                    assert module_node is None
                    docstring = f"{name}\n\n{description}".strip()
                    import_any = ast.ImportFrom(
                        module="typing",  # the module name
                        names=[ast.alias(name="Any", asname=None)],
                        level=0,  # import at the top level
                    )
                    import_pytest = ast.Import(
                        names=[ast.alias(name="pytest", asname=None)]
                    )
                    import_tursu = ast.ImportFrom(
                        module="tursu",  # the module name
                        names=[ast.alias(name="StepRegistry", asname=None)],
                        level=0,  # import at the top level
                    )
                    module_node = ast.Module(
                        body=[
                            ast.Expr(value=ast.Constant(docstring), lineno=1),
                            import_any,
                            import_pytest,
                            import_tursu,
                        ],
                        type_ignores=[],
                    )
                    module_name = f"test_{GherkinCompiler.feat_idx}_{sanitize(name)}.py"
                    GherkinCompiler.feat_idx += 1

                case GherkinBackground(
                    id=_,
                    location=_,
                    keyword=_,
                    name=_,
                    description=_,
                    steps=steps,
                ):
                    background_steps = steps

                case GherkinScenario(
                    id=id,
                    location=location,
                    tags=_,
                    keyword=_,
                    name=name,
                    description=description,
                    steps=steps,
                ):
                    fixtures = self.build_fixtures([*background_steps, *steps])

                    args = [
                        ast.arg(
                            arg="registry",
                            annotation=ast.Name(id="StepRegistry", ctx=ast.Load()),
                        )
                    ]
                    for key, _val in fixtures.items():
                        args.append(
                            ast.arg(
                                arg=key,
                                # annotation=ast.Name(id=val.__name__, ctx=ast.Load()),
                            )
                        )

                    docstring = f"{name}\n\n    {description}".strip()

                    tag_decorator_list: list[ast.expr] = []
                    tags = self.get_tags(stack)
                    if tags:
                        for tag in tags:
                            decorator = ast.Attribute(
                                value=ast.Name(id="pytest", ctx=ast.Load()),
                                attr="mark",
                                ctx=ast.Load(),
                            )
                            tag_decorator = ast.Attribute(
                                value=decorator, attr=tag, ctx=ast.Load()
                            )
                            tag_decorator_list.append(tag_decorator)

                    test_function = ast.FunctionDef(
                        name=f"test_{id}_{sanitize(name)}",
                        args=ast.arguments(
                            args=args,
                            posonlyargs=[],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[],
                        ),
                        body=[
                            ast.Expr(
                                value=ast.Constant(docstring), lineno=location.line + 1
                            ),
                        ],
                        decorator_list=tag_decorator_list,
                        lineno=location.line,
                    )
                    assert module_node is not None
                    last_keyword = None
                    module_node.body.append(test_function)
                    if background_steps:
                        for step in background_steps:
                            last_keyword = self._handle_step(
                                test_function, step, last_keyword
                            )

                case GherkinScenarioOutline(
                    id=id,
                    location=location,
                    tags=_,
                    keyword=_,
                    name=name,
                    description=description,
                    steps=steps,
                    examples=examples,
                ):
                    decorator_list: list[ast.expr] = []

                    tags = self.get_tags(stack)
                    if tags:
                        for tag in tags:
                            decorator = ast.Attribute(
                                value=ast.Name(id="pytest", ctx=ast.Load()),
                                attr="mark",
                                ctx=ast.Load(),
                            )
                            tag_decorator = ast.Attribute(
                                value=decorator, attr=tag, ctx=ast.Load()
                            )
                            decorator_list.append(tag_decorator)

                    examples_keys = [c.value for c in examples[0].table_header.cells]
                    params = ",".join(examples_keys)
                    params_name = ast.Constant(params)

                    data: list[ast.expr] = []
                    for ex in examples:
                        id_ = ex.name or ex.keyword
                        for row in ex.table_body:
                            parametrized_set = ast.Attribute(
                                value=ast.Name(id="pytest", ctx=ast.Load()),
                                attr="param",
                                ctx=ast.Load(),
                            )
                            dataset: list[ast.expr] = [
                                ast.Constant(c.value) for c in row.cells
                            ]
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

                    fixtures = self.build_fixtures([*background_steps, *steps])

                    args = [
                        ast.arg(
                            arg="registry",
                            annotation=ast.Name(id="StepRegistry", ctx=ast.Load()),
                        )
                    ]
                    for key, _val in fixtures.items():
                        args.append(
                            ast.arg(
                                arg=key,
                                annotation=ast.Name(id="Any", ctx=ast.Load()),
                            )
                        )

                    for exkeys in examples_keys:
                        args.append(
                            ast.arg(
                                arg=exkeys,
                                annotation=ast.Name(id="str", ctx=ast.Load()),
                            )
                        )

                    docstring = f"{name}\n\n    {description}".strip()

                    test_function = ast.FunctionDef(
                        name=f"test_{id}_{sanitize(name)}",
                        args=ast.arguments(
                            args=args,
                            posonlyargs=[],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[],
                        ),
                        body=[
                            ast.Expr(
                                value=ast.Constant(docstring), lineno=location.line + 1
                            ),
                        ],
                        decorator_list=decorator_list,
                        lineno=location.line,
                    )
                    assert module_node is not None
                    last_keyword = None
                    module_node.body.append(test_function)
                    if background_steps:
                        for step in background_steps:
                            last_keyword = self._handle_step(
                                test_function, step, last_keyword
                            )

                case GherkinStep(
                    id=_,
                    location=_,
                    keyword=_,
                    text=_,
                    keyword_type=_,
                    data_table=_,
                    doc_string=_,
                ):
                    assert test_function is not None
                    expls: Any = None
                    if stack[-2].keyword == "scenario outline":
                        expls = stack[-2].examples
                    last_keyword = self._handle_step(
                        test_function, el, last_keyword, expls
                    )

                case _:
                    # print(el)
                    ...

        assert module_node is not None
        assert module_name is not None
        return TestModule(module_name, module_node)
