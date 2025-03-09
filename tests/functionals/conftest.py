import pytest

from tursu.registry import StepRegistry


@pytest.fixture(scope="session")
def registry():
    return StepRegistry().scan()
