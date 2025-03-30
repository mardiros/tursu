# {py:mod}`tursu.runtime.exceptions`

```{py:module} tursu.runtime.exceptions
```

```{autodoc2-docstring} tursu.runtime.exceptions
:parser: myst
:allowtitles:
```

## Module Contents

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TEMPLATE_WITHOUT_MATCHED_STEPS <tursu.runtime.exceptions.TEMPLATE_WITHOUT_MATCHED_STEPS>`
  - ```{autodoc2-docstring} tursu.runtime.exceptions.TEMPLATE_WITHOUT_MATCHED_STEPS
    :parser: myst
    :summary:
    ```
* - {py:obj}`TEMPLATE_WITH_MATCHED_STEPS <tursu.runtime.exceptions.TEMPLATE_WITH_MATCHED_STEPS>`
  - ```{autodoc2-docstring} tursu.runtime.exceptions.TEMPLATE_WITH_MATCHED_STEPS
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} TEMPLATE_WITHOUT_MATCHED_STEPS
:canonical: tursu.runtime.exceptions.TEMPLATE_WITHOUT_MATCHED_STEPS
:value: <Multiline-String>

```{autodoc2-docstring} tursu.runtime.exceptions.TEMPLATE_WITHOUT_MATCHED_STEPS
:parser: myst
```

````

````{py:data} TEMPLATE_WITH_MATCHED_STEPS
:canonical: tursu.runtime.exceptions.TEMPLATE_WITH_MATCHED_STEPS
:value: <Multiline-String>

```{autodoc2-docstring} tursu.runtime.exceptions.TEMPLATE_WITH_MATCHED_STEPS
:parser: myst
```

````

````{py:exception} Unregistered(registry: tursu.runtime.registry.Tursu, step: tursu.domain.model.steps.StepKeyword, text: str)
:canonical: tursu.runtime.exceptions.Unregistered

Bases: {py:obj}`RuntimeError`

```{autodoc2-docstring} tursu.runtime.exceptions.Unregistered
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.exceptions.Unregistered.__init__
:parser: myst
```

````
