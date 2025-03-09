from pathlib import Path

import pytest

from tursu.entrypoint import main


def test_main_exists(tmp_path: Path):
    with pytest.raises(SystemExit) as exc_info:
        main(["tursu", "init", "-o", str(tmp_path)])
    assert exc_info.value.code == 1


def test_main(tmp_path: Path):
    main(["tursu", "init", "-o", str(tmp_path), "--overwrite"])
    files = {f.name: f.read_text() for f in tmp_path.glob("**/*.py")}
    assert set(files.keys()) == {"__init__.py", "conftest.py"}


def test_main_replace_file(tmp_path: Path):
    (tmp_path / "tursu").write_text("dummy")
    main(["tursu", "init", "-o", str(tmp_path / "tursu"), "--overwrite"])
    files = {f.name: f.read_text() for f in tmp_path.glob("tursu/*.py")}
    assert set(files.keys()) == {"__init__.py", "conftest.py"}
