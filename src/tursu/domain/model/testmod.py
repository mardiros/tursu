import ast


class TestModule:
    def __init__(self, scenario: str, module_node: ast.Module):
        self.scenario = scenario
        self.module_node = module_node

    def __str__(self) -> str:
        return ast.unparse(self.module_node)

    @property
    def filename(self) -> str:
        return f"test_{self.scenario}.py"

    __repr__ = __str__
