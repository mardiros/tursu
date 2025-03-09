Feature: As a user I logged in with my password

  Background:
    Given a user Bob with password dumbsecret

  Scenario: I properly logged in
    When Bob login with password dumbsecret
    Then I am connected with username Bob

  Scenario: I hit the wrong password
    When Bob login with password notthat
    Then I am not connected
