# {py:mod}`tursu.registry`

```{py:module} tursu.registry
```

```{autodoc2-docstring} tursu.registry
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Tursu <tursu.registry.Tursu>`
  - ```{autodoc2-docstring} tursu.registry.Tursu
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`given <tursu.registry.given>`
  - ```{autodoc2-docstring} tursu.registry.given
    :parser: myst
    :summary:
    ```
* - {py:obj}`then <tursu.registry.then>`
  - ```{autodoc2-docstring} tursu.registry.then
    :parser: myst
    :summary:
    ```
* - {py:obj}`when <tursu.registry.when>`
  - ```{autodoc2-docstring} tursu.registry.when
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`VENUSIAN_CATEGORY <tursu.registry.VENUSIAN_CATEGORY>`
  - ```{autodoc2-docstring} tursu.registry.VENUSIAN_CATEGORY
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} Tursu()
:canonical: tursu.registry.Tursu

```{autodoc2-docstring} tursu.registry.Tursu
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.registry.Tursu.__init__
:parser: myst
```

````{py:method} extract_fixtures(step: tursu.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> collections.abc.Mapping[str, typing_extensions.Any]
:canonical: tursu.registry.Tursu.extract_fixtures

```{autodoc2-docstring} tursu.registry.Tursu.extract_fixtures
:parser: myst
```

````

````{py:method} register_handler(type: tursu.steps.StepKeyword, pattern: str | tursu.pattern_matcher.AbstractPattern, handler: tursu.steps.Handler) -> None
:canonical: tursu.registry.Tursu.register_handler

```{autodoc2-docstring} tursu.registry.Tursu.register_handler
:parser: myst
```

````

````{py:method} run_step(tursu_runner: tursu.runner.TursuRunner, step: tursu.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> None
:canonical: tursu.registry.Tursu.run_step

```{autodoc2-docstring} tursu.registry.Tursu.run_step
:parser: myst
```

````

````{py:method} scan(mod: types.ModuleType | None = None) -> tursu.registry.Tursu
:canonical: tursu.registry.Tursu.scan

```{autodoc2-docstring} tursu.registry.Tursu.scan
:parser: myst
```

````

`````

````{py:data} VENUSIAN_CATEGORY
:canonical: tursu.registry.VENUSIAN_CATEGORY
:value: >
   'tursu'

```{autodoc2-docstring} tursu.registry.VENUSIAN_CATEGORY
:parser: myst
```

````

````{py:function} given(pattern: str | tursu.pattern_matcher.AbstractPattern) -> typing.Callable[[tursu.steps.Handler], tursu.steps.Handler]
:canonical: tursu.registry.given

```{autodoc2-docstring} tursu.registry.given
:parser: myst
```
````

````{py:function} then(pattern: str | tursu.pattern_matcher.AbstractPattern) -> typing.Callable[[tursu.steps.Handler], tursu.steps.Handler]
:canonical: tursu.registry.then

```{autodoc2-docstring} tursu.registry.then
:parser: myst
```
````

````{py:function} when(pattern: str | tursu.pattern_matcher.AbstractPattern) -> typing.Callable[[tursu.steps.Handler], tursu.steps.Handler]
:canonical: tursu.registry.when

```{autodoc2-docstring} tursu.registry.when
:parser: myst
```
````
