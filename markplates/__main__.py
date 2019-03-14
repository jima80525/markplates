#!/usr/bin/env python3
import click
import errno
import jinja2
import os
import pathlib
import sys


class TemplateState():
    def __init__(self):
        self.path = pathlib.Path(".")

    def set_path(self, path):
        self.path = pathlib.Path(path)
        if not self.path.is_dir():
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),
                                    self.path)
        return ""

    def import_source(self, source, ranges=None):
        source_name = os.path.join(self.path, source)
        lines = open(source_name, 'r').readlines()
        if not ranges:
            ranges = ['2-$', ]

        lines = condense_ranges(lines, ranges)
        return "".join(lines).rstrip()


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


def process_template(template):
    # alias the block start and stop strings as they conflict with the
    # templating on RealPython.  Currently these are unused here.
    file_loader = jinja2.FileSystemLoader(str(template.parent))
    env = jinja2.Environment(loader=file_loader,
                             block_start_string='&&&&',
                             block_end_string='&&&&',
                            )
    template = env.get_template(str(template.name))

    template_state = TemplateState()
    for item in dir(TemplateState):
        if not item.startswith("__"):
            template.globals[item] = getattr(template_state, item)
    return template.render()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-v', '--verbose', type=bool, default=False,
              help='Verbose debugging info')
@click.argument('template', type=str)
def main(verbose, template):
    try:
        output = process_template(pathlib.Path(template))
        print(output)
    except FileNotFoundError as e:
        print(f"Unable to import file:{e.filename}", file=sys.stderr)


if __name__ == "__main__":
    main()
