import ast
from collections.abc import Iterator, Sequence
from typing import Annotated, Any, get_args, get_origin

from tursu.domain.model.ast.astfunction import AstFunction, is_step_keyword
from tursu.domain.model.ast.astmodule import AstModule
from tursu.domain.model.gherkin import (
    GherkinBackground,
    GherkinBackgroundEnvelope,
    GherkinDocument,
    GherkinEnvelope,
    GherkinExamples,
    GherkinFeature,
    GherkinRuleEnvelope,
    GherkinScenario,
    GherkinScenarioEnvelope,
    GherkinScenarioOutline,
    GherkinStep,
)
from tursu.domain.model.steps import StepKeyword
from tursu.domain.model.testmod import TestModule
from tursu.registry import Tursu


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


class GherkinCompiler:
    feat_idx = 1

    def __init__(self, doc: GherkinDocument, registry: Tursu) -> None:
        self.emmiter = GherkinIterator(doc)
        self.registry = registry

    def _handle_step(
        self,
        step_list: list[ast.stmt],
        stp: GherkinStep,
        stack: list[Any],
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
            registry_step = self.registry.get_step(keyword, stp.text)

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

                keywords.append(
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
                keywords.append(
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
                ast.Constant(value=last_keyword),
                call_format_node if call_format_node else text,
            ],
            keywords=keywords,
        )

        # Add the call node to the body of the function
        step_list.append(ast.Expr(value=call_node, lineno=stp.location.line))
        return last_keyword

    def to_module(self) -> TestModule:
        module_node = None
        test_function = None
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
                    name=_,
                    description=_,
                    children=_,
                ):
                    assert module_node is None
                    module_node = AstModule(el, self.registry, stack)

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
                    id=_,
                    location=_,
                    tags=_,
                    keyword=_,
                    name=_,
                    description=_,
                    steps=steps,
                ):
                    test_function = AstFunction(
                        el, self.registry, [*background_steps, *steps], stack
                    )
                    assert module_node is not None
                    last_keyword = None
                    module_node.append_test(test_function)
                    if background_steps:
                        for step in background_steps:
                            last_keyword = self._handle_step(
                                test_function.step_list, step, stack, last_keyword
                            )

                case GherkinScenarioOutline(
                    id=_,
                    location=_,
                    tags=_,
                    keyword=_,
                    name=_,
                    description=_,
                    steps=steps,
                    examples=_,
                ):
                    test_function = AstFunction(
                        el, self.registry, [*background_steps, *steps], stack
                    )
                    assert module_node is not None
                    last_keyword = None
                    module_node.append_test(test_function)
                    if background_steps:
                        for step in background_steps:
                            last_keyword = self._handle_step(
                                test_function.step_list, step, stack, last_keyword
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
                    if stack[-2].keyword == "Scenario Outline":
                        expls = stack[-2].examples
                    last_keyword = self._handle_step(
                        test_function.step_list, el, stack, last_keyword, expls
                    )

                case _:
                    # print(el)
                    ...

        assert module_node is not None
        return TestModule(module_node.module_name, module_node.to_ast())
