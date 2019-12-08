"""
Implementation of the Last Diminisher protocol
for fair cake-cutting among n agents.

Reference:

    Hugo Steinhaus (1948):
    ["The problem of fair division"](https://www.jstor.org/stable/1914289).
    Econometrica. 16 (1): 101–104.

Programmer: Erel Segal-Halevi
Since: 2019-12
"""

from agents import *
from allocations import *
from typing import *

import logging
logger = logging.getLogger(__name__)


def last_diminisher(agents: List[Agent])->Allocation:
    """
    :param agents: a list of Agent objects.
    :return: a proportional cake-allocation.

    >>> Alice = PiecewiseConstantAgent([33,33], "Alice")
    >>> last_diminisher([Alice])
    > Alice gets [(0, 2)] with value 66.00
    <BLANKLINE>
    >>> George = PiecewiseConstantAgent([11,55], "George")
    >>> last_diminisher([Alice, George])
    > Alice gets [(0, 1.0)] with value 33.00
    > George gets [(1.0, 2)] with value 55.00
    <BLANKLINE>
    >>> last_diminisher([George, Alice])
    > George gets [(1.0, 2)] with value 55.00
    > Alice gets [(0, 1.0)] with value 33.00
    <BLANKLINE>
    >>> Abraham = PiecewiseConstantAgent([4,1,1], "Abraham")
    >>> last_diminisher([Abraham, George, Alice])
    > Abraham gets [(0, 0.5)] with value 2.00
    > George gets [(1.1666666666666667, 2)] with value 45.83
    > Alice gets [(0.5, 1.1666666666666667)] with value 22.00
    <BLANKLINE>
    """
    num_of_agents = len(agents)
    if num_of_agents==0:
        raise ValueError("There must be at least one agent")
    allocation = Allocation(agents)
    start=0
    active_agents = list(range(num_of_agents))
    last_diminisher_recursive(start, agents, active_agents, allocation)
    return allocation


def last_diminisher_recursive(start:float, agents: List[Agent], active_agents:List[int], allocation:Allocation):
    """
    A recursive subroutine for last-diminisher.
    :param start: the leftmost end of the cake that should be allocated.
    :param agents: the list of all n agents in the original protocol.
    :param active_agents: list of indices of those agents who are still active (not allocated yet).
    :param allocation: the current allocation (will be updated during the run).
    :return: nothing - the allocation is modified in place.
    """
    num_of_active_agents = len(active_agents)

    if num_of_active_agents==1:
        remaining_agent_index = active_agents[0]
        remaining_agent = agents[remaining_agent_index]
        logger.info("\nOne agent remains (%s), and receives the entire remaining cake starting at %s.", remaining_agent.name(), start)
        allocation.set_piece(remaining_agent_index, [(start, remaining_agent.cake_length())])
        return

    num_of_agents = len(agents)
    logger.info("\n%d agents remain, and recursively allocate the cake starting at %f among them.", num_of_active_agents, start)

    first_agent_index = active_agents[0]
    first_agent = agents[first_agent_index]
    first_agent_mark = first_agent.mark(start, first_agent.cake_value() / num_of_agents)
    logger.info("%s marks at %f", first_agent.name(), first_agent_mark)

    current_mark = first_agent_mark
    current_marker_index = first_agent_index
    for next_agent_index in active_agents[1:]:
        next_agent = agents[next_agent_index]
        next_agent_mark = next_agent.mark(start, next_agent.cake_value() / num_of_agents)
        if next_agent_mark < current_mark:
            logger.info("%s diminishes the current mark to %f.", next_agent.name(), next_agent_mark)
            current_mark = next_agent_mark
            current_marker_index = next_agent_index
        else:
            logger.info("%s does not diminish the current mark.", next_agent.name())

    current_marker = agents[current_marker_index]
    allocation.set_piece(current_marker_index, [(start, current_mark)])
    logger.info("%s is the last diminisher, and gets the piece [%f,%f].", current_marker.name(), start, current_mark)

    active_agents.remove(current_marker_index)
    new_start = current_mark
    last_diminisher_recursive(new_start, agents, active_agents, allocation)

if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
