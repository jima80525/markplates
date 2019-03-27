import pytest

# Adding this file helps pytest work out path to simplify testing!


@pytest.fixture
def counting_lines():
    """ A simple list of strings, each with x\n where x is the line number. """
    def _gen_lines(limit=13):
        return [str(x + 1) + "\n" for x in range(limit)]
    return _gen_lines
