@asyncio
Feature: Basic Test

  Scenario: Hello world
    Given anonymous user on /
    Then I see the text "Hello, World!"
