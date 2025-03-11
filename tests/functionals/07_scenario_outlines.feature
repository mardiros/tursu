Feature: Scenario outlines

  Background:
    Given a user Alice with password plokiploki
    And a user Bob with password dumbsecret

  Scenario Outline: Successful login with valid credentials
    When <username> login with password <password>
    Then I am connected with username <username>

    Examples:
      | username | password   |
      | Alice    | plokiploki |
      | Bob      | dumbsecret |
