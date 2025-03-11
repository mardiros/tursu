import textwrap

import pytest

from tursu.compiler import GherkinCompiler, GherkinIterator
from tursu.domain.model.gherkin import GherkinDocument
from tursu.registry import StepRegistry

from .fixtures.steps import DummyApp


def test_emit_items(doc: GherkinDocument):
    gherkin_iter = GherkinIterator(doc)

    iter_step = gherkin_iter.emit()
    assert [repr(i) for i in next(iter_step)] == ["Document: scenario.feature"]

    assert [repr(i) for i in next(iter_step)] == [
        "Document: scenario.feature",
        "Feature: Discover Scenario",
    ]

    assert [repr(i) for i in next(iter_step)] == [
        "Document: scenario.feature",
        "Feature: Discover Scenario",
        "Background: ",
    ]

    assert [repr(i) for i in next(iter_step)] == [
        "Document: scenario.feature",
        "Feature: Discover Scenario",
        "Rule: I write a wip test",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "Document: scenario.feature",
        "Feature: Discover Scenario",
        "Rule: I write a wip test",
        "Scenario: I can find scenario based on tag",
    ]

    assert [repr(i) for i in next(iter_step)] == [
        "Document: scenario.feature",
        "Feature: Discover Scenario",
        "Rule: I write a wip test",
        "Scenario: I can find scenario based on tag",
        "When Bob create a mailbox bob@alice.net",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "Document: scenario.feature",
        "Feature: Discover Scenario",
        "Rule: I write a wip test",
        "Scenario: I can find scenario based on tag",
        "Then I see a mailbox bob@alice.net for Bob",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "Document: scenario.feature",
        "Feature: Discover Scenario",
        "Rule: I write a wip test",
        "Scenario: I can find scenario based on tag",
        'And the mailbox bob@alice.net "Welcome Bob" message is',
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "Document: scenario.feature",
        "Feature: Discover Scenario",
        "Rule: I write a wip test",
        "Scenario: I can find scenario based on tag",
        "And the API for bob@alice.net respond",
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
        from typing import Any
        import pytest
        from tursu import StepRegistry

        @pytest.mark.wip
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
