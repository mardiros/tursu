# {py:mod}`tursu.domain.model.gherkin`

```{py:module} tursu.domain.model.gherkin
```

```{autodoc2-docstring} tursu.domain.model.gherkin
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`GherkinBackground <tursu.domain.model.gherkin.GherkinBackground>`
  -
* - {py:obj}`GherkinBackgroundEnvelope <tursu.domain.model.gherkin.GherkinBackgroundEnvelope>`
  -
* - {py:obj}`GherkinCell <tursu.domain.model.gherkin.GherkinCell>`
  -
* - {py:obj}`GherkinComment <tursu.domain.model.gherkin.GherkinComment>`
  -
* - {py:obj}`GherkinDataTable <tursu.domain.model.gherkin.GherkinDataTable>`
  -
* - {py:obj}`GherkinDocString <tursu.domain.model.gherkin.GherkinDocString>`
  -
* - {py:obj}`GherkinDocument <tursu.domain.model.gherkin.GherkinDocument>`
  -
* - {py:obj}`GherkinExamples <tursu.domain.model.gherkin.GherkinExamples>`
  -
* - {py:obj}`GherkinFeature <tursu.domain.model.gherkin.GherkinFeature>`
  -
* - {py:obj}`GherkinLocation <tursu.domain.model.gherkin.GherkinLocation>`
  -
* - {py:obj}`GherkinRule <tursu.domain.model.gherkin.GherkinRule>`
  -
* - {py:obj}`GherkinRuleEnvelope <tursu.domain.model.gherkin.GherkinRuleEnvelope>`
  -
* - {py:obj}`GherkinScenario <tursu.domain.model.gherkin.GherkinScenario>`
  -
* - {py:obj}`GherkinScenarioEnvelope <tursu.domain.model.gherkin.GherkinScenarioEnvelope>`
  -
* - {py:obj}`GherkinStep <tursu.domain.model.gherkin.GherkinStep>`
  -
* - {py:obj}`GherkinTableRow <tursu.domain.model.gherkin.GherkinTableRow>`
  -
* - {py:obj}`GherkinTag <tursu.domain.model.gherkin.GherkinTag>`
  -
````

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`sanitize <tursu.domain.model.gherkin.sanitize>`
  - ```{autodoc2-docstring} tursu.domain.model.gherkin.sanitize
    :parser: myst
    :summary:
    ```
````

### Data

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`GherkinEnvelope <tursu.domain.model.gherkin.GherkinEnvelope>`
  - ```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinEnvelope
    :parser: myst
    :summary:
    ```
* - {py:obj}`GherkinKeyword <tursu.domain.model.gherkin.GherkinKeyword>`
  - ```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinKeyword
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} GherkinBackground(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinBackground

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} description
:canonical: tursu.domain.model.gherkin.GherkinBackground.description
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinBackground.description
:parser: myst
```

````

````{py:attribute} id
:canonical: tursu.domain.model.gherkin.GherkinBackground.id
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinBackground.id
:parser: myst
```

````

````{py:attribute} keyword
:canonical: tursu.domain.model.gherkin.GherkinBackground.keyword
:type: tursu.domain.model.gherkin.GherkinKeyword
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinBackground.keyword
:parser: myst
```

````

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinBackground.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinBackground.location
:parser: myst
```

````

````{py:attribute} name
:canonical: tursu.domain.model.gherkin.GherkinBackground.name
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinBackground.name
:parser: myst
```

````

````{py:attribute} steps
:canonical: tursu.domain.model.gherkin.GherkinBackground.steps
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinStep]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinBackground.steps
:parser: myst
```

````

`````

`````{py:class} GherkinBackgroundEnvelope(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinBackgroundEnvelope

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} background
:canonical: tursu.domain.model.gherkin.GherkinBackgroundEnvelope.background
:type: tursu.domain.model.gherkin.GherkinBackground
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinBackgroundEnvelope.background
:parser: myst
```

````

`````

`````{py:class} GherkinCell(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinCell

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinCell.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinCell.location
:parser: myst
```

````

````{py:attribute} value
:canonical: tursu.domain.model.gherkin.GherkinCell.value
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinCell.value
:parser: myst
```

````

`````

`````{py:class} GherkinComment(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinComment

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinComment.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinComment.location
:parser: myst
```

````

````{py:attribute} text
:canonical: tursu.domain.model.gherkin.GherkinComment.text
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinComment.text
:parser: myst
```

````

`````

`````{py:class} GherkinDataTable(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinDataTable

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinDataTable.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDataTable.location
:parser: myst
```

````

````{py:attribute} rows
:canonical: tursu.domain.model.gherkin.GherkinDataTable.rows
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinTableRow]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDataTable.rows
:parser: myst
```

````

`````

`````{py:class} GherkinDocString(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinDocString

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} content
:canonical: tursu.domain.model.gherkin.GherkinDocString.content
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDocString.content
:parser: myst
```

````

````{py:attribute} delimiter
:canonical: tursu.domain.model.gherkin.GherkinDocString.delimiter
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDocString.delimiter
:parser: myst
```

````

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinDocString.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDocString.location
:parser: myst
```

````

````{py:attribute} media_type
:canonical: tursu.domain.model.gherkin.GherkinDocString.media_type
:type: str | None
:value: >
   'Field(...)'

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDocString.media_type
:parser: myst
```

````

`````

`````{py:class} GherkinDocument(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinDocument

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} comments
:canonical: tursu.domain.model.gherkin.GherkinDocument.comments
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinComment]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDocument.comments
:parser: myst
```

````

````{py:attribute} feature
:canonical: tursu.domain.model.gherkin.GherkinDocument.feature
:type: tursu.domain.model.gherkin.GherkinFeature
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDocument.feature
:parser: myst
```

````

````{py:attribute} filepath
:canonical: tursu.domain.model.gherkin.GherkinDocument.filepath
:type: pathlib.Path
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDocument.filepath
:parser: myst
```

````

````{py:method} from_file(file: pathlib.Path) -> tursu.domain.model.gherkin.GherkinDocument
:canonical: tursu.domain.model.gherkin.GherkinDocument.from_file
:classmethod:

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDocument.from_file
:parser: myst
```

````

````{py:attribute} name
:canonical: tursu.domain.model.gherkin.GherkinDocument.name
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinDocument.name
:parser: myst
```

````

`````

````{py:data} GherkinEnvelope
:canonical: tursu.domain.model.gherkin.GherkinEnvelope
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinEnvelope
:parser: myst
```

````

`````{py:class} GherkinExamples(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinExamples

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} description
:canonical: tursu.domain.model.gherkin.GherkinExamples.description
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinExamples.description
:parser: myst
```

````

````{py:attribute} id
:canonical: tursu.domain.model.gherkin.GherkinExamples.id
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinExamples.id
:parser: myst
```

````

````{py:attribute} keyword
:canonical: tursu.domain.model.gherkin.GherkinExamples.keyword
:type: tursu.domain.model.gherkin.GherkinKeyword
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinExamples.keyword
:parser: myst
```

````

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinExamples.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinExamples.location
:parser: myst
```

````

````{py:attribute} name
:canonical: tursu.domain.model.gherkin.GherkinExamples.name
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinExamples.name
:parser: myst
```

````

````{py:attribute} table_body
:canonical: tursu.domain.model.gherkin.GherkinExamples.table_body
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinTableRow]
:value: >
   'Field(...)'

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinExamples.table_body
:parser: myst
```

````

````{py:attribute} table_header
:canonical: tursu.domain.model.gherkin.GherkinExamples.table_header
:type: tursu.domain.model.gherkin.GherkinTableRow
:value: >
   'Field(...)'

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinExamples.table_header
:parser: myst
```

````

````{py:attribute} tags
:canonical: tursu.domain.model.gherkin.GherkinExamples.tags
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinTag]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinExamples.tags
:parser: myst
```

````

`````

`````{py:class} GherkinFeature(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinFeature

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} children
:canonical: tursu.domain.model.gherkin.GherkinFeature.children
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinEnvelope]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinFeature.children
:parser: myst
```

````

````{py:attribute} description
:canonical: tursu.domain.model.gherkin.GherkinFeature.description
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinFeature.description
:parser: myst
```

````

````{py:attribute} keyword
:canonical: tursu.domain.model.gherkin.GherkinFeature.keyword
:type: tursu.domain.model.gherkin.GherkinKeyword
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinFeature.keyword
:parser: myst
```

````

````{py:attribute} language
:canonical: tursu.domain.model.gherkin.GherkinFeature.language
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinFeature.language
:parser: myst
```

````

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinFeature.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinFeature.location
:parser: myst
```

````

````{py:attribute} name
:canonical: tursu.domain.model.gherkin.GherkinFeature.name
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinFeature.name
:parser: myst
```

````

````{py:attribute} tags
:canonical: tursu.domain.model.gherkin.GherkinFeature.tags
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinTag]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinFeature.tags
:parser: myst
```

````

`````

````{py:data} GherkinKeyword
:canonical: tursu.domain.model.gherkin.GherkinKeyword
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinKeyword
:parser: myst
```

````

`````{py:class} GherkinLocation(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinLocation

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} column
:canonical: tursu.domain.model.gherkin.GherkinLocation.column
:type: int | None
:value: >
   'Field(...)'

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinLocation.column
:parser: myst
```

````

````{py:attribute} line
:canonical: tursu.domain.model.gherkin.GherkinLocation.line
:type: int
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinLocation.line
:parser: myst
```

````

`````

`````{py:class} GherkinRule(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinRule

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} children
:canonical: tursu.domain.model.gherkin.GherkinRule.children
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinEnvelope]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinRule.children
:parser: myst
```

````

````{py:attribute} description
:canonical: tursu.domain.model.gherkin.GherkinRule.description
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinRule.description
:parser: myst
```

````

````{py:attribute} id
:canonical: tursu.domain.model.gherkin.GherkinRule.id
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinRule.id
:parser: myst
```

````

````{py:attribute} keyword
:canonical: tursu.domain.model.gherkin.GherkinRule.keyword
:type: tursu.domain.model.gherkin.GherkinKeyword
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinRule.keyword
:parser: myst
```

````

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinRule.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinRule.location
:parser: myst
```

````

````{py:attribute} name
:canonical: tursu.domain.model.gherkin.GherkinRule.name
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinRule.name
:parser: myst
```

````

````{py:attribute} tags
:canonical: tursu.domain.model.gherkin.GherkinRule.tags
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinTag]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinRule.tags
:parser: myst
```

````

`````

`````{py:class} GherkinRuleEnvelope(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinRuleEnvelope

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} rule
:canonical: tursu.domain.model.gherkin.GherkinRuleEnvelope.rule
:type: GherkinRule
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinRuleEnvelope.rule
:parser: myst
```

````

`````

`````{py:class} GherkinScenario(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinScenario

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} description
:canonical: tursu.domain.model.gherkin.GherkinScenario.description
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinScenario.description
:parser: myst
```

````

````{py:attribute} examples
:canonical: tursu.domain.model.gherkin.GherkinScenario.examples
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinExamples]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinScenario.examples
:parser: myst
```

````

````{py:attribute} id
:canonical: tursu.domain.model.gherkin.GherkinScenario.id
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinScenario.id
:parser: myst
```

````

````{py:attribute} keyword
:canonical: tursu.domain.model.gherkin.GherkinScenario.keyword
:type: tursu.domain.model.gherkin.GherkinKeyword
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinScenario.keyword
:parser: myst
```

````

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinScenario.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinScenario.location
:parser: myst
```

````

````{py:attribute} name
:canonical: tursu.domain.model.gherkin.GherkinScenario.name
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinScenario.name
:parser: myst
```

````

````{py:attribute} steps
:canonical: tursu.domain.model.gherkin.GherkinScenario.steps
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinStep]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinScenario.steps
:parser: myst
```

````

````{py:attribute} tags
:canonical: tursu.domain.model.gherkin.GherkinScenario.tags
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinTag]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinScenario.tags
:parser: myst
```

````

`````

`````{py:class} GherkinScenarioEnvelope(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinScenarioEnvelope

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} scenario
:canonical: tursu.domain.model.gherkin.GherkinScenarioEnvelope.scenario
:type: tursu.domain.model.gherkin.GherkinScenario
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinScenarioEnvelope.scenario
:parser: myst
```

````

`````

`````{py:class} GherkinStep(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinStep

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} data_table
:canonical: tursu.domain.model.gherkin.GherkinStep.data_table
:type: tursu.domain.model.gherkin.GherkinDataTable | None
:value: >
   'Field(...)'

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinStep.data_table
:parser: myst
```

````

````{py:attribute} docstring
:canonical: tursu.domain.model.gherkin.GherkinStep.docstring
:type: tursu.domain.model.gherkin.GherkinDocString | None
:value: >
   'Field(...)'

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinStep.docstring
:parser: myst
```

````

````{py:attribute} id
:canonical: tursu.domain.model.gherkin.GherkinStep.id
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinStep.id
:parser: myst
```

````

````{py:attribute} keyword
:canonical: tursu.domain.model.gherkin.GherkinStep.keyword
:type: tursu.domain.model.gherkin.GherkinKeyword
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinStep.keyword
:parser: myst
```

````

````{py:attribute} keyword_type
:canonical: tursu.domain.model.gherkin.GherkinStep.keyword_type
:type: str
:value: >
   'Field(...)'

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinStep.keyword_type
:parser: myst
```

````

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinStep.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinStep.location
:parser: myst
```

````

````{py:attribute} text
:canonical: tursu.domain.model.gherkin.GherkinStep.text
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinStep.text
:parser: myst
```

````

`````

`````{py:class} GherkinTableRow(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinTableRow

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} cells
:canonical: tursu.domain.model.gherkin.GherkinTableRow.cells
:type: collections.abc.Sequence[tursu.domain.model.gherkin.GherkinCell]
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinTableRow.cells
:parser: myst
```

````

````{py:attribute} id
:canonical: tursu.domain.model.gherkin.GherkinTableRow.id
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinTableRow.id
:parser: myst
```

````

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinTableRow.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinTableRow.location
:parser: myst
```

````

`````

`````{py:class} GherkinTag(/, **data: typing.Any)
:canonical: tursu.domain.model.gherkin.GherkinTag

Bases: {py:obj}`pydantic.BaseModel`

````{py:attribute} id
:canonical: tursu.domain.model.gherkin.GherkinTag.id
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinTag.id
:parser: myst
```

````

````{py:attribute} location
:canonical: tursu.domain.model.gherkin.GherkinTag.location
:type: tursu.domain.model.gherkin.GherkinLocation
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinTag.location
:parser: myst
```

````

````{py:attribute} name
:canonical: tursu.domain.model.gherkin.GherkinTag.name
:type: str
:value: >
   None

```{autodoc2-docstring} tursu.domain.model.gherkin.GherkinTag.name
:parser: myst
```

````

`````

````{py:function} sanitize(value: typing.Any) -> str
:canonical: tursu.domain.model.gherkin.sanitize

```{autodoc2-docstring} tursu.domain.model.gherkin.sanitize
:parser: myst
```
````
