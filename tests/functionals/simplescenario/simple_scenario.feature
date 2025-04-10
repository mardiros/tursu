Feature: Discover Scenario

  Scenario: I can find scenario based on tag
    Given a user Bob
    When Bob creates a mailbox bob@alice.net
    Then Bob sees a mailbox bob@alice.net
    And the mailbox bob@alice.net contains "Welcome Bob"
