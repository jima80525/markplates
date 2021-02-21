from pathlib import Path

from markplates.__main__ import find_in_source


def test_find_source():
    p = Path(__file__).resolve().parent / "data/source.py"

    code = find_in_source(p, "area")
    assert "area of a rectangle" in code
    assert code.count("\n") == 3

    code = find_in_source(p, "Square.area")
    assert "Area of this square" in code
    assert code.count("\n") == 3

    # find_in_source strips comments due to using AST
    # code = find_in_source(p, "my_squares")
    # assert "twice as much" in code
    # assert code.count("\n") == 4
