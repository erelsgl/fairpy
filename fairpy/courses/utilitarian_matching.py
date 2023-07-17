#!python3

"""

Utilitarian matching - maximizes the sum of agents' valuations.

Programmer: Erel Segal-Halevi
Since : 2023-07
"""


from fairpy.courses.graph_utils import many_to_many_matching_using_network_flow
from fairpy.courses.instance    import Instance

import logging
logger = logging.getLogger(__name__)


def utilitarian_matching(instance: Instance):
    """
    Finds a maximum-weight matching with the given preferences, agent_weights and capacities.
    :param agents: maps each agent to a map from an item's name to its value for the agent.
    :param item_capacities [optional]: maps each item to its number of units. Default is 1.
    :param agent_weights [optional]: maps each agent to an integer priority. The weights of each agent are multiplied by WEIGHT_BASE^priority.

    >>> from dicttools import stringify

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=1, item_capacities=1)
    >>> map_agent_name_to_bundle = utilitarian_matching(instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x'], beni:['w']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=2, item_capacities=1)
    >>> map_agent_name_to_bundle = utilitarian_matching(instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y'], beni:['w', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=3, item_capacities=2)
    >>> map_agent_name_to_bundle = utilitarian_matching(instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y', 'z'], beni:['w', 'y', 'z']}"

    >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=4, item_capacities=2)
    >>> map_agent_name_to_bundle = utilitarian_matching(instance)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['w', 'x', 'y', 'z'], beni:['w', 'x', 'y', 'z']}"
    """
    return many_to_many_matching_using_network_flow(
        items=instance.items,
        item_capacity=instance.item_capacity,
        agents=instance.agents,
        agent_capacity=instance.agent_capacity,
        agent_item_value=instance.agent_item_value)


utilitarian_matching.logger = logger




#### MAIN

if __name__ == "__main__":
    import sys
    logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest
    print(doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE))
