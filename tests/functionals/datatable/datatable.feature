Feature: data table

  Scenario: see the datatable
    Given a user Alice with password yolo5
    And a user Bob with password dumbsecret
    Then the user sees the data_table
      | username | password   |
      | Alice    | yolo5      |
      | Bob      | dumbsecret |

  Scenario: parse a datatable
    Given a set of users:
      | username | password   |
      | Bob      | dumbsecret |
      | Henry    |            |
      |          |            |
    When Bob signs in with password dumbsecret
    Then the user Bob is connected

  @wip
  Scenario: parse reversed datatable
    Given a user with the following properties:
      | username | Bob        |
      | password | dumbsecret |
      When Bob signs in with password dumbsecret
    Then the user Bob is connected
