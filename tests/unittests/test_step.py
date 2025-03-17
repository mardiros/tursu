from tursu.pattern_matcher import DefaultPatternMatcher, RegEx, RegExPatternMatcher
from tursu.steps import Step


def dummy_hook(): ...


def test_default_step():
    step = Step("a step", dummy_hook)
    assert isinstance(step.pattern, DefaultPatternMatcher)
    assert step.pattern.pattern == "a step"
    assert step.hook == dummy_hook
    assert step != object()

    step2 = Step("a step", dummy_hook)
    assert step2 == step

    step3 = Step(RegEx("a step"), dummy_hook)
    assert isinstance(step3.pattern, RegExPatternMatcher)
    assert step3 != step

    assert repr(step) == 'Step("a step", dummy_hook)'
