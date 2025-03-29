import textwrap
from collections.abc import Sequence
from typing import cast

import pytest

from tests.unittests.runtime.fixtures.conftest import DummyApp, DummyMail
from tests.unittests.runtime.fixtures.dataset_factory import (
    Dataset,
    a_set_of_users,
    assert_dataset,
)
from tests.unittests.runtime.fixtures.steps import (
    assert_api_response,
    assert_dataset_raw,
    assert_mailbox_contains,
    assert_user_has_mailbox,
    create_mailbox,
    give_user,
)
from tursu.domain.model.steps import Step, StepKeyword
from tursu.runtime.registry import Tursu, Unregistered
from tursu.runtime.runner import TursuRunner


@pytest.fixture()
def tursu_runner(
    registry: Tursu, request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str]
) -> TursuRunner:
    return TursuRunner(request, capsys, registry, ["📄 Document: ..."])


@pytest.fixture()
def dummy_app() -> DummyApp:
    return DummyApp()


def test_scan():
    registry = Tursu()
    registry.scan()
    assert registry._handlers == {
        "Given": [
            Step("a set of users:", a_set_of_users),
            Step("a user {username}", give_user),
        ],
        "Then": [
            Step("the users dataset is", assert_dataset),
            Step("the API for {username} respond", assert_api_response),
            Step("the users raw dataset is", assert_dataset_raw),
            Step('the mailbox {email} "{subject}" message is', assert_mailbox_contains),
            Step("{username} see a mailbox {email}", assert_user_has_mailbox),
        ],
        "When": [
            Step("{username} create a mailbox {email}", create_mailbox),
        ],
    }


def test_registry_handler(registry: Tursu):
    assert registry._handlers == {
        "Given": [
            Step("a set of users:", a_set_of_users),
            Step("a user {username}", give_user),
        ],
        "When": [
            Step("{username} create a mailbox {email}", create_mailbox),
        ],
        "Then": [
            Step("the users dataset is", assert_dataset),
            Step("the API for {username} respond", assert_api_response),
            Step("the users raw dataset is", assert_dataset_raw),
            Step('the mailbox {email} "{subject}" message is', assert_mailbox_contains),
            Step("{username} see a mailbox {email}", assert_user_has_mailbox),
        ],
    }


def test_registry_get_step(registry: Tursu):
    step = registry.get_step("Given", "a user Bob")
    assert step == Step("a user {username}", give_user)


def test_registry_get_step_none(registry: Tursu):
    step = registry.get_step("When", "a user Bob")
    assert step is None


def test_registry_datatable(registry: Tursu):
    registry.register_data_table(Step("the users dataset is", assert_dataset))
    assert registry.models_types[Dataset] == "Dataset1"


def test_registry_doc_string(registry: Tursu):
    registry.register_doc_string(Step("the API for {username} respond", assert_dataset))
    assert registry.models_types[DummyMail] == "DummyMail2"


def test_registry_step(tursu_runner: TursuRunner, dummy_app: DummyApp, registry: Tursu):
    tursu_runner.verbose = 0
    registry.run_step(tursu_runner, "Given", "a user Bob", dummy_app=dummy_app)
    registry.run_step(
        tursu_runner, "When", "Bob create a mailbox bob@alice.net", dummy_app=dummy_app
    )
    registry.run_step(
        tursu_runner,
        "Then",
        "Bob see a mailbox bob@alice.net",
        dummy_app=dummy_app,
    )

    registry.run_step(
        tursu_runner,
        "Then",
        "the API for Bob respond",
        dummy_app=dummy_app,
        doc_string=[
            DummyMail(email="bob@alice.net", subject="Welcome Bob", body="...")
        ],
    )

    assert dummy_app.mailboxes == {
        "Bob": [
            DummyMail(email="bob@alice.net", subject="Welcome Bob", body="..."),
        ],
    }

    with pytest.raises(Unregistered) as ctx:
        registry.run_step(tursu_runner, "When", 'Bob see a mailbox "bob@alice.net"')

    assert str(ctx.value) == textwrap.dedent(
        """\

        Unregistered step:

            When Bob see a mailbox "bob@alice.net"

        Maybe you look for:

            Then {username} see a mailbox {email}
            When {username} create a mailbox {email}

        Otherwise, to register this new step:

            @when("Bob see a mailbox \\"bob@alice.net\\"")
            def step_definition(): ...

        """
    )

    assert (
        tursu_runner.remove_ansi_escape_sequences(tursu_runner.fancy())
        == """
┌────────────────────────────────────────────┐
│ 📄 Document: ...                           │
│ ✅ Given a user Bob                        │
│ ✅ When Bob create a mailbox bob@alice.net │
│ ✅ Then Bob see a mailbox bob@alice.net    │
│ ✅ Then the API for Bob respond            │
│ ❌ When Bob see a mailbox "bob@alice.net"  │
└────────────────────────────────────────────┘
"""
    )


def test_registry_step_unregistered_extract_fixtures(
    tursu_runner: TursuRunner, dummy_app: DummyApp, registry: Tursu
):
    with pytest.raises(Unregistered) as ctx:
        registry.extract_fixtures("Given", "a nickname Bob", dummy_app=dummy_app)
    assert str(ctx.value) == textwrap.dedent("""
            Unregistered step:

                Given a nickname Bob

            Maybe you look for:

                Given a user {username}

            Otherwise, to register this new step:

                @given("a nickname Bob")
                def step_definition(): ...

            """)


def test_registry_step_unregistered_no_step(
    tursu_runner: TursuRunner, dummy_app: DummyApp, registry: Tursu
):
    with pytest.raises(Unregistered) as ctx:
        registry.extract_fixtures(
            "Given",
            "some stuff that can't match any registered step",
            dummy_app=dummy_app,
        )
    assert str(ctx.value) == textwrap.dedent("""
            Unregistered step:

                Given some stuff that can't match any registered step

            To register this new step:

                @given("some stuff that can't match any registered step")
                def step_definition(): ...

            """)


@pytest.mark.wip
@pytest.mark.parametrize(
    "steps, text,expected",
    [
        pytest.param(
            ["Given a user {username}"],
            "Given a user Bob",
            ["Given a user {username}"],
            id="One match",
        ),
        pytest.param(
            ["Given a user {name}", "Given a buzzer {name}"],
            "Given a uzer name",
            [
                "Given a buzzer {name}",
                "Given a user {name}",
            ],
            id="Many match",
        ),
        pytest.param(
            [
                "Given a user {name}",
                "When the user click on the {role} {name}",
                "When the user click on the 1st {role} {name}",
            ],
            "Then the user click on button",
            [
                "When the user click on the {role} {name}",
                "When the user click on the 1st {role} {name}",
            ],
            id="Many match",
        ),
    ],
)
def test_get_best_match(steps: list[str], text: str, expected: Sequence[str]):
    registry = Tursu()
    for step in steps:
        stp, rest = step.split(" ", 1)
        registry.register_handler(cast(StepKeyword, stp), rest, lambda: None)
    assert registry.get_best_matches(text) == expected
