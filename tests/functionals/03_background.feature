Feature: As a user I logged in with my password

  Background:
    Given a user Bob with password dumbsecret

  Scenario: User can login
    When Bob login with password dumbsecret
    Then the user Bob is connected

  Scenario: User can't login with wrong password
    When Bob login with password notthat
    Then I am not connected
