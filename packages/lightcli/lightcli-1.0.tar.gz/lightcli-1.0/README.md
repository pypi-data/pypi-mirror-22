# lightcli
A Python 3 library module for lightweight terminal interaction

## Index
- [Installing](#installing)
- [Introduction](#introduction)
- [Functions](#functions)
- [Copyright](#copyright)

## Installing
See the latest instructions on the [releases page](https://github.com/dogoncouch/lightcli/releases).


# Introdutcion

## Synopsis
    import lightcli
    
    choice = lightcli.choice_input([options=<options>], [prompt=<prompt>], [showopts={True|False}], [qopt={True|False}])
    multiline = lightcli.long_input([prompt=<prompt>])
    mylist = lightcli.list_input([prompt=<prompt>])
    outputfile = lightcli.outfile_input([extension=<extension>])

## Description
lightcli is a Python 3 module for lightweight terminal interaction.


# Functions

### lightcli.choice\_input([options=\<options\>], [prompt=\<prompt\>], [showopts={True|False}], [qopt={True|False}])

Options:
- `` options `` - list of acceptable answers (list of strings)
- `` prompt `` - text shown when asking for input (a string)
- `` showopts `` - toggles display of options list (default is True)
- `` qopt `` - toggles a 'q to quit' option (default is False)

Prompts for and returns input from a list of choices.

### lightcli.long\_input([prompt=\<prompt\>], [maxlines=\<maxlines\>], [maxlength=\<maxlength\>])

Options:
- `` prompt `` - text shown when asking for input (a string)
- `` maxlines `` - sets the maximum number of lines
- `` maxlength `` - sets the maximum line length

Gets a multi-line string as input. Entering an EOF on a blank line ends the input (ctrl-D in \*nix, ctrl-Z in Windows).

### lightcli.list\_input([prompt=\<prompt\>], [maxitems=\<maxitems\>], [maxlength=\<maxlength\>])

Options:
- `` prompt `` - text shown when asking for input (a string)
- `` maxitems `` - sets the maximum number of items
- `` maxlength `` - sets the maximum item length

Gets a list of strings as input. Each item is entered on a separate line; entering an EOF on a blank line ends the input (ctrl-D in \*nix, ctrl-Z in Windows).

### lightcli.outfile\_input([extension=\<extension\>])

Options:
- `` extension `` - sets the file extension

Returns the name of a writeable output file.


# Copyright
MIT License

Copyright (c) 2017 Dan Persons (dpersonsdev@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
