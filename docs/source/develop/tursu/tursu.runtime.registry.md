# {py:mod}`tursu.runtime.registry`

```{py:module} tursu.runtime.registry
```

```{autodoc2-docstring} tursu.runtime.registry
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Tursu <tursu.runtime.registry.Tursu>`
  - ```{autodoc2-docstring} tursu.runtime.registry.Tursu
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`given <tursu.runtime.registry.given>`
  - ```{autodoc2-docstring} tursu.runtime.registry.given
    :parser: myst
    :summary:
    ```
* - {py:obj}`then <tursu.runtime.registry.then>`
  - ```{autodoc2-docstring} tursu.runtime.registry.then
    :parser: myst
    :summary:
    ```
* - {py:obj}`when <tursu.runtime.registry.when>`
  - ```{autodoc2-docstring} tursu.runtime.registry.when
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`VENUSIAN_CATEGORY <tursu.runtime.registry.VENUSIAN_CATEGORY>`
  - ```{autodoc2-docstring} tursu.runtime.registry.VENUSIAN_CATEGORY
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} Tursu()
:canonical: tursu.runtime.registry.Tursu

```{autodoc2-docstring} tursu.runtime.registry.Tursu
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.registry.Tursu.__init__
:parser: myst
```

````{py:attribute} DATA_TABLE_EMPTY_CELL
:canonical: tursu.runtime.registry.Tursu.DATA_TABLE_EMPTY_CELL
:value: <Multiline-String>

```{autodoc2-docstring} tursu.runtime.registry.Tursu.DATA_TABLE_EMPTY_CELL
:parser: myst
```

````

````{py:property} models_types
:canonical: tursu.runtime.registry.Tursu.models_types
:type: dict[type, str]

```{autodoc2-docstring} tursu.runtime.registry.Tursu.models_types
:parser: myst
```

````

````{py:method} extract_fixtures(step: tursu.domain.model.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> collections.abc.Mapping[str, typing_extensions.Any]
:canonical: tursu.runtime.registry.Tursu.extract_fixtures

```{autodoc2-docstring} tursu.runtime.registry.Tursu.extract_fixtures
:parser: myst
```

````

````{py:method} get_step(step: tursu.domain.model.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> tursu.domain.model.steps.Step | None
:canonical: tursu.runtime.registry.Tursu.get_step

```{autodoc2-docstring} tursu.runtime.registry.Tursu.get_step
:parser: myst
```

````

````{py:method} register_data_table(step: tursu.domain.model.steps.Step) -> None
:canonical: tursu.runtime.registry.Tursu.register_data_table

```{autodoc2-docstring} tursu.runtime.registry.Tursu.register_data_table
:parser: myst
```

````

````{py:method} register_handler(type: tursu.domain.model.steps.StepKeyword, pattern: str | tursu.runtime.pattern_matcher.AbstractPattern, handler: tursu.domain.model.steps.Handler) -> None
:canonical: tursu.runtime.registry.Tursu.register_handler

```{autodoc2-docstring} tursu.runtime.registry.Tursu.register_handler
:parser: myst
```

````

````{py:method} run_step(tursu_runner: tursu.runtime.runner.TursuRunner, step: tursu.domain.model.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> None
:canonical: tursu.runtime.registry.Tursu.run_step

```{autodoc2-docstring} tursu.runtime.registry.Tursu.run_step
:parser: myst
```

````

````{py:method} scan(mod: types.ModuleType | None = None) -> tursu.runtime.registry.Tursu
:canonical: tursu.runtime.registry.Tursu.scan

```{autodoc2-docstring} tursu.runtime.registry.Tursu.scan
:parser: myst
```

````

`````

````{py:data} VENUSIAN_CATEGORY
:canonical: tursu.runtime.registry.VENUSIAN_CATEGORY
:value: >
   'tursu'

```{autodoc2-docstring} tursu.runtime.registry.VENUSIAN_CATEGORY
:parser: myst
```

````

````{py:function} given(pattern: str | tursu.runtime.pattern_matcher.AbstractPattern) -> typing.Callable[[tursu.domain.model.steps.Handler], tursu.domain.model.steps.Handler]
:canonical: tursu.runtime.registry.given

```{autodoc2-docstring} tursu.runtime.registry.given
:parser: myst
```
````

````{py:function} then(pattern: str | tursu.runtime.pattern_matcher.AbstractPattern) -> typing.Callable[[tursu.domain.model.steps.Handler], tursu.domain.model.steps.Handler]
:canonical: tursu.runtime.registry.then

```{autodoc2-docstring} tursu.runtime.registry.then
:parser: myst
```
````

````{py:function} when(pattern: str | tursu.runtime.pattern_matcher.AbstractPattern) -> typing.Callable[[tursu.domain.model.steps.Handler], tursu.domain.model.steps.Handler]
:canonical: tursu.runtime.registry.when

```{autodoc2-docstring} tursu.runtime.registry.when
:parser: myst
```
````
