Feature: Scenario outlines

  Background:
    Given a user Alice with password plokiploki
    And a user Bob with password dumbsecret

  Scenario Outline: Successful login with valid credentials
    When <username> login with password <password>
    Then the user <username> is connected

    Examples:
      | username | password   |
      | Alice    | plokiploki |
      | Bob      | dumbsecret |
