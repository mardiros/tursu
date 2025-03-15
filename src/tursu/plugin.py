import atexit
import inspect
import sys
from collections.abc import Iterable
from pathlib import Path
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
    def __init__(self, path: Path, **kwargs: Any) -> None:
        doc = GherkinDocument.from_file(path)
        self.gherkin_doc = path.name
        compiler = GherkinCompiler(doc, _tursu)
        case = compiler.to_module()

        test_casefile = path.parent / case.filename
        test_casefile.write_text(str(case))
        atexit.register(lambda: test_casefile.unlink(missing_ok=True))

        super().__init__(path=test_casefile, **kwargs)

    def __repr__(self) -> str:
        return f"<GherkinDocument {self.gherkin_doc}>"

    def collect(self) -> Iterable[pytest.Item | pytest.Collector]:
        ret = super().collect()
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
            ret = GherkinTestModule.from_parent(parent, path=file_path, name=doc.name)
            return ret

    conftest_mod.pytest_collect_file = pytest_collect_file  # type: ignore
