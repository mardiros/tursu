Feature: data table

  Scenario: see the doc string
    Given a user Alice with password yolo5
    And a user Bob with password dumbsecret
    Then I see the data_table
      | username | password   |
      | Alice    | yolo5      |
      | Bob      | dumbsecret |
