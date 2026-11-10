import markplates
import click.testing


def test_no_template():
    """ Specifying a non-existent template in a non-zero exit code. """
    runner = click.testing.CliRunner()
    result = runner.invoke(markplates.main, ["NoTemplateAtAll"])
    assert result.exit_code == 1
    assert result.exception


def test_bad_path_from_main(tmp_path):
    # test setpath to non existent directory
    template = tmp_path / "bad_path.mdt"
    template.write_text('{{ set_path("/does/not/exist") }}')
    runner = click.testing.CliRunner()
    result = runner.invoke(markplates.main, [str(template)])
    assert result.exit_code == 1
    assert result.output.startswith("Unable to import file:")


def test_successful_path_in_main(tmp_path):
    """ Being anal retentive here to get the last line covered. :) """
    template = tmp_path / "good_path.mdt"
    template.write_text("just normal text")
    markplates.process_template(template, False)
    runner = click.testing.CliRunner()
    result = runner.invoke(markplates.main, [str(template)])
    assert result.exit_code == 0
    assert result.output == "just normal text\n"


def test_unknown_function_from_main(tmp_path):
    """ Unknown function is a clean CLI error, not a traceback. """
    source_file = tmp_path / "source.py"
    source_file.write_text("def area(x):\n    return x\n")
    template = tmp_path / "unknown_func.mdt"
    template.write_text(
        '{{ set_path("%s") }}{{ import_function("%s", "not_present") }}'
        % (tmp_path.as_posix(), source_file.name)
    )
    runner = click.testing.CliRunner()
    result = runner.invoke(markplates.main, [str(template)])
    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert result.output.startswith("Unable to import function:")
    assert "Traceback" not in result.output
