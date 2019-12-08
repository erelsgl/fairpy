"""
Defines agents with various kinds of valuation functions.

Programmer: Erel Segal-Halevi
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

        >>> a = PiecewiseConstantAgent([1,2,3,4])
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

    >>> a = PiecewiseConstantAgent([11,22,33,44]) # Four desired intervals: the leftmost has value 11, the second one 22, etc.
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


    >>> Alice = PiecewiseConstantAgent([11,22,33,44], "Alice")
    >>> Alice.name()
    'Alice'
    """

    def __init__(self, values:list, name:str=None):
        super().__init__(name)
        self.values = np.array(values)
        self.length = len(values)
        self.total_value_cache = sum(values)

    def __repr__(self):
        return "{} is a piecewise-constant agent with values {} and total value={}".format(self.my_name, self.values, self.total_value_cache)

    def cake_value(self):
        return self.total_value_cache

    def cake_length(self):
        return self.length

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

        val = 0.0
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



class PiecewiseUniformAgent(Agent):
    """
    A PiecewiseUniformAgent is an Agent with a finite number of desired intervals, all of which have the same value-density (1).

    >>> a = PiecewiseUniformAgent([(0,1),(2,4),(6,9)])   # Three desired intervals: (0..1) and (2..4) and (6..9).
    >>> a.cake_value()
    6
    >>> a.cake_length()
    9
    >>> a.eval(0,1.5)
    1.0
    >>> a.mark(0, 2)
    3
    >>> a.name()
    'Anonymous'


    >>> George = PiecewiseUniformAgent([(0,1),(2,4),(6,9)], "George")
    >>> George.name()
    'George'
    """

    def __init__(self, desired_regions:List[tuple], name:str=None):
        super().__init__(name)
        self.desired_regions = desired_regions
        self.desired_regions.sort(key=lambda region:region[0]) # sort desired regions from left to right
        self.length = max([region[1] for region in desired_regions])
        self.total_value_cache = sum([region[1]-region[0] for region in desired_regions])

    def __repr__(self):
        return "{} is a piecewise-uniform agent with desired regions {} and total value={}".format(self.my_name, self.desired_regions, self.total_value_cache)

    def cake_value(self):
        return self.total_value_cache

    def cake_length(self):
        return self.length

    def eval(self, start:float, end:float):
        """
        Answer an Eval query: return the value of the interval [start,end].

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]

        >>> a = PiecewiseUniformAgent([(0,1),(2,4),(6,9)])
        >>> a.eval(0,1)
        1.0
        >>> a.eval(-1, 1.5)
        1.0
        >>> a.eval(0.5, 1.5)
        0.5
        >>> a.eval(0.5, 2.5)
        1.0
        >>> a.eval(0.5, 4.5)
        2.5
        >>> a.eval(1.5, 11)
        5.0
        >>> a.eval(3, 11)
        4.0
        >>> a.eval(3, 1)
        0.0
        """
        if end <= start:
            return 0.0  # special case not covered by loop below

        val = 0.0
        for (region_start, region_end) in self.desired_regions:
            if region_end < start:
                continue  # the entire region is to the left of the eval start point - ignore region.
            if end < region_start:
                continue  # the entire region is to the right of the eval start point - ignore region.

            # Here, start <= region_end and region_start <= end.
            # So,   start <= min(end,region_end) and region_start <= min(end,region_end).
            # So,   max(start,region_start) <= min(end,region_end).
            value_from_region = min(end, region_end) - max(start, region_start)
            val += value_from_region

        return val

    def mark(self, start:float, target_value:float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is target_value.

        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of target_value.
        If the value is too high - returns None.

        >>> a = PiecewiseUniformAgent([(0,1),(2,4),(6,9)])
        >>> a.mark(0, 1)
        1
        >>> a.mark(0, 1.5)
        2.5
        >>> a.mark(0.5, 1.5)
        3.0
        >>> a.mark(1.5, 0.01)
        2.01
        >>> a.mark(1.5, 2)
        4
        >>> a.mark(1, 100)
        >>> a.mark(1, 0)
        1
        """
        # the cake to the left of 0 and to the right of length is considered worthless.
        if target_value < 0:
            raise ValueError("sum out of range (should be positive): {}".format(sum))

        for (region_start, region_end) in self.desired_regions:
            if region_end < start:
                continue    # the entire region is to the left of the mark start point - ignore region.

            effective_start = max(start, region_start)
            region_value = region_end - effective_start

            if region_value < target_value:  # the entire region is to the left of the mark start point - ignore region.
                target_value -= region_value
                continue

            # Here, start <= region_end and region_value >= target_value.
            return effective_start + target_value

        # Value is too high: return None
        return None



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
