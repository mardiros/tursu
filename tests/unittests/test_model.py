from tursu.domain.model.gherkin import GherkinDocument


def test_model(doc: GherkinDocument):
    docdict = doc.model_dump(exclude_unset=True)
    assert doc.name == "scenario"
    childrens = docdict["feature"].pop("children")
    assert docdict["feature"] == {
        "description": "",
        "keyword": "feature",
        "language": "en",
        "location": {
            "column": 1,
            "line": 1,
        },
        "name": "Discover Scenario",
        "tags": [],
    }
    assert len(childrens) == 2
    assert childrens[0] == {
        "background": {
            "description": "",
            "id": "1",
            "keyword": "background",
            "location": {
                "column": 3,
                "line": 3,
            },
            "name": "",
            "steps": [
                {
                    "id": "0",
                    "keyword": "given",
                    "keyword_type": "Context",
                    "location": {
                        "column": 5,
                        "line": 4,
                    },
                    "text": "a user Bob",
                },
            ],
        },
    }

    rules_children = childrens[1]["rule"].pop("children")

    assert childrens[1]["rule"] == {
        "description": "",
        "id": "8",
        "keyword": "rule",
        "location": {
            "column": 1,
            "line": 6,
        },
        "name": "I write a wip test",
        "tags": [],
    }

    assert len(rules_children) == 1
    assert rules_children[0]["scenario"] == {
        "description": "",
        "id": "7",
        "keyword": "scenario",
        "location": {
            "column": 3,
            "line": 9,
        },
        "name": "I can find scenario based on tag",
        "steps": [
            {
                "id": "2",
                "keyword": "when",
                "keyword_type": "Action",
                "location": {
                    "column": 5,
                    "line": 10,
                },
                "text": "Bob create a mailbox bob@alice.net",
            },
            {
                "id": "3",
                "keyword": "then",
                "keyword_type": "Outcome",
                "location": {
                    "column": 5,
                    "line": 11,
                },
                "text": "I see a mailbox bob@alice.net for Bob",
            },
            {
                "doc_string": {
                    "content": "...",
                    "delimiter": '"""',
                    "location": {
                        "column": 7,
                        "line": 13,
                    },
                },
                "id": "4",
                "keyword": "and",
                "keyword_type": "Conjunction",
                "location": {
                    "column": 5,
                    "line": 12,
                },
                "text": 'the mailbox bob@alice.net "Welcome Bob" message is',
            },
            {
                "doc_string": {
                    "content": [
                        {
                            "body": "...",
                            "email": "bob@alice.net",
                            "subject": "Welcome Bob",
                        },
                    ],
                    "delimiter": '"""',
                    "location": {
                        "column": 7,
                        "line": 17,
                    },
                    "media_type": "json",
                },
                "id": "5",
                "keyword": "and",
                "keyword_type": "Conjunction",
                "location": {
                    "column": 5,
                    "line": 16,
                },
                "text": "the API for bob@alice.net respond",
            },
        ],
        "tags": [
            {
                "id": "6",
                "location": {
                    "column": 3,
                    "line": 8,
                },
                "name": "wip",
            },
        ],
    }


def test_model_outlined(outline_doc: GherkinDocument):
    docdict = outline_doc.model_dump(exclude_unset=True)
    assert outline_doc.name == "scenario_outline"
    childrens = docdict["feature"].pop("children")
    assert docdict["feature"] == {
        "description": "This feature is complex and require a comment.",
        "keyword": "feature",
        "language": "en",
        "location": {
            "column": 1,
            "line": 1,
        },
        "name": "Discover Scenario Outline",
        "tags": [],
    }

    assert len(childrens) == 2
    assert childrens[0] == {
        "background": {
            "description": "",
            "id": "1",
            "keyword": "background",
            "location": {
                "column": 3,
                "line": 4,
            },
            "name": "",
            "steps": [
                {
                    "id": "0",
                    "keyword": "given",
                    "keyword_type": "Context",
                    "location": {
                        "column": 5,
                        "line": 5,
                    },
                    "text": "a user momo",
                },
            ],
        },
    }

    assert (
        childrens[1]["scenario"]["description"]
        == "This scenario is complex and require a comment."
    )

    assert childrens[1]["scenario"]["steps"] == [
        {
            "id": "2",
            "keyword": "given",
            "keyword_type": "Context",
            "location": {"column": 5, "line": 11},
            "text": "a user <username>",
        },
        {
            "id": "3",
            "keyword": "when",
            "keyword_type": "Action",
            "location": {"column": 5, "line": 12},
            "text": "<username> create a mailbox <email>",
        },
        {
            "id": "4",
            "keyword": "then",
            "keyword_type": "Outcome",
            "location": {"column": 5, "line": 13},
            "text": "I see a mailbox <email> for <username>",
        },
    ]

    assert childrens[1]["scenario"]["examples"] == [
        {
            "description": "",
            "id": "8",
            "keyword": "examples",
            "location": {"column": 5, "line": 15},
            "name": "",
            "table_body": [
                {
                    "cells": [
                        {
                            "location": {"column": 9, "line": 17},
                            "value": "Alice",
                        },
                        {
                            "location": {"column": 20, "line": 17},
                            "value": "alice@alice.net",
                        },
                    ],
                    "id": "6",
                    "location": {"column": 7, "line": 17},
                },
                {
                    "cells": [
                        {
                            "location": {"column": 9, "line": 18},
                            "value": "Bob",
                        },
                        {
                            "location": {"column": 20, "line": 18},
                            "value": "bob@bob.net",
                        },
                    ],
                    "id": "7",
                    "location": {"column": 7, "line": 18},
                },
            ],
            "table_header": {
                "cells": [
                    {
                        "location": {"column": 9, "line": 16},
                        "value": "username",
                    },
                    {
                        "location": {"column": 20, "line": 16},
                        "value": "email",
                    },
                ],
                "id": "5",
                "location": {"column": 7, "line": 16},
            },
            "tags": [],
        },
    ]
