#!python3

"""
Article name : Optimal Envy-Free Cake Cutting
Authors : Yuga J. Cohler, John K. Lai, David C. Parkes and Ariel D. Procaccia
Algorithm #1 : opt_piecewise_constant
Algorithm #2 : opt_piecewise_linear
Programmer: Tom Goldenberg
Since: 2020-05
"""

from agents import *
from allocations import *

import logging

logger = logging.getLogger(__name__)


def opt_piecewise_constant(agents: List[Agent], values: List[List]) -> Allocation:
    """
    algorithm for finding an optimal EF allocation when agents have piecewise constant valuations.
    :param agents: a list of agents
    :param values: a list of lists holding the values for each interval
    :return: an optimal envy-free allocation

    >>> ALICE = PiecewiseUniformAgent([(0, 0.5), (0.7, 0.9)], "ALICE")
    >>> BOB = PiecewiseUniformAgent([(0.1, 0.8)], "BOB")
    >>> _values = [[0.5, 0.5], [1]]
    >>> print(str(opt_piecewise_constant([ALICE,BOB], _values)))
    > ALICE gets [(0, 0.1), (0.7, 0.9)] with value 0.6
    > BOB gets [(0.1, 0.7)] with value 0.9
    """
    pass


def opt_piecewise_linear(agents: List[Agent], values: List[List], slopes: List[List]) -> Allocation:
    """
     algorithm for finding an optimal EF allocation when agents have piecewise linear valuations.
    :param agents: a list of agents
    :param values: a list of lists holding the values for each interval (start of the interval)
    :param slopes: a list of lists holding the slope for each interval
    :return: an optimal envy-free allocation
    >>> ALICE = PiecewiseUniformAgent([(0, 0.5), (0.7, 0.9)], "ALICE")
    >>> BOB = PiecewiseUniformAgent([(0.1, 0.8)], "BOB")
    >>> values = [[1, 2], [1]]
    >>> _slopes = [[1, -2], [2]]
    >>> print(str(opt_piecewise_constant([ALICE,BOB], values)))
    > ALICE gets [(0, 0.1), (0.7, 0.9)] with value 0.6
    > BOB gets [(0.1, 0.7)] with value 0.9
    """
    pass


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures,tests))
