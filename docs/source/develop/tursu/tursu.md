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

* - {py:obj}`RegEx <tursu.runtime.pattern_matcher.RegEx>`
  - ```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegEx
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
* - {py:obj}`tursu_collect_file <tursu.entrypoints.plugin.tursu_collect_file>`
  - ```{autodoc2-docstring} tursu.entrypoints.plugin.tursu_collect_file
    :parser: myst
    :summary:
    ```
* - {py:obj}`when <tursu.runtime.registry.when>`
  - ```{autodoc2-docstring} tursu.runtime.registry.when
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} RegEx(pattern: str)
:canonical: tursu.runtime.pattern_matcher.RegEx

Bases: {py:obj}`tursu.runtime.pattern_matcher.AbstractPattern`

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegEx
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegEx.__init__
:parser: myst
```

````{py:method} __repr__() -> str
:canonical: tursu.runtime.pattern_matcher.RegEx.__repr__

````

````{py:method} get_matcher() -> type[tursu.runtime.pattern_matcher.AbstractPatternMatcher]
:canonical: tursu.runtime.pattern_matcher.RegEx.get_matcher
:classmethod:

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegEx.get_matcher
:parser: myst
```

````

`````

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

````{py:function} tursu_collect_file() -> None
:canonical: tursu.entrypoints.plugin.tursu_collect_file

```{autodoc2-docstring} tursu.entrypoints.plugin.tursu_collect_file
:parser: myst
```
````

````{py:function} when(pattern: str | tursu.runtime.pattern_matcher.AbstractPattern) -> typing.Callable[[tursu.domain.model.steps.Handler], tursu.domain.model.steps.Handler]
:canonical: tursu.runtime.registry.when

```{autodoc2-docstring} tursu.runtime.registry.when
:parser: myst
```
````
