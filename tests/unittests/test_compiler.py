import textwrap

import pytest

from tursu.compiler import GherkinCompiler, GherkinIterator
from tursu.domain.model.gherkin import GherkinDocument
from tursu.registry import Tursu

from .fixtures.steps import DummyApp


def test_emit_items(doc: GherkinDocument):
    gherkin_iter = GherkinIterator(doc)

    iter_step = gherkin_iter.emit()
    assert [repr(i) for i in next(iter_step)] == ["📄 Document: scenario.feature"]

    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: scenario.feature",
        "🥒 Feature: Discover Scenario",
    ]

    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: scenario.feature",
        "🥒 Feature: Discover Scenario",
        "Background: ",
    ]

    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: scenario.feature",
        "🥒 Feature: Discover Scenario",
        "🔹 Rule: I write a wip test",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: scenario.feature",
        "🥒 Feature: Discover Scenario",
        "🔹 Rule: I write a wip test",
        "🎬 Scenario: I can find scenario based on tag",
    ]

    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: scenario.feature",
        "🥒 Feature: Discover Scenario",
        "🔹 Rule: I write a wip test",
        "🎬 Scenario: I can find scenario based on tag",
        "When Bob create a mailbox bob@alice.net",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: scenario.feature",
        "🥒 Feature: Discover Scenario",
        "🔹 Rule: I write a wip test",
        "🎬 Scenario: I can find scenario based on tag",
        "Then Bob see a mailbox bob@alice.net",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: scenario.feature",
        "🥒 Feature: Discover Scenario",
        "🔹 Rule: I write a wip test",
        "🎬 Scenario: I can find scenario based on tag",
        'And the mailbox bob@alice.net "Welcome Bob" message is',
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: scenario.feature",
        "🥒 Feature: Discover Scenario",
        "🔹 Rule: I write a wip test",
        "🎬 Scenario: I can find scenario based on tag",
        "And the API for Bob respond",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: scenario.feature",
        "🥒 Feature: Discover Scenario",
        "🔹 Rule: I write a wip test",
        "🎬 Scenario: I can find scenario based on tag",
        "And the users dataset is",
    ]

    with pytest.raises(StopIteration):
        next(iter_step)

    assert gherkin_iter.stack == []


def test_compiler(doc: GherkinDocument, registry: Tursu, dummy_app: DummyApp) -> None:
    compiler = GherkinCompiler(doc, registry)
    code = compiler.to_module()

    assert (
        str(code)
        == textwrap.dedent(
            '''
        """Discover Scenario"""
        from typing import Any
        import pytest
        from tursu.registry import Tursu
        from tursu.runner import TursuRunner

        @pytest.mark.wip
        def test_10_I_can_find_scenario_based_on_tag(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu, dummy_app: Any):
            """I can find scenario based on tag"""
            with TursuRunner(request, capsys, tursu, ['📄 Document: scenario.feature', '🥒 Feature: Discover Scenario', '🔹 Rule: I write a wip test', '🎬 Scenario: I can find scenario based on tag']) as tursu_runner:
                tursu_runner.run_step('Given', 'a user Bob', dummy_app=dummy_app)
                tursu_runner.run_step('When', 'Bob create a mailbox bob@alice.net', dummy_app=dummy_app)
                tursu_runner.run_step('Then', 'Bob see a mailbox bob@alice.net', dummy_app=dummy_app)
                tursu_runner.run_step('Then', 'the mailbox bob@alice.net "Welcome Bob" message is', dummy_app=dummy_app, doc_string='...')
                tursu_runner.run_step('Then', 'the API for Bob respond', dummy_app=dummy_app, doc_string=[{'email': 'bob@alice.net', 'subject': 'Welcome Bob', 'body': '...'}])
                tursu_runner.run_step('Then', 'the users dataset is', dummy_app=dummy_app, data_table=[{'username': 'Bob', 'mailbox': 'bob@alice.net'}])
            '''
        ).strip()
    )


def test_compiler_compile_outline(
    outline_doc: GherkinDocument, registry: Tursu, dummy_app: DummyApp
) -> None:
    compiler = GherkinCompiler(outline_doc, registry)
    code = compiler.to_module()

    assert (
        str(code)
        == textwrap.dedent(
            '''
    """Discover Scenario Outline

    This feature is complex and require a comment."""
    from typing import Any
    import pytest
    from tursu.registry import Tursu
    from tursu.runner import TursuRunner

    @pytest.mark.oulined
    @pytest.mark.parametrize('username,email', [pytest.param('Alice', 'alice@alice.net', id='Examples'), pytest.param('Bob', 'bob@bob.net', id='Examples')])
    def test_10_I_can_load_scenario_outline(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu, dummy_app: Any, username: str, email: str):
        """I can load scenario outline

        This scenario is complex and require a comment."""
        with TursuRunner(request, capsys, tursu, ['📄 Document: scenario_outline.feature', '🥒 Feature: Discover Scenario Outline', '🎬 Scenario Outline: I can load scenario outline']) as tursu_runner:
            tursu_runner.run_step('Given', 'a user momo', dummy_app=dummy_app)
            tursu_runner.run_step('Given', tursu_runner.format_example_step('a user <username>', username=username, email=email), dummy_app=dummy_app)
            tursu_runner.run_step('When', tursu_runner.format_example_step('<username> create a mailbox <email>', username=username, email=email), dummy_app=dummy_app)
            tursu_runner.run_step('Then', tursu_runner.format_example_step('<username> see a mailbox <email>', username=username, email=email), dummy_app=dummy_app)
     '''
        ).strip()
    )
