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

````{py:method} format_example_step(text: str, **kwargs: typing_extensions.Any) -> str
:canonical: tursu.registry.Tursu.format_example_step

```{autodoc2-docstring} tursu.registry.Tursu.format_example_step
:parser: myst
```

````

````{py:method} register_handler(type: tursu.steps.StepKeyword, pattern: str, handler: tursu.steps.Handler) -> None
:canonical: tursu.registry.Tursu.register_handler

```{autodoc2-docstring} tursu.registry.Tursu.register_handler
:parser: myst
```

````

````{py:method} run_step(request: _pytest.fixtures.FixtureRequest, step: tursu.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> None
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
