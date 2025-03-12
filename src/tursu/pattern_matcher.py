"""
Pattern matcher
"""

import abc
import re
from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from inspect import Signature
from typing import Any, Literal, get_args, get_origin


def cast_to_annotation(
    value: str, annotation: type[int | float | bool | str | date | datetime | Enum]
) -> int | float | bool | str | date | datetime | Enum:
    """
    Safely casts a string to the given annotation.

    :param value: The parameter to be cast.
    :param annotation: the constructor.

    :return: The casted value if successful, otherwise raises a ValueError.
    """

    # Define safe standard library types
    safe_types = (int, float, bool, str, date, datetime)
    if annotation in safe_types:
        # Handle special case for bool
        if annotation is bool:
            true_vals = {"true", "1", "yes", "on"}
            false_vals = {"false", "0", "no", "off"}
            lower_val = value.lower()
            if lower_val in true_vals:
                return True
            elif lower_val in false_vals:
                return False
            else:
                raise ValueError(
                    f"Cannot cast '{value}' to bool: "
                    f"use one of {(', ').join(sorted([*true_vals, *false_vals]))}"
                )

        if annotation is date:
            try:
                return date.fromisoformat(value)
            except ValueError:
                raise ValueError(
                    f"Cannot cast '{value}' to date: use iso format"
                ) from None

        if annotation is datetime:
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(
                    f"Cannot cast '{value}' to datetime: use iso format"
                ) from None

        try:
            # the type can't be a date or a datetime anymore
            return annotation(value)  # type: ignore
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Cannot cast '{value}' to {annotation}: {exc}") from exc

    if get_origin(annotation) is Literal:
        if value in get_args(annotation):
            return value
        raise ValueError(
            f"Value '{value}' is not a valid Literal: {get_args(annotation)}"
        )

    if isinstance(annotation, type) and issubclass(annotation, Enum):  # type: ignore
        try:
            return annotation[value]
        except KeyError:
            raise ValueError(
                f"Cannot cast '{value}' to Enum {annotation.__name__}"
            ) from None

    raise TypeError(f"Unsafe or unsupported type: {annotation}")


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

    @abc.abstractmethod
    def extract_fixtures(self, text: str) -> Mapping[str, Any] | None: ...


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
                    # if enclosed by double quote, use double quote as escaper
                    # not a gherkin spec.
                    re_pattern = re_pattern.replace(
                        f'"{{{key}}}"', rf'"(?P<{key}>[^"]+)"'
                    )
                    # otherwise, match one word
                    re_pattern = re_pattern.replace(f"{{{key}}}", rf"(?P<{key}>[^\s]+)")
        self.re_pattern = re.compile(f"^{re_pattern}$")

    def get_matches(
        self, text: str, kwargs: Mapping[str, Any]
    ) -> Mapping[str, Any] | None:
        matches = self.re_pattern.match(text)
        if matches:
            res = {}
            matchdict = matches.groupdict()
            for key, val in self.signature.parameters.items():
                if key in matchdict:
                    # transform the annotation to call the constructror with the value
                    typ = self.signature.parameters[key].annotation
                    res[key] = cast_to_annotation(matchdict[key], typ)
                elif key in kwargs:
                    res[key] = kwargs[key]
                elif val.default and val.default != val.empty:
                    res[key] = val.default
            return res

        return None

    def extract_fixtures(self, text: str) -> Mapping[str, Any] | None:
        matches = self.re_pattern.match(text)
        if matches:
            res = {}
            matchdict = matches.groupdict()
            for key, val in self.signature.parameters.items():
                if key in matchdict:
                    continue
                elif key == "doc_string":
                    continue
                elif key == "data_table":
                    continue
                if val.default != val.empty:
                    continue
                res[key] = val.annotation
            return res

        return None
