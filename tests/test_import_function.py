import markplates


def test_import_func(tmp_path):
    simple_source = """
    def first(arg):
        pass


    def second(arg, arg2):
        code
        pass



    def third(arg1, 2):
        pass
    """
    # must match simple_source
    expected_result = """    def second(arg, arg2):
        code
        pass"""

    file_name = "fake_source.py"
    source_file = tmp_path / file_name
    source_file.write_text(simple_source)
    template = tmp_path / "t_import.mdt"
    template.write_text(
        '{{ set_path("%s") }}{{ import_function("%s", "second") }}'
        % (tmp_path, file_name)
    )
    fred = markplates.process_template(template)
    print(fred)
    assert fred == expected_result


def test_import_no_spacing(tmp_path):
    simple_source = """
    def first(arg):
        pass
    def second(arg, arg2):
        code
        pass
    def third(arg1, 2):
        pass
    """
    # must match simple_source
    expected_result = """    def second(arg, arg2):
        code
        pass"""

    file_name = "fake_source.py"
    source_file = tmp_path / file_name
    source_file.write_text(simple_source)
    template = tmp_path / "t_import.mdt"
    template.write_text(
        '{{ set_path("%s") }}{{ import_function("%s", "second") }}'
        % (tmp_path, file_name)
    )
    fred = markplates.process_template(template)
    print(fred)
    assert fred == expected_result


def test_import_different_levels(tmp_path):
    """ Test finding the end of a function when the next logical block is at a
    lower level of indentation. """
    simple_source = """
class fred():
    def function1(self):
        pass
        # more stuff here
        #
        #

    def second(arg, arg2):
        code
        pass

def higher_scope(stuff):
    with session.get(url) as response:
        print(f"Read {len(response.content)} from {url}")
"""
    # must match simple_source
    expected_result = """    def second(arg, arg2):
        code
        pass"""

    file_name = "fake_source.py"
    source_file = tmp_path / file_name
    source_file.write_text(simple_source)
    template = tmp_path / "t_import.mdt"
    template.write_text(
        '{{ set_path("%s") }}{{ import_function("%s", "second") }}'
        % (tmp_path, file_name)
    )
    fred = markplates.process_template(template)
    print(fred)
    assert fred == expected_result
