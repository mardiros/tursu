Feature: User sign in with their own password

  Scenario: User Bob can login
    Given a user Bob signs in with password dumbsecret
    When Bob signs in with password dumbsecret
    Then the user is connected with username Bob

  Scenario: Random user can login
    Given a user
    When user login
    Then the user is connected
