Feature: Regex Pattern Matcher

  Scenario: Extract parameters using regular expression
    Given a user Bob
    When Bob create a mailbox bob@alice.net
    Then Bob see a mailbox bob@alice.net
    And the mailbox bob@alice.net contains "Welcome Bob"
