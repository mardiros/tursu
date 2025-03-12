# {py:mod}`tursu.steps`

```{py:module} tursu.steps
```

```{autodoc2-docstring} tursu.steps
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Step <tursu.steps.Step>`
  - ```{autodoc2-docstring} tursu.steps.Step
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`Handler <tursu.steps.Handler>`
  - ```{autodoc2-docstring} tursu.steps.Handler
    :parser: myst
    :summary:
    ```
* - {py:obj}`StepKeyword <tursu.steps.StepKeyword>`
  - ```{autodoc2-docstring} tursu.steps.StepKeyword
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} Handler
:canonical: tursu.steps.Handler
:value: >
   None

```{autodoc2-docstring} tursu.steps.Handler
:parser: myst
```

````

`````{py:class} Step(pattern: str | tursu.pattern_matcher.AbstractPattern, hook: tursu.steps.Handler)
:canonical: tursu.steps.Step

```{autodoc2-docstring} tursu.steps.Step
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.steps.Step.__init__
:parser: myst
```

````{py:method} __call__(**kwargs: typing.Any) -> None
:canonical: tursu.steps.Step.__call__

```{autodoc2-docstring} tursu.steps.Step.__call__
:parser: myst
```

````

````{py:method} __eq__(other: typing.Any) -> bool
:canonical: tursu.steps.Step.__eq__

````

````{py:method} __repr__() -> str
:canonical: tursu.steps.Step.__repr__

````

````{py:method} highlight(matches: collections.abc.Mapping[str, typing.Any]) -> str
:canonical: tursu.steps.Step.highlight

```{autodoc2-docstring} tursu.steps.Step.highlight
:parser: myst
```

````

`````

````{py:data} StepKeyword
:canonical: tursu.steps.StepKeyword
:value: >
   None

```{autodoc2-docstring} tursu.steps.StepKeyword
:parser: myst
```

````
