from tursu.domain.model.gherkin import GherkinDocument


def test_model(doc: GherkinDocument):
    docdict = doc.model_dump(exclude_unset=True)
    assert doc.name == "login"
    childrens = docdict["feature"].pop("children")
    assert docdict["feature"] == {
        "description": "",
        "keyword": "Feature",
        "language": "en",
        "location": {
            "column": 1,
            "line": 1,
        },
        "name": "User sign in with their own password",
        "tags": [],
    }
    assert len(childrens) == 4


def test_model_background(doc: GherkinDocument):
    docdict = doc.model_dump(exclude_unset=True)
    childrens = docdict["feature"].pop("children")

    assert childrens[0] == {
        "background": {
            "description": "",
            "id": "4",
            "keyword": "Background",
            "location": {
                "column": 3,
                "line": 3,
            },
            "name": "",
            "steps": [
                {
                    "data_table": {
                        "location": {
                            "column": 7,
                            "line": 5,
                        },
                        "rows": [
                            {
                                "cells": [
                                    {
                                        "location": {
                                            "column": 9,
                                            "line": 5,
                                        },
                                        "value": "username",
                                    },
                                    {
                                        "location": {
                                            "column": 20,
                                            "line": 5,
                                        },
                                        "value": "password",
                                    },
                                ],
                                "id": "0",
                                "location": {
                                    "column": 7,
                                    "line": 5,
                                },
                            },
                            {
                                "cells": [
                                    {
                                        "location": {
                                            "column": 9,
                                            "line": 6,
                                        },
                                        "value": "Bob",
                                    },
                                    {
                                        "location": {
                                            "column": 20,
                                            "line": 6,
                                        },
                                        "value": "dumbsecret",
                                    },
                                ],
                                "id": "1",
                                "location": {
                                    "column": 7,
                                    "line": 6,
                                },
                            },
                            {
                                "cells": [
                                    {
                                        "location": {
                                            "column": 9,
                                            "line": 7,
                                        },
                                        "value": "Alice",
                                    },
                                    {
                                        "location": {
                                            "column": 20,
                                            "line": 7,
                                        },
                                        "value": "anothersecret",
                                    },
                                ],
                                "id": "2",
                                "location": {
                                    "column": 7,
                                    "line": 7,
                                },
                            },
                        ],
                    },
                    "id": "3",
                    "keyword": "Given",
                    "keyword_type": "Context",
                    "location": {
                        "column": 5,
                        "line": 4,
                    },
                    "text": "a set of users:",
                },
            ],
        },
    }


def test_model_scenario(doc: GherkinDocument):
    docdict = doc.model_dump(exclude_unset=True)
    childrens = docdict["feature"].pop("children")

    assert childrens[1] == {
        "scenario": {
            "description": "",
            "id": "7",
            "keyword": "Scenario",
            "location": {
                "column": 3,
                "line": 9,
            },
            "name": "User can login",
            "steps": [
                {
                    "id": "5",
                    "keyword": "When",
                    "keyword_type": "Action",
                    "location": {
                        "column": 5,
                        "line": 10,
                    },
                    "text": "Bob signs in with password dumbsecret",
                },
                {
                    "id": "6",
                    "keyword": "Then",
                    "keyword_type": "Outcome",
                    "location": {
                        "column": 5,
                        "line": 11,
                    },
                    "text": "the user is connected with username Bob",
                },
            ],
            "tags": [],
        },
    }


def test_model_outlined(doc: GherkinDocument):
    docdict = doc.model_dump(exclude_unset=True)
    childrens = docdict["feature"].pop("children")
    assert childrens[3] == {
        "scenario": {
            "description": "",
            "examples": [
                {
                    "description": "",
                    "id": "16",
                    "keyword": "Examples",
                    "location": {
                        "column": 5,
                        "line": 21,
                    },
                    "name": "",
                    "table_body": [
                        {
                            "cells": [
                                {
                                    "location": {
                                        "column": 9,
                                        "line": 23,
                                    },
                                    "value": "Bob",
                                },
                                {
                                    "location": {
                                        "column": 20,
                                        "line": 23,
                                    },
                                    "value": "anothersecret",
                                },
                            ],
                            "id": "14",
                            "location": {
                                "column": 7,
                                "line": 23,
                            },
                        },
                        {
                            "cells": [
                                {
                                    "location": {
                                        "column": 9,
                                        "line": 24,
                                    },
                                    "value": "Alice",
                                },
                                {
                                    "location": {
                                        "column": 20,
                                        "line": 24,
                                    },
                                    "value": "dumbsecret",
                                },
                            ],
                            "id": "15",
                            "location": {
                                "column": 7,
                                "line": 24,
                            },
                        },
                    ],
                    "table_header": {
                        "cells": [
                            {
                                "location": {
                                    "column": 9,
                                    "line": 22,
                                },
                                "value": "username",
                            },
                            {
                                "location": {
                                    "column": 20,
                                    "line": 22,
                                },
                                "value": "password",
                            },
                        ],
                        "id": "13",
                        "location": {
                            "column": 7,
                            "line": 22,
                        },
                    },
                    "tags": [],
                },
            ],
            "id": "17",
            "keyword": "Scenario Outline",
            "location": {
                "column": 3,
                "line": 17,
            },
            "name": "User can't login with someone else username",
            "steps": [
                {
                    "id": "11",
                    "keyword": "When",
                    "keyword_type": "Action",
                    "location": {
                        "column": 5,
                        "line": 18,
                    },
                    "text": "<username> signs in with password <password>",
                },
                {
                    "id": "12",
                    "keyword": "Then",
                    "keyword_type": "Outcome",
                    "location": {
                        "column": 5,
                        "line": 19,
                    },
                    "text": "the user is not connected",
                },
            ],
            "tags": [],
        }
    }
