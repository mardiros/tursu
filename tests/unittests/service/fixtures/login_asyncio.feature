Feature: User signs in with the right password

  Background:
    Given a set of users:
      | username | password      |
      | Bob      | dumbsecret    |
      | Alice    | anothersecret |

  Rule: Successful login

    @asyncio
    Scenario: Successful sign-in with valid credentials
      When Bob signs in with password dumbsecret
      Then the user is connected with username Bob
