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


def asymmetric_protocol(agents: List[Agent])->Allocation:
    """
    Asymmetric cut-and-choose protocol: one cuts and the other chooses.

    :param agents: a list that must contain exactly 2 Agent objects.
    :return: a proportional and envy-free allocation.

    >>> Alice = PiecewiseConstantAgent([33,33], "Alice")
    >>> George = PiecewiseConstantAgent([11,55], "George")
    >>> asymmetric_protocol([Alice, George])
    > Alice gets [(0, 1.0)] with value 33.00
    > George gets [(1.0, 2)] with value 55.00
    <BLANKLINE>
    >>> asymmetric_protocol([George, Alice])
    > George gets [(1.4, 2)] with value 33.00
    > Alice gets [(0, 1.4)] with value 46.20
    <BLANKLINE>

    >>> Alice = PiecewiseConstantAgent([33,33,33], "Alice")
    >>> asymmetric_protocol([Alice, George])
    > Alice gets [(1.5, 3)] with value 49.50
    > George gets [(0, 1.5)] with value 38.50
    <BLANKLINE>
    >>> asymmetric_protocol([George, Alice])
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


def symmetric_protocol(agents: List[Agent])->Allocation:
    """
    Symmetric cut-and-choose protocol: both agents cut, the manager chooses who gets what.

    :param agents: a list that must contain exactly 2 Agent objects.
    :return: a proportional and envy-free allocation.

    >>> Alice = PiecewiseConstantAgent([33,33], "Alice")
    >>> George = PiecewiseConstantAgent([11,55], "George")
    >>> symmetric_protocol([Alice, George])
    > Alice gets [(0, 1.2)] with value 39.60
    > George gets [(1.2, 2)] with value 44.00
    <BLANKLINE>
    >>> symmetric_protocol([George, Alice])
    > George gets [(1.2, 2)] with value 44.00
    > Alice gets [(0, 1.2)] with value 39.60
    <BLANKLINE>

    >>> Alice = PiecewiseConstantAgent([33,33,33], "Alice")
    >>> symmetric_protocol([Alice, George])
    > Alice gets [(1.45, 3)] with value 51.15
    > George gets [(0, 1.45)] with value 35.75
    <BLANKLINE>
    >>> symmetric_protocol([George, Alice])
    > George gets [(0, 1.45)] with value 35.75
    > Alice gets [(1.45, 3)] with value 51.15
    <BLANKLINE>
    """

    num_of_agents = len(agents)
    if num_of_agents!=2:
        raise ValueError("Cut and choose works only for two agents")

    allocation = Allocation(agents)

    marks = [agent.mark(0, agent.cake_value() / 2) for agent in agents]
    logger.info("The agents mark at %f, %f", marks[0], marks[1])
    cut = sum(marks)/2
    logger.info("The cake is cut at %f.", cut)

    if marks[0] < marks[1]:
        logger.info("%s's mark is to the left of %s's mark.", agents[0].name(),  agents[1].name())
        allocation.set_piece(0, [(0,cut)])
        allocation.set_piece(1, [(cut, agents[1].cake_length())])
    else:
        logger.info("%s's mark is to the left of %s's mark.", agents[1].name(),  agents[0].name())
        allocation.set_piece(1, [(0,cut)])
        allocation.set_piece(0, [(cut, agents[0].cake_length())])

    return allocation


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
