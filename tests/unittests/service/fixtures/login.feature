Feature: User login with their own password

  Background:
    Given a set of users:
      | username | password      |
      | Bob      | dumbsecret    |
      | Alice    | anothersecret |

  Rule: Successful login

    Scenario: User can login
      When Bob login with password dumbsecret
      Then the user is connected with username Bob

  Rule: Failed login attempts

    Scenario: User can't login with wrong password
      When Bob login with password notthat
      Then the user is not connected

    Scenario Outline: User can't login with someone else username
      When <username> login with password <password>
      Then the user is not connected

      Examples:
        | username | password      |
        | Bob      | anothersecret |
        | Alice    | dumbsecret    |
