Feature: doc string

  Background:
    Given a user Bob with password dumbsecret

  Scenario: see the doc string
    When Bob login with password dumbsecret
    Then I see the docstring
    """json
    {
      "nick": "Bob"
    }
    """
