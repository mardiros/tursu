# {py:mod}`tursu.domain.model.steps`

```{py:module} tursu.domain.model.steps
```

```{autodoc2-docstring} tursu.domain.model.steps
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`StepDefinition <tursu.domain.model.steps.StepDefinition>`
  - ```{autodoc2-docstring} tursu.domain.model.steps.StepDefinition
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`discover_fixtures <tursu.domain.model.steps.discover_fixtures>`
  - ```{autodoc2-docstring} tursu.domain.model.steps.discover_fixtures
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AsyncHandler <tursu.domain.model.steps.AsyncHandler>`
  - ```{autodoc2-docstring} tursu.domain.model.steps.AsyncHandler
    :parser: myst
    :summary:
    ```
* - {py:obj}`Handler <tursu.domain.model.steps.Handler>`
  - ```{autodoc2-docstring} tursu.domain.model.steps.Handler
    :parser: myst
    :summary:
    ```
* - {py:obj}`StepKeyword <tursu.domain.model.steps.StepKeyword>`
  - ```{autodoc2-docstring} tursu.domain.model.steps.StepKeyword
    :parser: myst
    :summary:
    ```
* - {py:obj}`SyncHandler <tursu.domain.model.steps.SyncHandler>`
  - ```{autodoc2-docstring} tursu.domain.model.steps.SyncHandler
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} AsyncHandler
:canonical: tursu.domain.model.steps.AsyncHandler
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.steps.AsyncHandler
:parser: myst
```

````

````{py:data} Handler
:canonical: tursu.domain.model.steps.Handler
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.steps.Handler
:parser: myst
```

````

`````{py:class} StepDefinition(pattern: str | tursu.runtime.pattern_matcher.AbstractPattern, hook: tursu.domain.model.steps.Handler)
:canonical: tursu.domain.model.steps.StepDefinition

```{autodoc2-docstring} tursu.domain.model.steps.StepDefinition
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.domain.model.steps.StepDefinition.__init__
:parser: myst
```

````{py:method} __call__(**kwargs: typing.Any) -> None | collections.abc.Coroutine[typing.Any, typing.Any, typing.Any]
:canonical: tursu.domain.model.steps.StepDefinition.__call__

```{autodoc2-docstring} tursu.domain.model.steps.StepDefinition.__call__
:parser: myst
```

````

````{py:method} __eq__(other: typing.Any) -> bool
:canonical: tursu.domain.model.steps.StepDefinition.__eq__

````

````{py:method} __repr__() -> str
:canonical: tursu.domain.model.steps.StepDefinition.__repr__

````

````{py:method} highlight(matches: collections.abc.Mapping[str, typing.Any], color: str = '\x1b[36m', reset: str = '\x1b[0m') -> str
:canonical: tursu.domain.model.steps.StepDefinition.highlight

```{autodoc2-docstring} tursu.domain.model.steps.StepDefinition.highlight
:parser: myst
```

````

`````

````{py:data} StepKeyword
:canonical: tursu.domain.model.steps.StepKeyword
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.steps.StepKeyword
:parser: myst
```

````

````{py:data} SyncHandler
:canonical: tursu.domain.model.steps.SyncHandler
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.steps.SyncHandler
:parser: myst
```

````

````{py:function} discover_fixtures(hook: tursu.domain.model.steps.Handler) -> dict[str, type]
:canonical: tursu.domain.model.steps.discover_fixtures

```{autodoc2-docstring} tursu.domain.model.steps.discover_fixtures
:parser: myst
```
````
