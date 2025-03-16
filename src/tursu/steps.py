"""Represent a gherkin hook."""

import inspect
from collections.abc import Mapping
from typing import Any, Callable, Literal

from .pattern_matcher import (
    AbstractPattern,
    AbstractPatternMatcher,
    DefaultPatternMatcher,
)

StepKeyword = Literal["given", "when", "then"]
Handler = Callable[..., None]


class Step:
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
        return self.pattern.hightlight(matches)
