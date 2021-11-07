#!python3
"""
Defines various kinds of valuation functions on a cake.

Programmer: Erel Segal-Halevi
and         Shalev Goldshtein for PiecewiseConstantValuationNormalized
Since: 2019-11
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import *

from scipy import integrate


class Valuation(ABC):
    """
    An abstract class that describes a valuation of a cake.
    It can answer the standard "mark" and "eval" queries.
    """

    @abstractmethod
    def eval(self, start:float, end:float)->float:
        """
        Answer an Eval query: return the value of the interval [start,end].

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]
        """
        pass

    @abstractmethod
    def mark(self, start:float, targetValue:float)->float:
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is targetValue.

        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of targetValue.
        """
        pass

    @abstractmethod
    def total_value(self):
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

    def value(self, piece:List[tuple]):
        """
        Evaluate a piece made of several intervals.
        :param piece: a list of tuples [(start1,end1), (start2,end2),...]
        :return:
        """
        if(piece==None):
            return 0
        return sum([self.eval(*interval) for interval in piece])

    def partition_values(self, partition:List[float]):
        """
        Evaluate all the pieces in the given partition.
        :param partition: a list of k cut-points [cut1,cut2,...]
        :return: a list of k+1 values: eval(0,cut1), eval(cut1,cut2), ...

        >>> a = PiecewiseConstantValuation([1,2,3,4])
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


class PiecewiseConstantValuation(Valuation):
    """
    A PiecewiseConstantValuation is a valuation with a constant density on a finite number of intervals.

    >>> a = PiecewiseConstantValuation([11,22,33,44]) # Four desired intervals: the leftmost has value 11, the second one 22, etc.
    >>> a.total_value()
    110
    >>> a.cake_length()
    4
    >>> a.eval(1,3)
    55.0
    >>> a.mark(1, 77)
    3.5
    >>> a.value([(0,1),(2,3)])
    44.0
    """

    def __init__(self, values:list):
        self.values = np.array(values)
        self.length = len(values)
        self.total_value_cache = sum(values)

    def __repr__(self):
        return f"Piecewise-constant valuation with values {self.values} and total value={self.total_value_cache}"

    def total_value(self):
        return self.total_value_cache

    def cake_length(self):
        return self.length

    def eval(self, start:float, end:float):
        """
        Answer an Eval query: return the value of the interval [start,end].

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]

        >>> a = PiecewiseConstantValuation([11,22,33,44])
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

        >>> a = PiecewiseConstantValuation([11,22,33,44])
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
        start = max(0, start)
        if start >= self.length:
            return None  # value is too high

        if target_value < 0:
            raise ValueError("sum out of range (should be positive): {}".format(sum))

        start_floor = int(np.floor(start))
        if start_floor >= len(self.values):
            raise ValueError("mark({},{}): start_floor ({}) is >= length of values ({})".format(start, target_value, start_floor, self.values))

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





class PiecewiseConstantValuation1Segment(Valuation):

    def __init__(self, values:list):
        super().__init__()
        self.values = np.array(values)
        self.length = len(values)
        self.total_value_cache = sum(values)

    def total_value(self):
        return self.total_value_cache

    def __repr__(self):
        return f"Piecewise-constant valuation with values {self.values} and total value={self.total_value_cache}"

    def cake_length(self):
        return self.length

    def eval(self, start: float, end: float):
        """
        Answer an Eval query: return the value of the interval [start,end].

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]
        """
        start = start*self.cake_length()
        end = end*self.cake_length()
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, min(start, self.length))
        end = max(0, min(end, self.length))
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

        return val/self.total_value()

    def mark(self, start: float, target_value: float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is target_value.

        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of target_value.
        If the value is too high - returns None.
        """
        start = start*self.cake_length()
        target_value = target_value*self.total_value()
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, min(start, self.length))
        if target_value < 0:
            raise ValueError("sum out of range (should be positive): {}".format(sum))

        start_floor = int(np.floor(start))
        start_fraction = (start_floor + 1 - start)

        value = self.values[start_floor]
        if value * start_fraction >= target_value:
            return (start + (target_value / value))/self.cake_length()
        target_value -= (value * start_fraction)
        for i in range(start_floor + 1, self.length):
            value = self.values[i]
            if target_value <= value:
                return (i + (target_value / value))/self.cake_length()
            target_value -= value

        # Value is too high: return None
        return None



class PiecewiseUniformValuation(Valuation):
    """
    A PiecewiseUniformValuation has a finite number of desired intervals, all of which have the same value-density (1).

    >>> a = PiecewiseUniformValuation([(0,1),(2,4),(6,9)])   # Three desired intervals: (0..1) and (2..4) and (6..9).
    >>> a.total_value()
    6
    >>> a.cake_length()
    9
    >>> a.eval(0,1.5)
    1.0
    >>> a.mark(0, 2)
    3
    """

    def __init__(self, desired_regions:List[tuple]):
        self.desired_regions = desired_regions
        self.desired_regions.sort(key=lambda region:region[0]) # sort desired regions from left to right
        self.length = max([region[1] for region in desired_regions])
        self.total_value_cache = sum([region[1]-region[0] for region in desired_regions])

    def __repr__(self):
        return f"Piecewise-uniform agent with desired regions {self.desired_regions} and total value={self.total_value_cache}"

    def total_value(self):
        return self.total_value_cache

    def cake_length(self):
        return self.length

    def eval(self, start:float, end:float):
        """
        Answer an Eval query: return the value of the interval [start,end].

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]

        >>> a = PiecewiseUniformValuation([(0,1),(2,4),(6,9)])
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

        >>> a = PiecewiseUniformValuation([(0,1),(2,4),(6,9)])
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


class PiecewiseConstantValuationNormalized(Valuation):

    # the init of the agent
    def __init__(self, values: list):
        super().__init__()

        # the len of the values list
        self.length = len(values)
        self.total_value_cache = sum(values)
        # self.values = np.array(values)
        ls = [None] * len(values)
        # normalize the cake to values between 0.0 and 1.0
        # by dividing the values by there sum
        for i in range(len(values)):
            ls[i] = values[i] / self.total_value_cache

        # the list of the values
        self.values = np.array(ls)

        self.normal = 1 / self.total_value_cache

    def __repr__(self):
        return f"Normalized piecewise-constant valuation with values {self.values}"

    def total_value(self):
        return self.total_value_cache

    def cake_length(self):
        return self.length

    # the evaluation of the agents
    def eval(self, start: float, end: float):
        """
        Answer an Eval query: return the value of the interval [start,end] {{{[(NORMALIZED)]}}}.

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]

        >>> a = PiecewiseConstantValuationNormalized([11,22,33,44])
        >>> a.eval(0.5,1)
        0.7
        >>> a.eval(0.25,1)
        0.9
        >>> a.eval(0,0.25)
        0.1
        >>> a.eval(0,0.375)
        0.2

        """
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, min(start * self.length, self.length))
        end = max(0, min(end * self.length, self.length))
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

    # the mark is for finding the point where it's equals to  the target value
    def mark(self, start: float, target_value: float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is target_value  {[(NORMALIZED)]}.

        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of target_value.
        If the value is too high - returns None.

        >>> a = PiecewiseConstantValuationNormalized([11,22,33,44])
        >>> a.mark(0.5, 0.7)
        1.0
        >>> a.mark(0.375, 0.1)
        0.5
        >>> a.mark(0, 0.2)
        0.375
        >>> a.mark(0.25, 0.2)
        0.5
        >>> a.mark(0, 0.9)
        0.9375

        """
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, start * self.length)
        if start >= self.length:
            return None  # value is too high

        if target_value < 0:
            raise ValueError("sum out of range (should be positive): {}".format(sum))

        start_floor = int(np.floor(start))
        if start_floor >= len(self.values):
            raise ValueError(
                f"mark({start},{target_value}): start_floor ({start_floor}) is >= length of values ({self.values})")

        start_fraction = (start_floor + 1 - start)

        value = self.values[start_floor]
        if value * start_fraction >= target_value:
            # i added the division by self.length for normalzing
            return ((start + (target_value / value)) / self.length)
        target_value -= (value * start_fraction)
        for i in range(start_floor + 1, self.length):
            value = self.values[i]
            if target_value <= value:
                # i added the division by self.length for normalzing
                return ((i + (target_value / value)) / self.length)
            target_value -= value

        # Value is too high: return None
        return None


class PiecewiseConstantValuationNormalized(Valuation):

    # the init of the agent
    def __init__(self, values: list):
        super().__init__()

        # the len of the values list
        self.length = len(values)
        self.total_value_cache = sum(values)
        # self.values = np.array(values)
        ls = [None] * len(values)
        # normalize the cake to values between 0.0 and 1.0
        # by dividing the values by there sum
        for i in range(len(values)):
            ls[i] = values[i] / self.total_value_cache

        # the list of the values
        self.values = np.array(ls)

        self.normal = 1 / self.total_value_cache

    def __repr__(self):
        return f"Piecewise-constant agent with values {self.values} (((NORMALIZED)))"

    def total_value(self):
        return self.total_value_cache

    def cake_length(self):
        return self.length

    # the evaluation of the agents
    def eval(self, start: float, end: float):
        """
        Answer an Eval query: return the value of the interval [start,end] {{{[(NORMALIZED)]}}}.

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]

        >>> a = PiecewiseConstantValuationNormalized([11,22,33,44])
        >>> a.eval(0.5,1)
        0.7
        >>> np.round(a.eval(0.25,1), decimals=1)
        0.9
        >>> a.eval(0,0.25)
        0.1
        >>> np.round(a.eval(0,0.375), decimals=1)
        0.2

        """
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, min(start * self.length, self.length))
        end = max(0, min(end * self.length, self.length))
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

    # the mark is for finding the point where it's equals to  the target value
    def mark(self, start: float, target_value: float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is target_value  {[(NORMALIZED)]}.

        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of target_value.
        If the value is too high - returns None.

        >>> a = PiecewiseConstantValuationNormalized([11,22,33,44])
        >>> a.mark(0.5, 0.7)
        1.0
        >>> a.mark(0.375, 0.1)
        0.5
        >>> a.mark(0, 0.2)
        0.375
        >>> a.mark(0.25, 0.2)
        0.5
        >>> a.mark(0, 0.9)
        0.9375

        """
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, start * self.length)
        if start >= self.length:
            return None  # value is too high

        if target_value < 0:
            raise ValueError("sum out of range (should be positive): {}".format(sum))

        start_floor = int(np.floor(start))
        if start_floor >= len(self.values):
            raise ValueError(
                "mark({},{}): start_floor ({}) is >= length of values ({})".format(start, target_value, start_floor,
                                                                                   self.values))

        start_fraction = (start_floor + 1 - start)

        value = self.values[start_floor]
        if value * start_fraction >= target_value:
            # i added the division by self.length for normalzing
            return ((start + (target_value / value)) / self.length)
        target_value -= (value * start_fraction)
        for i in range(start_floor + 1, self.length):
            value = self.values[i]
            if target_value <= value:
                # i added the division by self.length for normalzing
                return ((i + (target_value / value)) / self.length)
            target_value -= value

        # Value is too high: return None
        return None


class PiecewiseLinearValuation(Valuation):
    """
    Author: Tom Goldenberg
    Since:  2020-06

    A PiecewiseLinearValuation is an Valuation whose value function has a piecewise linear density.
    PiecewiseLinearValuation([11,22],[1,0])
    the first list ([11,22]) is the value of pieces e.g. 1st piece has a value of 11 and the second has a value of 22
    the second list ([1,0]) are the slopes of the piece value, meaning: for each piece the corresponding lists will be used
     to build the equation y = mx + c => (y = 1*x + c, y = 0*x + c) and the 11 and 22 are the integral value of the equation
     from x_0 = 0 -> x_1 = 1
    >>> a = PiecewiseLinearValuation([11,22,33,44],[1,2,3,-2]) # Four desired intervals: the leftmost has value 11, the second one 22,  etc.
    >>> a.total_value()
    110
    >>> a.cake_length()
    4
    >>> a.eval(1,3)
    55.0
    >>> a.value([(0,1),(2,3)])
    44.0
    >>> a = PiecewiseLinearValuation([2],[1])
    >>> a.length
    1
    >>> a.values
    array([2])
    >>> a.total_value()
    2
    >>> a.value([(0,1)])
    2.0
    >>> a.eval(0,1)
    2.0
    >>> a = PiecewiseLinearValuation([2,2],[1,0])
    >>> a.total_value()
    4
    >>> a.value([(0,1)])
    2.0
    >>> a.value([(1,1.5)])
    1.0
    >>> a.value([(1,2)])
    2.0
    >>> a.value([(0.5,2)])
    3.125
    """

    def __init__(self, values: list, slopes: list):
        if len(values) != len(slopes):
            raise ValueError(f'Values amount: {len(values)} not equal to slopes: {len(slopes)} ')
        super().__init__()
        self.piece_poly = [set_poly_func(values[i], slopes[i], 0, 1) for i in range(len(values))]
        self.values_integral = [set_integral_func(self.piece_poly[i], 0, 1) for i in range(len(values))]
        self.values = np.array(values)
        self.length = len(values)
        self.total_value_cache = sum(values)

    def __repr__(self):
        return f"Piecewise-linear valuation with values {self.values} and total value={self.total_value_cache}"

    def total_value(self):
        return self.total_value_cache

    def cake_length(self):
        return self.length

    def eval(self, start: float, end: float):
        """
        Answer an Eval query: return the value of the interval [start,end].

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]

        >>> a = PiecewiseLinearValuation([11,22,33,44],[1,2,3,-2])
        >>> a.eval(1,3)
        55.0
        >>> a.eval(1.5,3)
        44.25
        >>> a.eval(1,3.25)
        66.1875
        >>> a.eval(1.5,3.25)
        55.4375
        >>> a.eval(3,3)
        0.0
        """
        if start < 0 or end > self.length:
            raise ValueError(f'Interval range are invalid start={start}, end={end}, length={self.length}')

        if end <= start:
            return 0.0  # special case not covered by loop below

        fromFloor = int(np.floor(start))
        fromFraction = (fromFloor + 1 - start) if start > fromFloor else 0.0
        toCeiling = int(np.ceil(end))
        toCeilingRemovedFraction = (toCeiling - end)

        val = 0.0
        for func_i in range(fromFloor, toCeiling):
            interval_start = fromFraction
            interval_end = 1 if (func_i + 1) != toCeiling else 1 - toCeilingRemovedFraction
            val += self.values_integral[func_i](interval_start, interval_end)
            fromFraction = 0
        return val

    def mark(self, start: float, target_value: float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is target_value.

        :param start: Location on cake where the calculation starts.
        :param target_value: required value for the piece [start,end]
        :return: the end of an interval with a value of target_value.
        If the value is too high - returns None.

        >>> a = PiecewiseLinearValuation([11,22,33,44],[1,2,0,-4])
        >>> a.mark(1, 55)
        3
        >>> a.mark(1.5, 44)
        2.992
        >>> a.mark(1, 66)
        3.242
        >>> a.mark(1.5, 55)
        3.236
        >>> a.mark(1, 99)
        4
        >>> a.mark(1, 100)
        >>> a.mark(1, 0)
        1.0
        >>> a = PiecewiseLinearValuation([2,2],[1,0])
        >>> a.mark(0,1)
        0.562
        >>> a.mark(1,1)
        1.5
        >>> a.mark(1,2)
        2
        >>> a.mark(0,3)
        1.5
        >>> a.mark(0,6) # returns none since no such value exists
        >>> a.mark(0,0.2)
        0.128
        """
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, start)
        if start >= self.length:
            return None  # value is too high

        if target_value < 0:
            raise ValueError("sum out of range (should be positive): {}".format(sum))

        start_floor = int(np.floor(start))
        if start_floor >= len(self.values):
            raise ValueError(
                f"mark({start},{target_value}): start_floor ({start_floor}) is >= length of values ({self.values})")

        start_fraction = (start_floor + 1 - start) if start > start_floor else 0.0
        current_value = self.values_integral[start_floor](start_fraction, 1)
        if current_value == target_value:
            return start_floor + 1
        elif current_value < target_value:
            return self.mark(start_floor + 1, target_value - current_value)
        else:
            inte_poly = np.polyint(self.piece_poly[start_floor])
            if inte_poly.order > 1:
                temp_poly = np.poly1d([target_value])
                target_poly = inte_poly - temp_poly
                for root in target_poly.r:
                    if 0 <= root <= 1:
                        return round(start_floor + root, 3)
            else:
                return round((target_value / current_value) + start_floor, 3)
        # Value is too high: return None
        return None


def set_poly_func(value, slope, x_0, x_1):
    value_0, _ = integrate.quad(func_x(slope), x_0, x_1)
    const = (value - value_0)/(x_1 - x_0)
    return np.poly1d([slope, const])


def set_integral_func(poly, x_0, x_1):
    integ = poly.integ()
    return lambda start, end: ((integ(end) - integ(start)) if x_0 <= start and end <= x_1 else 0)


def func_x(m, c=0):
    return lambda x: m * x + c


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
