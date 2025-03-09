import pytest

from tursu.domain.model.gherkin import GherkinDocument, GherkinScenarioEnvelope
from tursu.registry import StepRegitry
from tursu.runner import GherkinIterator, GherkinRunner

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


def test_runner(doc: GherkinDocument, registry: StepRegitry, dummy_app: DummyApp):
    runner = GherkinRunner(doc, registry)
    runner.run()
    assert dummy_app.mailboxes == {
        "Bob": {
            "bob@alice.net": [
                "Welcome Bob",
            ],
        },
    }
