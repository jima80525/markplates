# ![license_markplates](https://raw.githubusercontent.com/jima80525/markplates/master/license_markplates.jpg)

# MarkPlates

> A templating utility for keeping code included in Markdown documents in sync with the original source.

[![CircleCI](https://circleci.com/gh/jima80525/markplates.svg?style=svg)](https://circleci.com/gh/jima80525/markplates) ![black](https://img.shields.io/badge/code%20style-black-000000.svg) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![pyup.io](https://pyup.io/repos/github/jima80525/markplates/shield.svg)](https://pyup.io/account/repos/github/jima80525/markplates/) [![PyPI version](https://badge.fury.io/py/markplates.svg)](https://badge.fury.io/py/markplates) [![Coverage Status](https://coveralls.io/repos/github/jima80525/markplates/badge.svg?branch=master)](https://coveralls.io/github/jima80525/markplates?branch=master)

The problem I hope to solve is to simplify keeping external files up to date with markdown documents that contain them. This happens to me frequently when an editor makes a suggestion to an article that will modify the underlying code it is quoting.

## Installing

You can download and install the latest version of MarkPlates from the PyPI with this command:

```bash
$ pip install --upgrade markplates
```

MarkPlates is currently tested against Python 3.6 and Python 3.7.

## Usage

Running `markplates` is as simple as handing it a file:

```bash
$ markplates template.mdt
```

This will process the template in `template.mdt`, filling it in with data specified in the template.

The `examples` directory has the `simple.mdt` template:

```markdown
# Sample MarkPlates Template
{{ set_path("./examples") }}

This is an example of importing an entire file (minus the first line):
{{ import_source("testfile.py") }}

While this silly example imports some of the lines from the file, demonstrating ranges:
{{ import_source("testfile.py", [5, "2", 3, "8-$", ]) }}

{{ import_repl(
"""
def func(x):
    if x:
        print(x)

func(True)
func(False) """) }}
```

This demonstrates setting the path and pulling in some of the lines of a file. You can also examine the `README.mdt` file in this library which is used to create this `README.md`.

To use on your own project create a markdown document with special tags to indicate a `markplates` function call.  The delimiter for these tags is `{{` function goes here `}}`.

> **Note:** if you need to add `{{` characters which should not be processed as a template, you can put them in a `{{ '' }}`  block to escape them. Template processing is done with `Jinja2` so Markplates uses the same escape sequences.

`Markplates` supports these functions:

*  `set_path("path/to/source/files")`
* `import_source("source_file_name", [list of line number ranges])`
* `import_function("source_file_name", "function_name")`
* `import_repl("code to run in repl")`

### `set_path()`

The `set_path()` function allows you to specify the base directory to use when searching for source files.  Each call to this function will apply from that point in the template down.

The path must be included in single or double qoutes. If not specified, the path defaults to ".", the current directory.

Examples:


```
{{set_path(".")}}  #sets path to the default
{{set_path("/home/user/my/project")}} # points the path to your project
```

The `set_path()` command is not required as all other functions will take full paths to files.

### `import_source()`

The `import_source()` function will pull in the contents of a source file.  Optional line number ranges can be specified (see description below). The filename must be in quotes.

If no line number ranges are specified, the first line of the file will be omitted.  This is to prevent the `#!/usr/bin/env python` line from cluttering the markdown article. If you want to include the first line, use the range: `1-$`.

Examples:

```
{{import_source("__main__.py")}} # includes all but line 1 from `__main__.py` file
{{import_source("__main__.py", ["1-$",])}} # imports all lines from `__main__.py`
{{import_source("__main__.py", [1, "3", "5-$"])}} # imports all lines except lines 2 and 4 from `__main__.py`
```

`MarkPlates` will display an error message to `stderr` if a file is not found.

### `import_function()`

The `inport_function` function will search the source file and include only the specified function. If there are multiple functions with the same name in the source_file, only the first will be included (and you shouldn't have multiple functions with the same name anyway!).

Whitespace following the function will not be included.

Examples:

```
{{import_function("__main__.py", "condense_ranges")}} # imports the function named `condense_ranges` from `__main__.py`
```

`MarkPlates` handles nested functions, included any functions nested in the specified function.

### `import_repl()`

The `import_repl` function takes the input parameter and splits it into separate lines.  Each line of the input will be run in a REPL with the `stdout` and `stderr` captured to insert into the final output. The result should appear similar to a copy-paste from running the same commands manually.

There is an exception, however.  Blank input lines are used for spacing and will not display the `>>>` prompt one would normally see in the REPL.

Example:

```
{{import_repl(
"""
def func(x):
    if x:
        print(x)

func(True)
func(False) """) }}
```


Output:
```
>>> def func(x):
...     if x:
...         print(x)

>>> func(True)
True
>>> func(False)

```

### Line Number Ranges

Line number ranges allow you to specify which lines you want to include from the source file.   Ranges can be in the following form:

* 3 or "3" : an integer adds just that line from the input

* "5-7" : a range adds lines between start and end inclusive (so 5, 6, 7)

* "10-$" : an unlimited range includes start line to the end of the file

> **Note:** LINE NUMBERING STARTS AT 1!

## Features to Come

I'd like to add:

* Capturing the results of a shell command and inserting into the file
* Copying the resultant Markdown file to the clipboard
* Running `black` over the included Python source
* Windows and Mac testing/support

## Interested?

Let me know!  If you're interested in the results or would like to help out, please raise an issue and I'll be in touch!

## Release History

* 1.1.0 Added `import_repl` functionality

* 1.0.0 Initial release

License plate graphic thanks to [ACME License Maker](https://www.acme.com/licensemaker/)
