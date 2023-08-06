# quizlight
quizlight is a simple terminal-based program for test taking and creation. It is written in Python 3. It comes with a Python 3 test module, based on [The Python Tutorial](https://docs.python.org/3/tutorial/).

## Installing
See the latest instructions on the [releases page](https://github.com/dogoncouch/quizlight/releases)


# Usage

## Options
    usage: quizlight [-h] [--version] [-d DIRECTORY] [--learn] [file]
    
    positional arguments:
      file          set the module import file
    
    optional arguments:
      -h, --help    show this help message and exit
      --version     show program's version number and exit
      -d DIRECTORY  set the module import directory
      --learn       turn on learning mode (immediate answer feedback)

## Interface
quizlight has a menu driven interface, based on the lightcli library. There are two modes: test mode, and edit mode.

### Test mode
Test mode is for taking tests. Tests in `/usr/share/doc/quizlight/modules` are loaded by default, unless another directory or file is specified.

Test mode is somewhat secure. EOF and Keyboard Interrupt errors are caught, and there should be no way to get back to the start of the test after a result file is selected. To let someone take a test, save the results, and log them out of the system, run quizlight as follows:

    quizlight ; exit

Select the module, set the save file for results, and the test should be somewhat secure. This has NOT been extensively tested.

#### Learning mode
Learning mode turns on immediate answer feedback. After each question is answered, the correct answer is shown, along with the reason (if present).

### Edit mode
Edit mode is for creating and extending tests. It allows the user to create new tests, add new chapters to existing tests, and extend existing chapters. Editing requires write permission on the module file. Chapters and questions can not be deleted within quizlight.


# Modules

## Files
quizlight modules are stored in python JSON format. quizlight will automatically add the `.json` file extension to new modules, unless it is already there. Files can be written to and loaded from any directory (assuming the right permissions). By default, quizlight looks for modules to load in `/usr/share/doc/quizlight/modules`.

## Creating and Editing
Creating and editing modules is easy; edit mode functions as an interactive guide. There are four steps:
1. Enter a question prompt
2. Enter a list of answers
3. Set the correct answer
4. Enter a reason (optional)

Here is an example:

#### Enter a question prompt
    
    Which animal is the most dangerous?

    a. Fox
    b. Rabbit
    c. Lion
    d. Elephant

#### Enter a list of answers
    
    a
    b
    c
    d

#### Set the correct answer
    
    b

#### Enter a reason
    
    According to a well respected british documentary about King Arthur, there are very dangerous rabbits out there.

## Contributing
Community contributions are welcome! If you would like to add your test module so that others can use it, get in touch with the author at [dpersonsdev@gmail.com](mailto:dpersonsdev@gmail.com).


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
