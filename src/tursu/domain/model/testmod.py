"""Test module."""

import ast
import atexit
from pathlib import Path
from types import CodeType, ModuleType


class TestModule:
    """
    AST representation of a scenario.

    :param scenario: the scenario name representated.
    :param module_node: the AST generated code by the compiler of the scenario.
    """

    def __init__(self, scenario: str, module_node: ast.Module) -> None:
        self.scenario = scenario
        self.module_node = module_node

    def __str__(self) -> str:
        return ast.unparse(self.module_node)

    __repr__ = __str__

    @property
    def filename(self) -> str:
        """
        A python test file name used if we wrote the file to the disk.

        Test module are generated in memory, but, while using `--trace`
        tursu write the file to the disk in order to have steps in pdb.

        They are also writen with option `-vvv` in order to have the full traceback.
        """
        return f"test_{self.scenario}.py"

    @property
    def modname(self) -> str:
        """Name of the python module."""
        return self.filename[:-3]

    def compile(self) -> CodeType:
        """Compile ast code to python bytecode."""
        return compile(
            ast.unparse(self.module_node), filename=self.filename, mode="exec"
        )

    def to_python_module(self) -> ModuleType:
        """Generate a python module."""
        mod = ModuleType(self.modname)
        exec(self.compile(), mod.__dict__)
        return mod

    def write_temporary(self, parent: Path) -> None:
        """
        Temporary write the module on the disk. used while tracing to get debug step.
        """
        test_casefile = parent / self.filename
        test_casefile.write_text(str(self), encoding="utf-8")

        def delete_temporary_files() -> None:
            if hasattr(test_casefile, "unlink"):  # coverage: ignore
                test_casefile.unlink(missing_ok=True)  # coverage: ignore

        atexit.register(delete_temporary_files)
