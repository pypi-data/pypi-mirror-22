.. -*- coding: utf-8; -*-

########
Weaklisp
########

This is a tool to analyze and format very simple lisp code. It is
mostly directed to lisp extension languages found in CAD programs. It
can document the code in reStructuredText format.

#####
Setup
#####

To install, update or uninstall you can use pip_::

  pip install weaklisp

  pip install --upgrade weaklisp

  pip uninstall weaklisp

.. _pip: https://pip.pypa.io

#####
Usage
#####

.. code::

  $ python -m weaklisp -h
  usage: weaklisp [-h] [-q] [-o OUTPUT] [-f [FORMAT]] path [path ...]

  Analyze simple lisp code.

  positional arguments:
    path                  Path to lisp file to be parsed.

  optional arguments:
    -h, --help            show this help message and exit
    -q, --quiet           Do not print the output.
    -o OUTPUT, --output OUTPUT
                          Save a reStructuredText file.
    -f [FORMAT], --format [FORMAT]
                          Format of files, either 'lisp' or 'config'.

It can also be imported and used as a library.

####
Fork
####

The repository can be found here_.

.. _here: https://sourceforge.net/p/weaklisp/code


