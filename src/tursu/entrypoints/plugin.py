"""Pytest plugin"""

import inspect
import sys
from collections.abc import Iterable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from tursu.domain.model.gherkin import GherkinDocument
from tursu.runtime.registry import Tursu
from tursu.service.compiler import GherkinCompiler

_tursu = Tursu()


@pytest.fixture(scope="session")
def tursu() -> Tursu:
    """The tursu step registry, used to run Gherkin scenario."""
    return _tursu


class GherkinTestModule(pytest.Module):
    """
    A pytest collector made for gherkin .scenario files.

    While collecting, it generate ast code to run tests using the python runtime.
    """

    def __init__(self, path: Path, tursu: Tursu, **kwargs: Any) -> None:
        doc = GherkinDocument.from_file(path)
        self.gherkin_doc = path.name
        compiler = GherkinCompiler(doc, tursu)
        self.test_mod = case = compiler.to_module()

        self.test_casefile = path.parent / case.filename
        super().__init__(path=self.test_casefile, **kwargs)
        if (
            self.session.config.getoption("--trace")
            or self.session.config.option.verbose == 3
        ):
            case.write_temporary(path.parent)  # coverage: ignore
            # we preload before updating the path
            self._obj = super()._getobj()  # coverage: ignore

        self._nodeid = self.nodeid.replace(case.filename, path.name)
        self.path = path

    def _getobj(self) -> ModuleType:
        return self.test_mod.to_python_module()

    def __repr__(self) -> str:
        return f"<GherkinDocument {self.gherkin_doc}>"

    def collect(self) -> Iterable[pytest.Item | pytest.Collector]:
        path, self.path = self.path, self.test_casefile  # collect from the ast file
        ret = super().collect()
        self.path = path  # restore the scenario path to have a per path
        return ret


def tursu_collect_file() -> None:
    """
    Used to generate a `pytest_collect_file()` function in a conftest.py file.

    pytest comes with a hook
    [pytest_collect_file](https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.hookspec.pytest_collect_file)
    used to collect tests that tursu use to generate the tests suite from
    Gherkin files.

    the conftest.py has to be created with in the same directory structure of
    .scenario file.

    Function Tests Directory Structure:

    ```
    tests/functionals/
    │── conftest.py        # Must contains `tursu_collect_file()`
    │── steps.py           # Step definitions for Gherkin scenarios
    │── example.scenario   # Gherkin scenario file
    ```

    If you want to rearrange your scenario in subdirectory, or
    just your steps, it is not a problem, pytest will walk under all directory
    tree. Tursu will collect all steps definifition too.

    ```
    tests/functionals/
    │── conftest.py        # Must contains `tursu_collect_file()`
    │── steps.py           # Common step definitions for Gherkin scenarios
    │── features1/
    │   ├── other_steps.py    # Step definitions for Gherkin scenarios
    │   ├── example.scenario  # Gherkin scenario file
    ```

    ```{important}
    steps definition using the ([@given](#tursu.given),
    [@when](#tursu.when), [@then](#tursu.then)) are globals.

    Says differently, **they are not scoped per sub-directories**.
    ```
    """
    conftest_mod = inspect.getmodule(inspect.stack()[1][0])  # this is conftest.py
    assert conftest_mod

    def pytest_collect_file(  # type: ignore
        parent: pytest.Package, file_path: Path
    ) -> GherkinTestModule | None:
        module_name = conftest_mod.__name__
        parent_name = module_name.rsplit(".", 1)[0]  # Remove the last part
        mod = sys.modules.get(parent_name)
        _tursu.scan(mod)  # load steps before the scenarios

        if file_path.suffix == ".feature":
            doc = GherkinDocument.from_file(file_path)
            ret = GherkinTestModule.from_parent(
                parent, path=file_path, tursu=_tursu, name=doc.name
            )
            return ret

    conftest_mod.pytest_collect_file = pytest_collect_file  # type: ignore
