"""Registry of step definition."""

import difflib
import importlib
import sys
from collections import defaultdict
from collections.abc import Mapping, Sequence
from inspect import Parameter
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Annotated, Callable, get_args, get_origin

import venusian
from typing_extensions import Any

from tursu.domain.model.steps import Handler, StepDefinition, StepKeyword
from tursu.runtime.pattern_matcher import AbstractPattern
from tursu.shared.utils import is_mapping, is_sequence, is_union

if TYPE_CHECKING:
    from tursu.runtime.runner import TursuRunner

from tursu.runtime.exceptions import Unregistered

VENUSIAN_CATEGORY = "tursu"


def is_init_file(module: ModuleType) -> bool:
    """Check if a module corresponds to an __init__.py file."""
    return (
        hasattr(module, "__file__")
        and module.__file__ is not None
        and Path(module.__file__).name == "__init__.py"
    )


def normalize_module_name(module_name: str) -> str:
    """If the module is an __init__.py, keep its name. Otherwise, drop the last part."""
    module = importlib.import_module(module_name)
    if not is_init_file(module):
        module_name = ".".join(module_name.split(".")[:-1])
    if module_name.endswith(".steps"):
        module_name = module_name[: -len(".steps")]
    return module_name


def _step(
    keyword: StepKeyword, step_pattern: str | AbstractPattern
) -> Callable[[Handler], Handler]:
    def wrapper(wrapped: Handler) -> Handler:
        def callback(scanner: venusian.Scanner, name: str, ob: Handler) -> None:
            if not hasattr(scanner, "registry"):
                return  # coverage: ignore

            step_module = normalize_module_name(ob.__module__)

            scanner.registry.register_step_definition(  # type: ignore
                step_module, keyword, step_pattern, wrapped
            )

        venusian.attach(wrapped, callback, category=VENUSIAN_CATEGORY)
        return wrapped

    return wrapper


def given(pattern: str | AbstractPattern) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the `Given` Gherkin keyword.

    :param pattern: a pattern to extract parameter.
                    Refer to the [step definition documentation](#step-definition)
                    for the syntax.
    :return: the decorate function that have any parameter coming from
             the pattern matcher or pytest fixtures.
    """
    return _step("Given", pattern)


def when(pattern: str | AbstractPattern) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the `When` gherkin keyword.

    :param pattern: a pattern to extract parameter.
                    Refer to the [step definition documentation](#step-definition)
                    for the syntax.
    :return: the decorate function that have any parameter coming from
             the pattern matcher or pytest fixtures.
    """
    return _step("When", pattern)


def then(pattern: str | AbstractPattern) -> Callable[[Handler], Handler]:
    """
    Decorator to listen for the `Then` gherkin keyword.

    :param pattern: a pattern to extract parameter.
                    Refer to the [step definition documentation](#step-definition)
                    for the syntax.
    :return: the decorate function that have any parameter coming from
             the pattern matcher or pytest fixtures.
    """
    return _step("Then", pattern)


class ModRegistry:
    """
    Registry for a package.

    In a layered tests suite, step definitions are inherits from parent directories,
    so step definitions are saved per directory, or package.
    """

    def __init__(self) -> None:
        self._step_defs: dict[StepKeyword, list[StepDefinition]] = {
            "Given": [],
            "When": [],
            "Then": [],
        }
        self._models_types: dict[type, str] = {}

    @property
    def models_types(self) -> dict[type, str]:
        """
        Registered data types, used in order to build imports on tests.
        The type are aliased during registration to avoid conflict name at import time
        during the ast generation.

        :return: type as key, alias as value.
        """

        return self._models_types

    def append(self, stp: StepKeyword, step: StepDefinition) -> None:
        """
        Append a step definition to the registry.
        """
        self._step_defs[stp].append(step)
        self.register_data_table(step)
        self.register_doc_string(step)

    def get_fixtures(self) -> Mapping[str, type]:
        fixtures: dict[str, type] = {}
        for step_defs in self._step_defs.values():
            for stp in step_defs:
                fixtures.update(stp.fixtures)
        return fixtures

    def register_model(self, parameter: Parameter | None) -> None:
        """
        Register the model in the parameter of a signature for data_table or doc_string.

        :param parameter: the parameter from the signature.
        """
        if parameter and parameter.annotation:
            if is_union(parameter.annotation):
                # we don't register union types.
                return

            param_origin = get_origin(parameter.annotation)
            if param_origin is Annotated:
                # we are in a factory
                typ = get_args(parameter.annotation)[-1]
            elif param_origin and is_sequence(param_origin):
                # we are in a list
                typ = get_args(parameter.annotation)[0]
                item_orig = get_origin(typ)
                if not is_mapping(item_orig):
                    if item_orig is Annotated:
                        # the list has a factory
                        typ = get_args(typ)[-1]
            else:
                typ = parameter.annotation

            if typ.__module__ != "builtins" and typ not in self._models_types:
                self._models_types[typ] = f"{typ.__name__}{len(self._models_types)}"

    def register_data_table(self, step: StepDefinition) -> None:
        """
        This method register the data table as a model.

        :param step: The step containing a data_table parameter.
        """
        self.register_model(step.pattern.signature.parameters.get("data_table"))

    def register_doc_string(self, step: StepDefinition) -> None:
        """
        This method register the doc string as a model.

        :param step: The step containing a doc_string parameter.
        """
        self.register_model(step.pattern.signature.parameters.get("doc_string"))

    def get_best_matches(
        self,
        text: str,
        n: int = 5,
        cutoff: float = 0.3,
    ) -> Sequence[tuple[float, str]]:
        """
        Return the gherkin steps from the registry that look like the given text.
        This method is called if no step definition matches to build a proper hint
        for the user.

        :param text: text to match the definition.
        """
        possibilities = [
            *[f"Given {stp.pattern.pattern}" for stp in self._step_defs["Given"]],
            *[f"When {stp.pattern.pattern}" for stp in self._step_defs["When"]],
            *[f"Then {stp.pattern.pattern}" for stp in self._step_defs["Then"]],
        ]
        matches = difflib.get_close_matches(text, possibilities, n=n, cutoff=cutoff)

        scored_matches = [
            (difflib.SequenceMatcher(None, text, match).ratio(), match)
            for match in matches
        ]
        return scored_matches

    def get_step(self, keyword: StepKeyword, text: str) -> StepDefinition | None:
        """
        Get the first registered step that match the text.

        :param keyword: gherkin keyword for the definition.
        :param text: text to match the definition.
        :return: the register step if exists otherwise None.
        """

        step_defs = self._step_defs[keyword]
        for stp in step_defs:
            if stp.pattern.match(text):
                return stp
        return None


class Registry:
    """
    Layered step definitions registry.

    A facade for {class}`ModRegistry` to have step definitions in a tree.
    """

    def __init__(self) -> None:
        self._step_defs: dict[str, ModRegistry] = defaultdict(ModRegistry)

    def append(
        self, module_name: str, keyword: StepKeyword, step: StepDefinition
    ) -> None:
        """
        Append the step definition to the module name registry.

        :param module_name: the name of the module of the step is registered.
        :param keyword: gherkin keyword for the definition.
        :param step: step definition to append.
        """
        self._step_defs[module_name].append(keyword, step)

    def get_fixtures(self, module_name: str) -> Mapping[str, type]:
        """
        Return the list of fixtures that has to be imported at the module.

        :return: a mapping where the key is the alias name and value is the
            type to import.
        """
        fixtures: dict[str, type] = {}

        parts = module_name.split(".")
        module_name = parts.pop(0)
        while True:
            if module_name in self._step_defs:
                fixtures.update(self._step_defs[module_name].get_fixtures())
            if parts:
                module_name = f"{module_name}.{parts.pop(0)}"
            else:
                break
        return fixtures

    def get_models_types(self, module_name: str) -> dict[type, str]:
        """
        Registered data types, used in order to build imports on tests.
        The type are aliased during registration to avoid conflict name at import time
        during the ast generation.

        :param module_name: the name of the module the step is retrieve,
            and lookup from the current module to its ancestors,
            retrieving the first that match.
        :return: type as key, alias as value.
        """
        model_types: dict[type, str] = {}

        parts = module_name.split(".")
        module_name = parts.pop(0)
        while True:
            if module_name in self._step_defs:
                model_types.update(self._step_defs[module_name].models_types)
            if parts:
                module_name = f"{module_name}.{parts.pop(0)}"
            else:
                break
        return model_types

    def get_step(
        self, module_name: str, keyword: StepKeyword, text: str
    ) -> StepDefinition | None:
        """
        Get the first registered step that match the text.

        :param module_name: the name of the module the step is retrieve,
            and lookup from the current module to its ancestors,
            retrieving the first that match.
        :param keyword: gherkin keyword for the definition.
        :param text: text to match the definition.
        :return: the register step if exists otherwise None.
        """
        parts = module_name.split(".")
        while parts:
            mod_path = ".".join(parts)
            if mod_path in self._step_defs:
                if handle := self._step_defs[mod_path].get_step(keyword, text):
                    return handle
            parts.pop()
        return None

    def get_matched_step(
        self,
        module_name: str,
        keyword: StepKeyword,
        text: str,
        fixtures: Mapping[str, Any],
    ) -> tuple[StepDefinition | None, Mapping[str, Any]]:
        """
        Get the first registered step that match the text.

        :param module_name: the name of the module the step is retrieve,
            and lookup from the current module to its ancestors,
            retrieving the first that match.
        :param keyword: gherkin keyword for the definition.
        :param text: text to match the definition.
        :return: the register step if exists otherwise None with its associated step
            definition parameters.
        """
        step_def = self.get_step(module_name, keyword, text)
        if step_def:
            matches = step_def.pattern.get_matches(text, fixtures)
            return step_def, matches or {}
        return None, {}

    def get_best_matches(
        self,
        module_name: str,
        text: str,
    ) -> list[str]:
        """
        Get the first registered step that match the text.

        :param module_name: use the module and all its ancestors to retrieve a match.
        :param text: text to match the definition.
        :return: the list of steps that could be usefull.
        """
        parts = module_name.split(".")
        matches: list[tuple[float, str]] = []
        while parts:
            mod_path = ".".join(parts)
            if mod_path in self._step_defs:
                matches += self._step_defs[mod_path].get_best_matches(text)
            parts.pop()
        matches = list(set(matches))
        matches.sort(reverse=True)
        sure_threshold = 0.9
        while sure_threshold >= 0.4:
            match_text = [match[1] for match in matches if match[0] > sure_threshold]
            if match_text:
                return match_text
            sure_threshold -= 0.1
        return []


class Tursu:
    """Store all the handlers for gherkin action."""

    DATA_TABLE_EMPTY_CELL = ""
    """
    This value is used only in case of data_table types usage.
    If the table contains this value, then, it is ommited by the constructor in order
    to let the type default value works.

    In case of list[dict[str,str]], then this is ignored, empty cells exists with
    an empty string value.
    """

    def __init__(self) -> None:
        self.scanned: set[ModuleType] = set()
        self._registry = Registry()

    def get_fixtures(self, module_name: str) -> Mapping[str, type]:
        """
        Return the list of fixtures that has to be imported at the module.

        :return: a mapping where the key is the alias name and value is the
            type to import.
        """
        return self._registry.get_fixtures(module_name)

    def register_step_definition(
        self,
        module_name: str,
        keyword: StepKeyword,
        pattern: str | AbstractPattern,
        handler: Handler,
    ) -> None:
        """
        Register a step handler for a step definition.

        This method is the primitive for [@given](#tursu.given),
        [@when](#tursu.when) and [@then](#tursu.then) decorators.

        :param module_name: the name of the module of the step is registered.
        :param keyword: gherkin keyword for the definition.
        :param pattern: pattern to match the definition.
        :param handler: function called when a step in a scenario match the pattern.
        """
        step = StepDefinition(pattern, handler)
        self._registry.append(module_name, keyword, step)

    def get_step(
        self, module_name: str, keyword: StepKeyword, text: str
    ) -> StepDefinition | None:
        """
        Get the first registered step that match the text.

        :param module_name: the name of the current module.
        :param keyword: gherkin keyword for the definition.
        :param text: text to match the definition.
        :return: the register step if exists otherwise None.
        """
        return self._registry.get_step(module_name, keyword, text)

    def get_models_types(self, module_name: str) -> dict[type, str]:
        """
        Registered data types, used in order to build imports on tests.
        The type are aliased during registration to avoid conflict name at import time
        during the ast generation.

        :param module_name: the name of the module the step is retrieve,
            and lookup from the current module to its ancestors,
            retrieving the first that match.
        :return: type as key, alias as value.
        """
        return self._registry.get_models_types(module_name)

    def get_models_type(self, module_name: str, typ: type[Any]) -> str:
        """
        Get the alias name of a given type used to build the model type
        during AST compilation.

        :param module_name: the name of the module the step is retrieve,
            and lookup from the current module to its ancestors,
            retrieving the first that match.
        :param typ: the type of the model.
        :return: alias of the type.
        """
        return self._registry.get_models_types(module_name)[typ]

    def get_best_matches(self, module_name: str, text: str) -> list[str]:
        return self._registry.get_best_matches(module_name, text)

    def extract_fixtures(
        self, module_name: str, keyword: StepKeyword, text: str, **kwargs: Any
    ) -> Mapping[str, Any]:
        """
        Extract fixture for a step from the given pytest fixtures of the test function.

        :param module_name: module name where the step has to be found.
        :param keyword: gherkin step to match.
        :param text: text to match the definition.
        :param kwargs: the fixtures pytest fixtures from the test function.
        :return: the fixtures for the step handler.
        """
        step = self._registry.get_step(module_name, keyword, text)
        if step is None:
            raise Unregistered(module_name, self, keyword, text)
        return step.pattern.extract_fixtures(text) or {}

    def run_step(
        self,
        tursu_runner: "TursuRunner",
        keyword: StepKeyword,
        text: str,
        **kwargs: Any,
    ) -> None:
        """
        Run the step that match the parameter and emit information to the runner.

        :param tursu_runner: the fixtures pytest fixtures from the test function.
        :param keyword: gherkin step to match.
        :param text: text to match the definition.
        :param kwargs: the fixtures pytest fixtures from the test function.
        """
        handler, matches = self._registry.get_matched_step(
            tursu_runner.module_name, keyword, text, kwargs
        )
        if handler:
            tursu_runner.emit_running(keyword, handler, matches)
            try:
                handler(**matches)
            except Exception:
                tursu_runner.emit_error(keyword, handler, matches)
                raise
            else:
                tursu_runner.emit_success(keyword, handler, matches)
        else:
            tursu_runner.emit_error(
                keyword, StepDefinition(text, lambda: None), {}, unregistered=True
            )
            raise Unregistered(tursu_runner.module_name, self, keyword, text)

    def scan(self, mod: ModuleType | None = None) -> "Tursu":
        """
        Scan the module (or modules) containing steps.

        :param mod: optionally module to import, usually the function caller module.
        :return: the current tursu registry for multiple scan purpose.
        """
        if mod is None:
            import inspect

            mod = inspect.getmodule(inspect.stack()[1][0])
            assert mod
            module_name = mod.__name__
            if "." in module_name:  # Check if it's a submodule
                parent_name = module_name.rsplit(".", 1)[0]  # Remove the last part
                mod = sys.modules.get(parent_name)

        assert mod
        if mod not in self.scanned:
            self.scanned.add(mod)
            scanner = venusian.Scanner(registry=self)
            scanner.scan(mod, categories=[VENUSIAN_CATEGORY])
        return self
