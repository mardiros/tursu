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
                "name": "@wip",
            },
        ],
    }
