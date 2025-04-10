Feature: Discover Scenario Outline
  This feature is complex and require a comment.

  Background:
    Given a user momo

  @oulined
  Scenario Outline: I can load scenario outline
    This scenario is complex and require a comment.

    Given a user <username>
    When <username> creates a mailbox <email>
    Then <username> sees a mailbox <email>

    Examples:
      | username | email           |
      | Alice    | alice@alice.net |
      | Bob      | bob@bob.net     |
