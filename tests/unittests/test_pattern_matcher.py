import inspect
from collections.abc import Mapping

import pytest

from tursu.pattern_matcher import DefaultPatternMatcher


def dummy_str_pattern(param: str): ...


def dummy_int_pattern(param: int): ...


def no_param(): ...


def default_param(name: str = "Alice", age: int = 42): ...


def mix_param(name: str, age: int = 42): ...


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
    ],
)
def test_default_pattern_matcher_match(
    pattern: str,
    signature: inspect.Signature,
    text: str,
    expected: Mapping[str, str] | None,
):
    matcher = DefaultPatternMatcher(pattern, signature)
    assert matcher.get_matches(text) == expected
