import inspect
from collections.abc import Mapping
from datetime import UTC, date, datetime
from enum import Enum
from typing import Any, Literal

import pytest

from tursu.runtime.pattern_matcher import (
    AbstractPatternMatcher,
    DefaultPatternMatcher,
    PatternError,
    RegEx,
    RegExPatternMatcher,
    cast_to_annotation,
)


def dummy_str_pattern(param: str): ...


def dummy_int_pattern(param: int): ...


def no_param(): ...


def default_param(name: str = "Alice", age: int = 42): ...


def mix_param(name: str, age: int = 42): ...


def using_data_table(data_table: list[dict[str, str]]): ...


def using_doc_string(doc_string: dict[str, str]): ...


x = [
    {"username": "johndoe", "password": "secret123"},
    {"username": "janedoe", "password": "password1"},
]


class Foobar(Enum):
    foo = "Foo"
    bar = "Bar"


@pytest.mark.parametrize(
    "value,annotation,expected",
    [
        pytest.param("1", str, "1", id="str"),
        pytest.param("1", int, 1, id="int"),
        pytest.param("1", float, 1.0, id="float"),
        pytest.param("1", bool, True, id="bool[1]"),
        pytest.param("true", bool, True, id="bool[true]"),
        pytest.param("on", bool, True, id="bool[on]"),
        pytest.param("0", bool, False, id="bool[0]"),
        pytest.param("false", bool, False, id="bool[false]"),
        pytest.param("off", bool, False, id="bool[off]"),
        pytest.param("foo", Literal["foo", "bar"], "foo", id="literal"),
        pytest.param("foo", Foobar, Foobar.foo, id="enum"),
        pytest.param("2025-03-12", date, date(2025, 3, 12), id="date"),
        pytest.param(
            "2000-01-02T10:00", datetime, datetime(2000, 1, 2, 10), id="datetime"
        ),
        pytest.param(
            "2000-01-02T10:00Z",
            datetime,
            datetime(2000, 1, 2, 10, tzinfo=UTC),
            id="UTC datetime",
        ),
        pytest.param(
            "2000-01-02T10:00Z",
            date | datetime,
            datetime(2000, 1, 2, 10, tzinfo=UTC),
            id="union",
        ),
    ],
)
def test_cast_to_annotation(value: Any, annotation: Any, expected: Any) -> None:
    assert cast_to_annotation(value, annotation) == expected


@pytest.mark.parametrize(
    "value,annotation,expected",
    [
        pytest.param(
            "one",
            int,
            "Cannot cast 'one' to <class 'int'>: "
            "invalid literal for int() with base 10: 'one'",
            id="int",
        ),
        pytest.param(
            "one",
            float,
            "Cannot cast 'one' to <class 'float'>: "
            "could not convert string to float: 'one'",
            id="float",
        ),
        pytest.param(
            "one",
            bool,
            "Cannot cast 'one' to bool: use one of 0, 1, false, no, off, on, true, yes",
            id="bool",
        ),
        pytest.param(
            "monday",
            date,
            "Cannot cast 'monday' to date: use iso format",
            id="date",
        ),
        pytest.param(
            "yore",
            datetime,
            "Cannot cast 'yore' to datetime: use iso format",
            id="datetime",
        ),
        pytest.param(
            "Foo",
            Literal["foo", "bar"],
            "Value 'Foo' is not a valid Literal: ('foo', 'bar')",
            id="literal",
        ),
        pytest.param("Foo", Foobar, "Cannot cast 'Foo' to Enum Foobar", id="enum"),
        pytest.param(
            "2025, August the 1st",
            date | datetime,
            "Cannot cast '2025, August the 1st' to datetime.date | datetime.datetime",
            id="union",
        ),
    ],
)
def test_cast_to_annotation_value_error(
    value: Any, annotation: Any, expected: Any
) -> None:
    with pytest.raises(ValueError) as ctx:
        assert cast_to_annotation(value, annotation)

    assert str(ctx.value) == expected


def test_cast_to_annotation_type_error() -> None:
    with pytest.raises(TypeError) as ctx:
        assert cast_to_annotation("value", dict)  # type: ignore

    assert str(ctx.value) == "Unsafe or unsupported type: <class 'dict'>"


@pytest.mark.parametrize(
    "pattern,signature,text,expected",
    [
        pytest.param(
            "I have no params",
            inspect.signature(no_param),
            "I have no params",
            {},
            id="no params",
        ),
        pytest.param(
            "I have no params",
            inspect.signature(no_param),
            "unexpected",
            None,
            id="no params don't match",
        ),
        pytest.param(
            "I have {param} eggs",
            inspect.signature(dummy_str_pattern),
            "I have three eggs",
            {"param": "three"},
            id="text",
        ),
        pytest.param(
            "I have {param} gherkin",
            inspect.signature(dummy_str_pattern),
            "I have no eggs",
            None,
            id="text don't match",
        ),
        pytest.param(
            "I have {param} eggs",
            inspect.signature(dummy_int_pattern),
            "I have 3 eggs",
            {"param": 3},
            id="int",
        ),
        pytest.param(
            "I have {param} eggs",
            inspect.signature(dummy_int_pattern),
            "I have no eggs",
            None,
            id="int don't match",
        ),
        pytest.param(
            "I use default",
            inspect.signature(default_param),
            "I use default",
            {"name": "Alice", "age": 42},
            id="default parameters",
        ),
        pytest.param(
            "My name is {name}",
            inspect.signature(default_param),
            "My name is Bob",
            {"name": "Bob", "age": 42},
            id="default parameter int",
        ),
        pytest.param(
            "I am {age}",
            inspect.signature(default_param),
            "I am 21",
            {"name": "Alice", "age": 21},
            id="default parameter str",
        ),
        pytest.param(
            "I have no name",
            inspect.signature(mix_param),
            "I have no name",
            {"age": 42},
            id="mix parameter",
        ),
        pytest.param(
            "I use data table",
            inspect.signature(using_data_table),
            "I use data table",
            {},
            id="data_table",
        ),
        pytest.param(
            "I use doc string",
            inspect.signature(using_doc_string),
            "I use doc string",
            {},
            id="doc_string",
        ),
    ],
)
def test_default_pattern_matcher_match(
    pattern: str,
    signature: inspect.Signature,
    text: str,
    expected: Mapping[str, str] | None,
):
    matcher = DefaultPatternMatcher(pattern, signature)
    assert matcher.get_matches(text, {}) == expected


@pytest.mark.parametrize(
    "pattern,signature,text,expected",
    [
        pytest.param(
            "I have no params",
            inspect.signature(no_param),
            "I have no params",
            {},
            id="no params",
        ),
        pytest.param(
            "I have no params",
            inspect.signature(no_param),
            "unexpected",
            None,
            id="no params don't match",
        ),
        pytest.param(
            "I have {param} eggs",
            inspect.signature(dummy_str_pattern),
            "I have three eggs",
            {},
            id="text",
        ),
        pytest.param(
            "I have no name",
            inspect.signature(mix_param),
            "I have no name",
            {"name": str},
            id="fixture",
        ),
        pytest.param(
            "I use data table",
            inspect.signature(using_data_table),
            "I use data table",
            {},
            id="data_table",
        ),
        pytest.param(
            "I use doc string",
            inspect.signature(using_doc_string),
            "I use doc string",
            {},
            id="doc_string",
        ),
    ],
)
def test_extract_fixtures(
    pattern: str,
    signature: inspect.Signature,
    text: str,
    expected: Mapping[str, str] | None,
):
    matcher = DefaultPatternMatcher(pattern, signature)
    assert matcher.extract_fixtures(text) == expected


def test_pattern_python_magics():
    matcher = DefaultPatternMatcher(
        "I have {param}", inspect.signature(dummy_str_pattern)
    )
    matcher2 = DefaultPatternMatcher(
        "I have {param}", inspect.signature(dummy_str_pattern)
    )
    matcher3 = RegExPatternMatcher(
        r"I have (?P<param>[^\s]+)", inspect.signature(dummy_str_pattern)
    )
    assert matcher == matcher2
    assert matcher != matcher3
    assert str(matcher) == "I have {param}"
    assert str(matcher3) == r"I have (?P<param>[^\s]+)"

    assert repr(matcher) == '"I have {param}"'


@pytest.mark.parametrize(
    "pattern,signature,text,fixtures,expected",
    [
        pytest.param(
            "I have fixtures",
            inspect.signature(dummy_str_pattern),
            "I have fixtures",
            {"param": "foo"},
            {"param": "foo"},
            id="fixtures",
        ),
        pytest.param(
            "I have {name} and fixtures",
            inspect.signature(mix_param),
            "I have blaz and fixtures",
            {"age": 42},
            {"name": "blaz", "age": 42},
            id="fixtures",
        ),
    ],
)
def test_fixtures_pattern_matcher_match(
    pattern: str,
    signature: inspect.Signature,
    text: str,
    fixtures: Mapping[str, str],
    expected: Mapping[str, str] | None,
):
    matcher = DefaultPatternMatcher(pattern, signature)
    assert matcher.get_matches(text, fixtures) == expected


@pytest.mark.parametrize(
    "pattern,signature,text,fixtures,expected",
    [
        pytest.param(
            "I have fixtures",
            inspect.signature(dummy_str_pattern),
            "I have fixtures",
            {"param": "foo"},
            {"param": "foo"},
            id="fixtures",
        ),
        pytest.param(
            r"I have (?P<name>[^\s]+) and fixtures",
            inspect.signature(mix_param),
            "I have blaz and fixtures",
            {"age": 42},
            {"name": "blaz", "age": 42},
            id="fixtures",
        ),
    ],
)
def test_regex_pattern_matcher_match(
    pattern: str,
    signature: inspect.Signature,
    text: str,
    fixtures: Mapping[str, str],
    expected: Mapping[str, str] | None,
):
    matcher = RegExPatternMatcher(pattern, signature)
    assert matcher.get_matches(text, fixtures) == expected


@pytest.mark.parametrize(
    "pattern,matches,expected",
    [
        pytest.param(
            DefaultPatternMatcher(
                r"I have {param} yo", inspect.signature(dummy_str_pattern)
            ),
            {"param": "blaz"},
            "I have \033[36mblaz\033[0m yo",
            id="fixtures",
        ),
        pytest.param(
            RegExPatternMatcher(
                r"I have (?P<param>[^\s]+) yo", inspect.signature(dummy_str_pattern)
            ),
            {"param": "blaz"},
            "I have \033[36mblaz\033[0m yo",
            id="fixtures",
        ),
    ],
)
def test_regex_pattern_highlight(
    pattern: AbstractPatternMatcher,
    matches: Mapping[str, str],
    expected: str,
):
    assert pattern.hightlight(matches) == expected


def test_regex_invalid():
    with pytest.raises(PatternError) as exc:
        RegExPatternMatcher(
            r"I have error <?P<param>[^\s+)", inspect.signature(dummy_str_pattern)
        )

    assert (
        str(exc.value) == r"Can't compile to regex: I have error <?P<param>[^\s+): "
        "unterminated character set at position 24"
    )


def test_regex():
    regex = RegEx("pattern")
    assert regex.get_matcher() is RegExPatternMatcher
    assert repr(regex) == 'r"pattern"'
