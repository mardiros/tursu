# {py:mod}`tursu.service.compiler`

```{py:module} tursu.service.compiler
```

```{autodoc2-docstring} tursu.service.compiler
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`GherkinCompiler <tursu.service.compiler.GherkinCompiler>`
  - ```{autodoc2-docstring} tursu.service.compiler.GherkinCompiler
    :parser: myst
    :summary:
    ```
* - {py:obj}`GherkinIterator <tursu.service.compiler.GherkinIterator>`
  - ```{autodoc2-docstring} tursu.service.compiler.GherkinIterator
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} GherkinCompiler(doc: tursu.domain.model.gherkin.GherkinDocument, registry: tursu.runtime.registry.Tursu)
:canonical: tursu.service.compiler.GherkinCompiler

```{autodoc2-docstring} tursu.service.compiler.GherkinCompiler
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.service.compiler.GherkinCompiler.__init__
:parser: myst
```

````{py:attribute} feat_idx
:canonical: tursu.service.compiler.GherkinCompiler.feat_idx
:value: >
   1

```{autodoc2-docstring} tursu.service.compiler.GherkinCompiler.feat_idx
:parser: myst
```

````

````{py:method} to_module() -> tursu.domain.model.testmod.TestModule
:canonical: tursu.service.compiler.GherkinCompiler.to_module

```{autodoc2-docstring} tursu.service.compiler.GherkinCompiler.to_module
:parser: myst
```

````

`````

`````{py:class} GherkinIterator(doc: tursu.domain.model.gherkin.GherkinDocument)
:canonical: tursu.service.compiler.GherkinIterator

```{autodoc2-docstring} tursu.service.compiler.GherkinIterator
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.service.compiler.GherkinIterator.__init__
:parser: myst
```

````{py:method} emit() -> collections.abc.Iterator[typing.Any]
:canonical: tursu.service.compiler.GherkinIterator.emit

```{autodoc2-docstring} tursu.service.compiler.GherkinIterator.emit
:parser: myst
```

````

````{py:method} emit_feature(feature: tursu.domain.model.gherkin.GherkinFeature) -> collections.abc.Iterator[typing.Any]
:canonical: tursu.service.compiler.GherkinIterator.emit_feature

```{autodoc2-docstring} tursu.service.compiler.GherkinIterator.emit_feature
:parser: myst
```

````

````{py:method} emit_feature_from_enveloppe(enveloppe: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinEnvelope]) -> collections.abc.Iterator[typing.Any]
:canonical: tursu.service.compiler.GherkinIterator.emit_feature_from_enveloppe

```{autodoc2-docstring} tursu.service.compiler.GherkinIterator.emit_feature_from_enveloppe
:parser: myst
```

````

````{py:method} emit_scenario(scenario: tursu.domain.model.gherkin.GherkinScenario | tursu.domain.model.gherkin.GherkinScenarioOutline) -> collections.abc.Iterator[typing.Any]
:canonical: tursu.service.compiler.GherkinIterator.emit_scenario

```{autodoc2-docstring} tursu.service.compiler.GherkinIterator.emit_scenario
:parser: myst
```

````

`````
