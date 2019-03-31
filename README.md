# MarkPlates

> A templating utility for keeping code included in Markdown documents in sync with the original source.

The problem I hope to solve is to simplify keeping external files up to date with markdown documents that contain them. This happens to me frequently when an editor makes a suggestion to an article that will modify the underlying code it is quoting.

This is currently in the proof-of-concept stage.

[![CircleCI](https://circleci.com/gh/jima80525/markplates.svg?style=svg)](https://circleci.com/gh/jima80525/markplates) ![black](https://img.shields.io/badge/code%20style-black-000000.svg)

## Installing

Currently this is not packaged at all.   That's pretty high on the todo list.  Right now you have to copy it from github and run manually.

`Markplates` relies on the `jinja2` package which you can get via:

`pip3 install jinja2`

Markplates is currently tested against Python3.6 and Python3.7.

## Usage

You can test out the example in this package by running:

```bash
$ python -m markplates	simple.mdt examples
```

This will process the template in `examples/simple.mdt`, filling it in with data from `examples/testfile.py`.  This demonstrates setting the path and pulling in some of the lines of a file.

To use, create a markdown document with special tags to indicate a `markplates` function call.  Currently the delimiter for these tags is `{{` function goes here `}}`.

Current functions supported are:

*  `set_path("path/to/source/files")`
* `import_source("source_file_name", [list of line number ranges])`
* `import_function("source_file_name", "function_name")

### `set_path()`

The `set_path()` function allows you to specify the base directory to use when searching for source files.  Each call to this function will apply from that point in the template down.

The path defaults to ".", the current directory.

### `import_source()`

The `import_source()` function will pull in the contents of a source file.  Optional line number ranges can be specified (see description below).

If no line number ranges are specified, the first line of the file will be omitted.  This is to prevent the `#!/usr/bin/env python` line from cluttering the markdown article. If you want to include the first line, use the range: `1-$`.

### `import_function()`

The `inport_function` function will search the source file and include only the specified function. If there are multiple functions with the same name in the source_file, only the first will be included (and you shouldn't have multiple functions with the same name anyway!).

Whitespace following the function will not be included.

### Line Number Ranges

Line number ranges allow you to specify which lines you want to include from the source file.   Ranges can be in the following form:

* 3 or "3" : an integer adds just that line from the input

* "5-7" : a range adds lines between start and end inclusive (so 5, 6, 7)

* "10-$" : an unlimited range includes start line to the end of the file

> **Note:** LINE NUMBERING STARTS AT 1!

## Development Setup

You'll need jinja2, tox, and pytest at this point.  Requirements.txt file to come.

## Features to Come

I'd like to add:

* Capturing the results of a shell command and inserting into the file
* ReadTheDocs documentation
* Pytest unit tests
* Better examples
* Packaging
* Just about everything that would make this a package. :)
* Windows and Mac testing/support

## Interested?

Let me know!  I'll be working on this for the next few weeks.  If you're interested in the results or would like to help out, please raise an issue and I'll be in touch!

## Release History

* Not yet.
