(step-definition)=

# Step Definition

To match gherkin steps into python code, we used a
[pattern matcher](#tursu.runtime.pattern_matcher).

The definition of the step is written using the syntax of the pattern matcher.

Tursu has two pattern matcher, a default pattern matcher which is documented here,

and a regular expression pattern matcher for even more flexibility, but less readable.

## Default Pattern Matcher

The default pattern matcher is based on curly brace to discover variable,
and it match a single world.

But if it is enclosed by `"`, then it can be a sentence.

:::{list-table}
:widths: 20 40 40
:header-rows: 1

- - matcher
  - Python decorator example
  - Gherkin usage example
- - ```python
    {username}
    ```
  - ```python
    @given('a user {username}')
    ```
  - ```Gherkin
    Given a user Alice
    ```
- - ```python
    "{username}"
    ```
  - ```python
    @then('I see the text "{expected}"')
    ```
  - ```Gherkin
    I see the text "Welcome Alice"
    ```
:::

### Typing Support

The default matcher does not enforce the type in the text of the decorator,
**it use the function signature**.

Supported types are: `bool`, `date`, `datetime`, `float`, `int`, `str`, `Enum` and `Literal[...]`:

#### boolean

**Python signature:**

```python
@given('Given the feature flag "{feature_flag}" is set to {ff_toggle}')
def toggle_feature_flag(feature_flag: str, ff_toggle: bool):
    ...
```

**Gherkin example:**

```Gherkin
Given the feature flag "DARK_MODE" is set to true
Then the system status should be off
```

```{note}

* True values are `true`, `1`, `yes`, `on`
* False values are `false`, `0`, `no`, `off`

Those values are case insensitive.

Everything else will raise a value error.
```

#### date

**Python signature:**

```python
@given("the user's subscription expires on {expires_on}")
def given_expires_on_subscription(expires_on: date):
    ...
```

**Gherkin example:**

```Gherkin
Given the user's subscription expires on 2025-12-31
```

#### datetime

**Python signature:**

```python
@given("the user's subscription expires at {expires_at}")
def given_expires_at_subscription(expires_at: date):
    ...
```

**Gherkin example:**

```Gherkin
Given the user's subscription expires at 2025-12-31T08:00:00Z
```

#### float

**Python signature:**

```python
@given("the account balance is {account_balance}")
def toggle_feature_flag(account_balance: float):
    ...
```

**Gherkin example:**

```Gherkin
Given the account balance is 99.99
```

#### int

**Python signature:**

```python
@then("the cart should contain {items_count} items")
def assert_cart_items_count(feature_flag: int):
    ...
```

**Gherkin example:**

```Gherkin
Then the cart should contain 3 items
```

#### str

**Python signature:**

```python
@given('Given the user role {role} protected by passphrase "{passphrase}"')
def given_role(role: str, passphrase: str):
    ...
```

**Gherkin example:**

```Gherkin
Given the user role admin protected by passphrase "I am feeling lucky"
```

#### Enum

**Python signature:**

```python

from enum import Enum

class OrderStatus(Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"
    COMPLETED = "Completed"

@given("the order status is {order_status}")
def toggle_feature_flag(order_status: OrderSatus):
    ...
```

**Gherkin example:**

```Gherkin
Given the order status is PROCESSING
```

```{note}
For enum, the key must be passed, not the value.
```

#### Literal

**Python signature:**

```python
from typing import Literal

FeatureFlagName = Literal["dark_mode", "light_mode", "beta_feature"]

@given("the feature flag {feature} is set to {status}")
def set_feature_flag(feature: FeatureFlagName, status: bool):
    ...
```

**Gherkin example:**

```Gherkin
Given the feature flag dark_mode is set to on
```

## RegEx Pattern Matcher

This is less readable, but, may be usefull in certain situation,

Regular Expression can be used to match patterns.

First you need to import the [RegEx](#tursu.RegEx) class:

```python
from tursu import RegEx
```

Afterwhat, the named capturing group syntax has to be used `(?P<matched_name>regex_pattern)`:

:::{list-table}
:widths: 20 40 40
:header-rows: 1

- - matcher
  - Python decorator example
  - Gherkin usage example
- - ```python
    r"(?P<username>[^\s]+)"
    ```
  - ```python
    @given(
      RegEx(r'a user (?P<username>[^\s]+)')
    )
    ```
  - ```Gherkin
    Given a user Alice
    ```
- - ```python
    r'(?P<expected>[^\"]+)'
  - ```python
    @then(
      RegEx(r'I see the text "(?P<expected>[^\"]+)"')
    )
    ```
  - ```Gherkin
    I see the text "Welcome Alice"
    ```
:::


## Complex types from Gherkin DataTable and DocString

Regardless of the pattern matcher you use, a step definition can also include
a complex type derived directly from Gherkin grammar.

To handle long text or datasets,
Gherkin supports two features: **doc strings** and **data tables**.

These allow for multiline steps, and we'll begin with doc strings for JSON support.

### DocString

Multiline text are not feet for gherkin pattern matcher, so a doc string with the
following syntax can be used to capture multiline from a scenario.

#### As text

```python
@then("the page containts the following text:")
def create_user_from_json(page: Page, doc_string: string):
    ...
```

```Gherkin
Then the user provides the following profile data:
"""
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus.
Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor.
Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod
non, mi. Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum
diam nisl sit amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in,
pretium a, enim. Pellentesque congue. Ut in risus volutpat libero pharetra tempor.
"""
```

#### As JSON

```python
@given("the user provides the following profile data:")
def create_user_from_json(doc_string: dict[str, Any]):
    ...
```

```Gherkin
Given the user provides the following profile data:
  """json
  {
    "username": "johndoe",
    "email": "johndoe@example.com",
    "address": {
      "street": "123 Main St",
      "city": "Anytown",
      "postal_code": "12345"
    }
  }
  """
```

```{tip}
When a media type is set to `json` (`"""json` in the Gherkin doc string)
then tursu will parse the json using the python standard library.

Otherwise, a plain string will be returned.
```

(step-definition-data-table)=

### DataTable

Data table are usefull to get tabular data input. You may have multiple input
with many row, or a reversed datatable can be used for a single structured input.

(data-table-tabular-data)=

#### Tabular Data

In a tabula data, the data table, is column based and can be seen filled out like:

```Gherkin
Given users with the following informations:
  | username | password  |
  | johndoe  | secret123 |
  | janedoe  | password1 |
```

and in that case we can use the step definition bellow:

```python
@given("users with the following informations:")
def fill_user_table(data_table: list[dict[str, str]]):
    ...
```

````{note}
data_table looks like
```python
[
    {"username": "johndoe", "password": "secret123"},
    {"username": "janedoe", "password": "password1"},
]
```
````

The type **list** is very important to tell tursu that the data table is list base,
otherwise, tursu data table parser will interpret it as a row based data table,
also known as reversed data table.

(reversed-data-table)=

#### Reversed DataTable

A reversed data table is **column based**. It is a key value per.

And it is ideal to fill a profile with many attributes, here we set two attibutes
for brevity.

```Gherkin
Given a user with the following informations:
  | username | johndoe   |
  | password | secret123 |
```

```python
@given("a user with the following informations:")
def fill_user_profile(data_table: dict[str, str]):
    ...
```

````{note}
data_table looks like
```python
    {"username": "johndoe", "password": "secret123"},
```
````


Because there is no list type annotated, then the tursu parser will
only used the two first column of the table.

```{tip}
If you set more attributes on the table then they will be ignored.
Use them as comment if you want.
```

#### Using dataclass or pydantic objects.

Gherkin tabular data is nice and can be even nicer with advanced python
types, or even faked data, so


### Arbitrary type from a data table

```python

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


@given("the user provides the following informations:")
def fill_user_table(data_table: list[User]):
    ...
```

```Gherkin
Given the user provides the following informations:
  | username | password  |
  | johndoe  | secret123 |
  | janedoe  | password1 |
```

````{note}
data_table looks like
```python
[
    User(username="johndoe", password="secret123"),
    User(username="janedoe", password="password1"),
]
```
````

### Arbitrary type from a data table, with a faked values

```python
import factory
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class UserFactory(factory.Factory[User]):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.Faker("password")



@given("the user provides the following informations:")
def a_set_of_users(app: DummyApp, data_table: list[Annotated[User, UserFactory]]):
    ...
```

```Gherkin
Given the user provides the following informations:
  | username  | password   |
  | johndoe   | secret123  |
  | janedoe   |            |
  |           |            |
```

````{note}
data_table looks like
```python
[
    User(username="johndoe", password="secret123"),
    User(username="janedoe", password="<random value>"),
    User(username="<random value>", password="<random value>"),
]
```
````
