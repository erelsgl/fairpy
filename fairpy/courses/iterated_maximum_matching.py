#!python3

"""

The Iterated Maximum Matching algorithm for fair item allocation. Reference:

    Johannes Brustle, Jack Dippel, Vishnu V. Narayan, Mashbat Suzuki, Adrian Vetta (2019).
    ["One Dollar Each Eliminates Envy"](https://arxiv.org/abs/1912.02797).
    * Algorithm 1.

Programmer: Erel Segal-Halevi
Since : 2021-05
"""


from fairpy.courses.graph_utils import many_to_many_matching_using_network_flow
from fairpy.courses.instance    import Instance
from fairpy.courses.allocation_utils import AllocationBuilder

import logging
logger = logging.getLogger(__name__)


def iterated_maximum_matching(instance: Instance):
    """
    Finds a allocation for the given instance, using iterated maximum matching.

    >>> from dicttools import stringify

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=1, item_capacities=1)
    >>> map_agent_name_to_bundle = iterated_maximum_matching(instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x'], beni:['w']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=2, item_capacities=1)
    >>> map_agent_name_to_bundle = iterated_maximum_matching(instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y'], beni:['w', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=3, item_capacities=2)
    >>> map_agent_name_to_bundle = iterated_maximum_matching(instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y', 'z'], beni:['w', 'y', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=4, item_capacities=2)
    >>> map_agent_name_to_bundle = iterated_maximum_matching(instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['w', 'x', 'y', 'z'], beni:['w', 'x', 'y', 'z']}"
    """
    alloc = AllocationBuilder(instance)
    complete_allocation_using_iterated_maximum_matching(alloc)
    return alloc.sorted()



def complete_allocation_using_iterated_maximum_matching(alloc:AllocationBuilder):
    """
    A subroutine for iterated maximum matching: receives an instance and a partial allocation, 
    and completes the partial allocation using the given picking sequence.    

    :param alloc: a partial allocation (in an AllocationBuilder object).
    """
    iteration = 1
    while len(alloc.remaining_item_capacities)>0 and len(alloc.remaining_agent_capacities)>0:
        logger.info("\nIteration %d", iteration)
        logger.info("  remaining_agent_capacities: %s", alloc.remaining_agent_capacities)
        logger.info("  remaining_item_capacities: %s", alloc.remaining_item_capacities)
        logger.debug("  remaining_agent_item_value: %s", alloc.remaining_agent_item_value)
        map_agent_to_bundle = many_to_many_matching_using_network_flow(
            items=alloc.remaining_item_capacities.keys(), 
            item_capacity=alloc.remaining_item_capacities.__getitem__, 
            agents=alloc.remaining_agent_capacities.keys(),
            agent_capacity=lambda _:1,
            agent_item_value=lambda agent,item: alloc.remaining_agent_item_value[agent][item])
        logger.info("  matching: %s", dict(map_agent_to_bundle))
        for agent,bundle in map_agent_to_bundle.items():
            if len(bundle)==0:
                alloc.remove_agent(agent)
                continue
            for item in bundle:
                alloc.give(agent,item)
        iteration += 1


iterated_maximum_matching.logger = complete_allocation_using_iterated_maximum_matching.logger = logger





if __name__ == "__main__":
    import doctest
    print("\n",doctest.testmod(), "\n")

    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    from fairpy.courses.adaptors import divide_random_instance
    divide_random_instance(algorithm=iterated_maximum_matching, 
                           num_of_agents=10, num_of_items=4, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1)
