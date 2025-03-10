Feature: Discover Scenario

  Background:
    Given a user Bob

  @wip
  Scenario: I can find scenario based on tag
    When Bob create a mailbox bob@alice.net
    Then I see a mailbox bob@alice.net for Bob
    And the mailbox bob@alice.net "Welcome Bob" message is
      """
      ...
      """
    And the API for bob@alice.net respond
      """json
      [{"email": "bob@alice.net", "subject": "Welcome Bob", "body": "..."}]
      """
