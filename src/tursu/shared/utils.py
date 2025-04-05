"""
Utilities functions for introspection.
"""

import inspect
from collections.abc import Mapping, Sequence
from types import UnionType
from typing import Any, TypeGuard, Union, get_origin


def is_mapping(value: type[Any] | None) -> TypeGuard[Mapping[Any, Any]]:
    """Inspect type to define if it is a Mapping, such as dict or MutableMapping."""
    return value is not None and inspect.isclass(value) and issubclass(value, Mapping)


def is_sequence(value: type[Any] | None) -> TypeGuard[Sequence[Any]]:
    """Inspect type to define if it is a Sequence, such as list or MutableSequence."""
    if value is None or not inspect.isclass(value):
        return False
    if issubclass(value, str):
        return False
    return issubclass(value, Sequence)


def is_union(typ: type[Any]) -> bool:
    """Used to detect unions like Optional[T], Union[T, U] or T | U."""
    type_origin = get_origin(typ)
    if type_origin:
        if type_origin is Union:  # Optional[T]
            return True

        if type_origin is UnionType:  # T | U
            return True
    return False
