import textwrap

import pytest

from tursu.domain.model.gherkin import GherkinDocument
from tursu.runtime.registry import Tursu
from tursu.service.compiler import GherkinCompiler, GherkinIterator


def test_emit_items(doc: GherkinDocument):
    gherkin_iter = GherkinIterator(doc)

    iter_step = gherkin_iter.emit()
    assert [repr(i) for i in next(iter_step)] == ["📄 Document: login.feature"]

    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
    ]

    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "Background: ",
    ]

    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Successful login",
    ]

    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Successful login",
        "🎬 Scenario: Successful sign-in with valid credentials",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Successful login",
        "🎬 Scenario: Successful sign-in with valid credentials",
        "When Bob signs in with password dumbsecret",
    ]

    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Successful login",
        "🎬 Scenario: Successful sign-in with valid credentials",
        "Then the user is connected with username Bob",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Failed login attempts",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Failed login attempts",
        "🎬 Scenario: Sign-in fails with wrong password",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Failed login attempts",
        "🎬 Scenario: Sign-in fails with wrong password",
        "When Bob signs in with password notthat",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Failed login attempts",
        "🎬 Scenario: Sign-in fails with wrong password",
        "Then the user is not connected",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Failed login attempts",
        "🎬 Scenario Outline: User can't login with someone else username",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Failed login attempts",
        "🎬 Scenario Outline: User can't login with someone else username",
        "When <username> signs in with password <password>",
    ]
    assert [repr(i) for i in next(iter_step)] == [
        "📄 Document: login.feature",
        "🥒 Feature: User signs in with the right password",
        "🔹 Rule: Failed login attempts",
        "🎬 Scenario Outline: User can't login with someone else username",
        "Then the user is not connected",
    ]

    with pytest.raises(StopIteration):
        next(iter_step)

    assert gherkin_iter.stack == []


def test_compiler(doc: GherkinDocument, registry: Tursu) -> None:
    compiler = GherkinCompiler(doc, registry, "tests.unittests.service.fixtures")
    code = compiler.to_module()

    assert (
        str(code)
        == textwrap.dedent(
            '''
            """User signs in with the right password"""
            from typing import Any
            import pytest
            from tursu.runtime.registry import Tursu
            from tursu.runtime.runner import TursuRunner
            from tests.unittests.service.fixtures.steps import User as User0
            from tests.unittests.service.fixtures.steps import app

            def test_7_Successful_sign_in_with_valid_credentials(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu, app: Any):
                """Successful sign-in with valid credentials"""
                with TursuRunner(request, capsys, tursu, ['📄 Document: login.feature', '🥒 Feature: User signs in with the right password', '🔹 Rule: Successful login', '🎬 Scenario: Successful sign-in with valid credentials']) as tursu_runner:
                    tursu_runner.run_step('Given', 'a set of users:', app=app, data_table=[User0(username='Bob', password='dumbsecret'), User0(username='Alice', password='anothersecret')])
                    tursu_runner.run_step('When', 'Bob signs in with password dumbsecret', app=app)
                    tursu_runner.run_step('Then', 'the user is connected with username Bob', app=app)

            def test_11_Sign_in_fails_with_wrong_password(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu, app: Any):
                """Sign-in fails with wrong password"""
                with TursuRunner(request, capsys, tursu, ['📄 Document: login.feature', '🥒 Feature: User signs in with the right password', '🔹 Rule: Failed login attempts', '🎬 Scenario: Sign-in fails with wrong password']) as tursu_runner:
                    tursu_runner.run_step('Given', 'a set of users:', app=app, data_table=[User0(username='Bob', password='dumbsecret'), User0(username='Alice', password='anothersecret')])
                    tursu_runner.run_step('When', 'Bob signs in with password notthat', app=app)
                    tursu_runner.run_step('Then', 'the user is not connected', app=app)

            @pytest.mark.parametrize('username,password', [pytest.param('Bob', 'anothersecret', id='Examples'), pytest.param('Alice', 'dumbsecret', id='Examples')])
            def test_18_User_can_t_login_with_someone_else_username(request: pytest.FixtureRequest, capsys: pytest.CaptureFixture[str], tursu: Tursu, app: Any, username: str, password: str):
                """User can't login with someone else username"""
                with TursuRunner(request, capsys, tursu, ['📄 Document: login.feature', '🥒 Feature: User signs in with the right password', '🔹 Rule: Failed login attempts', "🎬 Scenario Outline: User can't login with someone else username"]) as tursu_runner:
                    tursu_runner.run_step('Given', 'a set of users:', app=app, data_table=[User0(username='Bob', password='dumbsecret'), User0(username='Alice', password='anothersecret')])
                    tursu_runner.run_step('When', tursu_runner.format_example_step('<username> signs in with password <password>', username=username, password=password), app=app)
                    tursu_runner.run_step('Then', tursu_runner.format_example_step('the user is not connected', username=username, password=password), app=app)
            '''
        ).strip()
    )
