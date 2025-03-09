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
from tursu.registry import StepRegitry
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


def step_keyword(value: GherkinKeyword) -> TypeGuard[StepKeyword]:
    return value in get_args(StepKeyword)


class GherkinRunner:
    def __init__(self, doc: GherkinDocument, registry: StepRegitry) -> None:
        self.emmiter = GherkinIterator(doc)
        self.registry = registry

    def run(self) -> None:
        last_keyword: StepKeyword | None = None
        for stack in self.emmiter.emit():
            el = stack[-1]
            match el:
                case GherkinStep(
                    id=_,
                    location=_,
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
                    assert step_keyword(keyword)
                    self.registry.run_step(keyword, text)
                    last_keyword = keyword
                case _:
                    # print(el)
                    ...
