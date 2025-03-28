"""Step definition hooks."""

import inspect
from collections.abc import Mapping
from typing import Any, Callable, Literal

from tursu.runtime.pattern_matcher import (
    AbstractPattern,
    AbstractPatternMatcher,
    DefaultPatternMatcher,
)

StepKeyword = Literal["Given", "When", "Then"]
"""Gherkin keywords that can be mapped to step definitions."""

Handler = Callable[..., None]
"""
The hook handler is a decorated function that have any parameters
but can't return anything.

The decorated method parameters comes from the pattern matcher first
and fallback to pytest fixtures.
"""


class Step:
    """
    Step definition.

    :param pattern: pattern matcher for the step.
    :param hook: The decorated method.
    """

    def __init__(self, pattern: str | AbstractPattern, hook: Handler):
        matcher: type[AbstractPatternMatcher]
        if isinstance(pattern, str):
            matcher = DefaultPatternMatcher
        else:
            matcher = pattern.get_matcher()
            pattern = pattern.pattern

        self.pattern = matcher(pattern, inspect.signature(hook))
        self.hook = hook

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Step):
            return False
        return self.pattern == other.pattern and self.hook == other.hook

    def __repr__(self) -> str:
        return f'Step("{self.pattern}", {self.hook.__qualname__})'

    def __call__(self, **kwargs: Any) -> None:
        self.hook(**kwargs)

    def highlight(self, matches: Mapping[str, Any]) -> str:
        """Highlith representation of a step that has matched for the terminal."""
        return self.pattern.hightlight(matches)
