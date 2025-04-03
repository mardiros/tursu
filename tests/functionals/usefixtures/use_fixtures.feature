Feature: Use pytest fixtures in step tags

  Scenario: I can find scenario based on tag
    Given a user Bob
    When Bob create a mailbox bob@alice.net
    Then Bob see a mailbox bob@alice.net
    And the mailbox bob@alice.net contains "Welcome Bob"
