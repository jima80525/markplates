import markplates
import pytest


@pytest.fixture
def counting_lines():
    """ A simple list of strings, each with x\n where x is the line number. """
    return [str(x + 1) + "\n" for x in range(13)]


def test_counting_range(counting_lines):
    # only pull line two
    ranges = [2]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert output_lines == ["2\n"]

    # only pull line two as string
    ranges = ["2"]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert output_lines == ["2\n"]

    # pull even lines
    ranges = [2, "4", 6, "8"]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert output_lines == ["2\n", "4\n", "6\n", "8\n"]

    # pull 8 to the end
    ranges = ["8-$"]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert output_lines == ["8\n", "9\n", "10\n", "11\n", "12\n", "13\n"]

    # pull 8 to 10
    ranges = ["8-10"]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert output_lines == ["8\n", "9\n", "10\n"]


def test_spacing(counting_lines):
    # only pull line two
    ranges = [" 2    "]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert output_lines == ["2\n"]

    # pull 8 to the end
    ranges = ["8    -\t$               "]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert output_lines == ["8\n", "9\n", "10\n", "11\n", "12\n", "13\n"]

    # pull 8 to 10
    ranges = ["\t8\t-\t10\t"]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert output_lines == ["8\n", "9\n", "10\n"]


def test_ordering(counting_lines):
    # test mixed up rants
    ranges = ["9-$", "2", "5-6", 3, "5-6", "9-$"]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert output_lines == [
        "2\n",
        "3\n",
        "5\n",
        "6\n",
        "9\n",
        "10\n",
        "11\n",
        "12\n",
        "13\n",
    ]

    # test repeated lines
    ranges = ["2", "5-6", 2, "5-6", "6"]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert output_lines == ["2\n", "5\n", "6\n"]
