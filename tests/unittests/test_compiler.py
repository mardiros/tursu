import textwrap

import pytest

from tursu.compiler import GherkinCompiler, GherkinIterator
from tursu.domain.model.gherkin import GherkinDocument, GherkinScenarioEnvelope
from tursu.registry import StepRegistry

from .fixtures.steps import DummyApp


def test_emit_items(doc: GherkinDocument):
    gherkin_iter = GherkinIterator(doc)

    iter_step = gherkin_iter.emit()
    assert next(iter_step) == [doc]
    assert next(iter_step) == [doc, doc.feature]

    assert isinstance(doc.feature.children[0], GherkinScenarioEnvelope)
    assert next(iter_step) == [doc, doc.feature, doc.feature.children[0].scenario]
    assert next(iter_step) == [
        doc,
        doc.feature,
        doc.feature.children[0].scenario,
        doc.feature.children[0].scenario.steps[0],
    ]
    assert next(iter_step) == [
        doc,
        doc.feature,
        doc.feature.children[0].scenario,
        doc.feature.children[0].scenario.steps[1],
    ]
    assert next(iter_step) == [
        doc,
        doc.feature,
        doc.feature.children[0].scenario,
        doc.feature.children[0].scenario.steps[2],
    ]
    assert next(iter_step) == [
        doc,
        doc.feature,
        doc.feature.children[0].scenario,
        doc.feature.children[0].scenario.steps[3],
    ]
    with pytest.raises(StopIteration):
        next(iter_step)

    assert gherkin_iter.stack == []


def test_compiler(
    doc: GherkinDocument, registry: StepRegistry, dummy_app: DummyApp
) -> None:
    compiler = GherkinCompiler(doc, registry)
    code = compiler.to_module()

    assert (
        str(code)
        == textwrap.dedent(
            '''
    """Discover Scenario"""
    from tursu import StepRegistry

    def test_5_I_can_find_scenario_based_on_tag(registry: StepRegistry, dummy_app):
        """I can find scenario based on tag"""
        registry.run_step('given', 'a user Bob', dummy_app=dummy_app)
        registry.run_step('when', 'Bob create a mailbox bob@alice.net', dummy_app=dummy_app)
        registry.run_step('then', 'I see a mailbox bob@alice.net for Bob', dummy_app=dummy_app)
        registry.run_step('then', 'the mailbox bob@alice.net contains "Welcome Bob"', dummy_app=dummy_app)
            '''
        ).strip()
    )
