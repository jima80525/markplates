# MarkPlates 

> A templating utility for keeping code in Markdown documents in sync.


The problem I hope to solve is to simplify keeping external files up to date with markdown documents that contain them.  This happens to me frequently when an editor makes a suggestion to an article that will modify the underlying code it is quoting.  

This is currently in the proof-of-concept stage.

## Installing

Currently this is not packaged at all.   That's pretty high on the todo list.  Right now you have to copy it from github and run manually.

`Markplates` relies on the `jinja2` package which you can get via:

`pip3 install jinja2`

The prototype has only been tested on Python3.7.  Expanding tested versions is also on the TODO list.

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
* Tox testing to cover several Py3 versions (Py2 support not planned at this point)
* Pytest unit tests
* Better examples
* Packaging
* Just about everything that would make this a package. :) 
* Windows and Mac testing/support

## Interested?

Let me know!  I'll be working on this for the next few weeks.  If you're interested in the results or would like to help out, please raise an issue and I'll be in touch!

## Release History

* Not yet.