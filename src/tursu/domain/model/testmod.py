import ast
from types import CodeType


class TestModule:
    def __init__(self, filename: str, module_node: ast.Module):
        self.filename = filename
        self.module_node = module_node

    @property
    def modname(self) -> str:
        return self.filename[:-3]

    def compile(self) -> CodeType:
        return compile(
            ast.unparse(self.module_node), filename=self.filename, mode="exec"
        )

    def __str__(self) -> str:
        return ast.unparse(self.module_node)

    __repr__ = __str__
