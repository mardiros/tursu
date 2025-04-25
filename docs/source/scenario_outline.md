# Scenario Outline

A Scenario Outline in Gherkin is used to run the same scenario multiple times
with different sets of input data.
Instead of writing out the same steps repeatedly for each case, you define
the steps once and provide a table of example values.

In pytest this behavior is similar to `@pytest.mark.parametrize` and this is
why the Turşu AST compiler convert this kind of scenario to a parametrized test
function.

## Example

```gherkin

  Scenario Outline: Mix data table and example table
    Given a user with the following properties:
      | username | <username> |
      | password | <password> |
    When <username> signs in with password <password>
    Then the user <username> is connected

    Examples:
      | username | password             |
      | Bob      | dumbsecret           |
      | Alice    | alice-hasabetter_pwd |

```

Gherkin Scenario Outline use placeholder using `<` and `>` to enclose a parameter
name, and they are replaced before matching the step definitions.
It means that the step definitions does not have to take care about scenario
outlines directly.

This example will generate a parametrized tests with too sample.

The [data table](#advanced-data-table) values supports placeholder replacement, **but not the data table
headers**.
The values must match exactly the placeholder, it **does not accept** string concatenation
such as `<username>:<password>`.

Also [doc strings](#advanced-doc-string) does not supports any replacement directly.

```{important}
The first row of examples, which is the header, identified the placeholder.

Those placeholder must be **valid python identifiers**.
```

## Advanced usage

Because the placeholder replacement has its limitation, a parameter `example_row`
is available to manually simulate the parameterization.

In some edge case, you may want to write a custom step definition that need to get
the whole example row, e.g. the parameters of the `@pytest.mark.parametrize` values,
they are available in a pseudo fixtures `example_row` that can be added as a
step definition parameter. This is not a pytest fixtures, but it is a parameter,
with type `dict[str, str]` available like the `data_table` or the `doc_string`
step definition parameters. **It is not possible to override the type `dict[str, str]`
to a custom model**.

```python
@then("the user sees the docstring from the example")
def assert_parsed_docstring_custom(
    app: DummyApp, doc_string: dict[str, str], example_row: dict[str, str]
):
    # replace <placeholder> by placeholder
    assert example_row[doc_string["nick"][1:-1]] == app.connected_user
```
