# {py:mod}`tursu.service.ast.astmodule`

```{py:module} tursu.service.ast.astmodule
```

```{autodoc2-docstring} tursu.service.ast.astmodule
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TestModuleWriter <tursu.service.ast.astmodule.TestModuleWriter>`
  - ```{autodoc2-docstring} tursu.service.ast.astmodule.TestModuleWriter
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} TestModuleWriter(feature: tursu.domain.model.gherkin.GherkinFeature, registry: tursu.runtime.registry.Tursu, stack: collections.abc.Sequence[typing.Any])
:canonical: tursu.service.ast.astmodule.TestModuleWriter

```{autodoc2-docstring} tursu.service.ast.astmodule.TestModuleWriter
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.service.ast.astmodule.TestModuleWriter.__init__
:parser: myst
```

````{py:method} append_test(fn: tursu.service.ast.astfunction.TestFunctionWriter) -> None
:canonical: tursu.service.ast.astmodule.TestModuleWriter.append_test

```{autodoc2-docstring} tursu.service.ast.astmodule.TestModuleWriter.append_test
:parser: myst
```

````

````{py:method} to_ast() -> ast.Module
:canonical: tursu.service.ast.astmodule.TestModuleWriter.to_ast

```{autodoc2-docstring} tursu.service.ast.astmodule.TestModuleWriter.to_ast
:parser: myst
```

````

`````
