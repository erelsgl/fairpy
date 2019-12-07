"""
Implementation of the classic cut-and-choose protocol
for fair cake-cutting among two agents.

References:

    Abram, Genesis 13:8-9.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""

from agents import *
from allocations import *
from typing import *

import logging
logger = logging.getLogger(__name__)


def cut_and_choose(agents: List[Agent])->Allocation:
    """
    :param agents: a list that must contain exactly 2 Agent objects.
    :return: a list that contains 2 pieces, where each piece is a list of intervals.

    >>> Alice = PiecewiseConstantAgent([33,33], "Alice")
    >>> George = PiecewiseConstantAgent([11,55], "George")
    >>> cut_and_choose([Alice, George])
    > Alice gets [(0, 1.0)] with value 33.00
    > George gets [(1.0, 2)] with value 55.00
    <BLANKLINE>
    >>> cut_and_choose([George, Alice])
    > George gets [(1.4, 2)] with value 33.00
    > Alice gets [(0, 1.4)] with value 46.20
    <BLANKLINE>

    >>> Alice = PiecewiseConstantAgent([33,33,33], "Alice")
    >>> cut_and_choose([Alice, George])
    > Alice gets [(1.5, 3)] with value 49.50
    > George gets [(0, 1.5)] with value 38.50
    <BLANKLINE>
    >>> cut_and_choose([George, Alice])
    > George gets [(0, 1.4)] with value 33.00
    > Alice gets [(1.4, 3)] with value 52.80
    <BLANKLINE>
    """

    num_of_agents = len(agents)
    if num_of_agents!=2:
        raise ValueError("Cut and choose works only for two agents")

    allocation = Allocation(agents)

    (cutter,chooser) = agents
    cut = cutter.mark(0, cutter.cake_value() / 2)
    logger.info("The cutter (%s) cuts at %.2f.", cutter.name(), cut)

    if chooser.eval(0,cut) > chooser.cake_value()/2:
        logger.info("The chooser (%s) chooses the leftmost piece.", chooser.name())
        allocation.set_piece(1, [(0,cut)])
        allocation.set_piece(0, [(cut, cutter.cake_length())])
    else:
        logger.info("The chooser (%s) chooses the rightmost piece.", chooser.name())
        allocation.set_piece(1, [(cut, chooser.cake_length())])
        allocation.set_piece(0, [(0,cut)])

    return allocation


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
