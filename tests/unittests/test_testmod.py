import ast
import textwrap
from pathlib import Path

from tursu.domain.model.testmod import TestModule

module = ast.Module(
    body=[
        ast.FunctionDef(
            name="hello_world",
            args=ast.arguments(
                args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None
            ),
            body=[
                ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id="print", ctx=ast.Load()),
                        args=[ast.Str(s="Hello, World!")],
                        keywords=[],
                    )
                )
            ],
            decorator_list=[],
            lineno=1,
        )
    ],
    type_ignores=[],
)


def test_testmodule(tmpdir: Path):
    tmod = TestModule("dummy", module)
    tmod.write_temporary(tmpdir)
    assert (tmpdir / tmod.filename).read_text(encoding="utf-8") == textwrap.dedent(
        """\
        def hello_world():
            print('Hello, World!')
        """
    ).strip()
