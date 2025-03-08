from typing import Any, Callable, Literal

Keyword = Literal["given", "when", "then"]
Handler = Callable[..., None]


class Step:
    def __init__(self, pattern: str, hook: Handler):
        self.pattern = pattern
        self.hook = hook

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Step):
            return False
        return self.pattern == other.pattern and self.hook == other.hook

    def __repr__(self) -> str:
        return f'Step("{self.pattern}", {self.hook.__qualname__})'
