"""
Implement an "almost-egalitarian" course allocation,
by rounding a linear program.

Programmer: Erel Segal-Halevi.
Since: 2023-07
"""

from fairpy.items.leximin import leximin_optimal_allocation
from fairpy.courses.instance import Instance

import logging
logger = logging.getLogger(__name__)

def almost_egalitarian_allocation(instance: Instance):
    """
    Finds an almost-egalitarian allocation.

    >>> from dicttools import stringify

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=1, item_capacities=1)
    >>> stringify(almost_egalitarian_allocation(instance))
    "{avi:['x'], beni:['w']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=2, item_capacities=1)
    >>> stringify(almost_egalitarian_allocation(instance))
    "{avi:['x', 'y'], beni:['w', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=3, item_capacities=2)
    >>> stringify(almost_egalitarian_allocation(instance))
    "{avi:['x', 'y', 'z'], beni:['w', 'y', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=4, item_capacities=2)
    >>> stringify(almost_egalitarian_allocation(instance))
    "{avi:['w', 'x', 'y', 'z'], beni:['w', 'x', 'y', 'z']}"
    """
    map_agent_name_to_final_bundle = {agent: [] for agent in instance.agents}
    remaining_item_capacities = {item: instance.item_capacity(item) for item in instance.items}
    remaining_agents = [agent for agent in instance.agents if instance.agent_capacity(agent)>0]
    remaining_agent_item_value = {agent: {item:instance.agent_item_value(agent,item) for item in instance.items} for agent in instance.agents}
    while len(remaining_item_capacities)>0:
        logger.info("\nremaining_agents: %s", remaining_agents)
        logger.info("remaining_item_capacities: %s", remaining_item_capacities)
        logger.info("remaining_agent_item_value: %s", remaining_agent_item_value)
        map_agent_to_bundle = many_to_many_matching_using_network_flow(
            items=remaining_item_capacities.keys(), 
            item_capacity=remaining_item_capacities.__getitem__, 
            agents=remaining_agents,
            agent_capacity=lambda _:1,
            agent_item_value=lambda agent,item: remaining_agent_item_value[agent][item])
        logger.info("matching: %s", map_agent_to_bundle)
        for agent,bundle in map_agent_to_bundle.items():
            if len(bundle)==0:
                remaining_agents.remove(agent)
            map_agent_name_to_final_bundle[agent] += bundle
            for item in bundle:
                remaining_item_capacities[item]-=1
                if remaining_item_capacities[item]==0:
                    del remaining_item_capacities[item]
                remaining_agent_item_value[agent][item] = -1  # prevent the agent from getting the same item again.
            if len(map_agent_name_to_final_bundle[agent])>=instance.agent_capacity(agent):
                remaining_agents.remove(agent)
        if len(remaining_agents)==0 or len(remaining_item_capacities)==0:
            break
    for agent,bundle in map_agent_name_to_final_bundle.items():
        bundle.sort()
    return map_agent_name_to_final_bundle
