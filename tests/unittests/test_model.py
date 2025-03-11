from tursu.domain.model.gherkin import GherkinDocument


def test_model(doc: GherkinDocument):
    docdict = doc.model_dump(exclude_unset=True)
    assert doc.name == "scenario"
    assert docdict["feature"] == {
        "children": [
            {
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
            },
            {
                "scenario": {
                    "description": "",
                    "id": "7",
                    "keyword": "scenario",
                    "location": {
                        "column": 3,
                        "line": 7,
                    },
                    "name": "I can find scenario based on tag",
                    "steps": [
                        {
                            "id": "2",
                            "keyword": "when",
                            "keyword_type": "Action",
                            "location": {
                                "column": 5,
                                "line": 8,
                            },
                            "text": "Bob create a mailbox bob@alice.net",
                        },
                        {
                            "id": "3",
                            "keyword": "then",
                            "keyword_type": "Outcome",
                            "location": {
                                "column": 5,
                                "line": 9,
                            },
                            "text": "I see a mailbox bob@alice.net for Bob",
                        },
                        {
                            "doc_string": {
                                "content": "...",
                                "delimiter": '"""',
                                "location": {
                                    "column": 7,
                                    "line": 11,
                                },
                            },
                            "id": "4",
                            "keyword": "and",
                            "keyword_type": "Conjunction",
                            "location": {
                                "column": 5,
                                "line": 10,
                            },
                            "text": 'the mailbox bob@alice.net "Welcome Bob" message '
                            "is",
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
                                    "line": 15,
                                },
                                "media_type": "json",
                            },
                            "id": "5",
                            "keyword": "and",
                            "keyword_type": "Conjunction",
                            "location": {
                                "column": 5,
                                "line": 14,
                            },
                            "text": "the API for bob@alice.net respond",
                        },
                    ],
                    "tags": [
                        {
                            "id": "6",
                            "location": {
                                "column": 3,
                                "line": 6,
                            },
                            "name": "@wip",
                        },
                    ],
                },
            },
        ],
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
