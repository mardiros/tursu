from collections.abc import Sequence
from pathlib import Path
from typing import Annotated, Any, Literal

from gherkin import Parser
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator


def sanitize(value: Any) -> str:
    return value.strip().lower() if isinstance(value, str) else value


GherkinKeyword = Annotated[
    Literal["feature", "scenario", "background", "given", "when", "then", "and", "but"],
    BeforeValidator(sanitize),
]


class GherkinLocation(BaseModel):
    line: int
    column: int | None = Field(default=None)


class GherkinComment(BaseModel):
    location: GherkinLocation
    text: str


class GherkinTag(BaseModel):
    id: str
    location: GherkinLocation
    name: str


class GherkinCell(BaseModel):
    location: GherkinLocation
    value: str


class GherkinTableRow(BaseModel):
    id: str
    location: GherkinLocation
    cells: Sequence[GherkinCell]


class GherkinDataTable(BaseModel):
    location: GherkinLocation
    rows: Sequence[GherkinTableRow]


class GherkinDocString(BaseModel):
    location: GherkinLocation
    content: str
    delimiter: str
    media_type: str | None = Field(alias="mediaType")


class GherkinStep(BaseModel):
    id: str
    location: GherkinLocation
    keyword: GherkinKeyword
    text: str
    keyword_type: str = Field(alias="keywordType")
    data_table: GherkinDataTable | None = Field(default=None, alias="data_table")
    docstring: GherkinDocString | None = Field(default=None, alias="docstring")


class GherkinBackground(BaseModel):
    id: str
    location: GherkinLocation
    keyword: GherkinKeyword
    name: str
    description: str
    steps: Sequence[GherkinStep]


class GherkinExamples(BaseModel):
    id: str
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    keyword: GherkinKeyword
    name: str
    description: str
    table_header: GherkinTableRow = Field(alias="tableHeader")
    table_body: Sequence[GherkinTableRow] = Field(alias="tableBody")


class GherkinScenario(BaseModel):
    id: str
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    keyword: GherkinKeyword
    name: str
    description: str
    steps: Sequence[GherkinStep]
    examples: Sequence[GherkinExamples]


class GherkinBackgroundEnvelope(BaseModel):
    background: GherkinBackground


class GherkinScenarioEnvelope(BaseModel):
    scenario: GherkinScenario


class GherkinRuleEnvelope(BaseModel):
    rule: "GherkinRule"


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


class GherkinFeature(BaseModel):
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    language: str
    keyword: GherkinKeyword
    name: str
    description: str
    children: Sequence[GherkinEnvelope]


class GherkinDocument(BaseModel):
    name: str
    filepath: Path
    feature: GherkinFeature
    comments: Sequence[GherkinComment]

    @classmethod
    def from_file(cls, file: Path) -> "GherkinDocument":
        return GherkinDocument(
            name=file.name[: -len(".feature")],
            filepath=file,
            **Parser().parse(file.read_text()),  # type: ignore
        )
