(advanced-doc-string)=

# Doc String With Pydantic & Dataclass Support

In the chapter before the previous one, we learnt [basics doc string supports](#step-definition-doc-string)

but as we learnt in the [advanced data table](#advanced-data-table),

docstring also support complex model types.

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
def fill_user_table(doc_string: list[User]):
    ...

@given("a user with the following informations:")
def fill_user_profile(doc_string: User):
    ...
```

And that's it. Now Turşu will provide doc_string mapped to previous given models.

So the following step will failed:

```Gherkin
Given a user with the following informations:
  """json
  {"username": "john", "password": "pass"}
  """
```

## Adding model factory with faker.

If the model of the doc_string argument is **Annotated**, then the factory
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
def a_set_of_users(app: DummyApp, doc_string: list[Annotated[User, UserFactory]]):
    ...

@given("a user with the following informations:")
def fill_user_profile(doc_string: Annotated[User, UserFactory]):
    ...
```

In that case, the gherkin scenario with empty data, are filled by faker values:

```Gherkin
Given the user provides the following informations:
  """json
  [
    {"username": "johndoe", "password": "secret123"},
    {"username": "janedoe"},
    {},
  ]
  """
```

````{note}
doc_string looks like
```python
[
    User(username="johndoe", password="secret123"),
    User(username="janedoe", password="<random value>"),
    User(username="<random value>", password="<random value>"),
]
```
````
