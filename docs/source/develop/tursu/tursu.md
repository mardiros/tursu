# {py:mod}`tursu`

```{py:module} tursu
```

```{autodoc2-docstring} tursu
:parser: myst
:allowtitles:
```

## Package Contents

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

### API

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
