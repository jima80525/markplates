""" Task definitions for invoke command line utility for building, testing and
    releasing markplates. """
from invoke import run
from invoke import task
import pytest
from setuptools import sandbox


@task
def test(c):
    pytest.main(
        [
            "--cov=markplates",
            "--cov-report=term-missing",
            "--cov-report=term:skip-covered",
            "tests",
        ]
    )


@task
def build(c):
    sandbox.run_setup("setup.py", ["clean", "bdist_wheel"])


@task
def tox(c):
    print("coming soon!")


@task
def release(c):
    print("coming soon!")


@task
def format(c):
    run("black -l 80 markplates")
    run("black -l 80 tests")


@task
def clean(c, bytecode=False, test=False, extra=""):
    patterns = ["build/", "dist/", "markplates.egg-info/"]
    if bytecode:
        patterns.append("__pycache__/")
        patterns.append("markplates/__pycache__/")
        patterns.append("tests/__pycache__/")
    if test:
        patterns.append(".coverage")
        patterns.append(".pytest_cache/")
        patterns.append(".tox/")
    if extra:
        patterns.append(extra)
    for pattern in patterns:
        c.run("rm -rf {}".format(pattern))


@task
def distclean(c):
    clean(c, True, True)
