import textwrap
from pathlib import Path
from typing import Any

import pytest

from tursu.entrypoints.cli import main


def test_main_exists(tmp_path: Path, capsys: Any):
    (tmp_path / "functionals").mkdir()
    with pytest.raises(SystemExit) as exc_info:
        main(["tursu", "init", "-o", str(tmp_path)])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.err.strip() == f"{tmp_path} already exists"


def test_main(tmp_path: Path):
    main(["tursu", "init", "-o", str(tmp_path), "--overwrite"])
    files = {f.name: f.read_text() for f in tmp_path.glob("**/*.py")}
    assert set(files.keys()) == {"__init__.py", "conftest.py", "steps.py"}


def test_main_replace__init__(tmp_path: Path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "__init__.py").write_text("# dummy")
    main(["tursu", "init", "-o", str(tmp_path / "tests"), "--overwrite"])
    assert (tmp_path / "tests" / "__init__.py").read_text() == textwrap.dedent("""\
        import pytest

        pytest.register_assert_rewrite("tests.functionals")
        """)


def test_main_ignore__init__(tmp_path: Path, capsys: Any):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "__init__.py").write_text("# dummy")
    main(["tursu", "init", "-o", str(tmp_path / "tests")])
    assert (tmp_path / "tests" / "__init__.py").write_text("# dummy")
    captured = capsys.readouterr()

    assert captured.err == textwrap.dedent(f"""\
        {(tmp_path / "tests" / "__init__.py")} exists, stay intact.
        Manually add the following instruction to get pytest assertion on step files:

            import pytest

            pytest.register_assert_rewrite("tests.functionals")


        """)


def test_main_replace_file(tmp_path: Path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "functionals").write_text("dummy")
    main(["tursu", "init", "-o", str(tmp_path / "tests"), "--overwrite"])
    files = {f.name: f.read_text() for f in tmp_path.glob("tests/*.py")}
    assert set(files.keys()) == {"__init__.py"}
    files = {f.name: f.read_text() for f in tmp_path.glob("tests/functionals/*.py")}
    assert set(files.keys()) == {"__init__.py", "conftest.py", "steps.py"}


def test_main_no_dummies(tmp_path: Path):
    main(["tursu", "init", "-o", str(tmp_path / "tursu"), "--no-dummies"])
    files = {f.name: f.read_text() for f in tmp_path.glob("tursu/functionals/*.py")}
    assert set(files.keys()) == {"__init__.py", "conftest.py"}
