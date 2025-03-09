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
* - {py:obj}`sanitize <tursu.compiler.sanitize>`
  - ```{autodoc2-docstring} tursu.compiler.sanitize
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} GherkinCompiler(doc: tursu.domain.model.gherkin.GherkinDocument, registry: tursu.registry.StepRegistry)
:canonical: tursu.compiler.GherkinCompiler

```{autodoc2-docstring} tursu.compiler.GherkinCompiler
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.compiler.GherkinCompiler.__init__
:parser: myst
```

````{py:attribute} feat_idx
:canonical: tursu.compiler.GherkinCompiler.feat_idx
:value: >
   1

```{autodoc2-docstring} tursu.compiler.GherkinCompiler.feat_idx
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

````{py:method} emit_scenario(scenario: tursu.domain.model.gherkin.GherkinScenario) -> collections.abc.Iterator[typing.Any]
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

````{py:function} sanitize(name: str) -> str
:canonical: tursu.compiler.sanitize

```{autodoc2-docstring} tursu.compiler.sanitize
:parser: myst
```
````
