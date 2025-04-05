from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import Any, Union

import pytest

from tursu.shared.utils import is_mapping, is_sequence, is_union


@pytest.mark.parametrize(
    "typ,expected",
    [
        pytest.param(int, False, id="int"),
        pytest.param(str, False, id="str"),
        pytest.param(int | str, True, id="int | str"),
        pytest.param(
            Union[int, str],
            True,
            id="Union[int, str]",
        ),
    ],
)
def test_is_union(typ: type[Any], expected: bool):
    assert is_union(typ) is expected


@pytest.mark.parametrize(
    "typ,expected",
    [
        pytest.param(int, False, id="int"),
        pytest.param(str, False, id="str"),
        pytest.param(list, False, id="list"),
        pytest.param(dict, True, id="dict"),
        pytest.param(Mapping, True, id="Mapping"),
        pytest.param(MutableMapping, True, id="MutableMapping"),
    ],
)
def test_is_mapping(typ: type[Any], expected: bool):
    assert is_mapping(typ) is expected


@pytest.mark.parametrize(
    "typ,expected",
    [
        pytest.param(int, False, id="int"),
        pytest.param(str, False, id="str"),
        pytest.param(dict, False, id="dict"),
        pytest.param(list, True, id="list"),
        pytest.param(Sequence, True, id="Sequence"),
        pytest.param(MutableSequence, True, id="MutableSequence"),
    ],
)
def test_is_sequence(typ: type[Any], expected: bool):
    assert is_sequence(typ) is expected
