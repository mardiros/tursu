@asyncio
Feature: asynchronous step

  Background:
    Given a user Bob

  Rule: I write a wip test

    Scenario: I can find scenario based on tag
      When Bob creates a mailbox bob@alice.net
      Then Bob sees a mailbox bob@alice.net
      And the mailbox bob@alice.net "Welcome Bob" message is
        """
        ...
        """
      And the async API for Bob respond
        """json
        [{"email": "bob@alice.net", "subject": "Welcome Bob", "body": "..."}]
        """
