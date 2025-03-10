import textwrap

import pytest

from tursu.compiler import GherkinCompiler, GherkinIterator
from tursu.domain.model.gherkin import (
    GherkinBackgroundEnvelope,
    GherkinDocument,
    GherkinScenarioEnvelope,
)
from tursu.registry import StepRegistry

from .fixtures.steps import DummyApp


def test_emit_items(doc: GherkinDocument):
    gherkin_iter = GherkinIterator(doc)

    iter_step = gherkin_iter.emit()
    assert next(iter_step) == [doc]
    assert next(iter_step) == [doc, doc.feature]

    assert isinstance(doc.feature.children[0], GherkinBackgroundEnvelope)
    assert next(iter_step) == [doc, doc.feature, doc.feature.children[0].background]

    assert isinstance(doc.feature.children[1], GherkinScenarioEnvelope)
    assert next(iter_step) == [doc, doc.feature, doc.feature.children[1].scenario]
    assert next(iter_step) == [
        doc,
        doc.feature,
        doc.feature.children[1].scenario,
        doc.feature.children[1].scenario.steps[0],
    ]
    assert next(iter_step) == [
        doc,
        doc.feature,
        doc.feature.children[1].scenario,
        doc.feature.children[1].scenario.steps[1],
    ]
    assert next(iter_step) == [
        doc,
        doc.feature,
        doc.feature.children[1].scenario,
        doc.feature.children[1].scenario.steps[2],
    ]
    assert next(iter_step) == [
        doc,
        doc.feature,
        doc.feature.children[1].scenario,
        doc.feature.children[1].scenario.steps[3],
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

        def test_7_I_can_find_scenario_based_on_tag(registry: StepRegistry, dummy_app):
            """I can find scenario based on tag"""
            registry.run_step('given', 'a user Bob', dummy_app=dummy_app)
            registry.run_step('when', 'Bob create a mailbox bob@alice.net', dummy_app=dummy_app)
            registry.run_step('then', 'I see a mailbox bob@alice.net for Bob', dummy_app=dummy_app)
            registry.run_step('then', 'the mailbox bob@alice.net "Welcome Bob" message is', dummy_app=dummy_app, doc_string='...')
            registry.run_step('then', 'the API for bob@alice.net respond', dummy_app=dummy_app, doc_string=[{'email': 'bob@alice.net', 'subject': 'Welcome Bob', 'body': '...'}])
            '''
        ).strip()
    )
