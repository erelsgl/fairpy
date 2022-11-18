#!python3

"""

The Iterated Maximum Matching algorithm for fair item allocation. Reference:

    Johannes Brustle, Jack Dippel, Vishnu V. Narayan, Mashbat Suzuki, Adrian Vetta (2019).
    ["One Dollar Each Eliminates Envy"](https://arxiv.org/abs/1912.02797).
    * Algorithm 1.

Programmer: Erel Segal-Halevi
Since : 2021-05
"""


import networkx
from typing import *
from fairpy.items.utilitarian_matching import instance_to_graph, matching_to_allocation
from fairpy import AgentList

import logging
logger = logging.getLogger(__name__)


def iterated_maximum_matching(agents: AgentList, item_capacities: Dict[str,int]=None, agent_weights: Dict[str, int]=None):
    """
    Finds a maximum-weight matching with the given preferences, agent_weights and capacities.
    :param agents: maps each agent to a map from an item's name to its value for the agent.
    :param item_capacities [optional]: maps each item to its number of units. Default is 1.
    :param agent_weights [optional]: maps each agent to an integer priority. The weights of each agent are multiplied by WEIGHT_BASE^priority.

    >>> from dicttools import stringify
    >>> agents = AgentList({"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}})
    >>> map_agent_name_to_bundle = iterated_maximum_matching(agents, item_capacities={"x":1,"y":1,"z":1,"w":1})
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y'], beni:['w', 'z']}"

    >>> agents = AgentList([[5,4,3,2],[2,3,4,5]])
    >>> map_agent_name_to_bundle = iterated_maximum_matching(agents)
    >>> stringify(map_agent_name_to_bundle)
    '{Agent #0:[0, 1], Agent #1:[3, 2]}'
    """
    assert isinstance(agents, AgentList)
    all_items = agents[0].all_items()
    if item_capacities is None:
        item_capacities = {item:1 for item in all_items}
    map_agent_name_to_final_bundle = {agent.name(): [] for agent in agents}
    while len(item_capacities)>0:
        graph = instance_to_graph(agents, agent_weights=agent_weights, item_capacities=item_capacities)
        logger.info("Graph edges: %s", list(graph.edges.data()))
        matching = networkx.max_weight_matching(graph, maxcardinality=False)
        logger.info("Matching: %s", matching)
        map_agent_to_bundle = matching_to_allocation(matching, agent_names=agents.agent_names())
        for agent,bundle in map_agent_to_bundle.items():
            map_agent_name_to_final_bundle[agent] += bundle
        allocated_items = sum([bundle for bundle in map_agent_to_bundle.values()], [])
        item_capacities = _remove_items(item_capacities, allocated_items)
    return map_agent_name_to_final_bundle



def iterated_maximum_matching_categories(agents: AgentList, categories: List[List[str]], agent_weights: Dict[str, int]=None):
    """
    Finds a maximum-weight matching with the given preferences and agent_weights, where the items are pre-divided into categories. Each agent gets at most a single item from each category.
    :param agents: maps each agent to a map from an item's name to its value for the agent.
    :param categories: a list of lists; each list is a category of items.
    :param agent_weights [optional]: maps each agent to an integer priority. The weights of each agent are multiplied by WEIGHT_BASE^priority.

    >>> from dicttools import stringify
    >>> agents = AgentList({"agent1": {"t1+": 0, "t1-": -3,   "t2+": 0, "t2-": -9,   "t3+": 0, "t3-": -2},	"agent2": {"t1+": 0, "t1-": -6,   "t2+": 0, "t2-": -9,   "t3+": 0, "t3-": -1}})
    >>> categories = [["t1+","t1-"],["t2+","t2-"],["t3+","t3-"]]
    >>> stringify(iterated_maximum_matching_categories(agents, categories, agent_weights={"agent1":1,"agent2":0}))
    "{agent1:['t1+', 't2+', 't3+'], agent2:['t1-', 't2-', 't3-']}"
    >>> stringify(iterated_maximum_matching_categories(agents, categories, agent_weights={"agent1":1,"agent2":1}))
    "{agent1:['t1-', 't2-', 't3+'], agent2:['t1+', 't2+', 't3-']}"
    >>> stringify(iterated_maximum_matching_categories(agents, categories, agent_weights={"agent1":0,"agent2":1}))
    "{agent1:['t1-', 't2-', 't3-'], agent2:['t1+', 't2+', 't3+']}"

    >>> agents = AgentList([[55,44,33,22],[22,33,44,55]])
    >>> stringify(iterated_maximum_matching_categories(agents, categories= [[0,1],[2,3]]))
    '{Agent #0:[0, 2], Agent #1:[1, 3]}'
    >>> stringify(iterated_maximum_matching_categories(agents, categories= [[0,2],[1,3]]))
    '{Agent #0:[0, 1], Agent #1:[2, 3]}'
    """
    assert isinstance(agents, AgentList)
    agent_names=agents.agent_names()
    map_agent_name_to_final_bundle = {name: [] for name in agent_names}
    for index,category in enumerate(categories):
        graph = instance_to_graph(agents, agent_weights=agent_weights, item_capacities={item:1 for item in category})
        logger.info("Category %d:",index)
        logger.info("  Graph edges: %s", list(graph.edges.data()))
        matching = networkx.max_weight_matching(graph, maxcardinality=True)
        logger.info("  Matching: %s", matching)
        map_agent_to_bundle = matching_to_allocation(matching, agent_names=agent_names)
        for name in agent_names:
            if map_agent_to_bundle[name] is not None:
                map_agent_name_to_final_bundle[name] += map_agent_to_bundle[name]
    return map_agent_name_to_final_bundle


iterated_maximum_matching.logger = logger




#### INTERNAL FUNCTIONS

def _remove_items(item_capacities:Dict[str,int], items_to_remove:List[str])->Dict[str,int]:
    """
    Remove the given items from the given dict.

    >>> from dicttools import stringify
    >>> stringify(_remove_items({"x":3, "y":2, "z":1, "w":0}, ["x","y"]))
    '{x:2, y:1, z:1}'
    >>> stringify(_remove_items({"x":3, "y":2, "z":1, "w":0}, ["y","z"]))
    '{x:3, y:1}'
    """
    for item in items_to_remove:
        item_capacities[item] -= 1
    return {item:new_capacity for item,new_capacity in item_capacities.items() if new_capacity > 0}




#### MAIN

if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE)
    print("{} failures, {} tests".format(failures, tests))
