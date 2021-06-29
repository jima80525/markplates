#!/usr/bin/env python3
import ast
import asttokens
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
import pyperclip

# Global set from command line options. Don't know of a good way to pass options
# through jinja2 to the functions being called from the template
g_indicate_skipped_lines = False


def _descend_tree(atok, parent, local_name, name_parts):
    for node in ast.iter_child_nodes(parent):
        if (
            node.__class__ in [ast.FunctionDef, ast.ClassDef]
            and node.name == local_name
        ):
            if len(name_parts) == 0:
                # Found the node, return the code
                return atok.get_text(node) + "\n"

            # Found a fn or class, but looking for a child of it
            return _descend_tree(atok, node, name_parts[0], name_parts[1:])

        if (
            node.__class__ == ast.Assign
            and node.first_token.string == local_name
            and len(name_parts) == 0
        ):
            return atok.get_text(node) + "\n"

    return ""


def find_in_source(source, name):
    with open(source) as f:
        source_text = f.read()

    try:
        atok = asttokens.ASTTokens(source_text, parse=True)
    except SyntaxError as synErr:
        print(f"Failed to parse {source}: {synErr}")
        sys.exit(1)

    name_parts = name.split(".")
    return _descend_tree(atok, atok.tree, name_parts[0], name_parts[1:])


class TemplateState:
    def __init__(self):
        self.path = pathlib.Path(".")

    def set_path(self, path, show_skipped=False):
        global g_indicate_skipped_lines
        g_indicate_skipped_lines = show_skipped
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

        lines = condense_ranges(lines, ranges, source_name)
        lines = remove_double_blanks(lines)
        # If the trailing line doesn't have a \n, add one here
        if lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"
        self._strip_trailing_blanks(lines)
        lines = left_justify(lines)
        self._add_filename(filename, source, lines)
        self._add_language(language, lines)
        return "".join(lines).rstrip()

    def import_function(
        self, source, function_name, language=None, filename=False
    ):
        """ Search for and extract a function."""
        source_name = self.path / source
        code = find_in_source(source_name, function_name)
        if not code:
            raise Exception(f"Function not found: {function_name}")

        output_lines = code.splitlines(keepends=True)
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
        prompt = ps1

        with io.StringIO() as output:
            with contextlib.redirect_stdout(output):
                with contextlib.redirect_stderr(output):
                    ps2 = "... "
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
            while outputString[-1] == "\n":
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


def condense_ranges(input_lines, ranges, source_name):
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
            if _range == "$":
                # $ on its own means last line
                output_numbers.add(len(input_lines))
            else:
                # If it's not a single line, look for a range
                start, end = _range.split("-")
                if start == "$":
                    # Support negative indexing on lines, end will be the last
                    # line, start will be the last line minus the "end" value
                    # in the range
                    count = int(end)
                    end = len(input_lines)
                    start = end - count
                else:
                    # Start of range is a number
                    start = int(start)
                    # check for $ on end first
                    end = len(input_lines) if end.strip() == "$" else int(end)
                # output_numbers.update(list(range(start, end+1)))
                output_numbers.update(range(start, end + 1))
    output_numbers = sorted(output_numbers)
    # fail if they explicitly requested beyond the end of the file
    if len(input_lines) < output_numbers[-1]:
        print(
            f"Requested {output_numbers[-1]} lines from {source_name}. "
            "Past end of file!"
        )
        sys.exit(1)
    if g_indicate_skipped_lines:
        output = []
        for index, line_number in enumerate(output_numbers):
            line = input_lines[line_number - 1]
            output.append(line)
            if (
                index + 1 < len(output_numbers)
                and output_numbers[index + 1] - output_numbers[index] > 2
            ):
                if len(input_lines[line_number - 2]) != 0:
                    output.append("\n")

                num_indent = len(line) - len(line.lstrip())
                prefix = " " * num_indent
                output.append(f"{prefix}# ...\n")
                if len(input_lines[line_number]) != 0:
                    output.append("\n")
    else:
        output = [input_lines[number - 1] for number in output_numbers]

    return output


def process_template(template, square):
    # alias the block start and stop strings as they conflict with the
    # templating on RealPython.  Currently these are unused here.
    file_loader = jinja2.FileSystemLoader(str(template.parent))

    kwargs = {
        "loader":file_loader, 
        "block_start_string":"&&&&", 
        "block_end_string":"&&&&"
    }

    if square:
        kwargs.update({
            'variable_start_string':'[[',
            'variable_end_string':']]',
        })

    env = jinja2.Environment(**kwargs)
    template = env.get_template(str(template.name))

    template_state = TemplateState()
    for item in dir(TemplateState):
        if not item.startswith("__"):
            template.globals[item] = getattr(template_state, item)
    return template.render()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-v", "--verbose", is_flag=True, help="Verbose debugging info")
@click.option(
    "-c", "--clip", is_flag=True, help="RealPython output to clipboard"
)
@click.option(
    "-s", "--square", is_flag=True, help="Use [[ ]] for template tags"
)
@click.argument("template", type=str)
def main(verbose, clip, square, template):
    try:
        output = process_template(pathlib.Path(template), square)
        print(output)
        sys.stdout.flush()
        if clip:
            # copy lines to clipboard, but skip the first title and the
            # subsequent blank line
            lines = output.split("\n")
            to_clip = "\n".join(lines[2:])

            # NOTE: there seems to be a bug in pyperclip that is emitting output
            # to stdout when the clipboard gets too large. Redirecting stdout
            # to devnull seems to resolve the issue (along with the flush()
            # above).  This is ugly, but works
            fdnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(fdnull, 1)
            try:
                pyperclip.copy(to_clip)
            finally:
                os.close(fdnull)

    except FileNotFoundError as e:
        print(f"Unable to import file:{e.filename}", file=sys.stderr)
        sys.exit(1)
    except jinja2.exceptions.TemplateNotFound as e:
        print(f"Unable to import file:{e}", file=sys.stderr)
        sys.exit(1)
