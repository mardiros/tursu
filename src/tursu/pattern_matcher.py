import abc
import re
from collections.abc import Mapping
from inspect import Signature
from typing import Any


class AbstractPatternMatcher(abc.ABC):
    def __init__(self, pattern: str, signature: Signature) -> None:
        self.pattern = pattern
        self.signature = signature

    def __eq__(self, other: Any) -> bool:
        if self.__class__ != other.__class__:
            return False
        return self.pattern == self.pattern

    def __str__(self) -> str:
        return self.pattern

    def __repr__(self) -> str:
        return f'"{self.pattern}"'

    @abc.abstractmethod
    def get_matches(
        self, text: str, kwargs: Mapping[str, Any]
    ) -> Mapping[str, Any] | None: ...


class AbstractPattern(abc.ABC):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    @classmethod
    @abc.abstractmethod
    def get_matcher(cls) -> type[AbstractPatternMatcher]: ...


class DefaultPatternMatcher(AbstractPatternMatcher):
    def __init__(self, pattern: str, signature: Signature) -> None:
        super().__init__(pattern, signature)
        re_pattern = pattern
        for key, val in signature.parameters.items():
            match val.annotation:
                case type() if val.annotation is int:
                    re_pattern = re_pattern.replace(f"{{{key}}}", rf"(?P<{key}>\d+)")
                case _:
                    re_pattern = re_pattern.replace(f"{{{key}}}", rf"(?P<{key}>.+)")
        self.re_pattern = re.compile(re_pattern)

    def get_matches(
        self, text: str, kwargs: Mapping[str, Any]
    ) -> Mapping[str, Any] | None:
        matches = self.re_pattern.search(text)
        if matches:
            res = {}
            matchdict = matches.groupdict()
            for key, val in self.signature.parameters.items():
                if key in matchdict:
                    res[key] = self.signature.parameters[key].annotation(matchdict[key])
                elif key in kwargs:
                    res[key] = kwargs[key]
                elif val.default and val.default != val.empty:
                    res[key] = val.default
            return res

        return None
