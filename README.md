# fairpy

![PyTest result](https://github.com/erelsgl/fairpy/workflows/pytest/badge.svg)

An open-source library of [fair division algorithms](https://en.wikipedia.org/wiki/Fair_division) in Python.
Designed for three target audiences:

* Laypeople, who want to use existing fair division algorithms for real-life problems.
* Researchers, who develop new fair division algorithms and want to quickly implement them and compare to existing algorithms.
* Students, who want to trace the execution of algorithms to understand how they work.

## Installation

    clone https://github.com/erelsgl/fairpy.git
    cd fairpy
    pip install -r requirements.txt
    pip install -e .

To verify that everything was installed correctly, run one of the example programs, e.g.

    python examples/items.py
    python examples/cake.py

## Features and Examples

1. [Various input formats](examples/input_formats.md), to easily use by both researchers and end-users.

1. [Various output formats](examples/output_formats.md).

1. [Optional logging](examples/loggers.md), to learn and understand how the algorithms work.

1. [Decorators](examples/decorators.md), to easily code new algorithms.

1. [Item allocation algorithms](examples/items.md), for both divisible and indivisible items.

1. [Cake-cutting algorithms](examples/cake.md).


## Implemented algorithms

For a partial list of algorithms and their implementation status, see:

* [Cake-cutting algorithms](fairpy/cake/README.md)
* [Item allocation algorithms](fairpy/items/README.md)


## Development

Many algorithms can be added to `fairpy`. See:

* [Cake-cutting algorithms for future work](fairpy/cake/README-future.md)  
* [Item allocation algorithms for future work](fairpy/items/README-future.md)

You can run all doctests by either `pytest` or `tox`.

**See also**: [other open-source projects related to fairness](related.md).
