import pytest

from tursu.domain.model.gherkin import GherkinDocument, GherkinScenarioEnvelope
from tursu.runner import Runner


def test_emit_items(doc: GherkinDocument):
    runner = Runner(doc)

    iter_step = runner.emit()
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

    assert runner.stack == []
