0.15.1 - Released on 2025-04-05
-------------------------------
* Fix type inference for union types on data_table and doc_string.
  It will not raise an error anymore but they will never be interpreted.

0.15.0 - Released on 2025-04-04
-------------------------------
* Breaking change: Step definitions are not globals anymore,
  they are scoped like pytest fixtures. they lives in a module and all its sub modules.
  A submodules steps can be used to define the definition of the current scenario directory.
  See the [project layout documentation](#(project-layout)) for the details.
* pytest fixtures can be created in the same modules than step definitions.
  Sometimes fixtures does not need to be shared accross submodules, they are locals of a
  part of a test, like having a [@when](#tursu.when) that save a value like downloading a file in the browser,
  and a [@then](#tursu.then) that check its content.

0.14.2 - Released on 2025-03-31
-------------------------------
* Fix docstring in pure str (properly typed...).
* Add support of docstring using python literals.

0.14.1 - Released on 2025-03-30
-------------------------------
* Remove backslash in f-string for python 3.10 an 3.11 support.

0.14.0 - Released on 2025-03-30
-------------------------------
* Implement type model for Gherkin json docstring.
* Fix bug of error reported when a step is not registered.
* Improve hint whe a step definition has not been found.
* More documentation.

0.13.0 - Released on 2025-03-29
-------------------------------
* Breaking changes: the tursu_collect_file has moved, so the conftest.py
  must updated to:
    ```python
    from tursu import tursu_collect_file

    tursu_collect_file()
    ```
* Implement revered data table ( Column Based ).
* Documentation improved.
* Fix usage of request, capsys or even tursu from step definition functions.
* Refactor and cleanup code

0.12.5 - Released on 2025-03-22
-------------------------------
* Internal refactor without new feature.
* Update the documentation.
* Update gherkin step to follow some good gherkin rules.

0.12.4 - Released on 2025-03-19
-------------------------------
* Write the test module on disk only if --trace or -vvv is used.
  This allows to have the full traceback when a test failed with the AST generated code
  displayed.

0.12.3 - Released on 2025-03-19
-------------------------------
* Refactor collect of tests if the module is not loaded.

0.12.2 - Released on 2025-03-17
-------------------------------
* Fix collect of tests if the module is not loaded.

0.12.1 - Released on 2025-03-17
-------------------------------
* Add a pattern matcher based on regular expression.
* fix the cli command while choosing a .feature file directly from the cli.
* Update the doc, add a migrate pytest-bdd.

0.11.1 - Released on 2025-03-15
-------------------------------
* Update description for pypi.
* Update Dockerfile.

0.11.0 - Released on 2025-03-15
-------------------------------
* Breaking change: now tursu is declared as a pytest plugin using entrypoint.
  * the __init__.py will not scan the module, pytest will.
    remove the code here.
  * the conftest.py of the tested file has to be updated.
    The tursu fixture is registered by the plugin, and now, to register tests,
    the new command is:
    ```python
    from tursu.entrypoints.plugin import tursu_collect_file

    tursu_collect_file()
    ```

0.10.1 - Released on 2025-03-15
-------------------------------
* Improve test display on the term.

0.10.0 - Released on 2025-03-14
-------------------------------
* Improve test display.
* Add more doc about playwright and behave.

0.9.0 - Released on 2025-03-12
------------------------------
* Improve test display.
* Add docs on tags.
* Refactor code to use a runner object to have a running state.

0.8.0 - Released on 2025-03-12
------------------------------
* Add support of date and datetime in the pattern matcher.
* Improve the doc.

0.7.0 - Released on 2025-03-11
------------------------------
* Breaking change: Now the registry is named tursu.
* Using -v will print the current gherkin step.

0.6.2 - Released on 2025-03-11
------------------------------
* Implement scenario outline.
* Implement data table.

0.5.1 - Released on 2025-03-10
------------------------------
* Remove asyncio dependency.

0.5.0 - Released on 2025-03-10
------------------------------
* Remove asyncio support.

0.4.0 - Released on 2025-03-10
------------------------------
* Now autorize async method for given when then decorated methods.
* Implement tags converted to pytest marker.
* Implement Rule (do nothing except adding tags).

0.3.1 - Released on 2025-03-10
------------------------------
* Fix annotation support for literal, enums, boolean and float types.

0.3.0 - Released on 2025-03-10
------------------------------
* Add support of docstring in tests.

0.2.0 - Released on 2025-03-09
------------------------------
* Implement a tursu init command.
* Implement the Background keyword.

0.1.3 - Released on 2025-03-09
------------------------------
* Publish the doc.

0.1.2 - Released on 2025-03-09
------------------------------
* Initial release.
