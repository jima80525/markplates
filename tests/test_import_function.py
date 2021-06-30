import markplates
from pathlib import Path
import pytest


def __load_source():
    source_file = Path(__file__).parent.resolve() / "data/source.py"
    with open(source_file) as f:
        source_content = f.read()

    source = source_content.splitlines(keepends=True)
    return source_file, source


def test_import_func(tmp_path):
    source_file, source = __load_source()
    expected = ("".join(source[9:12])).rstrip()

    template = tmp_path / "t_import.mdt"
    template.write_text(
        '{{ set_path("%s") }}{{ import_function("%s", "area") }}'
        % (source_file.parent, source_file.name)
    )
    fred = markplates.process_template(template, False)
    assert fred == expected


def test_import_bad_name(tmp_path):
    source_file, source = __load_source()

    # must match simple_source
    template = tmp_path / "t_import.mdt"
    template.write_text(
        '{{ set_path("%s") }}{{ import_function("%s", "not_present") }}'
        % (source_file.parent, source_file.name)
    )
    with pytest.raises(Exception):
        markplates.process_template(template, False)


def test_add_filename(tmp_path):
    source_file, source = __load_source()
    expected = ("".join(source[9:12])).rstrip()
    expected = "# source.py\n" + expected

    template = tmp_path / "t_import.mdt"
    template.write_text(
        '{{ set_path("%s") }}{{ import_function("%s", "area", None, True) }}'
        % (source_file.parent, source_file.name)
    )
    fred = markplates.process_template(template, False)
    assert fred == expected


# a more complete test of languages is in import_source tests.  It uses the
# same underlying function so we won't retest all of it here.
def test_add_language(tmp_path):
    source_file, source = __load_source()
    expected = "".join(source[9:12])
    expected = "```python\n" + expected + "```"

    template = tmp_path / "t_import.mdt"
    template.write_text(
        '{{ set_path("%s") }}{{ import_function("%s", "area", "Python", False) }}'
        % (source_file.parent, source_file.name)
    )
    fred = markplates.process_template(template, False)
    assert fred == expected
