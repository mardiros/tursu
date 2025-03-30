Feature: User login with their own password

  Scenario: User Bob can login
    Given a user Bob login with password dumbsecret
    When Bob login with password dumbsecret
    Then the user is connected with username Bob

  Scenario: Random user can login
    Given a user
    When user login
    Then the user is connected
