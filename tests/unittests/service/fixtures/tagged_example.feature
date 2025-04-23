Feature: Localized tests per tag

  Background:
    Given a set of users:
      | username | password      |
      | Bob      | dumbsecret    |
      | Robert   | anothersecret |

  Scenario Outline: The app is localized
    When <username> signs in with password <password>
    Then the user is not connected

    @en
    Examples: english
      | username | password      | message                      |
      | Bob      | anothersecret | Invalid username of password |

    @fr
    Examples: french
      | username | password      | message                                      |
      | Robert   | anothersecret | Nom d'utilisateur ou mot de passe incorrect. |
