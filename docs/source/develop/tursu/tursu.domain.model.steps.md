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

* - {py:obj}`Step <tursu.domain.model.steps.Step>`
  - ```{autodoc2-docstring} tursu.domain.model.steps.Step
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

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
````

### API

````{py:data} Handler
:canonical: tursu.domain.model.steps.Handler
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.steps.Handler
:parser: myst
```

````

`````{py:class} Step(pattern: str | tursu.runtime.pattern_matcher.AbstractPattern, hook: tursu.domain.model.steps.Handler)
:canonical: tursu.domain.model.steps.Step

```{autodoc2-docstring} tursu.domain.model.steps.Step
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.domain.model.steps.Step.__init__
:parser: myst
```

````{py:method} __call__(**kwargs: typing.Any) -> None
:canonical: tursu.domain.model.steps.Step.__call__

```{autodoc2-docstring} tursu.domain.model.steps.Step.__call__
:parser: myst
```

````

````{py:method} __eq__(other: typing.Any) -> bool
:canonical: tursu.domain.model.steps.Step.__eq__

````

````{py:method} __repr__() -> str
:canonical: tursu.domain.model.steps.Step.__repr__

````

````{py:method} highlight(matches: collections.abc.Mapping[str, typing.Any]) -> str
:canonical: tursu.domain.model.steps.Step.highlight

```{autodoc2-docstring} tursu.domain.model.steps.Step.highlight
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
