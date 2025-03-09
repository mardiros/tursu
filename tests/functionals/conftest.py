import pytest

from tursu.registry import StepRegistry


@pytest.fixture()
def registry() -> StepRegistry:
    return StepRegistry().scan()
