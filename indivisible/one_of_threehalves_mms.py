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

def one_of_threehalves_mms(v:ValuationMatrix, map_agent_to_value_threshold:List[float]) -> Allocation:
    """
    Runs a bi-directional bag-filling algorithm.
    Assumes that the instance is ordered: item 0 is the highest-valued for all agents, then item 1, etc.

    >>> identical_valuations = [97,96,90,12,3,2,1,1,1]
    >>> valuations = ValuationMatrix(3*[identical_valuations])
    >>> alloc = one_of_threehalves_mms(valuations, map_agent_to_value_threshold=[100,100,100])
    >>> alloc
    Agent #0 gets {0,6,7,8} with value 100.
    Agent #1 gets {1,4,5} with value 101.
    Agent #2 gets {2,3} with value 102.
    <BLANKLINE>
    """
    v = ValuationMatrix(v)
    v.verify_ordered()
    if len(map_agent_to_value_threshold) != v.num_of_agents:
        raise ValueError(f"Number of valuations {v.num_of_agents} differs from number of thresholds {len(map_agent_to_value_threshold)}")

    allocations = [None] * v.num_of_agents
    remaining_objects = list(v.objects())
    remaining_agents  = list(v.agents())
    while True:
        if len(remaining_agents)==0:
            break
        if len(remaining_objects)==0:
            break

        # Initialize a bag with the highest-valued object:
        bag = Bag(v, map_agent_to_value_threshold)
        highest_valued_object = remaining_objects.pop(0)
        bag.append(highest_valued_object)
        
        while True:
            # If an agent is willing to accept the bag, allocate it immediately:
            if (willing_agent := bag.willing_agent(remaining_agents)) is not None:
                allocations[willing_agent] = bag.objects
                remaining_agents.remove(willing_agent)
                break
            if len(remaining_objects)==0:
                break
            lowest_valued_object = remaining_objects.pop(-1)
            bag.append(lowest_valued_object)

    valuations = [v.agent_value_for_bundle(agent,allocations[agent]) for agent in v.agents()]
    return Allocation(v.agents(), allocations, valuations)



### MAIN

if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)
    #
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
