import ast
from types import CodeType, ModuleType


class TestModule:
    def __init__(self, scenario: str, module_node: ast.Module) -> None:
        self.scenario = scenario
        self.module_node = module_node

    def __str__(self) -> str:
        return ast.unparse(self.module_node)

    __repr__ = __str__

    @property
    def filename(self) -> str:
        return f"test_{self.scenario}.py"

    @property
    def modname(self) -> str:
        return self.filename[:-3]

    def compile(self) -> CodeType:
        return compile(
            ast.unparse(self.module_node), filename=self.filename, mode="exec"
        )

    def to_python_module(self) -> ModuleType:
        mod = ModuleType(self.modname)
        exec(self.compile(), mod.__dict__)
        return mod
