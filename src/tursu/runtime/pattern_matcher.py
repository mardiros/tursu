"""
Pattern matcher module is used to make the link between gherkin step from a scenario

and step from the registry, registered via the [@given](#tursu.given),
[@when](#tursu.when) and [@then](#tursu.then) decorators.
"""

import abc
import re
from collections.abc import Mapping
from datetime import date, datetime
from enum import Enum
from inspect import Signature
from typing import Any, Literal, get_args, get_origin


class PatternError(RuntimeError):
    """
    Raised if a pattern is invalid.

    This exception happens during the log of the [step registry](#tursu.runtime.registry.Tursu).
    """


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
    """
    Base class to that implement the maghin pattern.
    """

    pattern: str
    """The string reprentation of the pattern to match."""
    signature: Signature
    """
    The decorated function signature used for introspecting fixtures and type hinting.
    """

    def __init__(self, pattern: str, signature: Signature) -> None:
        """
        :param pattern: Step decorator text.
        :param signature: Signature of the decorated method.
        """
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
    def match(self, text: str) -> bool:
        """Return true if its a match"""

    @abc.abstractmethod
    def get_matches(
        self, text: str, fixtures: Mapping[str, Any]
    ) -> Mapping[str, Any] | None:
        """
        Used to know if the gherkin step from a scenario has matched the step,

        and return the associated paramters.

        :param text: the text to match
        :param fixtures: the fixtures provided trom the test function, that have
                         to be passed to fill the parameters of the function
                         not provided by the matcher.
        """

    @abc.abstractmethod
    def extract_fixtures(self, text: str) -> Mapping[str, Any] | None:
        """Get the fixtures list to use from the text."""

    @abc.abstractmethod
    def hightlight(
        self,
        matches: Mapping[str, Any],
        color: str = "\033[36m",
        reset: str = "\033[0m",
    ) -> str:
        """
        Return a text representation of the step with the matched text highlighted
        for the terminal.

        :param matched: the list of matched step to consume.
        :return: the highlighted version.
        """


class AbstractPattern(abc.ABC):
    """
    Identifier of a pattern in a step.

    Technically its an
    [AbstractPatternMatcher](#tursu.runtime.pattern_matcher.AbstractPatternMatcher) factory.
    """

    pattern: str
    """The text representation of the pattern in the step."""

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    @classmethod
    @abc.abstractmethod
    def get_matcher(cls) -> type[AbstractPatternMatcher]:
        """Return the appropriate matcher for the step."""


class RegexBasePattern(AbstractPatternMatcher):
    """Base class for pattern matcher that consume a regex."""

    re_pattern: re.Pattern[str]
    """The compiled version of the pattern."""

    def match(self, text: str) -> bool:
        matches = self.re_pattern.match(text)
        return bool(matches)

    def get_matches(
        self, text: str, fixtures: Mapping[str, Any]
    ) -> Mapping[str, Any] | None:
        """
        Used to know if the gherkin step from a scenario has matched the step,

        and return the associated paramters.

        :param text: the text to match
        :param fixtures: the fixtures provided trom the test function, that have
                         to be passed to fill the parameters of the function
                         not provided by the matcher.
        """

        matches = self.re_pattern.match(text)
        if matches:
            res = {}
            matchdict = matches.groupdict()
            for key, val in self.signature.parameters.items():
                if key in matchdict:
                    # transform the annotation to call the constructror with the value
                    typ = self.signature.parameters[key].annotation
                    res[key] = cast_to_annotation(matchdict[key], typ)
                elif key in fixtures:
                    res[key] = fixtures[key]
                elif val.default and val.default != val.empty:
                    res[key] = val.default
            return res

        return None

    def extract_fixtures(self, text: str) -> Mapping[str, Any] | None:
        """
        Get the fixtures list to use from the text.

        :param text: the text from a gherkin step in a scenario.
        """
        matches = self.re_pattern.match(text)
        if matches:
            res = {}
            matchdict = matches.groupdict()
            for key, val in self.signature.parameters.items():
                if key in matchdict:
                    continue
                elif key in ("doc_string", "data_table"):
                    continue
                if val.default != val.empty:
                    continue
                res[key] = val.annotation
            return res

        return None


class DefaultPatternMatcher(RegexBasePattern):
    """
    The pattern matcher that look like the python format.
    """

    def __init__(self, pattern: str, signature: Signature) -> None:
        """
        :param pattern: Step decorator text.
        :param signature: Signature of the decorated method.
        """
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

    def hightlight(
        self,
        matches: Mapping[str, Any],
        color: str = "\033[36m",
        reset: str = "\033[0m",
    ) -> str:
        """
        Return a text representation of the step with the matched text highlighted
        for the terminal.

        :param matched: the list of matched step to consume.
        :return: the highlighted version.
        """
        colored_matches = {
            key: f"{color}{value}{reset}" for key, value in matches.items()
        }
        return self.pattern.format(**colored_matches)


class RegExPatternMatcher(RegexBasePattern):
    """
    The pattern matcher that look like the python regular expression.
    """

    def __init__(self, pattern: str, signature: Signature) -> None:
        """
        :param pattern: Step decorator text that contain the regex.
        :param signature: Signature of the decorated method.
        """
        super().__init__(pattern, signature)
        try:
            self.re_pattern = re.compile(f"^{pattern}$")
        except re.PatternError as exc:
            raise PatternError(f"Can't compile to regex: {pattern}: {exc}") from exc

    def hightlight(
        self,
        matches: Mapping[str, Any],
        color: str = "\033[36m",
        reset: str = "\033[0m",
    ) -> str:
        """
        Return a text representation of the step with the matched text highlighted
        for the terminal.

        :param matched: the list of matched step to consume.
        :return: the highlighted version.
        """
        colored_matches = {
            key: f"{color}{value}{reset}" for key, value in matches.items()
        }
        ret = self.pattern
        for key, val in colored_matches.items():
            ret = re.sub(rf"\(\?P<{key}>[^\)]+\)", val, ret)
        return ret


class RegEx(AbstractPattern):
    """Marker for regex in a step decorator."""

    @classmethod
    def get_matcher(cls) -> type[AbstractPatternMatcher]:
        """Return the appropriate matcher for the step."""
        return RegExPatternMatcher

    def __repr__(self) -> str:
        return f'r"{self.pattern}"'
