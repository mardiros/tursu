# {py:mod}`tursu.runtime.pattern_matcher`

```{py:module} tursu.runtime.pattern_matcher
```

```{autodoc2-docstring} tursu.runtime.pattern_matcher
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AbstractPattern <tursu.runtime.pattern_matcher.AbstractPattern>`
  - ```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPattern
    :parser: myst
    :summary:
    ```
* - {py:obj}`AbstractPatternMatcher <tursu.runtime.pattern_matcher.AbstractPatternMatcher>`
  - ```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPatternMatcher
    :parser: myst
    :summary:
    ```
* - {py:obj}`DefaultPatternMatcher <tursu.runtime.pattern_matcher.DefaultPatternMatcher>`
  - ```{autodoc2-docstring} tursu.runtime.pattern_matcher.DefaultPatternMatcher
    :parser: myst
    :summary:
    ```
* - {py:obj}`RegEx <tursu.runtime.pattern_matcher.RegEx>`
  - ```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegEx
    :parser: myst
    :summary:
    ```
* - {py:obj}`RegExPatternMatcher <tursu.runtime.pattern_matcher.RegExPatternMatcher>`
  - ```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegExPatternMatcher
    :parser: myst
    :summary:
    ```
* - {py:obj}`RegexBasePattern <tursu.runtime.pattern_matcher.RegexBasePattern>`
  - ```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegexBasePattern
    :parser: myst
    :summary:
    ```
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`cast_to_annotation <tursu.runtime.pattern_matcher.cast_to_annotation>`
  - ```{autodoc2-docstring} tursu.runtime.pattern_matcher.cast_to_annotation
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} AbstractPattern(pattern: str)
:canonical: tursu.runtime.pattern_matcher.AbstractPattern

Bases: {py:obj}`abc.ABC`

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPattern
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPattern.__init__
:parser: myst
```

````{py:method} get_matcher() -> type[tursu.runtime.pattern_matcher.AbstractPatternMatcher]
:canonical: tursu.runtime.pattern_matcher.AbstractPattern.get_matcher
:abstractmethod:
:classmethod:

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPattern.get_matcher
:parser: myst
```

````

````{py:attribute} pattern
:canonical: tursu.runtime.pattern_matcher.AbstractPattern.pattern
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPattern.pattern
:parser: myst
```

````

`````

`````{py:class} AbstractPatternMatcher(pattern: str, signature: inspect.Signature)
:canonical: tursu.runtime.pattern_matcher.AbstractPatternMatcher

Bases: {py:obj}`abc.ABC`

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPatternMatcher
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPatternMatcher.__init__
:parser: myst
```

````{py:method} __eq__(other: typing.Any) -> bool
:canonical: tursu.runtime.pattern_matcher.AbstractPatternMatcher.__eq__

````

````{py:method} __repr__() -> str
:canonical: tursu.runtime.pattern_matcher.AbstractPatternMatcher.__repr__

````

````{py:method} __str__() -> str
:canonical: tursu.runtime.pattern_matcher.AbstractPatternMatcher.__str__

````

````{py:method} extract_fixtures(text: str) -> collections.abc.Mapping[str, typing.Any] | None
:canonical: tursu.runtime.pattern_matcher.AbstractPatternMatcher.extract_fixtures
:abstractmethod:

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPatternMatcher.extract_fixtures
:parser: myst
```

````

````{py:method} get_matches(text: str, fixtures: collections.abc.Mapping[str, typing.Any]) -> collections.abc.Mapping[str, typing.Any] | None
:canonical: tursu.runtime.pattern_matcher.AbstractPatternMatcher.get_matches
:abstractmethod:

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPatternMatcher.get_matches
:parser: myst
```

````

````{py:method} hightlight(matches: collections.abc.Mapping[str, typing.Any], color: str = '\x1b[36m', reset: str = '\x1b[0m') -> str
:canonical: tursu.runtime.pattern_matcher.AbstractPatternMatcher.hightlight
:abstractmethod:

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPatternMatcher.hightlight
:parser: myst
```

````

````{py:method} match(text: str) -> bool
:canonical: tursu.runtime.pattern_matcher.AbstractPatternMatcher.match
:abstractmethod:

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPatternMatcher.match
:parser: myst
```

````

````{py:attribute} pattern
:canonical: tursu.runtime.pattern_matcher.AbstractPatternMatcher.pattern
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPatternMatcher.pattern
:parser: myst
```

````

````{py:attribute} signature
:canonical: tursu.runtime.pattern_matcher.AbstractPatternMatcher.signature
:type: inspect.Signature
:value: >
   None

```{autodoc2-docstring} tursu.runtime.pattern_matcher.AbstractPatternMatcher.signature
:parser: myst
```

````

`````

`````{py:class} DefaultPatternMatcher(pattern: str, signature: inspect.Signature)
:canonical: tursu.runtime.pattern_matcher.DefaultPatternMatcher

Bases: {py:obj}`tursu.runtime.pattern_matcher.RegexBasePattern`

```{autodoc2-docstring} tursu.runtime.pattern_matcher.DefaultPatternMatcher
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.pattern_matcher.DefaultPatternMatcher.__init__
:parser: myst
```

````{py:method} hightlight(matches: collections.abc.Mapping[str, typing.Any], color: str = '\x1b[36m', reset: str = '\x1b[0m') -> str
:canonical: tursu.runtime.pattern_matcher.DefaultPatternMatcher.hightlight

```{autodoc2-docstring} tursu.runtime.pattern_matcher.DefaultPatternMatcher.hightlight
:parser: myst
```

````

`````

````{py:exception} PatternError()
:canonical: tursu.runtime.pattern_matcher.PatternError

Bases: {py:obj}`RuntimeError`

```{autodoc2-docstring} tursu.runtime.pattern_matcher.PatternError
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.pattern_matcher.PatternError.__init__
:parser: myst
```

````

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

`````{py:class} RegExPatternMatcher(pattern: str, signature: inspect.Signature)
:canonical: tursu.runtime.pattern_matcher.RegExPatternMatcher

Bases: {py:obj}`tursu.runtime.pattern_matcher.RegexBasePattern`

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegExPatternMatcher
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegExPatternMatcher.__init__
:parser: myst
```

````{py:method} hightlight(matches: collections.abc.Mapping[str, typing.Any], color: str = '\x1b[36m', reset: str = '\x1b[0m') -> str
:canonical: tursu.runtime.pattern_matcher.RegExPatternMatcher.hightlight

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegExPatternMatcher.hightlight
:parser: myst
```

````

`````

`````{py:class} RegexBasePattern(pattern: str, signature: inspect.Signature)
:canonical: tursu.runtime.pattern_matcher.RegexBasePattern

Bases: {py:obj}`tursu.runtime.pattern_matcher.AbstractPatternMatcher`

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegexBasePattern
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegexBasePattern.__init__
:parser: myst
```

````{py:method} extract_fixtures(text: str) -> collections.abc.Mapping[str, typing.Any] | None
:canonical: tursu.runtime.pattern_matcher.RegexBasePattern.extract_fixtures

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegexBasePattern.extract_fixtures
:parser: myst
```

````

````{py:method} get_matches(text: str, fixtures: collections.abc.Mapping[str, typing.Any]) -> collections.abc.Mapping[str, typing.Any] | None
:canonical: tursu.runtime.pattern_matcher.RegexBasePattern.get_matches

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegexBasePattern.get_matches
:parser: myst
```

````

````{py:method} match(text: str) -> bool
:canonical: tursu.runtime.pattern_matcher.RegexBasePattern.match

````

````{py:attribute} re_pattern
:canonical: tursu.runtime.pattern_matcher.RegexBasePattern.re_pattern
:type: re.Pattern[str]
:value: >
   None

```{autodoc2-docstring} tursu.runtime.pattern_matcher.RegexBasePattern.re_pattern
:parser: myst
```

````

`````

````{py:function} cast_to_annotation(value: str, annotation: type[int | float | bool | str | datetime.date | datetime.datetime | enum.Enum]) -> int | float | bool | str | datetime.date | datetime.datetime | enum.Enum
:canonical: tursu.runtime.pattern_matcher.cast_to_annotation

```{autodoc2-docstring} tursu.runtime.pattern_matcher.cast_to_annotation
:parser: myst
```
````
