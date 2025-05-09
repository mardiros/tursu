Feature: Discover Scenario

  Background:
    Given a user Bob

  Rule: I write a wip test

    @wip
    Scenario: I can find scenario based on tag
      When Bob creates a mailbox bob@alice.net
      Then Bob sees a mailbox bob@alice.net
      And the mailbox bob@alice.net "Welcome Bob" message is
        """
        ...
        """
      And the raw API for Bob is responding
        """json
        [{"email": "bob@alice.net", "subject": "Welcome Bob", "body": "..."}]
        """
      And the API for Bob is responding
        """json
        [{"email": "bob@alice.net", "subject": "Welcome Bob", "body": "..."}]
        """
      And the users raw dataset is
        | username | mailbox       |
        | Bob      | bob@alice.net |
      And the users dataset is
        | username | mailbox       |
        | Bob      | bob@alice.net |
