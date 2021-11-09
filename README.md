# fairpy

![Tox result](https://github.com/erelsgl/fairpy/workflows/tox/badge.svg)

An open-source library of [fair division algorithms](https://en.wikipedia.org/wiki/Fair_division) in Python.

## Installation

    clone https://github.com/erelsgl/fairpy.git
    cd fairpy
    pip install -r requirements.txt
    pip install -e .

To verify that everything was installed correctly, run one of the example programs, e.g.

    python examples/items.py
    python examples/cake.py

## Features and Examples

1. [Various input formats](examples/input_formats.md), making it easy to use for both researchers and end-users.

2. [Various output formats](examples/output_formats.md).

3. [Optional logging](examples/loggers.md), making it easy to learn and understand how the algorithms work.

4. [Item allocation algorithms](examples/items.md), for both divisible and indivisible items.

5. [Cake-cutting algorithms](examples/cake.md).

## Implemented algorithms

For a partial list of algorithms and their implementation status, see:

* [Cake-cutting algorithms](fairpy/cake/README.md)  
* [Item allocation algorithms](fairpy/items/README.md)


## Development

Many algorithms can be added to `fairpy`. See:

* [Cake-cutting algorithms for future work](fairpy/cake/README-future.md)  
* [Item allocation algorithms for future work](fairpy/items/README-future.md)

You can run all doctests by either one of these commands:

    pytest --doctest-modules --ignore=examples/_pweave.py
    tox

