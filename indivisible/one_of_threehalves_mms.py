#!python3
"""
An algorithm for 1-out-of-(3n/2) MMS allocation of indivisible objects.

Programmer: Erel Segal-Halevi
Since:  2021-04
"""

from fairpy.valuations import ValuationMatrix
from fairpy.allocations import Allocation
from fairpy.indivisible.bag_filling import Bag

from typing import List

import logging
logger = logging.getLogger(__name__)

def bidirectional_bag_filling(valuations:ValuationMatrix, thresholds:List[float]) -> Allocation:
    """
    Runs a bi-directional bag-filling algorithm.
    Assumes that the instance is ordered: item 0 is the highest-valued for all agents, then item 1, etc.

    >>> Allocation.default_separator=","
    >>> identical_valuations = [97,96,90,12,3,2,1,1,1]
    >>> valuations = ValuationMatrix(3*[identical_valuations])
    >>> bidirectional_bag_filling(valuations, thresholds=[100,100,100])
    Agent #0 gets {0,6,7,8} with value 100.
    Agent #1 gets {1,4,5} with value 101.
    Agent #2 gets {2,3} with value 102.
    <BLANKLINE>
    >>> bidirectional_bag_filling(valuations, thresholds=[101,101,101])
    Agent #0 gets {0,5,6,7,8} with value 102.
    Agent #1 gets {1,3,4} with value 111.
    Agent #2 gets None with value 0.
    <BLANKLINE>
    """
    v = ValuationMatrix(valuations)
    v.verify_ordered()
    if len(thresholds) != v.num_of_agents:
        raise ValueError(f"Number of valuations {v.num_of_agents} differs from number of thresholds {len(thresholds)}")

    allocations = [None] * v.num_of_agents
    remaining_objects = list(v.objects())
    remaining_agents  = list(v.agents())
    bag = Bag(v, thresholds)
    while True:
        if len(remaining_agents)==0:   break
        if len(remaining_objects)==0:  break

        # Initialize a bag with the highest-valued object:
        highest_valued_object = remaining_objects[0]
        bag.append(highest_valued_object)

        # Fill the bag with the lowest-valued objects:
        (willing_agent, allocated_objects) = bag.fill(reversed(remaining_objects[1:]), remaining_agents)
        if willing_agent is None: break
        allocations[willing_agent] = allocated_objects
        remaining_agents.remove(willing_agent)
        for o in allocated_objects: remaining_objects.remove(o)
        logger.info("Agent %d takes the bag with objects %s. Remaining agents: %s. Remaining objects: %s.", willing_agent, allocated_objects, remaining_agents, remaining_objects)
        bag.reset()

    map_agent_to_value = [v.agent_value_for_bundle(agent,allocations[agent]) for agent in v.agents()]
    return Allocation(v.agents(), allocations, map_agent_to_value)



### MAIN

if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    # import fairpy.indivisible.bag_filling as bag_filling
    # bag_filling.logger.addHandler(logging.StreamHandler(sys.stdout))
    # bag_filling.logger.setLevel(logging.INFO)
    
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
