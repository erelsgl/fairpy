#!python3
"""
An algorithm for 1-out-of-(3n/2) MMS allocation of indivisible objects.

Programmer: Erel Segal-Halevi
Since:  2021-04
"""

from fairpy.valuations import ValuationMatrix
from fairpy.allocations import Allocation
from fairpy.indivisible.bag_filling import Bag

import logging
logger = logging.getLogger(__name__)


def round_robin(items:Bundle, agents:List[AdditiveAgent], agent_order:List[int]) -> Allocation:
    """
    Allocate the given items to the given agents using the round-robin protocol, in the given agent-order.

    >>> Alice = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0}, name="Alice")
    >>> George = AdditiveAgent({"x": 2, "y": 1, "z": 6, "w":3}, name="George")
    >>> allocation = round_robin("xyzw", [Alice,George], [0,1])
    >>> allocation
    Alice gets {y,z} with value 6.
    George gets {w,x} with value 5.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation.get_bundle(0), allocation.get_bundles())
    True
    >>> George.is_EF1(allocation.get_bundle(1), allocation.get_bundles())
    True
    >>> Alice.is_EF(allocation.get_bundle(0), allocation.get_bundles())
    True
    >>> George.is_EF(allocation.get_bundle(1), allocation.get_bundles())
    False
    """
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



### MAIN

if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)
    #
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
