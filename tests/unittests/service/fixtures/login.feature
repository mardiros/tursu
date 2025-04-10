Feature: User signs in with the right password

  Background:
    Given a set of users:
      | username | password      |
      | Bob      | dumbsecret    |
      | Alice    | anothersecret |

  Rule: Successful login

    Scenario: Successful sign-in with valid credentials
      When Bob signs in with password dumbsecret
      Then the user is connected with username Bob

  Rule: Failed login attempts

    Scenario: Sign-in fails with wrong password
      When Bob signs in with password notthat
      Then the user is not connected

    Scenario Outline: User can't login with someone else username
      When <username> signs in with password <password>
      Then the user is not connected

      Examples:
        | username | password      |
        | Bob      | anothersecret |
        | Alice    | dumbsecret    |
