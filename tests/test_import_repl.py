import markplates


def test_syntax_error(tmp_path):
    template = tmp_path / "t_import.mdt"
    template.write_text('{{ import_repl("""++++++""") }}')
    result = markplates.process_template(template)
    assert "SyntaxError" in result


def test_all_spaces(tmp_path):
    expected_result = "before\n\n\n\nafter"
    template = tmp_path / "t_import.mdt"
    with open(template, "w") as temp:
        temp.write('before{{ import_repl("""\n')
        temp.write("\n")
        temp.write("\n")
        temp.write("\n")
        temp.write('"""\n')
        temp.write(") }}after\n")
    result = markplates.process_template(template)
    assert result == expected_result


def test_bad_import(tmp_path):
    template = tmp_path / "t_import.mdt"
    template.write_text('{{ import_repl("""os.path()""") }}')
    result = markplates.process_template(template)
    assert "NameError" in result


def test_function_format(tmp_path):
    expected_result = (
        """before\n>>> def func():\n...     pass\n\n>>> pass\n\n\nafter"""
    )

    template = tmp_path / "t_import.mdt"
    with open(template, "w") as temp:
        temp.write("before\n")
        temp.write('{{ import_repl("""\n')
        temp.write("def func():\n")
        temp.write("    pass\n")
        temp.write("\n")
        temp.write("pass\n")
        temp.write('"""\n')
        temp.write(") }}\n")
        temp.write("after\n")
    result = markplates.process_template(template)
    print(result)
    assert result == expected_result
