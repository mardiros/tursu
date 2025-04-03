"""AST helpers at the test module level."""

import ast
from collections.abc import Sequence
from typing import Any

from tursu.domain.model.gherkin import GherkinFeature
from tursu.runtime.registry import Tursu
from tursu.service.ast.astfunction import TestFunctionWriter


class TestModuleWriter:
    """
    Prepare a python test module for the given feature.

    :param feature: the feature that will be compiled to a python module.
    :param registry: tursu registry containing the steps definition.
    :param stack: current stack of the gherkin document traversal.
    """

    def __init__(
        self,
        feature: GherkinFeature,
        registry: Tursu,
        stack: Sequence[Any],
        package_name: str,
    ) -> None:
        self.feature = feature
        self.fixtures: dict[str, type] = {}
        self.registry = registry

        self.package_name = package_name
        self.module_name = stack[0].name
        self.tests_fn: list[ast.stmt] = []

    def append_fixtures(self, fixtures: dict[str, type]) -> None:
        self.fixtures.update(fixtures)

    def import_stmt(self) -> list[ast.stmt]:
        import_mods: list[ast.stmt] = [
            ast.Expr(
                value=ast.Constant(
                    f"{self.feature.name}\n\n{self.feature.description}".strip(),
                    lineno=1,
                )
            ),
            ast.ImportFrom(
                module="typing",
                names=[ast.alias(name="Any", asname=None)],
                level=0,
            ),
            ast.Import(names=[ast.alias(name="pytest", asname=None)]),
            ast.ImportFrom(
                module="tursu.runtime.registry",
                names=[
                    ast.alias(name="Tursu", asname=None),
                ],
                level=0,
            ),
            ast.ImportFrom(
                module="tursu.runtime.runner",
                names=[
                    ast.alias(name="TursuRunner", asname=None),
                ],
                level=0,
            ),
        ]
        for typ, alias in self.registry.get_models_types(self.package_name).items():
            import_mods.append(
                ast.ImportFrom(
                    module=typ.__module__,
                    names=[
                        ast.alias(name=typ.__name__, asname=alias),
                    ],
                    level=0,
                )
            )

        fixtures = self.registry.get_fixtures(self.package_name)

        for key, _typ in self.fixtures.items():
            # register fixture that are declared with their step definition
            if key in fixtures:
                import_mods.append(
                    ast.ImportFrom(
                        module=fixtures[key].__module__,
                        names=[
                            ast.alias(name=fixtures[key].__name__),
                        ],
                        level=0,
                    )
                )
            # we may import the type and type it in the ast function.

        return import_mods

    def append_test(self, fn: TestFunctionWriter) -> None:
        """Append a test function to the module."""
        self.tests_fn.append(fn.to_ast())

    def to_ast(self) -> ast.Module:
        """Convert the current state to ast code."""
        return ast.Module(
            body=self.import_stmt() + self.tests_fn,
            type_ignores=[],
        )
