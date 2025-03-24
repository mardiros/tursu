Feature: Scenario with a set of user

  Background:
    Given a set of users:
      | username | password   |
      | Bob      | dumbsecret |
      | Henry    |            |
      |          |            |

  Scenario: Fill a dataset with a factory
    When Bob create a mailbox bob@alice.net
    Then Bob see a mailbox bob@alice.net
