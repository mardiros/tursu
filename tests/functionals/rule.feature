Feature: User signs in with the right password

  Background:
    Given a user Bob with password dumbsecret

  Rule: It works

    Scenario: Successful sign-in with valid credentials
      When Bob signs in with password dumbsecret
      Then the user Bob is connected

  Rule: It does not works

    Scenario: Sign-in fails with wrong password
      When Bob signs in with password notthat
      Then the user is not connected
