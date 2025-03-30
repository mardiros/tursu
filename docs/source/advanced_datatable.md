(advanced-data-table)=

# Data Table With Pydantic & Dataclass Support

In the previous chapter, we learnt [basics data table supports](#step-definition-data-table)

but there is more, Turşu is able to map gherkin table to pydantic model, or dataclasses.

It works for [Data table](#data-table-tabular-data) and [reversed data table](reversed-data-table).

From the previous example, we **list[dict[str, str]]** and the **dict[str, str]** can
be replaced by typed object.

Here is wome class definition for the [previous example](#step-definition-data-table).

## Dataclass

```python
from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str

```

## Pydantic

If you prefer go with pydantic, it also works.

```python

from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str

```

## Usage of model based class.

After the type has been devined, we can replace it in step definitions,
like this:

```python

@given("the user provides the following informations:")
def fill_user_table(data_table: list[User]):
    ...

@given("a user with the following informations:")
def fill_user_profile(data_table: User):
    ...
```

And that's it. Now Turşu will provide data_table mapped to your given models.

```{important}
Nested model are not implemented in data table in Turşu,

You can achieve it usign a [Doc String that use a model](#advanced-doc-string).
This is the subject of the [next chapter](#advanced-doc-string).
```

You may also notive that the **blanked gherkin column will not be passed to model constructurors**.,
They will be removed and the default values of the field will be used instead.
To get more control of the model construction, you can passed a factory.

So the following step will failed:

```Gherkin
Given a user with the following informations:
  | username | johndoe   |
  | password |           |
```

The step above failed because the password is ommited, and
there is no default value set on the model, and Turşu will parse the table
to **User(username='johndoe')**, of course you can define a **field_factory**
on the model, or you may use a factory, that le you reuse the type for different
purpose.

## Adding model factory with faker.

If the model of the data_table argument is **Annotated**, then the factory
will be used to contruct the model, it can be usefull to inject the data
you need for you expectation, or random data.

Here is an example with factory-boy:

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

@given("a user with the following informations:")
def fill_user_profile(data_table: Annotated[User, UserFactory]):
    ...
```

In that case, the gherkin scenario with empty data, are filled by faker values:

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
