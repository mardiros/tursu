# {py:mod}`tursu.service.ast.astfunction`

```{py:module} tursu.service.ast.astfunction
```

```{autodoc2-docstring} tursu.service.ast.astfunction
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TestFunctionWriter <tursu.service.ast.astfunction.TestFunctionWriter>`
  - ```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`is_step_keyword <tursu.service.ast.astfunction.is_step_keyword>`
  - ```{autodoc2-docstring} tursu.service.ast.astfunction.is_step_keyword
    :parser: myst
    :summary:
    ```
* - {py:obj}`repr_stack <tursu.service.ast.astfunction.repr_stack>`
  - ```{autodoc2-docstring} tursu.service.ast.astfunction.repr_stack
    :parser: myst
    :summary:
    ```
* - {py:obj}`sanitize <tursu.service.ast.astfunction.sanitize>`
  - ```{autodoc2-docstring} tursu.service.ast.astfunction.sanitize
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} TestFunctionWriter(scenario: tursu.domain.model.gherkin.GherkinScenario | tursu.domain.model.gherkin.GherkinScenarioOutline, registry: tursu.runtime.registry.Tursu, steps: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinStep], stack: collections.abc.Sequence[typing.Any], package_name: str, examples: tursu.domain.model.gherkin.GherkinExamples | None = None)
:canonical: tursu.service.ast.astfunction.TestFunctionWriter

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.__init__
:parser: myst
```

````{py:method} add_step(stp: tursu.domain.model.gherkin.GherkinStep, stack: list[typing.Any], examples: tursu.domain.model.gherkin.GherkinExamples | None = None) -> None
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.add_step

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.add_step
:parser: myst
```

````

````{py:method} build_args(fixtures: collections.abc.Mapping[str, typing.Any], examples_keys: collections.abc.Sequence[typing.Any] | None = None) -> list[ast.arg]
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.build_args

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.build_args
:parser: myst
```

````

````{py:method} build_fixtures(steps: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinStep], registry: tursu.runtime.registry.Tursu) -> dict[str, type]
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.build_fixtures

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.build_fixtures
:parser: myst
```

````

````{py:method} build_step_args(step_keyword: tursu.domain.model.steps.StepKeyword, stp: tursu.domain.model.gherkin.GherkinStep, examples: tursu.domain.model.gherkin.GherkinExamples | None = None) -> list[ast.expr]
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.build_step_args

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.build_step_args
:parser: myst
```

````

````{py:method} build_step_kwargs(step_keyword: tursu.domain.model.steps.StepKeyword, stp: tursu.domain.model.gherkin.GherkinStep, examples: tursu.domain.model.gherkin.GherkinExamples | None = None) -> list[ast.keyword]
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.build_step_kwargs

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.build_step_kwargs
:parser: myst
```

````

````{py:method} build_tags_decorators(stack: collections.abc.Sequence[typing.Any]) -> list[ast.expr]
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.build_tags_decorators

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.build_tags_decorators
:parser: myst
```

````

````{py:method} get_keyword(stp: tursu.domain.model.gherkin.GherkinStep) -> tursu.domain.model.steps.StepKeyword
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.get_keyword

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.get_keyword
:parser: myst
```

````

````{py:method} get_tags(stack: collections.abc.Sequence[typing.Any]) -> set[str]
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.get_tags

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.get_tags
:parser: myst
```

````

````{py:method} parse_data_table(step_keyword: tursu.domain.model.steps.StepKeyword, stp: tursu.domain.model.gherkin.GherkinStep, examples: tursu.domain.model.gherkin.GherkinExamples | None = None) -> ast.keyword
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.parse_data_table

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.parse_data_table
:parser: myst
```

````

````{py:method} parse_doc_string(step_keyword: tursu.domain.model.steps.StepKeyword, stp: tursu.domain.model.gherkin.GherkinStep) -> ast.keyword
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.parse_doc_string

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.parse_doc_string
:parser: myst
```

````

````{py:method} to_ast() -> ast.FunctionDef | ast.AsyncFunctionDef
:canonical: tursu.service.ast.astfunction.TestFunctionWriter.to_ast

```{autodoc2-docstring} tursu.service.ast.astfunction.TestFunctionWriter.to_ast
:parser: myst
```

````

`````

````{py:function} is_step_keyword(value: tursu.domain.model.gherkin.GherkinKeyword) -> typing.TypeGuard[tursu.domain.model.steps.StepKeyword]
:canonical: tursu.service.ast.astfunction.is_step_keyword

```{autodoc2-docstring} tursu.service.ast.astfunction.is_step_keyword
:parser: myst
```
````

````{py:function} repr_stack(stack: collections.abc.Sequence[typing.Any]) -> collections.abc.Sequence[str]
:canonical: tursu.service.ast.astfunction.repr_stack

```{autodoc2-docstring} tursu.service.ast.astfunction.repr_stack
:parser: myst
```
````

````{py:function} sanitize(name: str) -> str
:canonical: tursu.service.ast.astfunction.sanitize

```{autodoc2-docstring} tursu.service.ast.astfunction.sanitize
:parser: myst
```
````
