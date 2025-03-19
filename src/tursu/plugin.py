import atexit
import inspect
import sys
from collections.abc import Iterable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from tursu.compiler import GherkinCompiler
from tursu.domain.model.gherkin import GherkinDocument
from tursu.registry import Tursu

_tursu = Tursu()


@pytest.fixture(scope="session")
def tursu() -> Tursu:
    """The tursu step registry, used to run Gherkin scenario."""
    return _tursu


class GherkinTestModule(pytest.Module):
    def __init__(self, path: Path, tursu: Tursu, **kwargs: Any) -> None:
        doc = GherkinDocument.from_file(path)
        self.gherkin_doc = path.name
        compiler = GherkinCompiler(doc, tursu)
        self.test_mod = case = compiler.to_module()

        self.test_casefile = path.parent / case.filename
        self.test_casefile.write_text(str(case))  # sould be done only if traced
        atexit.register(lambda: self.test_casefile.unlink(missing_ok=True))

        super().__init__(path=self.test_casefile, **kwargs)
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
