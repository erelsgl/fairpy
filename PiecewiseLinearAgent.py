#!python3

"""
Programmer: Tom Goldenberg
"""
from allocations import *
import logging
import numpy as np
import scipy.integrate as integrate

# logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class PiecewiseLinearAgent(Agent):
    """
    A PiecewiseLinearAgent is an Agent whose value function has a piecewise linear density.
    PiecewiseLinearAgent([11,22],[1,0])
    the first list ([11,22]) is the value of pieces e.g. 1st piece has a value of 11 and the second has a value of 22
    the second list ([1,0]) are the slopes of the piece value, meaning: for each piece the corresponding lists will be used
     to build the equation y = mx + c => (y = 1*x + c, y = 0*x + c) and the 11 and 22 are the integral value of the equation
     from x_0 = 0 -> x_1 = 1
    >>> a = PiecewiseLinearAgent([11,22,33,44],[1,2,3,-2],name="alice") # Four desired intervals: the leftmost has value 11, the second one 22,  etc.
    >>> a.cake_value()
    110
    >>> a.cake_length()
    4
    >>> a.eval(1,3)
    55.0
    >>> a.piece_value([(0,1),(2,3)])
    44.0
    >>> a = PiecewiseLinearAgent([2],[1],name="alice")
    >>> a.length
    1
    >>> a.values
    array([2])
    >>> a.cake_value()
    2
    >>> a.piece_value([(0,1)])
    2.0
    a.eval(0,1)
    2.0
    >>> a = PiecewiseLinearAgent([2,2],[1,0],name="alice")
    >>> a.cake_value()
    4
    >>> a.piece_value([(0,1)])
    2.0
    >>> a.piece_value([(1,1.5)])
    1.0
    >>> a.piece_value([(1,2)])
    2.0
    >>> a.piece_value([(0.5,2)])
    3.125
    """

    def __init__(self, values: list, slopes: list, name: str = None):
        if len(values) != len(slopes):
            raise ValueError(f'Values amount: {len(values)} not equal to slopes: {len(slopes)} ')
        super().__init__(name)
        self.piece_poly = [set_poly_func(values[i], slopes[i], 0, 1) for i in range(len(values))]
        self.values_integral = [set_integral_func(self.piece_poly[i], 0, 1) for i in range(len(values))]
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

        >>> a = PiecewiseLinearAgent([11,22,33,44],[1,2,0,-4])
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
        >>> a = PiecewiseLinearAgent([2,2],[1,0],name="alice")
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
        current_value = self.values_integral[start_floor](start_fraction, 1)
        logger.debug(f'start {start}, start_floor {start_floor}, curr_val {current_value}, target value {target_value}')
        if current_value == target_value:
            return start_floor + 1
        elif current_value < target_value:
            return self.mark(start_floor + 1, target_value - current_value)
        else:
            inte_poly = np.polyint(self.piece_poly[start_floor])
            if inte_poly.order > 1:
                temp_poly = np.poly1d([target_value])
                target_poly = inte_poly - temp_poly
                logger.info(f'mark function polynomials\n{inte_poly}=inte_poly, {temp_poly}=temp_poly,{target_poly}=target_poly')
                for root in target_poly.r:
                    logger.info(f'root')
                    if 0 <= root <= 1:
                        return round(start_floor + root, 3)
            else:
                return round((target_value / current_value) + start_floor, 3)
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


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))