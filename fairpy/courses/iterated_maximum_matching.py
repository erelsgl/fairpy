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
from fairpy.courses.allocation import sorted_allocation

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
    map_agent_name_to_final_bundle = {agent: [] for agent in instance.agents}
    remaining_item_capacities  = {item: instance.item_capacity(item) for item in instance.items}
    remaining_agent_capacities = {agent: instance.agent_capacity(agent) for agent in instance.agents}
    remaining_agent_item_value = {agent: {item:instance.agent_item_value(agent,item) for item in instance.items} for agent in instance.agents}

    iteration = 1
    while len(remaining_item_capacities)>0 and len(remaining_agent_capacities)>0:
        logger.info("\nIteration %d", iteration)
        logger.info("  remaining_agent_capacities: %s", remaining_agent_capacities)
        logger.info("  remaining_item_capacities: %s", remaining_item_capacities)
        logger.debug("  remaining_agent_item_value: %s", remaining_agent_item_value)
        map_agent_to_bundle = many_to_many_matching_using_network_flow(
            items=remaining_item_capacities.keys(), 
            item_capacity=remaining_item_capacities.__getitem__, 
            agents=remaining_agent_capacities.keys(),
            agent_capacity=lambda _:1,
            agent_item_value=lambda agent,item: remaining_agent_item_value[agent][item])
        logger.info("  matching: %s", dict(map_agent_to_bundle))
        for agent,bundle in map_agent_to_bundle.items():
            if len(bundle)==0:
                del remaining_agent_capacities[agent]
                continue
            map_agent_name_to_final_bundle[agent] += bundle
            remaining_agent_capacities[agent]-=len(bundle)
            if remaining_agent_capacities[agent]==0:
                del remaining_agent_capacities[agent]
            for item in bundle:
                remaining_item_capacities[item]-=1
                if remaining_item_capacities[item]==0:
                    del remaining_item_capacities[item]
                remaining_agent_item_value[agent][item] = -1  # prevent the agent from getting the same item again.
        iteration += 1
    return sorted_allocation(map_agent_name_to_final_bundle)



iterated_maximum_matching.logger = logger




#### MAIN

if __name__ == "__main__":
    import doctest, sys
    print("\n",doctest.testmod(), "\n")

    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)

    from fairpy.courses.adaptors import divide_random_instance
    divide_random_instance(algorithm=iterated_maximum_matching, 
                           num_of_agents=10, num_of_items=4, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=None)
