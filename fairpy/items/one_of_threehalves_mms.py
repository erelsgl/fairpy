#!python3
"""
An algorithm for 1-out-of-(3n/2) MMS allocation of indivisible objects.

Programmer: Erel Segal-Halevi
Since:  2021-04
"""

from fairpy import ValuationMatrix
from fairpy.items.bag_filling import Bag, SequentialAllocation

from typing import List, Any

import logging
logger = logging.getLogger(__name__)

def bidirectional_bag_filling(valuation_matrix:ValuationMatrix, thresholds:List[float]) -> List[List[Any]]:
    """
    Runs a bi-directional bag-filling algorithm.
    Assumes that the instance is ordered: item 0 is the highest-valued for all agents, then item 1, etc.

    >>> identical_valuations = [97,96,90,12,3,2,1,1,1]
    >>> valuation_matrix = ValuationMatrix([identical_valuations for _ in range(3)])
    >>> bidirectional_bag_filling(valuation_matrix, thresholds=[100,100,100])
    [[0, 8, 7, 6], [1, 5, 4], [2, 3]]
    >>> bidirectional_bag_filling(valuation_matrix, thresholds=[101,101,101])
    [[0, 8, 7, 6, 5], [1, 4, 3], None]
    """
    valuation_matrix.verify_ordered()
    if len(thresholds) != valuation_matrix.num_of_agents:
        raise ValueError(f"Number of valuations {valuation_matrix.num_of_agents} differs from number of thresholds {len(thresholds)}")
    allocation = SequentialAllocation(valuation_matrix.agents(), valuation_matrix.objects(), logger)
    bag = Bag(valuation_matrix, thresholds)
    while True:
        if len(allocation.remaining_objects)==0:  break

        # Initialize a bag with the highest-valued object:
        highest_valued_object = allocation.remaining_objects[0]
        bag.append(highest_valued_object)

        # Fill the bag with the lowest-valued objects:
        lowest_valued_objects = reversed(allocation.remaining_objects[1:])
        (willing_agent, allocated_objects) = bag.fill(lowest_valued_objects, allocation.remaining_agents)
        if willing_agent is None: break
        allocation.let_agent_get_objects(willing_agent, allocated_objects)
        bag.reset()
    return allocation.bundles
    



if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    # import fairpy.items.bag_filling as bag_filling
    # bag_filling.logger.addHandler(logging.StreamHandler(sys.stdout))
    # bag_filling.logger.setLevel(logging.INFO)
    
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
