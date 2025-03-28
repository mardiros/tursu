# Gherkin in a nutshell

Gherkin was designed for writing behavior specifications in a human-readable
format for Behavior-Driven Development (BDD).

In Behavior-Driven Development (BDD), tests are written before the actual code.
This is part of the test-first approach, where scenarios are written based
on the expected behavior of the system before development begins.

So the first things we do is writing tests, in english language, with the
gherkin syntax.

```{note}
If you are already familiar with gherkin, you may skip this chapter.
```

## Starts with a simple Gherkin Scenario

Lets start by this simple example:

```gherkin
Feature: **feature description**

  Scenario: **scenario description**

    Given **context**
    When **action**
    Then **outcome**
```

Now what's in the `**` placeholder has to be replaced by something concrete
that have to be achieved.

It matches the definition of done.

Once the scenario has been written, the step definition has to be written for
the scenario.

What we call steps, is keywords **Given**, **When** and **Then**.

The step definition is the function thas have been decorated by
[@given](#tursu.given), [@when](#tursu.when), [@then](#tursu.then) decorators.

In this chapter, we are not going to dive deeper on that, but, in real life,
after writing a scenario in your repository, the first things to do is
to run the tests and implement the missing steps definition.

## Work in progress

While working on a new feature, I usually add a gherkin tag `@wip`, on the scenario.

It helps to stay focus on what you are working on.

```gherkin
Feature: **feature description**

  @wip
  Scenario: **scenario description**

    Given **context**
    When **action**
    Then **outcome**
```

To run the tests marked with wip use the command `pytest` with the option `-m wip`.

## Adding another scenario

When the first scenario works, you may write a new scenario and mark it as **@wip**.

```gherkin
Feature: **feature description**

  Scenario: **scenario description**

    Given **context**
    When **action**
    Then **outcome**

  @wip
  Scenario: **new scenario description**

    Given **context**
    When **action**
    Then **outcome**
```

## Use background to avoid repetition

You may have multiple scenario in one feature file, usually, the
given context may be the same, and, if it is the case, the scenario
can be refactor using a **Background** keyword.

```gherkin
Feature: **feature description**

  Background:
    Given **context**

  Scenario: **scenario description**

    When **action**
    Then **outcome**

  @wip
  Scenario: **new scenario description**

    When **action**
    Then **outcome**
```

In that case, the 2 scenario starts with the same given step.

## Adding more steps

```gherkin
Feature: **feature description**

  Scenario: **scenario description**

    Given **context**
    And **context 2**
    When **action**
    And **action 2**
    Then **outcome**
    And **outcome 2**
    But **outcome 3**
```

You can add multiple step and avoid repetition of the **Given** **When**
or **Then** by using a conjunction, which is **And** or **But**.
They are just here for clarity. the step definition is still using the same
[@given](#tursu.given), [@when](#tursu.when), [@then](#tursu.then) decorators.

## Use scenario outline to avoid repetition

Using a **When** happen after a **Then**, or even a**Given** is valid, but,
this is not recommended.

```gherkin
Feature: **bad feature description**


  Scenario: **scenario that is badly designed**

    Given **context**
    When **action** value11
    Then **outcome** value12
    When **action** value21
    Then **outcome** value22
```

should be writen

```gherkin
Feature: **bad feature description**


  Scenario Outline: **scenario rewritten**

    Given **context**
    When **action** <param1>
    Then **outcome** <param2>

    Examples:
    | param1  | param2  |
    | value11 | value12 |
    | value21 | value22 |
```

Using the gherkin chevron-enclosed placeholders (<param1> and <param2>)
make the tests more clear and will also generate 2 independants tests.


## Use data table to load multiple data.

```gherkin
Feature: **feature description**

  Scenario: **scenario description**

    Given **big contextcontext**:
      | param1  | param2  |
      | value11 | value12 |
      | value21 | value22 |
    When **action**
    Then **outcome**
```

it allows to have a step definition having a complex python type.

Note that it works also for the **When** and the **Then** keywords.

Now that we know gherkin, its time to dive into the next chapter and
define how we define the step definition using the pattern matcher.
