import pytest

from tursu.registry import StepRegistry


@pytest.fixture()
def registry():
    return StepRegistry().scan()
