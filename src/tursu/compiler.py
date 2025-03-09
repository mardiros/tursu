import ast
import re
from collections.abc import Iterator
from typing import Any, TypeGuard, get_args

from tursu.domain.model.gherkin import (
    GherkinBackgroundEnvelope,
    GherkinDocument,
    GherkinFeature,
    GherkinKeyword,
    GherkinRuleEnvelope,
    GherkinScenario,
    GherkinScenarioEnvelope,
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

    def emit_feature(self, feature: GherkinFeature) -> Iterator[Any]:
        self.stack.append(feature)
        yield self.stack
        for child in self.doc.feature.children:
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
                    self.stack.pop()
        self.stack.pop()

    def emit_scenario(self, scenario: GherkinScenario) -> Iterator[Any]:
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

    def to_module(self) -> TestModule:
        last_keyword: StepKeyword | None = None

        module_name = None
        module_node = None
        test_function = None
        args: Any = None

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
                    import_node = ast.ImportFrom(
                        module="tursu",  # the module name
                        names=[ast.alias(name="StepRegistry", asname=None)],
                        level=0,  # import at the top level
                    )
                    module_node = ast.Module(
                        body=[
                            ast.Expr(value=ast.Constant(docstring), lineno=1),
                            import_node,
                        ],
                        type_ignores=[],
                    )
                    module_name = f"test_{GherkinCompiler.feat_idx}_{sanitize(name)}.py"
                    GherkinCompiler.feat_idx += 1

                case GherkinScenario(
                    id=id,
                    location=location,
                    tags=_,
                    keyword=_,
                    name=name,
                    description=description,
                    steps=steps,
                    examples=_,
                ):
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

                    docstring = f"{name}\n\n{description}".strip()
                    test_function = ast.FunctionDef(
                        name=f"test_{id}_{sanitize(name)}",
                        args=ast.arguments(
                            args=args,
                        ),
                        body=[
                            ast.Expr(
                                value=ast.Constant(docstring), lineno=location.line + 1
                            ),
                        ],
                        decorator_list=[],
                        lineno=location.line,
                    )
                    assert module_node is not None
                    module_node.body.append(test_function)

                case GherkinStep(
                    id=_,
                    location=location,
                    keyword=keyword,
                    text=text,
                    keyword_type=keyword_type,
                    data_table=_,
                    docstring=_,
                ):
                    if keyword_type == "Conjunction":
                        assert last_keyword is not None, (
                            f"Using {keyword} without context"
                        )
                        keyword = last_keyword
                    assert is_step_keyword(keyword)
                    last_keyword = keyword

                    assert test_function is not None
                    keywords = []
                    step_fixtures = self.registry.extract_fixtures(last_keyword, text)
                    for key, _val in step_fixtures.items():
                        keywords.append(
                            ast.keyword(arg=key, value=ast.Name(id=key, ctx=ast.Load()))
                        )

                    call_node = ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id="registry", ctx=ast.Load()),
                            attr="run_step",
                            ctx=ast.Load(),
                        ),  # registry.run_step
                        args=[
                            ast.Constant(value=keyword),
                            ast.Constant(value=text),
                        ],
                        keywords=keywords,
                    )

                    # Add the call node to the body of the function
                    test_function.body.append(
                        ast.Expr(value=call_node, lineno=location.line)
                    )

                case _:
                    # print(el)
                    ...

        assert module_node is not None
        assert module_name is not None
        return TestModule(module_name, module_node)
