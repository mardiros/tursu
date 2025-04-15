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

* - {py:obj}`ModRegistry <tursu.runtime.registry.ModRegistry>`
  - ```{autodoc2-docstring} tursu.runtime.registry.ModRegistry
    :parser: myst
    :summary:
    ```
* - {py:obj}`Registry <tursu.runtime.registry.Registry>`
  - ```{autodoc2-docstring} tursu.runtime.registry.Registry
    :parser: myst
    :summary:
    ```
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
* - {py:obj}`is_init_file <tursu.runtime.registry.is_init_file>`
  - ```{autodoc2-docstring} tursu.runtime.registry.is_init_file
    :parser: myst
    :summary:
    ```
* - {py:obj}`normalize_module_name <tursu.runtime.registry.normalize_module_name>`
  - ```{autodoc2-docstring} tursu.runtime.registry.normalize_module_name
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

`````{py:class} ModRegistry()
:canonical: tursu.runtime.registry.ModRegistry

```{autodoc2-docstring} tursu.runtime.registry.ModRegistry
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.registry.ModRegistry.__init__
:parser: myst
```

````{py:method} append(stp: tursu.domain.model.steps.StepKeyword, step: tursu.domain.model.steps.StepDefinition) -> None
:canonical: tursu.runtime.registry.ModRegistry.append

```{autodoc2-docstring} tursu.runtime.registry.ModRegistry.append
:parser: myst
```

````

````{py:method} get_best_matches(text: str, n: int = 5, cutoff: float = 0.3) -> collections.abc.Sequence[tuple[float, str]]
:canonical: tursu.runtime.registry.ModRegistry.get_best_matches

```{autodoc2-docstring} tursu.runtime.registry.ModRegistry.get_best_matches
:parser: myst
```

````

````{py:method} get_fixtures() -> collections.abc.Mapping[str, type]
:canonical: tursu.runtime.registry.ModRegistry.get_fixtures

```{autodoc2-docstring} tursu.runtime.registry.ModRegistry.get_fixtures
:parser: myst
```

````

````{py:method} get_step(keyword: tursu.domain.model.steps.StepKeyword, text: str) -> tursu.domain.model.steps.StepDefinition | None
:canonical: tursu.runtime.registry.ModRegistry.get_step

```{autodoc2-docstring} tursu.runtime.registry.ModRegistry.get_step
:parser: myst
```

````

````{py:property} models_types
:canonical: tursu.runtime.registry.ModRegistry.models_types
:type: dict[type, str]

```{autodoc2-docstring} tursu.runtime.registry.ModRegistry.models_types
:parser: myst
```

````

````{py:method} register_data_table(step: tursu.domain.model.steps.StepDefinition) -> None
:canonical: tursu.runtime.registry.ModRegistry.register_data_table

```{autodoc2-docstring} tursu.runtime.registry.ModRegistry.register_data_table
:parser: myst
```

````

````{py:method} register_doc_string(step: tursu.domain.model.steps.StepDefinition) -> None
:canonical: tursu.runtime.registry.ModRegistry.register_doc_string

```{autodoc2-docstring} tursu.runtime.registry.ModRegistry.register_doc_string
:parser: myst
```

````

````{py:method} register_model(parameter: inspect.Parameter | None) -> None
:canonical: tursu.runtime.registry.ModRegistry.register_model

```{autodoc2-docstring} tursu.runtime.registry.ModRegistry.register_model
:parser: myst
```

````

`````

`````{py:class} Registry()
:canonical: tursu.runtime.registry.Registry

```{autodoc2-docstring} tursu.runtime.registry.Registry
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.registry.Registry.__init__
:parser: myst
```

````{py:method} append(module_name: str, keyword: tursu.domain.model.steps.StepKeyword, step: tursu.domain.model.steps.StepDefinition) -> None
:canonical: tursu.runtime.registry.Registry.append

```{autodoc2-docstring} tursu.runtime.registry.Registry.append
:parser: myst
```

````

````{py:method} get_best_matches(module_name: str, text: str) -> list[str]
:canonical: tursu.runtime.registry.Registry.get_best_matches

```{autodoc2-docstring} tursu.runtime.registry.Registry.get_best_matches
:parser: myst
```

````

````{py:method} get_fixtures(module_name: str) -> collections.abc.Mapping[str, type]
:canonical: tursu.runtime.registry.Registry.get_fixtures

```{autodoc2-docstring} tursu.runtime.registry.Registry.get_fixtures
:parser: myst
```

````

````{py:method} get_matched_step(module_name: str, keyword: tursu.domain.model.steps.StepKeyword, text: str, fixtures: collections.abc.Mapping[str, typing_extensions.Any]) -> tuple[tursu.domain.model.steps.StepDefinition | None, collections.abc.Mapping[str, typing_extensions.Any]]
:canonical: tursu.runtime.registry.Registry.get_matched_step

```{autodoc2-docstring} tursu.runtime.registry.Registry.get_matched_step
:parser: myst
```

````

````{py:method} get_models_types(module_name: str) -> dict[type, str]
:canonical: tursu.runtime.registry.Registry.get_models_types

```{autodoc2-docstring} tursu.runtime.registry.Registry.get_models_types
:parser: myst
```

````

````{py:method} get_step(module_name: str, keyword: tursu.domain.model.steps.StepKeyword, text: str) -> tursu.domain.model.steps.StepDefinition | None
:canonical: tursu.runtime.registry.Registry.get_step

```{autodoc2-docstring} tursu.runtime.registry.Registry.get_step
:parser: myst
```

````

`````

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

````{py:method} extract_fixtures(module_name: str, keyword: tursu.domain.model.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> collections.abc.Mapping[str, typing_extensions.Any]
:canonical: tursu.runtime.registry.Tursu.extract_fixtures

```{autodoc2-docstring} tursu.runtime.registry.Tursu.extract_fixtures
:parser: myst
```

````

````{py:method} get_best_matches(module_name: str, text: str) -> list[str]
:canonical: tursu.runtime.registry.Tursu.get_best_matches

```{autodoc2-docstring} tursu.runtime.registry.Tursu.get_best_matches
:parser: myst
```

````

````{py:method} get_fixtures(module_name: str) -> collections.abc.Mapping[str, type]
:canonical: tursu.runtime.registry.Tursu.get_fixtures

```{autodoc2-docstring} tursu.runtime.registry.Tursu.get_fixtures
:parser: myst
```

````

````{py:method} get_models_type(module_name: str, typ: type[typing_extensions.Any]) -> str
:canonical: tursu.runtime.registry.Tursu.get_models_type

```{autodoc2-docstring} tursu.runtime.registry.Tursu.get_models_type
:parser: myst
```

````

````{py:method} get_models_types(module_name: str) -> dict[type, str]
:canonical: tursu.runtime.registry.Tursu.get_models_types

```{autodoc2-docstring} tursu.runtime.registry.Tursu.get_models_types
:parser: myst
```

````

````{py:method} get_step(module_name: str, keyword: tursu.domain.model.steps.StepKeyword, text: str) -> tursu.domain.model.steps.StepDefinition | None
:canonical: tursu.runtime.registry.Tursu.get_step

```{autodoc2-docstring} tursu.runtime.registry.Tursu.get_step
:parser: myst
```

````

````{py:method} register_step_definition(module_name: str, keyword: tursu.domain.model.steps.StepKeyword, pattern: str | tursu.runtime.pattern_matcher.AbstractPattern, handler: tursu.domain.model.steps.Handler) -> None
:canonical: tursu.runtime.registry.Tursu.register_step_definition

```{autodoc2-docstring} tursu.runtime.registry.Tursu.register_step_definition
:parser: myst
```

````

````{py:method} run_step(tursu_runner: tursu.runtime.runner.TursuRunner, keyword: tursu.domain.model.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> None
:canonical: tursu.runtime.registry.Tursu.run_step

```{autodoc2-docstring} tursu.runtime.registry.Tursu.run_step
:parser: myst
```

````

````{py:method} run_step_async(tursu_runner: tursu.runtime.runner.TursuRunner, keyword: tursu.domain.model.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> None
:canonical: tursu.runtime.registry.Tursu.run_step_async
:async:

```{autodoc2-docstring} tursu.runtime.registry.Tursu.run_step_async
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

````{py:function} is_init_file(module: types.ModuleType) -> bool
:canonical: tursu.runtime.registry.is_init_file

```{autodoc2-docstring} tursu.runtime.registry.is_init_file
:parser: myst
```
````

````{py:function} normalize_module_name(module_name: str) -> str
:canonical: tursu.runtime.registry.normalize_module_name

```{autodoc2-docstring} tursu.runtime.registry.normalize_module_name
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
