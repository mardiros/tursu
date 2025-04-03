"""Step definition hooks."""

import inspect
import sys
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


def discover_fixtures(hook: Callable[..., None]) -> dict[str, type]:
    """
    Get all the fixtures that have been declared in the hook module
    from the signature of the hook.
    """
    signature = inspect.signature(hook)
    module = sys.modules[hook.__module__]
    fixtures: dict[str, type] = {}
    for key in signature.parameters:
        if hasattr(module, key):
            fixtures[key] = getattr(module, key)
    return fixtures


class StepDefinition:
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
        self.fixtures: Mapping[str, type] = discover_fixtures(hook)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, StepDefinition):
            return False
        return self.pattern == other.pattern and self.hook == other.hook

    def __repr__(self) -> str:
        return f'StepDefinition("{self.pattern}", {self.hook.__qualname__})'

    def __call__(self, **kwargs: Any) -> None:
        """Will call the hook with the given parameter."""
        self.hook(**kwargs)

    def highlight(
        self,
        matches: Mapping[str, Any],
        color: str = "\033[36m",
        reset: str = "\033[0m",
    ) -> str:
        """Highlith representation of a step that has matched for the terminal."""
        return self.pattern.hightlight(matches, color, reset)
