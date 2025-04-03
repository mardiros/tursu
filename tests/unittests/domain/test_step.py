from tests.unittests.domain.fixtures.steps import a_set_of_users, app
from tursu.domain.model.steps import StepDefinition, discover_fixtures
from tursu.runtime.pattern_matcher import (
    DefaultPatternMatcher,
    RegEx,
    RegExPatternMatcher,
)


def dummy_hook(): ...


def test_discover_fixtures():
    assert discover_fixtures(a_set_of_users) == {"app": app}


def test_default_step():
    step = StepDefinition("a step", dummy_hook)
    assert isinstance(step.pattern, DefaultPatternMatcher)
    assert step.pattern.pattern == "a step"
    assert step.hook == dummy_hook
    assert step != object()

    step2 = StepDefinition("a step", dummy_hook)
    assert step2 == step

    step3 = StepDefinition(RegEx("a step"), dummy_hook)
    assert isinstance(step3.pattern, RegExPatternMatcher)
    assert step3 != step

    assert repr(step) == 'StepDefinition("a step", dummy_hook)'
