# Project Structure and Feature File Organization

We called step definition, the python function that has to be written
to execute the scenario steps.

Step definitions are functions decorated by [@given](#tursu.given),
[@when](#tursu.when), [@then](#tursu.then) decorators.

This section will explain where to declare those step definitions.

## Simple example

```
src/
|    package/ # code base of the package
tests/
├── functionals/
│   │   ├── __init__.py    # unsure the tests is discovered has a package
│   │   ├── conftest.py    # (Optional) Fixtures for this module
│   │   ├── steps.py     # (exemple) reusable context
│   │   ├── login.feature
│   │   ├── signup.feature
│
├── unittests/
│   ├── ... # your unit tests go here
│
├── __init__.py  # unsure the tests is discovered has a package
├── conftest.py  # Not mandatory, fixture you may share between all tests.
```

The step definitions can be defined at the same level of the feature files.
For convention, using a `steps.py` for a few step definitions works, but,
when they have to be splitted, creating a steps directory to put the fixtures
named with proper named that match their intention is prefered.
By the way, the name of the python modules for step definition can be any python
valid module name, this is juste a convention. To have named python module,
the preferred way it to create those modules in a separate steps sub directory.

## Creating step definition in a step sub module.

```
src/
|    package/ # code base of the package
tests/
├── functionals/
│   │   ├── login.feature
│   │   ├── signup.feature
│   │   ├── __init__.py  # unsure the tests is discovered has a package
│   │   ├── steps/
│   │   │   ├── __init__.py  # unsure the tests is discovered has a package
│   │   │   ├── assertions.py  # (exemple) validate outcomes
│   │   │   ├── conftest.py    # (Optional) Fixtures for this module
│   │   │   ├── context.py     # (exemple) reusable context
│   │   │   ├── forms.py       # (exemple) filling forms
│   │
│
├── unittests/
│   ├── ... # your unit tests go here
│
├── __init__.py  # unsure the tests is discovered has a package
├── conftest.py  # Not mandatory, fixture you may share between all tests.
```

Step definitions can be declared in a sub modules of a steps module.
The name of the module here must be named **steps**.

Otherwise, it is will be considered as a nested feature directory, as
in the example bellow. And those steps where only available for the scenario
declared at the same level.

## Scaling functional codebase with nested scenario.

```
tests/
├── functionals/
│   ├── authentication/
│   │   ├── __init__.py
│   │   ├── login/
│   │   │   ├── __init__.py
│   │   │   ├── basic_login.feature
│   │   │   ├── social_login.feature
│   │   │   ├── steps.py  # step definitions available for login only
│   │   ├── signup/
│   │   │   ├── __init__.py
│   │   │   ├── email_signup.feature
│   │   │   ├── phone_signup.feature
│   │   │   ├── steps.py  # step definitions available for signup only
│   ├── cart/
│   │   ├── __init__.py
│   │   ├── checkout/
│   │   │   ├── __init__.py
│   │   │   ├── payment.feature
│   │   │   ├── shipping.feature
│   │   ├── add_to_cart.feature
│   │   ├── steps/  # steps available for add_to_cart, payment and shipping only
│   │   │   ├── __init__.py
│   │   │   ├── conftest.py
│   │   │   ├── add_to_cart.py
│   │   │   ├── payment.py
│   │   │   ├── shipping.py
│   │   ├── conftest.py  # step definitions available for all tests
│   │   ├── steps.py  # step definitions available for all tests
├── __init__
```

In this example, the login and the signup steps has been created and available
with the features, in a single module that may contain fixture and all the steps.

The cart checkout features has been splitted in a sub directory, that may
contains its own steps, but for the example, they are also in the cart steps,
only because checkout is a subdirectory of the cart.
