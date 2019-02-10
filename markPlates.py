#!/usr/bin/env python3
import jinja2
import os


class TemplateState():
    def __init__(self):
        self.path = None

    def set_path(self, path):
        self.path = path
        return "SET PATH TO " + path

    def import_source(self, source, ranges=None):
        print(f"IN FUNC: path: {self.path} source {source} ranges {ranges}")
        source_name = os.path.join(self.path, source)
        lines = open(source_name, 'r').readlines()
        if not ranges:
            ranges = ['2-$', ]

        # JHA TODO probably need to strip off trailing \n
        lines = condense_ranges(lines, ranges)
        return "".join(lines)


def condense_ranges(input_lines, ranges):
    ''' Takes a list of ranges and produces a sorted list of lines from the
    input file.
    Ranges can be in the following form:
        3 or "3" : an integer adds just that line from the input
        "5-7" : a range adds lines between start and end includsive (so 5, 6, 7)
        "10-$" : an unlimited range includes start line to the end of the file
    LINE NUMBERING STARTS AT 1!
    The algorithm to do this is wildly inefficient. There is almost certainly a
    clever way to use array slices to pull this off, but I found it easier to
    normalize the line numbers (i.e. got them in sorted order and removed
    duplicate number and combined overlaps) by simply creating a list of lines.
    '''
    output_numbers = set()
    for _range in ranges:
        # For the single line instances, just convert to int().  THis will cover
        # values that are already ints and '3'.
        try:
            rint = int(_range)
            output_numbers.add(rint)
        except ValueError:
            # If it's not a single line, look for a range
            start, end = _range.split('-')
            start = int(start)
            # check for $ on end first
            if end.strip() == '$':
                end = len(input_lines)
            else:
                end = int(end)
            # output_numbers.update(list(range(start, end+1)))
            output_numbers.update(range(start, end+1))
    # now we have normalized the line numbers, create the list of output lines
    output_lines = list()
    for number in sorted(output_numbers):
        output_lines.append(input_lines[number-1])
    return output_lines


def process_template(template_name, source_path):
    # alias the block start and stop strings as they conflict with dan's
    # templating
    file_loader = jinja2.FileSystemLoader(source_path)
    env = jinja2.Environment(loader=file_loader,
                             block_start_string='&&&&',
                             block_end_string='&&&&',
                            )
    template = env.get_template(template_name)

    template_state = TemplateState()
    template.globals['set_path'] = template_state.set_path
    template.globals['import_source'] = template_state.import_source

    return template.render()


if __name__ == "__main__":
    # JHA TODO add command line option to get path
    output = process_template('simple.mdt', 'tests')
    print(output)

def test_ranges():
    lines = open('tests/testfile.py', 'r').readlines()
    # ranges = ["2", 3, "5-6", "9-$", ]
    ranges = ["9-$", "2", "5-6", 3, "5-6", "9-$", ]
    output_lines = condense_ranges(lines, ranges)
    print(output_lines)
    output = "".join(output_lines)
    print(output)
