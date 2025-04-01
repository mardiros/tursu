Feature: Regex Pattern Matcher

  Scenario: Extract parameters using regular expression
    Given a user Bob using a regex
    When Bob create a mailbox bob@alice.net using a regex
    Then Bob see a mailbox bob@alice.net using a regex
    And the mailbox bob@alice.net contains "Welcome Bob" using a regex
