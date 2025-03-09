Feature: Discover Scenario

  Scenario: I can find scenario based on tag
    Given a user Bob using a fixture
    When Bob create a mailbox bob@alice.net using a fixture
    Then I see a mailbox bob@alice.net for Bob using a fixture
    And the mailbox bob@alice.net contains "Welcome Bob" using a fixture
