from tursu.domain.model.gherkin import GherkinDocument


def test_model(doc: GherkinDocument):
    assert doc.model_dump(exclude_unset=True) == {
        "name": "scenario",
        "feature": {
            "tags": [],
            "location": {"line": 1, "column": 1},
            "language": "en",
            "keyword": "feature",
            "name": "Discover Scenario",
            "description": "",
            "children": [
                {
                    "scenario": {
                        "id": "5",
                        "tags": [
                            {
                                "id": "4",
                                "location": {"line": 3, "column": 3},
                                "name": "@wip",
                            }
                        ],
                        "location": {"line": 4, "column": 3},
                        "keyword": "scenario",
                        "name": "I can find scenario based on tag",
                        "description": "",
                        "steps": [
                            {
                                "id": "0",
                                "location": {"line": 5, "column": 5},
                                "keyword": "given",
                                "keyword_type": "Context",
                                "text": "a user Bob",
                            },
                            {
                                "id": "1",
                                "location": {"line": 6, "column": 5},
                                "keyword": "when",
                                "keyword_type": "Action",
                                "text": "Bob create a mailbox bob@alice.net",
                            },
                            {
                                "id": "2",
                                "location": {"line": 7, "column": 5},
                                "keyword": "then",
                                "keyword_type": "Outcome",
                                "text": "I see a mailbox bob@alice.net for Bob",
                            },
                            {
                                "id": "3",
                                "location": {"line": 8, "column": 5},
                                "keyword": "and",
                                "keyword_type": "Conjunction",
                                "text": 'the mailbox bob@alice.net contains "Welcome Bob"',
                            },
                        ],
                        "examples": [],
                    }
                }
            ],
        },
        "comments": [],
        "filepath": doc.filepath,
    }
