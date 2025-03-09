# {py:mod}`tursu`

```{py:module} tursu
```

```{autodoc2-docstring} tursu
:parser: myst
:allowtitles:
```

## Package Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`StepRegistry <tursu.registry.StepRegistry>`
  - ```{autodoc2-docstring} tursu.registry.StepRegistry
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`generate_tests <tursu.compile_all.generate_tests>`
  - ```{autodoc2-docstring} tursu.compile_all.generate_tests
    :parser: myst
    :summary:
    ```
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

### API

`````{py:class} StepRegistry()
:canonical: tursu.registry.StepRegistry

```{autodoc2-docstring} tursu.registry.StepRegistry
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.registry.StepRegistry.__init__
:parser: myst
```

````{py:method} extract_fixtures(step: tursu.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> collections.abc.Mapping[str, typing_extensions.Any]
:canonical: tursu.registry.StepRegistry.extract_fixtures

```{autodoc2-docstring} tursu.registry.StepRegistry.extract_fixtures
:parser: myst
```

````

````{py:method} register_handler(type: tursu.steps.StepKeyword, pattern: str, handler: tursu.steps.Handler) -> None
:canonical: tursu.registry.StepRegistry.register_handler

```{autodoc2-docstring} tursu.registry.StepRegistry.register_handler
:parser: myst
```

````

````{py:method} run_step(step: tursu.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> None
:canonical: tursu.registry.StepRegistry.run_step

```{autodoc2-docstring} tursu.registry.StepRegistry.run_step
:parser: myst
```

````

````{py:method} scan(mod: types.ModuleType | None = None) -> tursu.registry.StepRegistry
:canonical: tursu.registry.StepRegistry.scan

```{autodoc2-docstring} tursu.registry.StepRegistry.scan
:parser: myst
```

````

`````

````{py:function} generate_tests() -> None
:canonical: tursu.compile_all.generate_tests

```{autodoc2-docstring} tursu.compile_all.generate_tests
:parser: myst
```
````

````{py:function} given(pattern: str) -> typing.Callable[[tursu.steps.Handler], tursu.steps.Handler]
:canonical: tursu.registry.given

```{autodoc2-docstring} tursu.registry.given
:parser: myst
```
````

````{py:function} then(pattern: str) -> typing.Callable[[tursu.steps.Handler], tursu.steps.Handler]
:canonical: tursu.registry.then

```{autodoc2-docstring} tursu.registry.then
:parser: myst
```
````

````{py:function} when(pattern: str) -> typing.Callable[[tursu.steps.Handler], tursu.steps.Handler]
:canonical: tursu.registry.when

```{autodoc2-docstring} tursu.registry.when
:parser: myst
```
````
