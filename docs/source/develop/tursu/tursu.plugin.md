# {py:mod}`tursu.plugin`

```{py:module} tursu.plugin
```

```{autodoc2-docstring} tursu.plugin
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`GherkinTestModule <tursu.plugin.GherkinTestModule>`
  -
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`tursu <tursu.plugin.tursu>`
  - ```{autodoc2-docstring} tursu.plugin.tursu
    :parser: myst
    :summary:
    ```
* - {py:obj}`tursu_collect_file <tursu.plugin.tursu_collect_file>`
  - ```{autodoc2-docstring} tursu.plugin.tursu_collect_file
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} GherkinTestModule(path: pathlib.Path, tursu: tursu.registry.Tursu, **kwargs: typing.Any)
:canonical: tursu.plugin.GherkinTestModule

Bases: {py:obj}`pytest.Module`

````{py:method} __repr__() -> str
:canonical: tursu.plugin.GherkinTestModule.__repr__

````

````{py:method} collect() -> collections.abc.Iterable[pytest.Item | pytest.Collector]
:canonical: tursu.plugin.GherkinTestModule.collect

````

`````

````{py:function} tursu() -> tursu.registry.Tursu
:canonical: tursu.plugin.tursu

```{autodoc2-docstring} tursu.plugin.tursu
:parser: myst
```
````

````{py:function} tursu_collect_file() -> None
:canonical: tursu.plugin.tursu_collect_file

```{autodoc2-docstring} tursu.plugin.tursu_collect_file
:parser: myst
```
````
