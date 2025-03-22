Feature: data table

  Scenario: see the datatable
    Given a user Alice with password yolo5
    And a user Bob with password dumbsecret
    Then I see the data_table
      | username | password   |
      | Alice    | yolo5      |
      | Bob      | dumbsecret |

  Scenario: parse a datatable
    Given a set of users:
      | username | password   |
      | Alice    | yolo5      |
      | Bob      | dumbsecret |
    Then I see the data_table
      | username | password   |
      | Alice    | yolo5      |
      | Bob      | dumbsecret |
