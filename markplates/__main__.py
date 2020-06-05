#!/usr/bin/env python3
import click
import code
import contextlib
import errno
import io
import jinja2
import os
import pathlib
import re
import sys


class TemplateState:
    def __init__(self):
        self.path = pathlib.Path(".")

    def set_path(self, path):
        self.path = pathlib.Path(path)
        if not self.path.is_dir():
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), self.path
            )
        return ""

    def _add_filename(self, to_add, source, lines):
        if to_add:
            lines.insert(0, "# %s\n" % source)

    def _add_language(self, language, lines):
        if language:
            if language.lower() in ["c", "cpp", "c++"]:
                language = "cpp"
            lines.insert(0, "```%s\n" % language.lower())
            lines.append("```")

    def _strip_trailing_blanks(self, lines):
        if lines:
            while re.search(r"^ *$", lines[-1]):
                del lines[-1]

    def import_source(self, source, ranges=None, language=None, filename=False):
        source_name = self.path / source
        lines = open(source_name, "r").readlines()
        if not ranges:
            ranges = ["2-$"]

        lines = condense_ranges(lines, ranges)
        lines = remove_double_blanks(lines)
        # If the trailing line doesn't have a \n, add one here
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += ("\n")
        self._strip_trailing_blanks(lines)
        lines = left_justify(lines)
        self._add_filename(filename, source, lines)
        self._add_language(language, lines)
        return "".join(lines).rstrip()

    def import_function(
        self, source, function_name, language=None, filename=False
    ):
        """ Search for and extract a function.  Uses VERY simplistic processing
        for this, so I"m concerned this will not play out as well as hoped.
        Basically searches for "def <function>` and then copies all but the
        trailing blank lines to the output.
        If you have two functions of the same name, it will select the first.
        """
        function_pattern = r"(\s*)def\s*" + function_name
        end_pattern = None
        output_lines = []
        source_name = self.path / source
        lines = open(source_name, "r").readlines()
        for line in lines:
            # first see if we're already copying use `end_pattern` as a flag
            if end_pattern:
                if re.search(end_pattern, line):
                    end_pattern = None
                else:
                    output_lines.append(line)
            else:
                matchObj = re.match(function_pattern, line)
                if matchObj:
                    output_lines.append(line)
                    end_pattern = r"^ {0,%d}\w" % len(matchObj.group(1))

        self._strip_trailing_blanks(output_lines)
        output_lines = left_justify(output_lines)
        self._add_filename(filename, source, output_lines)
        self._add_language(language, output_lines)
        return "".join(output_lines).rstrip()

    def import_repl(self, source):
        # split into individual lines
        lines = source.split("\n")
        # it's a bit cleaner to start the first line of code on the line after
        # the start of the string, so remove a single blank line from the start
        # if it's present
        if len(lines[0]) == 0:
            lines.pop(0)

        # set up the console and prompts
        console = code.InteractiveConsole()
        ps1 = ">>> "
        ps2 = "... "
        prompt = ps1

        with io.StringIO() as output:
            with contextlib.redirect_stdout(output):
                with contextlib.redirect_stderr(output):
                    for line in lines:
                        # don't show prompt on blank lines - spacing looks
                        # better this way
                        if len(line) != 0:
                            print(f"{prompt}{line}")
                        else:
                            print()
                        console.push(line)
                        if line.endswith(":"):
                            prompt = ps2
                        elif len(line) == 0:
                            prompt = ps1
            # Trim trailing blank lines
            outputString = output.getvalue()
            while outputString[-1] == "\n" and outputString[-2] == "\n":
                outputString = outputString[:-1]
                # degenerate case of entirely empty repl block
                # still return a single blank line
                if len(outputString) < 2:
                    return outputString
            return outputString


def remove_double_blanks(lines):
    """ Takes a list of lines and condenses multiple blank lines into a single
    blank line.
    """
    new_lines = []
    prev_line = ""  # empty line here will remove leading blank space
    for line in lines:
        if len(line.strip()) or len(prev_line.strip()):
            new_lines.append(line)
        prev_line = line
    return new_lines


def left_justify(lines):
    """ Removes a consistent amount of leading whitespace from the front of each
    line so that at least one line is left-justified.
    WARNING: this will fail on mixed tabs and spaces. Don't do that.
    """
    leads = [
        len(line) - len(line.lstrip()) for line in lines if len(line.strip())
    ]
    if not leads:  # degenerate case where there are only blank lines
        return lines
    min_lead = min(leads)
    new_lines = []
    for line in lines:
        if len(line.strip()):
            new_lines.append(line[min_lead:])
        else:
            new_lines.append(line)
    return new_lines


def condense_ranges(input_lines, ranges):
    """ Takes a list of ranges and produces a sorted list of lines from the
    input file.
    Ranges can be in the following form:
        3 or "3" : an integer adds just that line from the input
        "5-7" : a range adds lines between start and end inclusive (so 5, 6, 7)
        "10-$" : an unlimited range includes start line to the end of the file
    LINE NUMBERING STARTS AT 1!
    The algorithm to do this is wildly inefficient. There is almost certainly a
    clever way to use array slices to pull this off, but I found it easier to
    normalize the line numbers (i.e. got them in sorted order and removed
    duplicate number and combined overlaps) by simply creating a list of lines.
    """
    output_numbers = set()
    for _range in ranges:
        # For the single line instances, just convert to int().  This will
        # cover values that are already ints and '3'.
        try:
            rint = int(_range)
            output_numbers.add(rint)
        except ValueError:
            # If it's not a single line, look for a range
            start, end = _range.split("-")
            start = int(start)
            # check for $ on end first
            if end.strip() == "$":
                end = len(input_lines)
            else:
                end = int(end)
            # output_numbers.update(list(range(start, end+1)))
            output_numbers.update(range(start, end + 1))
    # now we have normalized the line numbers, create the list of output lines
    output_lines = list()
    for number in sorted(output_numbers):
        output_lines.append(input_lines[number - 1])
    return output_lines


def process_template(template):
    # alias the block start and stop strings as they conflict with the
    # templating on RealPython.  Currently these are unused here.
    file_loader = jinja2.FileSystemLoader(str(template.parent))
    env = jinja2.Environment(
        loader=file_loader, block_start_string="&&&&", block_end_string="&&&&"
    )
    template = env.get_template(str(template.name))

    template_state = TemplateState()
    for item in dir(TemplateState):
        if not item.startswith("__"):
            template.globals[item] = getattr(template_state, item)
    return template.render()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-v", "--verbose", type=bool, default=False, help="Verbose debugging info"
)
@click.argument("template", type=str)
def main(verbose, template):
    try:
        output = process_template(pathlib.Path(template))
        print(output)
    except FileNotFoundError as e:
        print(f"Unable to import file:{e.filename}", file=sys.stderr)
        sys.exit(1)
    except jinja2.exceptions.TemplateNotFound as e:
        print(f"Unable to import file:{e}", file=sys.stderr)
        sys.exit(1)
