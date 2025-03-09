import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

DEFAULT_INIT = """\
from tursu import generate_tests

generate_tests()
"""

DEFAULT_CONFTEST = """\
import pytest

from tursu.registry import StepRegistry


@pytest.fixture()
def registry() -> StepRegistry:
    return StepRegistry().scan()
"""


def init(outdir: str, overwrite: bool) -> None:
    outpath = Path(outdir)
    if outpath.exists() and not overwrite:
        print(f"{outdir} already exists")
        sys.exit(1)

    if outpath.is_file():
        outpath.unlink()

    outpath.mkdir(exist_ok=True)
    (outpath / "__init__.py").write_text(DEFAULT_INIT)
    (outpath / "conftest.py").write_text(DEFAULT_CONFTEST)


def main(args: Sequence[str] = sys.argv) -> None:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title="action", required=True)

    sp_action = subparsers.add_parser("init")
    sp_action.add_argument(
        "-o",
        "--out-dir",
        dest="outdir",
        default="tests/functionals",
        help="Directory where the handlers will be generated",
    )
    sp_action.add_argument(
        "--overwrite", action="store_true", dest="overwrite", default=False
    )

    sp_action.set_defaults(handler=init)
    kwargs = parser.parse_args(args[1:])
    kwargs_dict = vars(kwargs)

    handler = kwargs_dict.pop("handler")
    handler(**kwargs_dict)
