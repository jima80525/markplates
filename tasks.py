""" Task definitions for invoke command line utility for building, testing and
    releasing markplates. """
from invoke import run
from invoke import task
import pytest
import setuptools
import sys

VERSION = "1.3.0"


@task
def test(c):
    """ Run unit tests with coverage report. """
    pytest.main(
        [
            "--cov=markplates",
            "--cov-report=term-missing",
            "--cov-report=term:skip-covered",
            "tests",
        ]
    )


@task
def tox(c):
    """ Run tox to test all supported Python versions. """
    run("tox")


@task
def format(c):
    """ Run black over all source to reformat. """
    files = ["markplates", "tests", "tasks.py", "setup.py"]
    for name in files:
        run(f"black -l 80 {name}")


@task
def clean(c, bytecode=False, test=False, extra=""):
    """ Remove any built objects.  -b removes bytecode, -t testfiles -e extra"""
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


def status(s):
    """Prints things in bold."""
    print("\033[1m{0}\033[0m".format(s))


@task
def readme(c):
    """ Process the README.mdt into README.md. """
    status(f"Creating README.md…")
    run("./markplates.py README.mdt > README.md")


@task
def patch(c):
    """ Update version for patch release. """
    status(f"Updating version from {VERSION}…")
    run("bumpversion patch --tag --commit")


@task
def version(c):
    """ Update version for minor release. """
    status(f"Updating version from {VERSION}…")
    run("bumpversion minor --tag --commit")


@task
def distclean(c):
    """ Cleans up everything. """
    status("Cleaning project…")
    clean(c, True, True)


@task
def build(c):
    """ Builds source and wheel distributions """
    status("Building Source and Wheel (universal) distribution…")
    run("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))


@task
def check_dist(c):
    """ Uses twine to check distribution. """
    status("Checking dist")
    run("twine check dist/*")


@task(distclean, build, check_dist)
def release(c):
    """ Creates distribution and pushes to PyPi. """
    status("Uploading the package to PyPI via Twine…")
    run("twine upload dist/*")

    status("Pushing git tags…")
    run("git push --tags")


@task(distclean, build, check_dist)
def test_release(c):
    """ Push to test PyPi.
        Use this command to test the download:
        pip install --index-url https://test.pypi.org/simple/ \
                --extra-index-url https://pypi.org/simple your-package
    """
    status("Uploading the package to TEST PyPI via Twine…")
    run("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
