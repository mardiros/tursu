Feature: Discover Scenario

  @wip
  Scenario: I can find scenario based on tag
    Given a user Bob
    When Bob create a mailbox bob@alice.net
    Then I see a mailbox bob@alice.net for Bob
    And the mailbox bob@alice.net contains Welcome Bob
