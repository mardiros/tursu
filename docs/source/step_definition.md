(step-definition)=

# Step Definition

To match gherkin steps into python code, we used a
[pattern matcher](#tursu.runtime.pattern_matcher).

The definition of the step is written using the syntax of the pattern matcher.

Tursu has two pattern matcher, a default pattern matcher which is documented here,

and a regular expression pattern matcher for even more flexibility, but less readable.

## Default pattern matcher

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

### Typing support

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


## RegEx pattern matcher

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

### Json

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

```{note}
When a media type is set to `json` (`"""json` in gherkin docstring)
then tursu will parse the json and return it as a list or a dict.

Otherwise, a plain string will be returned.
```

### List of dict from a data table

```python
@given("the user provides the following login credentials:")
def fill_user_table(data_table: list[dict[str, str]]):
    ...
```

```Gherkin
Given the user provides the following login credentials:
  | username | password  |
  | johndoe  | secret123 |
  | janedoe  | password1 |
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

### Arbitrary type from a data table


```python

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


@given("the user provides the following login credentials:")
def fill_user_table(data_table: list[User]):
    ...
```

```Gherkin
Given the user provides the following login credentials:
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



@given("the user provides the following login credentials:")
def a_set_of_users(app: DummyApp, data_table: list[Annotated[User, UserFactory]]):
    ...
```

```Gherkin
Given the user provides the following login credentials:
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
