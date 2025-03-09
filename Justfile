package := 'tursu'
default_unittest_suite := 'tests/unittests'
default_functest_suite := 'tests/functionals'

install:
    uv sync --group dev --frozen

update:
    uv sync --group dev

upgrade:
    uv sync --group dev --upgrade

doc:
    uv sync --group dev --group docs
    cd docs && uv run make html
    xdg-open docs/build/html/index.html

cleandoc:
    rm -rf docs/build
    rm -rf docs/source/develop

lint:
    uv run ruff check .

typecheck:
    uv run mypy src

test: lint typecheck unittest functest

unittest test_suite=default_unittest_suite:
    uv run pytest -sxv {{test_suite}}

functest test_suite=default_functest_suite:
    uv run pytest -sxv {{test_suite}}

lf:
    uv run pytest -sxvvv --lf

cov test_suite=default_unittest_suite:
    rm -f .coverage
    rm -rf htmlcov
    uv run pytest --cov-report=html --cov={{package}} {{test_suite}}
    xdg-open htmlcov/index.html


fmt:
    uv run ruff check --fix .
    uv run ruff format src tests


release major_minor_patch: test && changelog
    uvx --with=pdm,pdm-bump --python-preference system pdm bump {{major_minor_patch}}
    uv sync --frozen --group dev

changelog:
    uv run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md

publish:
    git commit -am "Release $(uv run scripts/get_version.py)"
    git push
    git tag "v$(uv run scripts/get_version.py)"
    git push origin "v$(uv run scripts/get_version.py)"
