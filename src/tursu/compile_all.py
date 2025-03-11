import atexit
import inspect
from collections.abc import Iterator
from pathlib import Path

from tursu.compiler import GherkinCompiler
from tursu.domain.model.gherkin import GherkinDocument
from tursu.registry import Tursu


def walk_features(path: Path) -> Iterator[GherkinDocument]:
    for sub in path.glob("**/*.feature"):
        yield GherkinDocument.from_file(sub)


def generate_tests() -> None:
    """
    Generate the test suite.

    To run functional tests of your own, this function has to be added
    in the `__init__.py` file of the tests directory.

    ```python
    from tursu import generate_tests

    generate_tests()
    ```
    """
    caller_module = inspect.getmodule(inspect.stack()[1][0])
    assert caller_module
    assert caller_module.__file__

    reg = Tursu()
    reg.scan(caller_module)

    to_removes: list[Path] = []
    for doc in walk_features(Path(caller_module.__file__).parent):
        compiler = GherkinCompiler(doc, reg)

        case = compiler.to_module()
        casefile = doc.filepath.parent / case.filename
        casefile.write_text(str(case))
        to_removes.append(casefile)

    def clean_up() -> None:
        for r in to_removes:
            r.unlink()

    atexit.register(clean_up)
