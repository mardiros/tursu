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
    """
    Fixture used in generated test module to access to the runtime part.

    Tursu generate bytecode for running scenario. The bytecode is simple,
    and is designed to be highly debuggable.

    Tursu object is the registry of the steps definition that can be used
    at runtime to match those definition and run their associated hook.
    """
    return _tursu


def build_pkg(node: Any) -> str:
    parts: list[str] = []
    while node.__class__ is pytest.Package:
        parts.append(node.name)
        node = node.parent
    parts.reverse()
    return ".".join(parts)


class GherkinTestModule(pytest.Module):
    """
    A pytest collector made for gherkin .scenario files.

    While collecting, it generate ast code to run tests using the python runtime.

    :param path: test root directory.
    :param tursu: the tursu registry to register steps.
    :param **kwargs: pytest extra parameters.
    """

    def __init__(
        self,
        path: Path,
        tursu: Tursu,
        parent: pytest.Module | None = None,
        **kwargs: Any,
    ) -> None:
        doc = GherkinDocument.from_file(path)
        self.gherkin_doc = path.name
        assert parent

        self.module_name = build_pkg(parent)
        compiler = GherkinCompiler(doc, tursu, self.module_name)
        self.test_mod = case = compiler.to_module()

        self.test_casefile = path.parent / case.filename
        super().__init__(path=self.test_casefile, parent=parent, **kwargs)
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
        """Convert the scenario to a python module."""
        return self.test_mod.to_python_module()

    def __repr__(self) -> str:
        return f"<GherkinDocument {self.gherkin_doc}>"

    def collect(self) -> Iterable[pytest.Item | pytest.Collector]:
        """Will collect the scenario as an AST generated module."""
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
