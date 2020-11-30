"""
Defines agents with various kinds of valuation functions over indivisible items.

IN CONSTRUCTION

Programmer: Erel Segal-Halevi
Since: 2020-04
"""

from dicttools import stringify
from abc import ABC, abstractmethod

from typing import *
Item = Any
Bundle = Set[Item]
Alllocation = List[Bundle]




class Agent(ABC):
    """
    An abstract class that describes a participant in an algorithm for indivisible item allocation.
    It can evaluate a set of items.
    It may also have a name, which is used only in demonstrations and for tracing. The name may be left blank (None).
    """

    def __init__(self, name:str=None):
        if name is not None:
            self.my_name = name

    def name(self):
        if hasattr(self, 'my_name') and self.my_name is not None:
            return self.my_name
        else:
            return "Anonymous"

    @abstractmethod
    def value(self, items:Bundle):
        """
        Return the value of the given set of items.
        """
        pass

    @abstractmethod
    def total_value(self):
        """
        :return: the value of the set of all items.
        """
        pass


class AdditiveAgent(Agent):
    """
    An AdditiveAgent is an Agent who has a value for each item.
    Its value for a bundle is the sum of values of items in the bundle.

    >>> Alice = AdditiveAgent({'x':1, 'y':2, 'z':3}, "Alice")
    >>> Alice
    Alice is an additive agent with values {x:1, y:2, z:3} and total value=6
    >>> Alice.value({'x','y'})
    3
    >>> Alice.value({'y'})
    2
    >>> Alice.value({})
    0
    >>> Alice.is_envy_free({'z'},{'x','y'})
    True
    >>> Alice.is_envy_free({'y'},{'x','z'})
    False
    >>> Alice.is_envy_free(3.5,{'x','z'})
    False
    >>> Alice.is_EF1({'y'},{'x','z'})
    True
    >>> Alice.is_EF1({'x'},{'y','z'})
    False
    >>> Alice.is_EF1(2.5,{'y','z'})
    True
    """

    def __init__(self, values:Dict[Item,float], name:str=None):
        super().__init__(name)
        self.values = values
        self.num_of_items = len(values)
        self.total_value_cache = sum(values.values())

    def value(self, items:Bundle)->float:
        """
        Return the value of the given set of items.
        """
        return sum([self.values[item] for item in items])

    def total_value(self)->float:
        return self.total_value_cache

    def __repr__(self):
        return "{} is an additive agent with values {} and total value={}".format(self.name(), stringify(self.values), self.total_value_cache)

    def is_envy_free(self, my_bundle_or_value, other_bundle:Bundle):
        my_value = self.value(my_bundle_or_value) if isinstance(my_bundle_or_value,(list,set,str)) else my_bundle_or_value
        return my_value >= self.value(other_bundle)

    def is_EF1(self, my_bundle_or_value, other_bundle:Bundle):
        if len(other_bundle)==0: return True
        best_item_in_other_bundle = max([self.values[item] for item in other_bundle])
        my_value = self.value(my_bundle_or_value) if isinstance(my_bundle_or_value,(list,set,str)) else my_bundle_or_value
        return my_value >= self.value(other_bundle)-best_item_in_other_bundle

if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
