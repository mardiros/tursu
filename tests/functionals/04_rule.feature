Feature: As a user I logged in with my password

  Background:
    Given a user Bob with password dumbsecret

  Rule: It works

    Scenario: I properly logged in
      When Bob login with password dumbsecret
      Then I am connected with username Bob

  Rule: It does not works

    Scenario: I hit the wrong password
      When Bob login with password notthat
      Then I am not connected
