# {py:mod}`tursu.entrypoints.plugin`

```{py:module} tursu.entrypoints.plugin
```

```{autodoc2-docstring} tursu.entrypoints.plugin
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`GherkinTestModule <tursu.entrypoints.plugin.GherkinTestModule>`
  -
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`tursu <tursu.entrypoints.plugin.tursu>`
  - ```{autodoc2-docstring} tursu.entrypoints.plugin.tursu
    :parser: myst
    :summary:
    ```
* - {py:obj}`tursu_collect_file <tursu.entrypoints.plugin.tursu_collect_file>`
- ```{autodoc2-docstring} tursu.entrypoints.plugin.tursu_collect_file
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} GherkinTestModule(path: pathlib.Path, tursu: tursu.registry.Tursu, **kwargs: typing.Any)
:canonical: tursu.entrypoints.plugin.GherkinTestModule

Bases: {py:obj}`pytest.Module`

````{py:method} __repr__() -> str
:canonical: tursu.entrypoints.plugin.GherkinTestModule.__repr__

````

````{py:method} collect() -> collections.abc.Iterable[pytest.Item | pytest.Collector]
:canonical: tursu.entrypoints.plugin.GherkinTestModule.collect

````

`````

````{py:function} tursu() -> tursu.registry.Tursu
:canonical: tursu.entrypoints.plugin.tursu

```{autodoc2-docstring} tursu.entrypoints.plugin.tursu
:parser: myst
```
````

````{py:function} tursu_collect_file() -> None
:canonical: tursu.entrypoints.plugin.tursu_collect_file

```{autodoc2-docstring} tursu.entrypoints.plugin.tursu_collect_file
:parser: myst
```
````
