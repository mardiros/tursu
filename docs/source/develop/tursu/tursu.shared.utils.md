# {py:mod}`tursu.shared.utils`

```{py:module} tursu.shared.utils
```

```{autodoc2-docstring} tursu.shared.utils
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`is_mapping <tursu.shared.utils.is_mapping>`
  - ```{autodoc2-docstring} tursu.shared.utils.is_mapping
    :parser: myst
    :summary:
    ```
* - {py:obj}`is_sequence <tursu.shared.utils.is_sequence>`
  - ```{autodoc2-docstring} tursu.shared.utils.is_sequence
    :parser: myst
    :summary:
    ```
* - {py:obj}`is_union <tursu.shared.utils.is_union>`
  - ```{autodoc2-docstring} tursu.shared.utils.is_union
    :parser: myst
    :summary:
    ```
````

### API

````{py:function} is_mapping(value: type[typing.Any] | None) -> typing.TypeGuard[collections.abc.Mapping[typing.Any, typing.Any]]
:canonical: tursu.shared.utils.is_mapping

```{autodoc2-docstring} tursu.shared.utils.is_mapping
:parser: myst
```
````

````{py:function} is_sequence(value: type[typing.Any] | None) -> typing.TypeGuard[collections.abc.Sequence[typing.Any]]
:canonical: tursu.shared.utils.is_sequence

```{autodoc2-docstring} tursu.shared.utils.is_sequence
:parser: myst
```
````

````{py:function} is_union(typ: type[typing.Any]) -> bool
:canonical: tursu.shared.utils.is_union

```{autodoc2-docstring} tursu.shared.utils.is_union
:parser: myst
```
````
