Feature: Scenario with a set of user

  Background:
    Given a set of users:
      | username | password   |
      | Bob      | dumbsecret |
      | Henry    |            |
      |          |            |

  Scenario: Fill a dataset with a factory
    When Bob creates a mailbox bob@alice.net
    Then Bob sees a mailbox bob@alice.net
