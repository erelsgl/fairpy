# fairpy

![PyTest result](https://github.com/erelsgl/fairpy/workflows/pytest/badge.svg)

## This repository was forked from [here](https://github.com/erelsgl/fairpy).
### We added two files named:
* [two_players_fair_division](https://github.com/ItayHasidi/fairpy/blob/master/fairpy/items/two_players_fair_division.py) - The main algorithms file, for more information visit the [wiki](https://github.com/ItayHasidi/fairpy/wiki/Two-players-fair-division).
* [two_players_fair_division_utils](https://github.com/ItayHasidi/fairpy/blob/master/fairpy/items/two_players_fair_division_utils.py) - Many util helper functions.

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

or run the tests:

    pytest

## Usage

The function `fairpy.divide` can be used to activate all fair division algorithms. For example:

    import fairpy

    valuations = {"Alice": {"w":11,"x":22,"y":44,"z":0}, "George": {"w":22,"x":11,"y":66,"z":33}}

    ### Allocating indivisible items using the Iterated Maximum Matching algorithm:
    fairpy.divide(algorithm=fairpy.items.iterated_maximum_matching, input=valuations)

    ### Allocating divisible goods using the leximin algorithm:
    fairpy.divide(fairpy.items.leximin, valuations)

    ### Dividing a cake using cut-and-choose:
    from fairpy import PiecewiseConstantAgent
    Alice = PiecewiseConstantAgent([33,33], "Alice")
    George = PiecewiseConstantAgent([11,55], "George")
    fairpy.divide(algorithm=fairpy.cake.cut_and_choose.asymmetric_protocol, input=[George, Alice])


## Features and Examples

1. [Item allocation algorithms](examples/items.md), for both divisible and indivisible items;

1. [Cake-cutting algorithms](examples/cake.md);

1. [Various input formats](examples/input_formats.md), to easily use by both researchers and end-users;

1. [Various output formats](examples/output_formats.md);

1. [Optional logging](examples/loggers.md), to learn and understand how the algorithms work.


## Adding new algorithms

To add a new algorithm for item allocation, write a function that accepts one of the following parameters:

* [AgentList](fairpy/agentlist.py) - a list of [Agent](fairpy/agents.py) objects. See e.g. [the implementation of Round Robin](fairpy/items/round_robin.py) for usage example.
* [ValuationMatrix](fairpy/valuations.py) - a matrix v where v[i,j] is the value of agent i to item j. See e.g. [the implementation of Leximin](fairpy/items/leximin.py) for usage example.

Your function may accept any other custom parameters.


## See also

* [other open-source projects related to fairness](related.md).
