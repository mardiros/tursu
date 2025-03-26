import ast
from collections.abc import Sequence
from typing import Any

from tursu.domain.model.gherkin import GherkinFeature
from tursu.registry import Tursu
from tursu.service.ast.astfunction import TestFunctionWriter


class TestModuleWriter:
    def __init__(
        self, feature: GherkinFeature, registry: Tursu, stack: Sequence[Any]
    ) -> None:
        import_mods: list[ast.stmt] = [
            ast.Expr(
                value=ast.Constant(
                    f"{feature.name}\n\n{feature.description}".strip(), lineno=1
                )
            ),
            ast.ImportFrom(
                module="typing",
                names=[ast.alias(name="Any", asname=None)],
                level=0,
            ),
            ast.Import(names=[ast.alias(name="pytest", asname=None)]),
            ast.ImportFrom(
                module="tursu.registry",
                names=[
                    ast.alias(name="Tursu", asname=None),
                ],
                level=0,
            ),
            ast.ImportFrom(
                module="tursu.runner",
                names=[
                    ast.alias(name="TursuRunner", asname=None),
                ],
                level=0,
            ),
        ]
        for typ, alias in registry.data_tables_types.items():
            import_mods.append(
                ast.ImportFrom(
                    module=typ.__module__,
                    names=[
                        ast.alias(name=typ.__qualname__, asname=alias),
                    ],
                    level=0,
                )
            )

        self.module_name = stack[0].name
        self.module_node = ast.Module(
            body=import_mods,
            type_ignores=[],
        )

    def append_test(self, fn: TestFunctionWriter) -> None:
        self.module_node.body.append(fn.to_ast())

    def to_ast(self) -> ast.Module:
        return self.module_node
