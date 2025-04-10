Feature: User sign in

  Background:
    Given a user Bob with password dumbsecret

  Scenario: Successful sign-in with valid credentials with valid credentials
    When Bob signs in with password dumbsecret
    Then the user Bob is connected

  Scenario: Can't sign in with wrong password
    When Bob signs in with password notthat
    Then the user is not connected
