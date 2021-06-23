#!python3

"""
Classes for representing a Bundle (a set of objects given to an agent).
Used mainly for display purposes.

Programmer: Erel Segal-Halevi
Since: 2021-06
"""

from typing import List, Any, Dict
import numpy as np


DEFAULT_PRECISION = 3     # number of significant digits in printing
DEFAULT_SEPARATOR = ","   # separator between items in printing

from abc import ABC


class Bundle(ABC):
    def __repr__(self):
        separator = DEFAULT_SEPARATOR
        if self.items is None:
            return "None"
        else:
            return "{" + separator.join(map(str,self.items)) + "}"
    def __getitem__(self, index):
        return self.items.__getitem__(index)
    def __iter__(self):
       return self.items.__iter__() 
    def __len__(self):
       return self.items.__len__() 


class ListBundle(Bundle):
    """
    A bundle allocated to a single agent; contains a list of the item indices of names.
    >>> b = ListBundle([3,6])
    >>> b
    {3,6}
    >>> b[0]
    3
    >>> for item in b: print(item)
    3
    6
    >>> ListBundle({"x","z"})
    {x,z}
    """
    def __init__(self, items):
        if items is None:
            items = []
        self.items = sorted(items)


class FractionalBundle(Bundle):
    """
    A bundle allocated to a single agent; contains the fraction of each item given to that agent.
    >>> ### Vector of fractions:
    >>> FractionalBundle(fractions=[0,0,1,0,0.5])
    { 100% of 2, 50.0% of 4}
    >>> FractionalBundle(fractions=np.array([0.25, 1.  ]))
    { 25.0% of 0, 100.0% of 1}
    """
    def __init__(self, fractions):
        precision = DEFAULT_PRECISION
        self.fractions = fractions
        self.items = [
            f" {np.round(fraction*100, precision)}% of {item}"
            for item,fraction in enumerate(fractions)
            if fraction > 0
        ]


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
