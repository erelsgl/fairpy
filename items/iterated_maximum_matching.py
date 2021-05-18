#!python3

"""

The Iterated Maximum Matching algorithm for fair item allocation. Reference:

    Johannes Brustle, Jack Dippel, Vishnu V. Narayan, Mashbat Suzuki, Adrian Vetta (2019).
    ["One Dollar Each Eliminates Envy"](https://arxiv.org/abs/1912.02797).
    * Algorithm 1.

Programmer: Erel Segal-Halevi
Since : 2021-05
"""

import fairpy

import networkx
from typing import *
from collections import defaultdict
from dicttools import stringify
from fairpy.allocations import Allocation
from fairpy.items.utilitarian_matching import *


import logging
logger = logging.getLogger(__name__)

AgentsDict = Dict[str, Dict[str, int]]


def remove_items(item_capacities:Dict[str,int], items_to_remove:List[str])->Dict[str,int]:
    """
    Remove the given items from the given dict.

    >>> stringify(remove_items({"x":3, "y":2, "z":1, "w":0}, ["x","y"]))
    '{x:2, y:1, z:1}'
    >>> stringify(remove_items({"x":3, "y":2, "z":1, "w":0}, ["y","z"]))
    '{x:3, y:1}'
    """
    for item in items_to_remove:
        item_capacities[item] -= 1
    return {item:new_capacity for item,new_capacity in item_capacities.items() if new_capacity > 0}

def iterated_maximum_matching(agents: AgentsDict, agent_weights: Dict[str, int]=None, item_capacities: Dict[str,int]=None):
    """
    Finds a maximum-weight matching with the given preferences, agent_weights and capacities.
    :param agents: maps each agent to a map from an item's name to its value for the agent.
    :param agent_weights [optional]: maps each agent to an integer priority. The weights of each agent are multiplied by WEIGHT_BASE^priority.
    :param item_capacities [optional]: maps each item to its number of units. Default is 1.

    >>> prefs = {"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}
    >>> alloc = iterated_maximum_matching(prefs, item_capacities={"x":1,"y":1,"z":1,"w":1})
    >>> stringify(alloc.map_agent_to_bundle())
    "{avi:['x', 'y'], beni:['w', 'z']}"
    >>> stringify(alloc.map_item_to_agents())
    "{w:['beni'], x:['avi'], y:['avi'], z:['beni']}"

    >>> prefs = [[5,4,3,2],[2,3,4,5]]
    >>> alloc = iterated_maximum_matching(prefs)
    >>> stringify(alloc.map_agent_to_bundle())
    '{Agent #0:[0, 1], Agent #1:[3, 2]}'
    >>> stringify(alloc.map_item_to_agents())
    "{0:['Agent #0'], 1:['Agent #0'], 2:['Agent #1'], 3:['Agent #1']}"
    """
    agents_list = fairpy.agents_from(agents)
    agent_names = fairpy.agent_names_from(agents)
    all_items = agents_list[0].all_items()
    if item_capacities is None:
        item_capacities = {item:1 for item in all_items}
    map_agent_to_final_bundle = {agent.name(): [] for agent in agents_list}
    while len(item_capacities)>0:
        graph = instance_to_graph(agents, agent_weights=agent_weights, item_capacities=item_capacities)
        logger.info("Graph edges: %s", list(graph.edges.data()))
        matching = networkx.max_weight_matching(graph, maxcardinality=False)
        logger.info("Matching: %s", matching)
        map_agent_to_bundle = matching_to_allocation(matching, agent_names=agent_names)
        for agent,bundle in map_agent_to_bundle.items():
            map_agent_to_final_bundle[agent] += bundle
        allocated_items = sum([bundle for bundle in map_agent_to_bundle.values()], [])
        item_capacities = remove_items(item_capacities, allocated_items)
    return Allocation(agents, map_agent_to_final_bundle)


if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE)
    print("{} failures, {} tests".format(failures, tests))
