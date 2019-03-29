import markplates


def test_import_full(tmp_path, counting_lines):
    lines = counting_lines(3)
    # expect all lines except the first with \n after all except the last line
    expected_result = "".join(lines[1:]).rstrip()

    file_name = "fake_source.py"
    source_file = tmp_path / file_name
    source_file.write_text("".join(lines))
    template = tmp_path / "t_import.mdt"
    template.write_text(
        '{{ set_path("%s") }}{{ import_source("%s") }}' % (tmp_path, file_name)
    )
    fred = markplates.process_template(template)
    assert fred == expected_result


def test_import_partial(tmp_path, counting_lines):
    lines = counting_lines(5)
    # expect all lines except the first with \n after all except the last line
    expected_result = "".join(lines[2:]).rstrip()

    file_name = "fake_source.py"
    source_file = tmp_path / file_name
    source_file.write_text("".join(lines))
    template = tmp_path / "t_import.mdt"
    template.write_text(
        '{{ set_path("%s") }}{{ import_source("%s", ["3-5"]) }}'
        % (tmp_path, file_name)
    )
    fred = markplates.process_template(template)
    assert fred == expected_result
