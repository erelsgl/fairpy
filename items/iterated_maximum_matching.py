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

def iterated_maximum_matching(agents: AgentsDict, item_capacities: Dict[str,int]=None, agent_weights: Dict[str, int]=None):
    """
    Finds a maximum-weight matching with the given preferences, agent_weights and capacities.
    :param agents: maps each agent to a map from an item's name to its value for the agent.
    :param item_capacities [optional]: maps each item to its number of units. Default is 1.
    :param agent_weights [optional]: maps each agent to an integer priority. The weights of each agent are multiplied by WEIGHT_BASE^priority.

    >>> prefs = {"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}
    >>> alloc = iterated_maximum_matching(prefs, item_capacities={"x":1,"y":1,"z":1,"w":1})
    >>> stringify(alloc.map_agent_to_bundle())
    "{avi:['x', 'y'], beni:['w', 'z']}"
    >>> stringify(alloc.map_item_to_agents())
    "{w:['beni'], x:['avi'], y:['avi'], z:['beni']}"

    >>> prefs = [[5,4,3,2],[2,3,4,5]]
    >>> alloc = iterated_maximum_matching(prefs)
    >>> alloc
    Agent #0 gets {0,1} with value 9.
    Agent #1 gets {2,3} with value 9.
    <BLANKLINE>
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
    return Allocation(agents_list, map_agent_to_final_bundle)



def iterated_maximum_matching_categories(agents: AgentsDict, categories: List[List[str]], agent_weights: Dict[str, int]=None):
    """
    Finds a maximum-weight matching with the given preferences and agent_weights, where the items are pre-divided into categories. Each agent gets at most a single item from each category.
    :param agents: maps each agent to a map from an item's name to its value for the agent.
    :param categories: a list of lists; each list is a category of items.
    :param agent_weights [optional]: maps each agent to an integer priority. The weights of each agent are multiplied by WEIGHT_BASE^priority.

    >>> agents = {"agent1": {"t1+": 0, "t1-": -3,   "t2+": 0, "t2-": -9,   "t3+": 0, "t3-": -2},	"agent2": {"t1+": 0, "t1-": -6,   "t2+": 0, "t2-": -9,   "t3+": 0, "t3-": -1}}
    >>> categories = [["t1+","t1-"],["t2+","t2-"],["t3+","t3-"]]
    >>> iterated_maximum_matching_categories(agents, categories, agent_weights={"agent1":1,"agent2":0})
    agent1 gets {t1+,t2+,t3+} with value 0.
    agent2 gets {t1-,t2-,t3-} with value -16.
    <BLANKLINE>
    >>> iterated_maximum_matching_categories(agents, categories, agent_weights={"agent1":1,"agent2":1})
    agent1 gets {t1-,t2-,t3+} with value -12.
    agent2 gets {t1+,t2+,t3-} with value -1.
    <BLANKLINE>
    >>> iterated_maximum_matching_categories(agents, categories, agent_weights={"agent1":0,"agent2":1})
    agent1 gets {t1-,t2-,t3-} with value -14.
    agent2 gets {t1+,t2+,t3+} with value 0.
    <BLANKLINE>

    >>> agents = [[55,44,33,22],[22,33,44,55]]
    >>> iterated_maximum_matching_categories(agents, categories= [[0,1],[2,3]])
    Agent #0 gets {0,2} with value 88.
    Agent #1 gets {1,3} with value 88.
    <BLANKLINE>
    >>> iterated_maximum_matching_categories(agents, categories= [[0,2],[1,3]])
    Agent #0 gets {0,1} with value 99.
    Agent #1 gets {2,3} with value 99.
    <BLANKLINE>
    """
    agents_list = fairpy.agents_from(agents)
    agent_names = fairpy.agent_names_from(agents)
    map_agent_to_final_bundle = {agent.name(): [] for agent in agents_list}
    for index,category in enumerate(categories):
        graph = instance_to_graph(agents, agent_weights=agent_weights, item_capacities={item:1 for item in category})
        logger.info("Category %d:",index)
        logger.info("  Graph edges: %s", list(graph.edges.data()))
        matching = networkx.max_weight_matching(graph, maxcardinality=True)
        logger.info("  Matching: %s", matching)
        map_agent_to_bundle = matching_to_allocation(matching, agent_names=agent_names)
        for name in agent_names:
            if map_agent_to_bundle[name] is not None:
                map_agent_to_final_bundle[name] += map_agent_to_bundle[name]
    return Allocation(agents_list, map_agent_to_final_bundle)


iterated_maximum_matching.logger = logger


if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE)
    print("{} failures, {} tests".format(failures, tests))
