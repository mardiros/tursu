import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Annotated, Any, Literal

from gherkin import Parser
from pydantic import BaseModel, Field, model_validator
from pydantic.functional_validators import BeforeValidator


def sanitize(value: Any) -> str:
    return value.strip().lower() if isinstance(value, str) else value


GherkinKeyword = Annotated[
    Literal[
        "feature",
        "scenario",
        "scenario outline",
        "examples",
        "background",
        "rule",
        "given",
        "when",
        "then",
        "and",
        "but",
    ],
    BeforeValidator(sanitize),
]

GherkinScenarioKeyword = Annotated[Literal["scenario"], BeforeValidator(sanitize)]
GherkinScenarioOutlineKeyword = Annotated[
    Literal["scenario outline"], BeforeValidator(sanitize)
]


class GherkinLocation(BaseModel):
    line: int
    column: int | None = Field(default=None)


class GherkinComment(BaseModel):
    location: GherkinLocation
    text: str

    def __repr__(self) -> str:
        return f"{self.text}"


class GherkinTag(BaseModel):
    id: str
    location: GherkinLocation
    name: str

    def __repr__(self) -> str:
        return f"{self.name}"


class GherkinCell(BaseModel):
    location: GherkinLocation
    value: str

    def __repr__(self) -> str:
        return f"{self.value}"


class GherkinTableRow(BaseModel):
    id: str
    location: GherkinLocation
    cells: Sequence[GherkinCell]

    def __repr__(self) -> str:
        return f"| {' | '.join(repr(self.cells))} |"


class GherkinDataTable(BaseModel):
    location: GherkinLocation
    rows: list[GherkinTableRow]

    def __repr__(self) -> str:
        return f"{'\n'.join(repr(self.rows))}"


class GherkinDocString(BaseModel):
    location: GherkinLocation
    content: str | Mapping[str, Any] | Sequence[Any]
    delimiter: str
    media_type: str | None = Field(default=None, alias="mediaType")

    @model_validator(mode="after")
    def check_passwords_match(self) -> "GherkinDocString":
        if self.media_type == "json":
            self.content = json.loads(self.content)  # type: ignore
        return self

    def __repr__(self) -> str:
        return f"{self.delimiter}{self.content}{self.delimiter}"


class GherkinStep(BaseModel):
    id: str
    location: GherkinLocation
    keyword: GherkinKeyword
    text: str
    keyword_type: str = Field(alias="keywordType")
    data_table: GherkinDataTable | None = Field(default=None, alias="dataTable")
    doc_string: GherkinDocString | None = Field(default=None, alias="docString")

    def __repr__(self) -> str:
        return f"{self.keyword.capitalize()} {self.text}"


class GherkinBackground(BaseModel):
    id: str
    location: GherkinLocation
    keyword: GherkinKeyword
    name: str
    description: str
    steps: Sequence[GherkinStep]

    def __repr__(self) -> str:
        return f"Background: {self.name}"


class GherkinExamples(BaseModel):
    id: str
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    keyword: GherkinKeyword
    name: str
    description: str
    table_header: GherkinTableRow = Field(alias="tableHeader")
    table_body: Sequence[GherkinTableRow] = Field(alias="tableBody")

    def __repr__(self) -> str:
        return f"Example: {self.name}"


class GherkinScenario(BaseModel):
    id: str
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    keyword: GherkinScenarioKeyword
    name: str
    description: str
    steps: Sequence[GherkinStep]

    def __repr__(self) -> str:
        return f"Scenario: {self.name}"


class GherkinScenarioOutline(BaseModel):
    id: str
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    keyword: GherkinScenarioOutlineKeyword
    name: str
    description: str
    steps: Sequence[GherkinStep]
    examples: Sequence[GherkinExamples]

    def __repr__(self) -> str:
        return f"Scenario Outline: {self.name}"


class GherkinBackgroundEnvelope(BaseModel):
    background: GherkinBackground

    def __repr__(self) -> str:
        return "BackgroundEnvelope"


class GherkinScenarioEnvelope(BaseModel):
    scenario: GherkinScenario | GherkinScenarioOutline

    def __repr__(self) -> str:
        return "ScenarioEnvelope"


class GherkinRuleEnvelope(BaseModel):
    rule: "GherkinRule"

    def __repr__(self) -> str:
        return "RuleEnvelope"


GherkinEnvelope = (
    GherkinBackgroundEnvelope | GherkinScenarioEnvelope | GherkinRuleEnvelope
)


class GherkinRule(BaseModel):
    id: str
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    keyword: GherkinKeyword
    name: str
    description: str
    children: Sequence[GherkinEnvelope]

    def __repr__(self) -> str:
        return f"Rule: {self.name}"


class GherkinFeature(BaseModel):
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    language: str
    keyword: GherkinKeyword
    name: str
    description: str
    children: Sequence[GherkinEnvelope]

    def __repr__(self) -> str:
        return f"Feature: {self.name}"


class GherkinDocument(BaseModel):
    name: str
    filepath: Path
    feature: GherkinFeature
    comments: Sequence[GherkinComment]

    @classmethod
    def from_file(cls, file: Path) -> "GherkinDocument":
        official_doc = Parser().parse(file.read_text())
        return GherkinDocument(
            name=file.name[: -len(".feature")],
            filepath=file,
            **official_doc,  # type: ignore
        )

    def __repr__(self) -> str:
        return f"Document: {self.name}.feature"
