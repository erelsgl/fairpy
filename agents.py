"""
Defines agents with various kinds of valuation functions.

Author: Erel Segal-Halevi
Since: 2019-11
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import *


class Agent(ABC):
    """
    An abstract class that describes a participant in a cake-cutting algorithm.
    It can answer the standard "mark" and "eval" queries.

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
    def cake_value(self):
        """
        :return: the value of the entire cake for the agent.
        """
        pass


    @abstractmethod
    def cake_length(self):
        """
        :return: the total length of the cake that the agent cares about.
        """
        pass


    @abstractmethod
    def eval(self, start:float, end:float):
        """
        Answer an Eval query: return the value of the interval [start,end].

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]
        """
        pass

    @abstractmethod
    def mark(self, start:float, targetValue:float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is targetValue.

        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of targetValue.
        """
        pass

    def piece_value(self, piece:List[tuple]):
        """
        Evaluate a piece made of several intervals.
        :param piece: a list of tuples [(start1,end1), (start2,end2),...]
        :return:
        """
        return sum([self.eval(*interval) for interval in piece])

    def partition_values(self, partition:List[float]):
        """
        Evaluate all the pieces in the given partition.
        :param partition: a list of k cut-points [cut1,cut2,...]
        :return: a list of k+1 values: eval(0,cut1), eval(cut1,cut2), ...

        >>> a = Agent([1,2,3,4])
        >>> a.partition_values([1,2])
        [1.0, 2.0, 7.0]
        >>> a.partition_values([3,3])
        [6.0, 0.0, 4.0]
        """

        values = []
        values.append(self.eval(0, partition[0]))
        for i in range(len(partition) - 1):
            values.append(self.eval(partition[i], partition[i + 1]))
        values.append(self.eval(partition[-1], self.cake_length()))
        return values


class PiecewiseConstantAgent(Agent):
    """
    A PiecewiseConstantAgent is an Agent whose value function has a constant density on a finite number of intervals.

    >>> a = PiecewiseConstantAgent([11,22,33,44])
    >>> a.cake_value()
    110
    >>> a.cake_length()
    4
    >>> a.eval(1,3)
    55.0
    >>> a.mark(1, 77)
    3.5
    >>> a.name()
    'Anonymous'
    >>> a.piece_value([(0,1),(2,3)])
    44.0


    >>> b = PiecewiseConstantAgent([11,22,33,44], "Bob")
    >>> b.name()
    'Bob'
    """

    def __init__(self, values:list, name:str=None):
        super().__init__(name)
        self.values = np.array(values)
        self.length = len(values)
        self.total_length_cache = len(values)
        self.total_value_cache = sum(values)

    def __repr__(self):
        return "{}:PiecewiseConstantAgent{}".format(self.my_name, self.values)

    def cake_value(self):
        return self.total_value_cache

    def cake_length(self):
        return self.total_length_cache

    def eval(self, start:float, end:float):
        """
        Answer an Eval query: return the value of the interval [start,end].

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]

        >>> a = PiecewiseConstantAgent([11,22,33,44])
        >>> a.eval(1,3)
        55.0
        >>> a.eval(1.5,3)
        44.0
        >>> a.eval(1,3.25)
        66.0
        >>> a.eval(1.5,3.25)
        55.0
        >>> a.eval(3,3)
        0.0
        >>> a.eval(3,7)
        44.0
        >>> a.eval(-1,7)
        110.0
        """
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, min(start, self.length))
        end   = max(0, min(end,   self.length))
        if end <= start:
            return 0.0  # special case not covered by loop below

        fromFloor = int(np.floor(start))
        fromFraction = (fromFloor + 1 - start)
        toCeiling = int(np.ceil(end))
        toCeilingRemovedFraction = (toCeiling - end)

        val = 0.0;
        val += (self.values[fromFloor] * fromFraction)
        val += self.values[fromFloor + 1:toCeiling].sum()
        val -= (self.values[toCeiling - 1] * toCeilingRemovedFraction)

        return val

    def mark(self, start:float, target_value:float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is target_value.

        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of target_value.
        If the value is too high - returns None.

        >>> a = PiecewiseConstantAgent([11,22,33,44])
        >>> a.mark(1, 55)
        3.0
        >>> a.mark(1.5, 44)
        3.0
        >>> a.mark(1, 66)
        3.25
        >>> a.mark(1.5, 55)
        3.25
        >>> a.mark(1, 99)
        4.0
        >>> a.mark(1, 100)
        >>> a.mark(1, 0)
        1.0
        """
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, min(start, self.length))
        if target_value < 0:
            raise ValueError("sum out of range (should be positive): {}".format(sum))

        start_floor = int(np.floor(start))
        start_fraction = (start_floor + 1 - start)

        value = self.values[start_floor]
        if value * start_fraction >= target_value:
            return start + (target_value / value)
        target_value -= (value * start_fraction)
        for i in range(start_floor + 1, self.length):
            value = self.values[i]
            if target_value <= value:
                return i + (target_value / value)
            target_value -= value

        # Value is too high: return None
        return None


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
