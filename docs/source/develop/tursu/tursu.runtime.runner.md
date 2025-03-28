# {py:mod}`tursu.runtime.runner`

```{py:module} tursu.runtime.runner
```

```{autodoc2-docstring} tursu.runtime.runner
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`TursuRunner <tursu.runtime.runner.TursuRunner>`
  - ```{autodoc2-docstring} tursu.runtime.runner.TursuRunner
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`CYAN <tursu.runtime.runner.CYAN>`
  - ```{autodoc2-docstring} tursu.runtime.runner.CYAN
    :parser: myst
    :summary:
    ```
* - {py:obj}`EL <tursu.runtime.runner.EL>`
  - ```{autodoc2-docstring} tursu.runtime.runner.EL
    :parser: myst
    :summary:
    ```
* - {py:obj}`GREEN <tursu.runtime.runner.GREEN>`
  - ```{autodoc2-docstring} tursu.runtime.runner.GREEN
    :parser: myst
    :summary:
    ```
* - {py:obj}`GREY <tursu.runtime.runner.GREY>`
  - ```{autodoc2-docstring} tursu.runtime.runner.GREY
    :parser: myst
    :summary:
    ```
* - {py:obj}`ORANGE <tursu.runtime.runner.ORANGE>`
  - ```{autodoc2-docstring} tursu.runtime.runner.ORANGE
    :parser: myst
    :summary:
    ```
* - {py:obj}`RED <tursu.runtime.runner.RED>`
  - ```{autodoc2-docstring} tursu.runtime.runner.RED
    :parser: myst
    :summary:
    ```
* - {py:obj}`RESET <tursu.runtime.runner.RESET>`
  - ```{autodoc2-docstring} tursu.runtime.runner.RESET
    :parser: myst
    :summary:
    ```
* - {py:obj}`UP <tursu.runtime.runner.UP>`
  - ```{autodoc2-docstring} tursu.runtime.runner.UP
    :parser: myst
    :summary:
    ```
* - {py:obj}`logger <tursu.runtime.runner.logger>`
  - ```{autodoc2-docstring} tursu.runtime.runner.logger
    :parser: myst
    :summary:
    ```
````

### API

````{py:data} CYAN
:canonical: tursu.runtime.runner.CYAN
:value: >
   '\x1b[36m'

```{autodoc2-docstring} tursu.runtime.runner.CYAN
:parser: myst
```

````

````{py:data} EL
:canonical: tursu.runtime.runner.EL
:value: >
   '\x1b[K'

```{autodoc2-docstring} tursu.runtime.runner.EL
:parser: myst
```

````

````{py:data} GREEN
:canonical: tursu.runtime.runner.GREEN
:value: >
   '\x1b[92m'

```{autodoc2-docstring} tursu.runtime.runner.GREEN
:parser: myst
```

````

````{py:data} GREY
:canonical: tursu.runtime.runner.GREY
:value: >
   '\x1b[90m'

```{autodoc2-docstring} tursu.runtime.runner.GREY
:parser: myst
```

````

````{py:data} ORANGE
:canonical: tursu.runtime.runner.ORANGE
:value: >
   '\x1b[93m'

```{autodoc2-docstring} tursu.runtime.runner.ORANGE
:parser: myst
```

````

````{py:data} RED
:canonical: tursu.runtime.runner.RED
:value: >
   '\x1b[91m'

```{autodoc2-docstring} tursu.runtime.runner.RED
:parser: myst
```

````

````{py:data} RESET
:canonical: tursu.runtime.runner.RESET
:value: >
   '\x1b[0m'

```{autodoc2-docstring} tursu.runtime.runner.RESET
:parser: myst
```

````

````{py:exception} ScenarioFailed()
:canonical: tursu.runtime.runner.ScenarioFailed

Bases: {py:obj}`Exception`

```{autodoc2-docstring} tursu.runtime.runner.ScenarioFailed
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.runner.ScenarioFailed.__init__
:parser: myst
```

````

`````{py:class} TursuRunner(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: tursu.runtime.registry.Tursu, scenario: list[str])
:canonical: tursu.runtime.runner.TursuRunner

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.__init__
:parser: myst
```

````{py:attribute} IGNORE_TIMING_MS
:canonical: tursu.runtime.runner.TursuRunner.IGNORE_TIMING_MS
:value: >
   200

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.IGNORE_TIMING_MS
:parser: myst
```

````

````{py:attribute} OK_TIMING_MS
:canonical: tursu.runtime.runner.TursuRunner.OK_TIMING_MS
:value: >
   700

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.OK_TIMING_MS
:parser: myst
```

````

````{py:attribute} WARN_TIMING_MS
:canonical: tursu.runtime.runner.TursuRunner.WARN_TIMING_MS
:value: >
   2100

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.WARN_TIMING_MS
:parser: myst
```

````

````{py:method} __enter__() -> typing.Self
:canonical: tursu.runtime.runner.TursuRunner.__enter__

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.__enter__
:parser: myst
```

````

````{py:method} __exit__(exc_type: type[BaseException] | None, exc: BaseException | None, tb: types.TracebackType | None) -> None
:canonical: tursu.runtime.runner.TursuRunner.__exit__

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.__exit__
:parser: myst
```

````

````{py:method} emit_error(keyword: tursu.domain.model.steps.StepKeyword, step: tursu.domain.model.steps.Step, matches: collections.abc.Mapping[str, typing_extensions.Any]) -> None
:canonical: tursu.runtime.runner.TursuRunner.emit_error

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.emit_error
:parser: myst
```

````

````{py:method} emit_running(keyword: tursu.domain.model.steps.StepKeyword, step: tursu.domain.model.steps.Step, matches: collections.abc.Mapping[str, typing_extensions.Any]) -> None
:canonical: tursu.runtime.runner.TursuRunner.emit_running

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.emit_running
:parser: myst
```

````

````{py:method} emit_success(keyword: tursu.domain.model.steps.StepKeyword, step: tursu.domain.model.steps.Step, matches: collections.abc.Mapping[str, typing_extensions.Any]) -> None
:canonical: tursu.runtime.runner.TursuRunner.emit_success

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.emit_success
:parser: myst
```

````

````{py:method} fancy() -> str
:canonical: tursu.runtime.runner.TursuRunner.fancy

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.fancy
:parser: myst
```

````

````{py:method} format_example_step(text: str, **kwargs: typing_extensions.Any) -> str
:canonical: tursu.runtime.runner.TursuRunner.format_example_step

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.format_example_step
:parser: myst
```

````

````{py:method} log(text: str, replace_previous_line: bool = False, end: str = '\n') -> None
:canonical: tursu.runtime.runner.TursuRunner.log

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.log
:parser: myst
```

````

````{py:method} remove_ansi_escape_sequences(text: str) -> str
:canonical: tursu.runtime.runner.TursuRunner.remove_ansi_escape_sequences

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.remove_ansi_escape_sequences
:parser: myst
```

````

````{py:method} run_step(step: tursu.domain.model.steps.StepKeyword, text: str, **kwargs: typing_extensions.Any) -> None
:canonical: tursu.runtime.runner.TursuRunner.run_step

```{autodoc2-docstring} tursu.runtime.runner.TursuRunner.run_step
:parser: myst
```

````

`````

````{py:data} UP
:canonical: tursu.runtime.runner.UP
:value: >
   '\x1b[F'

```{autodoc2-docstring} tursu.runtime.runner.UP
:parser: myst
```

````

````{py:data} logger
:canonical: tursu.runtime.runner.logger
:value: >
   'getLogger(...)'

```{autodoc2-docstring} tursu.runtime.runner.logger
:parser: myst
```

````
