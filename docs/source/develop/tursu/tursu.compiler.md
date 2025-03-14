# {py:mod}`tursu.compiler`

```{py:module} tursu.compiler
```

```{autodoc2-docstring} tursu.compiler
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`GherkinCompiler <tursu.compiler.GherkinCompiler>`
  - ```{autodoc2-docstring} tursu.compiler.GherkinCompiler
    :parser: myst
    :summary:
    ```
* - {py:obj}`GherkinIterator <tursu.compiler.GherkinIterator>`
  - ```{autodoc2-docstring} tursu.compiler.GherkinIterator
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`is_step_keyword <tursu.compiler.is_step_keyword>`
  - ```{autodoc2-docstring} tursu.compiler.is_step_keyword
    :parser: myst
    :summary:
    ```
* - {py:obj}`repr_stack <tursu.compiler.repr_stack>`
  - ```{autodoc2-docstring} tursu.compiler.repr_stack
    :parser: myst
    :summary:
    ```
* - {py:obj}`sanitize <tursu.compiler.sanitize>`
  - ```{autodoc2-docstring} tursu.compiler.sanitize
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} GherkinCompiler(doc: tursu.domain.model.gherkin.GherkinDocument, registry: tursu.registry.Tursu)
:canonical: tursu.compiler.GherkinCompiler

```{autodoc2-docstring} tursu.compiler.GherkinCompiler
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.compiler.GherkinCompiler.__init__
:parser: myst
```

````{py:method} build_args(fixtures: dict[str, typing.Any], examples_keys: list[typing.Any] | None = None) -> list[ast.arg]
:canonical: tursu.compiler.GherkinCompiler.build_args

```{autodoc2-docstring} tursu.compiler.GherkinCompiler.build_args
:parser: myst
```

````

````{py:method} build_fixtures(steps: list[tursu.domain.model.gherkin.GherkinStep]) -> dict[str, type]
:canonical: tursu.compiler.GherkinCompiler.build_fixtures

```{autodoc2-docstring} tursu.compiler.GherkinCompiler.build_fixtures
:parser: myst
```

````

````{py:method} build_tags_decorators(stack: list[typing.Any]) -> list[ast.expr]
:canonical: tursu.compiler.GherkinCompiler.build_tags_decorators

```{autodoc2-docstring} tursu.compiler.GherkinCompiler.build_tags_decorators
:parser: myst
```

````

````{py:method} create_test_function(id: str, name: str, args: list[ast.arg], docstring: str, location: tursu.domain.model.gherkin.GherkinLocation, decorator_list: list[ast.expr], stack: list[typing.Any]) -> tuple[ast.FunctionDef, list[ast.stmt]]
:canonical: tursu.compiler.GherkinCompiler.create_test_function

```{autodoc2-docstring} tursu.compiler.GherkinCompiler.create_test_function
:parser: myst
```

````

````{py:attribute} feat_idx
:canonical: tursu.compiler.GherkinCompiler.feat_idx
:value: >
   1

```{autodoc2-docstring} tursu.compiler.GherkinCompiler.feat_idx
:parser: myst
```

````

````{py:method} get_tags(stack: list[typing.Any]) -> set[str]
:canonical: tursu.compiler.GherkinCompiler.get_tags

```{autodoc2-docstring} tursu.compiler.GherkinCompiler.get_tags
:parser: myst
```

````

````{py:method} to_module() -> tursu.domain.model.testmod.TestModule
:canonical: tursu.compiler.GherkinCompiler.to_module

```{autodoc2-docstring} tursu.compiler.GherkinCompiler.to_module
:parser: myst
```

````

`````

`````{py:class} GherkinIterator(doc: tursu.domain.model.gherkin.GherkinDocument)
:canonical: tursu.compiler.GherkinIterator

```{autodoc2-docstring} tursu.compiler.GherkinIterator
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.compiler.GherkinIterator.__init__
:parser: myst
```

````{py:method} emit() -> collections.abc.Iterator[typing.Any]
:canonical: tursu.compiler.GherkinIterator.emit

```{autodoc2-docstring} tursu.compiler.GherkinIterator.emit
:parser: myst
```

````

````{py:method} emit_feature(feature: tursu.domain.model.gherkin.GherkinFeature) -> collections.abc.Iterator[typing.Any]
:canonical: tursu.compiler.GherkinIterator.emit_feature

```{autodoc2-docstring} tursu.compiler.GherkinIterator.emit_feature
:parser: myst
```

````

````{py:method} emit_feature_from_enveloppe(enveloppe: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinEnvelope]) -> collections.abc.Iterator[typing.Any]
:canonical: tursu.compiler.GherkinIterator.emit_feature_from_enveloppe

```{autodoc2-docstring} tursu.compiler.GherkinIterator.emit_feature_from_enveloppe
:parser: myst
```

````

````{py:method} emit_scenario(scenario: tursu.domain.model.gherkin.GherkinScenario | tursu.domain.model.gherkin.GherkinScenarioOutline) -> collections.abc.Iterator[typing.Any]
:canonical: tursu.compiler.GherkinIterator.emit_scenario

```{autodoc2-docstring} tursu.compiler.GherkinIterator.emit_scenario
:parser: myst
```

````

`````

````{py:function} is_step_keyword(value: tursu.domain.model.gherkin.GherkinKeyword) -> typing.TypeGuard[tursu.steps.StepKeyword]
:canonical: tursu.compiler.is_step_keyword

```{autodoc2-docstring} tursu.compiler.is_step_keyword
:parser: myst
```
````

````{py:function} repr_stack(stack: list[typing.Any]) -> list[str]
:canonical: tursu.compiler.repr_stack

```{autodoc2-docstring} tursu.compiler.repr_stack
:parser: myst
```
````

````{py:function} sanitize(name: str) -> str
:canonical: tursu.compiler.sanitize

```{autodoc2-docstring} tursu.compiler.sanitize
:parser: myst
```
````
