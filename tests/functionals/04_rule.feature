Feature: User login with their own password

  Background:
    Given a user Bob with password dumbsecret

  Rule: It works

    Scenario: User can login
      When Bob login with password dumbsecret
      Then the user Bob is connected

  Rule: It does not works

    Scenario: User can't login with wrong password
      When Bob login with password notthat
      Then I am not connected
