@wip
Feature: Basic Test

  Scenario: Hello world
    Given anonymous user on /
    Then the user sees the text "Hello, World!"
