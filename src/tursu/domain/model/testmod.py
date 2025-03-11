import ast


class TestModule:
    def __init__(self, filename: str, module_node: ast.Module):
        self.filename = filename
        self.module_node = module_node

    def __str__(self) -> str:
        return ast.unparse(self.module_node)

    __repr__ = __str__
