#!python3

"""
Classes for representing a Bundle (a set of objects given to an agent).
Used mainly for display purposes.

Programmer: Erel Segal-Halevi
Since: 2021-06
"""

from typing import List, Any, Dict
import numpy as np
from collections.abc import Iterable


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
    >>> FractionalBundle(fractions=[0,0,1,0,0.5], object_names=["a","b","c","d","e"])
    { 100% of c, 50.0% of e}
    >>> bundle = FractionalBundle(fractions=[0.1111,0.4444,0.5555], object_names=["a","b","c"])
    >>> bundle
    { 11.11% of a, 44.44% of b, 55.55% of c}
    >>> bundle.round(2)
    { 11.0% of a, 44.0% of b, 56.0% of c}
    """
    def __init__(self, fractions, object_names=None):
        self.fractions = fractions
        self.object_names = object_names
        self._set_items()

    def _set_items(self):
        precision = DEFAULT_PRECISION
        self.items = [
            f" {np.round(fraction*100, precision)}% of {item}"
            for item,fraction in self.enumerate_fractions()
            if fraction != 0
        ]

    def round(self, num_digits:int):
        for i,fraction in enumerate(self.fractions):
            self.fractions[i] = np.round(fraction, num_digits)
        self._set_items()
        return self

    def enumerate_fractions(self):
        if self.object_names is None: 
            return enumerate(self.fractions)
        else:
            return zip(self.object_names, self.fractions)


def bundle_from(b:Any):
    if isinstance(b,Bundle):
        return b
    elif b is None:
        return ListBundle([])
    elif isinstance(b,Iterable):
        return ListBundle(b)
    else:
        raise TypeError(f"Unsupported bundle type {type(b)}")

if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
