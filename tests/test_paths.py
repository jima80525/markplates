import markplates
import pathlib
import pytest


def test_bad_import(tmp_path):
    # test failing import
    template = tmp_path / "bad_import.mdt"
    template.write_text('{{ import_source("no_file.py") }}')
    with pytest.raises(FileNotFoundError):
        markplates.process_template(template, False)

    # test successful import
    template = tmp_path / "good_import.mdt"
    template.write_text('{{ import_source("%s") }}' % __file__)
    markplates.process_template(template, False)


def test_bad_path(tmp_path):
    # test setpath to non existent directory
    template = tmp_path / "bad_path.mdt"
    template.write_text('{{ set_path("/does/not/exist") }}')
    with pytest.raises(FileNotFoundError):
        markplates.process_template(template, False)

    # test with filename
    template = tmp_path / "good_path.mdt"
    template.write_text('{{ set_path("%s") }}' % __file__)
    with pytest.raises(FileNotFoundError):
        markplates.process_template(template, False)

    # test with proper path
    good_dir = pathlib.Path(__file__).parent
    template = tmp_path / "good_path.mdt"
    template.write_text('{{ set_path("%s") }}' % good_dir)
    markplates.process_template(template, False)
