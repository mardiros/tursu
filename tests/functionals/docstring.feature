Feature: doc string

  Background:
    Given a user Bob with password dumbsecret

  Scenario: see the doc string
    When Bob signs in with password dumbsecret
    Then I see the docstring
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
