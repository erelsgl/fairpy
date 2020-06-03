from agents import *
from allocations import *
import operator
import logging
# from queue import PriorityQueue
import cvxpy
import numpy as np
import math
import scipy.integrate as integrate

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class PiecewiseLinearAgent(Agent):
    """
    A PiecewiseLinearAgent is an Agent whose value function has a piecewise linear density.

    >>> a = PiecewiseLinearAgent([11,22,33,44],[1,2,3,-2],name="alice") # Four desired intervals: the leftmost has value 11, the second one 22, etc.
    >>> a.cake_value()
    110
    >>> a.cake_length()
    4
    >>> a.eval(1,3)
    55.0
    >>> a.mark(1, 77)
    3.5
    >>> a.piece_value([(0,1),(2,3)])
    44.0
    """

    def __init__(self, values: list, slopes: list, name: str = None):
        if len(values) != len(slopes):
            raise ValueError(f'Values amount: {len(values)} not equal to slopes: {len(slopes)} ')
        super().__init__(name)
        self.piece_poly = [set_poly_func(values[i], slopes[i], i, i + 1) for i in range(len(values))]
        self.values_integral = [set_integral_func(self.piece_poly[i], i, i + 1) for i in range(len(values))]
        #         self.values_integral = [set_integral_func(values[i], slopes[i], i, i+1) for i in range(len(values))]
        self.values = np.array(values)
        self.length = len(values)
        self.total_value_cache = sum(values)

    def __repr__(self):
        return "{} is a piecewise-linear agent with values {} and total value={}".format(self.my_name, self.values,
                                                                                         self.total_value_cache)

    def cake_value(self):
        return self.total_value_cache

    def cake_length(self):
        return self.length

    def eval(self, start: float, end: float):
        """
        Answer an Eval query: return the value of the interval [start,end].

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]

        >>> a = PiecewiseLinearAgent([11,22,33,44],[1,2,3,-2],name="alice")
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
        if start < 0 or end > self.length:
            raise ValueError(f'Interval range are invalid')

        #         start_frac = start % 1
        #         end_frac = end % 1
        # #         end_frac += 0.0 if end_frac > 0.0 else 1
        # #         start //= 1
        #         start = int(start)
        #         end = int(end)
        #         end += 1
        if end <= start:
            return 0.0  # special case not covered by loop below

        fromFloor = int(np.floor(start))
        fromFraction = (fromFloor + 1 - start) if start > fromFloor else 0.0
        toCeiling = int(np.ceil(end))
        toCeilingRemovedFraction = (toCeiling - end)

        val = 0.0
        for func_i in range(fromFloor, toCeiling):
            interval_start = func_i + fromFraction  # if func_i != start else func_i + start_frac
            interval_end = func_i + 1 if (func_i + 1) != toCeiling else func_i + 1 - toCeilingRemovedFraction
            #             interval_start = func_i if func_i != start else func_i + start_frac
            #             interval_end = func_i + 1 if (func_i + 1) != end else func_i + end_frac
            #             v = self.values_integral[func_i](interval_start, interval_end)
            #             val += v
            val += self.values_integral[func_i](interval_start, interval_end)
            fromFraction = 0

        #         for func_i in range(start,end):
        #             interval_start = func_i if func_i != start else func_i + start_frac
        #             interval_end = func_i + 1 if (func_i + 1) != end else func_i + end_frac
        #             v = self.values_integral[func_i](interval_start, interval_end)
        #             val += v
        #             start_frac = 0
        return val

    def mark(self, start: float, target_value: float):
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
        logger.info(f'mark({start},{target_value})')
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, start)
        if start >= self.length:
            return None  # value is too high

        if target_value < 0:
            raise ValueError("sum out of range (should be positive): {}".format(sum))

        start_floor = int(np.floor(start))
        if start_floor >= len(self.values):
            raise ValueError(
                "mark({},{}): start_floor ({}) is >= length of values ({})".format(start, target_value, start_floor,
                                                                                   self.values))

        start_fraction = (start_floor + 1 - start) if start > start_floor else 0.0
        end = math.ceil(start) if start != start_floor else start + 1
        current_value = self.values_integral[start_floor](start + start_fraction, end)
        logger.info(f'start {start}, end {end}, start_floor {start_floor}, curr_val {current_value}')
        if current_value == target_value:
            return end
        elif current_value < target_value:
            return self.mark(end, target_value - current_value)
        else:
            inte_poly = np.polyint(self.piece_poly[start_floor])
            if inte_poly.order > 1:
                temp_poly = np.poly1d([target_value])
                target_poly = inte_poly - temp_poly
                logger.info(f'inte_poly {inte_poly}, temp_poly {temp_poly}, target_poly {target_poly}')
                for root in target_poly.r:
                    logger.info(f'root')
                    if root >= start and root <= end:
                        return start + root
            else:
                return (target_value / current_value) + start
        # Value is too high: return None
        return None


def set_poly_func(value, slope, x_0, x_1):
    value_0, _ = integrate.quad(func_x(slope), x_0, x_1)
    const = (value - value_0)/(x_1 - x_0)
    logger.info(f'set_poly_func: Creating poly1d with [{slope},{const}]')
    return np.poly1d([slope, const])

def set_integral_func(poly, x_0, x_1):
    integ = poly.integ()
    logger.info(f'set_integral_func: creating {poly} integral for range [{x_0},{x_1}] ')
    return lambda start, end: ((integ(end) - integ(start)) if x_0 <= start and end <= x_1 else 0)


def func_x(m, c=0):
    return lambda x: m * x + c
