Feature: As a user I logged in with my password

  Background:
    Given a set of users:
      | username | password      |
      | Bob      | dumbsecret    |
      | Alice    | anothersecret |

  Scenario: User can login
    When Bob login with password dumbsecret
    Then the user is connected with username Bob

  Scenario: User can't login with wrong password
    When Bob login with password notthat
    Then the user is not connected

  Scenario Outline: User can't login with someone else username
    When <user> login with password <password>
    Then the user is not connected

    Examples:
      | username | password      |
      | Bob      | anothersecret |
      | Alice    | dumbsecret    |
