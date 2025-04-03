"""
Gherkin feature files as DOM objects.

Turşu use the gherkin-official package to parse file, with a pydantic
layer in order to works with typed object instead of typed dict.

It also clean up keywords and add representation for the output.
"""

import ast
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Annotated, Any, Literal

from gherkin import Parser
from pydantic import BaseModel, Field, model_validator
from pydantic.functional_validators import BeforeValidator


def sanitize(value: Any) -> str:
    return value.strip().title() if isinstance(value, str) else value


GherkinKeyword = Annotated[
    Literal[
        "Feature",
        "Scenario",
        "Scenario Outline",
        "Examples",
        "Background",
        "Rule",
        "Given",
        "When",
        "Then",
        "And",
        "But",
    ],
    BeforeValidator(sanitize),
]

GherkinScenarioKeyword = Annotated[Literal["Scenario"], BeforeValidator(sanitize)]
GherkinScenarioOutlineKeyword = Annotated[
    Literal["Scenario Outline"], BeforeValidator(sanitize)
]

StrippedWhitespace = Annotated[
    str, BeforeValidator(lambda value: value.strip() if value else value)
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
    name: Annotated[
        str,
        BeforeValidator(lambda value: value.strip().lstrip("@") if value else value),
    ]


class GherkinCell(BaseModel):
    location: GherkinLocation
    value: str


class GherkinTableRow(BaseModel):
    id: str
    location: GherkinLocation
    cells: Sequence[GherkinCell]


class GherkinDataTable(BaseModel):
    location: GherkinLocation
    rows: list[GherkinTableRow]


class GherkinDocString(BaseModel):
    location: GherkinLocation
    content: str | Mapping[str, Any] | Sequence[Any]
    delimiter: str
    media_type: str | None = Field(default=None, alias="mediaType")

    @model_validator(mode="after")
    def check_passwords_match(self) -> "GherkinDocString":
        if not isinstance(self.content, str):
            return self
        match self.media_type:
            case "json":
                self.content = json.loads(self.content)
            case "python":
                self.content = ast.literal_eval(self.content)
            case _:
                ...
        return self


class GherkinStep(BaseModel):
    id: str
    location: GherkinLocation
    keyword: GherkinKeyword
    text: str
    keyword_type: str = Field(alias="keywordType")
    data_table: GherkinDataTable | None = Field(default=None, alias="dataTable")
    doc_string: GherkinDocString | None = Field(default=None, alias="docString")

    def __repr__(self) -> str:
        return f"{self.keyword} {self.text}"


class GherkinBackground(BaseModel):
    id: str
    location: GherkinLocation
    keyword: GherkinKeyword
    name: StrippedWhitespace
    description: StrippedWhitespace
    steps: Sequence[GherkinStep]

    def __repr__(self) -> str:
        return f"Background: {self.name}"


class GherkinExamples(BaseModel):
    id: str
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    keyword: GherkinKeyword
    name: StrippedWhitespace
    description: StrippedWhitespace
    table_header: GherkinTableRow = Field(alias="tableHeader")
    table_body: Sequence[GherkinTableRow] = Field(alias="tableBody")


class GherkinScenario(BaseModel):
    id: str
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    keyword: GherkinScenarioKeyword
    name: StrippedWhitespace
    description: StrippedWhitespace
    steps: Sequence[GherkinStep]

    def __repr__(self) -> str:
        return f"🎬 Scenario: {self.name}"


class GherkinScenarioOutline(BaseModel):
    id: str
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    keyword: GherkinScenarioOutlineKeyword
    name: StrippedWhitespace
    description: StrippedWhitespace
    steps: Sequence[GherkinStep]
    examples: Sequence[GherkinExamples]

    def __repr__(self) -> str:
        return f"🎬 Scenario Outline: {self.name}"


class GherkinBackgroundEnvelope(BaseModel):
    background: GherkinBackground


class GherkinScenarioEnvelope(BaseModel):
    scenario: GherkinScenario | GherkinScenarioOutline


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
    name: StrippedWhitespace
    description: StrippedWhitespace
    children: Sequence[GherkinEnvelope]

    def __repr__(self) -> str:
        return f"🔹 Rule: {self.name}"


class GherkinFeature(BaseModel):
    location: GherkinLocation
    tags: Sequence[GherkinTag]
    language: str
    keyword: GherkinKeyword
    name: StrippedWhitespace
    description: StrippedWhitespace
    children: Sequence[GherkinEnvelope]

    def __repr__(self) -> str:
        return f"🥒 Feature: {self.name}"


class GherkinDocument(BaseModel):
    name: StrippedWhitespace
    filepath: Path
    feature: GherkinFeature
    comments: Sequence[GherkinComment]

    @classmethod
    def from_file(cls, file: Path) -> "GherkinDocument":
        """
        Parse .scenario file from the given path and build the gherkin document.

        :param file: path on disk to the scenario file.
        """
        official_doc = Parser().parse(file.read_text())
        return GherkinDocument(
            name=file.name[: -len(".feature")],
            filepath=file,
            **official_doc,  # type: ignore
        )

    def __repr__(self) -> str:
        return f"📄 Document: {self.name}.feature"


class Stack(BaseModel):
    value: list[BaseModel]
