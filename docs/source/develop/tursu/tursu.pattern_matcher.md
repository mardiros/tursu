# {py:mod}`tursu.pattern_matcher`

```{py:module} tursu.pattern_matcher
```

```{autodoc2-docstring} tursu.pattern_matcher
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`AbstractPattern <tursu.pattern_matcher.AbstractPattern>`
  -
* - {py:obj}`AbstractPatternMatcher <tursu.pattern_matcher.AbstractPatternMatcher>`
  -
* - {py:obj}`DefaultPatternMatcher <tursu.pattern_matcher.DefaultPatternMatcher>`
  -
````

### API

`````{py:class} AbstractPattern(pattern: str)
:canonical: tursu.pattern_matcher.AbstractPattern

Bases: {py:obj}`abc.ABC`

````{py:method} get_matcher() -> type[tursu.pattern_matcher.AbstractPatternMatcher]
:canonical: tursu.pattern_matcher.AbstractPattern.get_matcher
:abstractmethod:
:classmethod:

```{autodoc2-docstring} tursu.pattern_matcher.AbstractPattern.get_matcher
:parser: myst
```

````

`````

`````{py:class} AbstractPatternMatcher(pattern: str, signature: inspect.Signature)
:canonical: tursu.pattern_matcher.AbstractPatternMatcher

Bases: {py:obj}`abc.ABC`

````{py:method} __eq__(other: typing.Any) -> bool
:canonical: tursu.pattern_matcher.AbstractPatternMatcher.__eq__

````

````{py:method} __repr__() -> str
:canonical: tursu.pattern_matcher.AbstractPatternMatcher.__repr__

````

````{py:method} __str__() -> str
:canonical: tursu.pattern_matcher.AbstractPatternMatcher.__str__

````

````{py:method} extract_fixtures(text: str) -> collections.abc.Mapping[str, typing.Any] | None
:canonical: tursu.pattern_matcher.AbstractPatternMatcher.extract_fixtures
:abstractmethod:

```{autodoc2-docstring} tursu.pattern_matcher.AbstractPatternMatcher.extract_fixtures
:parser: myst
```

````

````{py:method} get_matches(text: str, kwargs: collections.abc.Mapping[str, typing.Any]) -> collections.abc.Mapping[str, typing.Any] | None
:canonical: tursu.pattern_matcher.AbstractPatternMatcher.get_matches
:abstractmethod:

```{autodoc2-docstring} tursu.pattern_matcher.AbstractPatternMatcher.get_matches
:parser: myst
```

````

`````

`````{py:class} DefaultPatternMatcher(pattern: str, signature: inspect.Signature)
:canonical: tursu.pattern_matcher.DefaultPatternMatcher

Bases: {py:obj}`tursu.pattern_matcher.AbstractPatternMatcher`

````{py:method} extract_fixtures(text: str) -> collections.abc.Mapping[str, typing.Any] | None
:canonical: tursu.pattern_matcher.DefaultPatternMatcher.extract_fixtures

```{autodoc2-docstring} tursu.pattern_matcher.DefaultPatternMatcher.extract_fixtures
:parser: myst
```

````

````{py:method} get_matches(text: str, kwargs: collections.abc.Mapping[str, typing.Any]) -> collections.abc.Mapping[str, typing.Any] | None
:canonical: tursu.pattern_matcher.DefaultPatternMatcher.get_matches

```{autodoc2-docstring} tursu.pattern_matcher.DefaultPatternMatcher.get_matches
:parser: myst
```

````

`````
