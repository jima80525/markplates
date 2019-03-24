''' Task definitions for invoke command line utility for building, testing and
    releasing markplates. '''
from invoke import run
from invoke import task
import pytest


@task
def test(c):
    pytest.main(['--cov=markplates',
                 '--cov-report=term-missing',
                 '--cov-report=term:skip-covered',
                 'tests'])


@task
def tox(c):
    print("coming soon!")


@task
def release(c):
    print("coming soon!")


@task
def format(c):
    run("black -l 80 markplates")
    print("coming soon!")
