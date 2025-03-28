Feature: Use pytest fixtures in step tags

  Scenario: I can find scenario based on tag
    Given a user Bob using a fixture
    When Bob create a mailbox bob@alice.net using a fixture
    Then Bob see a mailbox bob@alice.net using a fixture
    And the mailbox bob@alice.net contains "Welcome Bob" using a fixture
