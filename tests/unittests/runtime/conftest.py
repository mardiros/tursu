import pytest

from tursu.runtime.registry import Tursu


@pytest.fixture(scope="session")
def registry():
    import tests.unittests.runtime.fixtures

    return Tursu().scan(tests.unittests.runtime.fixtures)
