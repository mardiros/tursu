# {py:mod}`tursu.runner`

```{py:module} tursu.runner
```

```{autodoc2-docstring} tursu.runner
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TursuRunner <tursu.runner.TursuRunner>`
  - ```{autodoc2-docstring} tursu.runner.TursuRunner
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`logger <tursu.runner.logger>`
  - ```{autodoc2-docstring} tursu.runner.logger
    :parser: myst
    :summary:
    ```
````

### API

```{py:exception} ScenarioFailed()
:canonical: tursu.runner.ScenarioFailed

Bases: {py:obj}`Exception`

```

`````{py:class} TursuRunner(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: tursu.registry.Tursu, scenario: list[str])
:canonical: tursu.runner.TursuRunner

```{autodoc2-docstring} tursu.runner.TursuRunner
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runner.TursuRunner.__init__
:parser: myst
```

````{py:method} __enter__() -> typing.Self
:canonical: tursu.runner.TursuRunner.__enter__

```{autodoc2-docstring} tursu.runner.TursuRunner.__enter__
:parser: myst
```

````

````{py:method} __exit__(exc_type: type[BaseException] | None, exc: BaseException | None, tb: types.TracebackType | None) -> None
:canonical: tursu.runner.TursuRunner.__exit__

```{autodoc2-docstring} tursu.runner.TursuRunner.__exit__
:parser: myst
```

````

````{py:method} emit_error(keyword: tursu.steps.StepKeyword, step: tursu.steps.Step, matches: collections.abc.Mapping[str, typing_extensions.Any]) -> None
:canonical: tursu.runner.TursuRunner.emit_error

```{autodoc2-docstring} tursu.runner.TursuRunner.emit_error
:parser: myst
```

````

````{py:method} emit_running(keyword: tursu.steps.StepKeyword, step: tursu.steps.Step, matches: collections.abc.Mapping[str, typing_extensions.Any]) -> None
:canonical: tursu.runner.TursuRunner.emit_running

```{autodoc2-docstring} tursu.runner.TursuRunner.emit_running
:parser: myst
```

````

````{py:method} emit_success(keyword: tursu.steps.StepKeyword, step: tursu.steps.Step, matches: collections.abc.Mapping[str, typing_extensions.Any]) -> None
:canonical: tursu.runner.TursuRunner.emit_success

```{autodoc2-docstring} tursu.runner.TursuRunner.emit_success
:parser: myst
```

````

````{py:method} fancy() -> str
:canonical: tursu.runner.TursuRunner.fancy

```{autodoc2-docstring} tursu.runner.TursuRunner.fancy
:parser: myst
```

````

````{py:method} format_example_step(text: str, **kwargs: typing_extensions.Any) -> str
:canonical: tursu.runner.TursuRunner.format_example_step

```{autodoc2-docstring} tursu.runner.TursuRunner.format_example_step
:parser: myst
```

````

````{py:method} log(text: str, remove_previous_line: bool = False, end: str = '\n') -> None
:canonical: tursu.runner.TursuRunner.log

```{autodoc2-docstring} tursu.runner.TursuRunner.log
:parser: myst
```

````

````{py:method} remove_ansi_escape_sequences(text: str) -> str
:canonical: tursu.runner.TursuRunner.remove_ansi_escape_sequences

```{autodoc2-docstring} tursu.runner.TursuRunner.remove_ansi_escape_sequences
:parser: myst
```

````

````{py:method} run_step(step: tursu.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> None
:canonical: tursu.runner.TursuRunner.run_step

```{autodoc2-docstring} tursu.runner.TursuRunner.run_step
:parser: myst
```

````

`````

````{py:data} logger
:canonical: tursu.runner.logger
:value: >
   'getLogger(...)'

```{autodoc2-docstring} tursu.runner.logger
:parser: myst
```

````
