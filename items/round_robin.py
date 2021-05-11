#!python3
"""
The Round Robin algorithm for item allocation.

Authors: folklore. See https://en.wikipedia.org/wiki/Round-robin_item_allocation

Programmer: Erel Segal-Halevi
Since:  2020-07
"""

from fairpy.allocations import Allocation
from fairpy.items.agents import *

import logging
logger = logging.getLogger(__name__)


def round_robin(agents, agent_order:List[int], items:Bundle=None) -> Allocation:
    """
    Allocate the given items to the given agents using the round-robin protocol, in the given agent-order.

    >>> Alice = AdditiveAgent({"x": 11, "y": 22, "z": 44, "w":0}, name="Alice")
    >>> George = AdditiveAgent({"x": 22, "y": 11, "z": 66, "w":33}, name="George")
    >>> allocation = round_robin([Alice,George], [0,1], items="xyzw")
    >>> allocation
    Alice gets {y,z} with value 66.
    George gets {w,x} with value 55.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation.get_bundle(0), allocation.get_bundles())
    True
    >>> George.is_EF1(allocation.get_bundle(1), allocation.get_bundles())
    True
    >>> Alice.is_EF(allocation.get_bundle(0), allocation.get_bundles())
    True
    >>> George.is_EF(allocation.get_bundle(1), allocation.get_bundles())
    False
    >>> # A different input format:
    >>> round_robin([[11,22,44,0],[22,11,66,33]], [0,1], items={0,1,2,3})
    Agent #0 gets {1,2} with value 66.
    Agent #1 gets {0,3} with value 55.
    <BLANKLINE>
    """
    agents = agents_from(agents)  # Handles various input formats
    logger.info("\nRound Robin with order %s", agent_order)
    allocations = [[] for _ in agents]
    agent_order = list(agent_order)
    remaining_items = list(items)
    while True:
        for agent_index in agent_order:
            if len(remaining_items)==0:
                return Allocation(agents, allocations)
            agent = agents[agent_index]
            best_item_for_agent = max(remaining_items, key=agent.value)
            best_item_value = agent.value(best_item_for_agent)
            allocations[agent_index].append(best_item_for_agent)
            logger.info("%s takes %s (value %d)", agent.name(), best_item_for_agent, best_item_value)
            remaining_items.remove(best_item_for_agent)


round_robin.logger = logger

### MAIN

if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)
    #
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
