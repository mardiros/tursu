Feature: doc string

  Background:
    Given a user Bob with password dumbsecret

  Scenario: see the doc string
    When Bob signs in with password dumbsecret
    Then the user sees the docstring
      """json
      {
        "nick": "Bob"
      }
      """

  Scenario: see the doc string
    When Bob signs in with password dumbsecret
    Then I can parse the docstring
      """json
      {
        "nick": "Bob"
      }
      """

  Scenario Outline: see the doc string
    When <username> signs in with password <password>
    Then the user sees the docstring from the example
      """json
      {
        "nick": "<username>"
      }
      """

    Examples:
      | username | password   |
      | Bob      | dumbsecret |
