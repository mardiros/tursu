from pathlib import Path
from typing import Any

import pytest

from tursu.entrypoints.cli import main


def test_main_exists(tmp_path: Path, capsys: Any):
    with pytest.raises(SystemExit) as exc_info:
        main(["tursu", "init", "-o", str(tmp_path)])
    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert captured.out.strip() == f"{tmp_path} already exists"


def test_main(tmp_path: Path):
    main(["tursu", "init", "-o", str(tmp_path), "--overwrite"])
    files = {f.name: f.read_text() for f in tmp_path.glob("**/*.py")}
    assert set(files.keys()) == {"__init__.py", "conftest.py", "steps.py"}


def test_main_replace_file(tmp_path: Path):
    (tmp_path / "tursu").write_text("dummy")
    main(["tursu", "init", "-o", str(tmp_path / "tursu"), "--overwrite"])
    files = {f.name: f.read_text() for f in tmp_path.glob("tursu/*.py")}
    assert set(files.keys()) == {"__init__.py"}
    files = {f.name: f.read_text() for f in tmp_path.glob("tursu/functionals/*.py")}
    assert set(files.keys()) == {"__init__.py", "conftest.py", "steps.py"}


def test_main_no_dummies(tmp_path: Path):
    main(["tursu", "init", "-o", str(tmp_path / "tursu"), "--no-dummies"])
    files = {f.name: f.read_text() for f in tmp_path.glob("tursu/functionals/*.py")}
    assert set(files.keys()) == {"__init__.py", "conftest.py"}
