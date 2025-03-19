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
    from tursu.plugin import tursu_collect_file

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
