Feature: doc string

  Background:
    Given a user Bob with password dumbsecret

  @wip
  Scenario: see the doc string
    When Bob signs in with password dumbsecret
    Then the user sees the docstring
    """json
    {
      "nick": "Bob"
    }
    """
