"""Gherkin scenario compiler."""

from collections.abc import Iterator, Sequence
from typing import Any

from tursu.domain.model.gherkin import (
    GherkinBackground,
    GherkinBackgroundEnvelope,
    GherkinDocument,
    GherkinEnvelope,
    GherkinFeature,
    GherkinRuleEnvelope,
    GherkinScenario,
    GherkinScenarioEnvelope,
    GherkinScenarioOutline,
    GherkinStep,
)
from tursu.domain.model.testmod import TestModule
from tursu.runtime.registry import Tursu
from tursu.service.ast.astfunction import TestFunctionWriter
from tursu.service.ast.astmodule import TestModuleWriter


class GherkinIterator:
    """
    Traverse the gherking feature document to emit gherkin objects.
    Keep the stack while traversing.

    :param doc: the document to iterate.
    """

    def __init__(self, doc: GherkinDocument) -> None:
        self.doc = doc
        self.stack: list[Any] = []

    def emit(self) -> Iterator[Any]:
        """Python iterator that emit the stack."""
        self.stack.append(self.doc)
        yield self.stack
        for _ in self.emit_feature(self.doc.feature):
            yield self.stack
        self.stack.pop()

    def emit_feature_from_enveloppe(
        self, enveloppe: Sequence[GherkinEnvelope]
    ) -> Iterator[Any]:
        """
        Helper to traverse Background, Scenario and Rule keywords from the scenario.

        :param enveloppe: Gherkin envelope that wrap the proper object to emit.
        """
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
        """
        Helper to traverse feature.

        :param feature: Gherkin feature to traverse.
        """
        self.stack.append(feature)
        yield self.stack
        yield from self.emit_feature_from_enveloppe(self.doc.feature.children)
        self.stack.pop()

    def emit_scenario(
        self, scenario: GherkinScenario | GherkinScenarioOutline
    ) -> Iterator[Any]:
        """
        Helper to traverse scenario.

        :param feature: Gherkin scenario or scenario outline to traverse.
        """
        for step in scenario.steps:
            self.stack.append(step)
            yield self.stack
            self.stack.pop()


class GherkinCompiler:
    """
    Gherkin compiler.

    :param doc: the gherkin file to compile.
    :param registry: the tursu registry where steps are already loaded.
    :param package_name: the parent module of the doc.
    """

    def __init__(
        self, doc: GherkinDocument, registry: Tursu, package_name: str
    ) -> None:
        self.emmiter = GherkinIterator(doc)
        self.registry = registry
        self.package_name = package_name

    def to_module(self) -> TestModule:
        """Get the compiled module."""
        module_node = None
        test_function = None
        background_steps: Sequence[GherkinStep] = []

        for stack in self.emmiter.emit():
            el = stack[-1]
            match el:
                case GherkinFeature():
                    assert module_node is None
                    module_node = TestModuleWriter(
                        el, self.registry, stack, self.package_name
                    )

                case GherkinBackground(steps=steps):
                    background_steps = steps

                case GherkinScenario(steps=steps):
                    test_function = TestFunctionWriter(
                        el,
                        self.registry,
                        [*background_steps, *steps],
                        stack,
                        self.package_name,
                    )
                    assert module_node is not None
                    module_node.append_test(test_function)
                    module_node.append_fixtures(test_function.fixtures)
                    if background_steps:
                        for step in background_steps:
                            test_function.add_step(step, stack)
                    for step in steps:
                        test_function.add_step(step, stack)

                case GherkinScenarioOutline(steps=steps, examples=examples):
                    test_function = TestFunctionWriter(
                        el,
                        self.registry,
                        [*background_steps, *steps],
                        stack,
                        self.package_name,
                    )
                    assert module_node is not None
                    module_node.append_test(test_function)
                    module_node.append_fixtures(test_function.fixtures)
                    if background_steps:
                        for step in background_steps:
                            test_function.add_step(step, stack)

                    for step in steps:
                        test_function.add_step(step, stack, examples)

                case _:
                    # print(el)
                    ...

        assert module_node is not None
        return TestModule(module_node.module_name, module_node.to_ast())
