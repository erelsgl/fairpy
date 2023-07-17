"""
SETTING: 
* There are n agents.
* There are k items; from each item, there may be several units.
* Each agent may have a different value for each item.

GOAL: Assign a single item-unit to each agent, such that the sum of values is maximum.

VARIANTS: allows to give priorities to agents, i.e., multiply their weights by a factor.

Author: Erel Segal-Halevi
Since : 2021-04
"""

from typing import *
from fairpy import AgentList
from fairpy.items.graph_utils import instance_to_graph, matching_to_allocation
import networkx

import logging
logger = logging.getLogger(__name__)


def utilitarian_matching(
    agents: AgentList, 
    agent_weights: Dict[str, int]=None, 
    item_capacities: Dict[str,int]=None, 
    agent_capacities: Dict[str,int]=None, 
    maxcardinality=True)->Dict[str,str]:
    """
    Finds a maximum-weight matching with the given preferences, agent_weights and capacities.
    :param agents: maps each agent to a map from an item's name to its value for the agent.
    :param agent_weights [optional]: maps each agent to an integer priority. The weights of each agent are multiplied by WEIGHT_BASE^priority.
    :param item_capacities [optional]: maps each item to its number of units. Default is 1.
    :param maxcardinality: True to require maximum weight subject to maximum cardinality. False to require only maximum weight.

    >>> from dicttools import stringify
    >>> prefs = AgentList({"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}})
    >>> map_agent_name_to_bundle = utilitarian_matching(prefs)
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x'], beni:['y']}"

    >>> prefs = AgentList({"avi": {"x":5, "y": -2}, "beni": {"x":2, "y":-3}})
    >>> stringify(utilitarian_matching(prefs, maxcardinality=True))
    "{avi:['x'], beni:['y']}"
    >>> stringify(utilitarian_matching(prefs, maxcardinality=False))
    "{avi:['x']}"

    >>> prefs = AgentList({"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}, "gadi": {"x":3, "y":2}})
    >>> map_agent_name_to_bundle = utilitarian_matching(prefs, item_capacities={"x":2, "y":2})
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x'], beni:['y'], gadi:['x']}"

    >>> map_agent_name_to_bundle = utilitarian_matching(prefs, item_capacities={"x":2, "y":2}, agent_capacities={"avi":2,"beni":1,"gadi":1})
    >>> stringify(map_agent_name_to_bundle)
    "{avi:['x', 'y'], beni:['y'], gadi:['x']}"

    >>> prefs = AgentList([[5,4],[3,2]])
    >>> map_agent_name_to_bundle = utilitarian_matching(prefs)
    >>> stringify(map_agent_name_to_bundle)
    '{Agent #0:[1], Agent #1:[0]}'
    """
    assert isinstance(agents, AgentList)
    graph = instance_to_graph(agents, agent_weights=agent_weights, item_capacities=item_capacities, agent_capacities=agent_capacities)
    logger.info("Graph edges: %s", list(graph.edges.data()))
    matching = networkx.max_weight_matching(graph, maxcardinality=maxcardinality)
    logger.info("Matching: %s", matching)
    map_agent_name_to_bundle = matching_to_allocation(matching, agent_names=agents.agent_names())
    return map_agent_name_to_bundle
    # return Allocation(agents, map_agent_name_to_bundle)




if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest
    print(doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE))
