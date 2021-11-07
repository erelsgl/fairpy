# fairpy

![Tox result](https://github.com/erelsgl/fairpy/workflows/tox/badge.svg)

An open-source library of [fair division algorithms](https://en.wikipedia.org/wiki/Fair_division) in Python.

## Installation

    clone https://github.com/erelsgl/fairpy.git
    cd fairpy
    pip install -r requirements.txt
    pip install -e .

To test the installation, run one of the [example programs](example/):

    python3 examples/items.py
    python3 examples/cake.py

## Features

1. [Various input formats](examples/input_formats.md), making it easy to use for both researchers and end-users.

2. [Various output formats](examples/output_formats.md).

3. [Optional logging](examples/loggers.md), making it easy to learn and understand how the algorithms work.



## Implemented algorithms

For a partial list of algorithms and their implementation status, see the subfolders:

* [Cake-cutting algorithms](fairpy/cake/README.md)  
* [Item allocation algorithms (divisible and indivisible)](fairpy/items/README.md)
