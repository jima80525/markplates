import markplates
import pathlib
import pytest

def test_condense_ranges():
    counting_lines = [str(x+1) + "\n" for x in range(13)]

    ranges = [2, ]
    output_lines = markplates.condense_ranges(counting_lines, ranges)
    assert '2\n' in output_lines
    assert '3\n' not in output_lines

    # output_lines = markPlates.condense_ranges(counting_lines, None)
    # ranges = ["2", 3, "5-6", "9-$", ]
    # ranges = ["9-$", "2", "5-6", 3, "5-6", "9-$", ]


def test_bad_import(tmp_path):
    # test failing import
    template = tmp_path / "bad_import.mdt"
    template.write_text('{{ import_source("no_file.py") }}')
    with pytest.raises(FileNotFoundError):
        markplates.process_template(template)

    # test successful import
    template = tmp_path / "good_import.mdt"
    template.write_text('{{ import_source("%s") }}' % __file__)
    markplates.process_template(template)


def test_bad_path(tmp_path):
    # test setpath to non existent directory
    template = tmp_path / "bad_path.mdt"
    template.write_text('{{ set_path("/does/not/exist") }}')
    with pytest.raises(FileNotFoundError):
        markplates.process_template(template)

    # test with filename
    template = tmp_path / "good_path.mdt"
    template.write_text('{{ set_path("%s") }}' % __file__)
    with pytest.raises(FileNotFoundError):
        markplates.process_template(template)

    # test with proper path
    good_dir = pathlib.Path(__file__).parent
    template = tmp_path / "good_path.mdt"
    template.write_text('{{ set_path("%s") }}' % good_dir)
    markplates.process_template(template)
