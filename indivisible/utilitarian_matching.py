#!python3

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

import networkx
from typing import *
from collections import OrderedDict, defaultdict
from dicttools import stringify

import logging
logger = logging.getLogger(__name__)

Prefs = Dict[str, Dict[str, int]]

def prefs_to_graph(prefs: Prefs,  priorities: Dict[str, int]=None, capacities: Dict[str,int]=None)->networkx.Graph:
    """
    Converts agents' preferences to a bipartite graph (a networkx object).
    :param prefs: maps each agent to a map from an item's name to its value for the agent.
    :param priorities [optional]: maps each agent to an integer priority. The weights of each agent are multiplied by WEIGHT_BASE^priority.
    :param capacities [optional]: maps each item to its number of units. Default is 1.

    >>> prefs = {"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}}
    >>> graph = prefs_to_graph(prefs) 
    >>> list(graph.edges.data())
    [('avi', 'x', {'weight': 5}), ('avi', 'y', {'weight': 4}), ('x', 'beni', {'weight': 2}), ('y', 'beni', {'weight': 3})]
    >>> graph = prefs_to_graph(prefs, capacities={"x":1, "y":2}) 
    >>> list(graph.edges.data())
    [('avi', 'x', {'weight': 5}), ('avi', ('y', 0), {'weight': 4}), ('avi', ('y', 1), {'weight': 4}), ('x', 'beni', {'weight': 2}), (('y', 0), 'beni', {'weight': 3}), (('y', 1), 'beni', {'weight': 3})]
    >>> graph = prefs_to_graph(prefs, priorities={"avi":0, "beni":1}) 
    >>> list(graph.edges.data())
    [('avi', 'x', {'weight': 5}), ('avi', 'y', {'weight': 4}), ('x', 'beni', {'weight': 200}), ('y', 'beni', {'weight': 300})]
    """
    WEIGHT_BASE = 100
    graph = networkx.Graph()
    for agent,agentprefs in prefs.items():
        for good,value in agentprefs.items():
            weight=value
            if priorities is not None:
                priority = priorities.get(agent,0)
                weight *= (WEIGHT_BASE**priority)
            num_of_units = 1 # default capacity
            if capacities is not None:
                num_of_units = capacities.get(good, 0)  # get the capacity from the map. If it is not in the map, the capacity is 0.
            if num_of_units==1:
                graph.add_edge(agent, good, weight=weight)
            else:
                for c in range(num_of_units):
                    graph.add_edge(agent, (good,c), weight=weight)
    return graph


def matching_to_maps(matching: list, agents:list, priorities: Dict[str, int]=None, sortkey=None)->(Dict[str,str], Dict[str,List[str]]):
    """
    Converts a one-to-many matching in a bipartite graph (output of networkx) to an allocation (given as two equivalent maps).
    :param matching: a list of pairs (agent,item).
    :param priorities [optional]: maps each agent to an integer priority. Used for sorting the agents in the list for each item.
    :param sortkey [optional]: a key for additional sorting of the agents in the list for each item.

    :return two maps: the first maps an agent to the (single) item he got, and the second maps an item to the list of agents who got units of that item.

    >>> matching = [("a", "xxx"), ("b", "yyy"), ("c", "yyy")]
    >>> (map_agent_to_matched_good, map_good_to_matched_agents) = matching_to_maps(matching, ["a","b","c"])
    >>> stringify(map_agent_to_matched_good)
    '{a:xxx, b:yyy, c:yyy}'
    >>> stringify(map_good_to_matched_agents)
    "{xxx:['a'], yyy:['b', 'c']}"
    >>> matching = [("a", "xxx"), ("b", "yyy"), ("c", "yyy")]
    >>> (map_agent_to_matched_good, map_good_to_matched_agents) = matching_to_maps(matching, ["a","b","c"], priorities={"a":0, "b":1, "c":2})
    >>> stringify(map_agent_to_matched_good)
    '{a:xxx, b:yyy, c:yyy}'
    >>> stringify(map_good_to_matched_agents)
    "{xxx:['a'], yyy:['c', 'b']}"
    """
    map_agent_to_matched_good = {}
    map_good_to_matched_agents = defaultdict(list)
    for edge in matching:
        if edge[0] in agents:  
            (agent,good)=edge
        elif edge[1] in agents:
            (good,agent)=edge
        else:
            raise ValueError(f"Cannot find an agent in {edge}")
        if isinstance(good, tuple):  # when there are several units of the same good...
            good = good[0]           # ... 0 is the good, 1 is the unit-number. 
        map_good_to_matched_agents[good].append(agent)
        map_agent_to_matched_good[agent] = good
    for good,agents in map_good_to_matched_agents.items():
        agents.sort(key=sortkey)
        if priorities is not None:
            agents.sort(key=lambda agent: -priorities.get(agent, 0))
    return (map_agent_to_matched_good, map_good_to_matched_agents)




def max_weight_matching(prefs: Prefs, priorities: Dict[str, int]=None, capacities: Dict[str,int]=None, sortkey=None, maxcardinality=True):
    """
    Finds a maximum-weight matching with the given preferences, priorities and capacities.
    :param prefs: maps each agent to a map from an item's name to its value for the agent.
    :param priorities [optional]: maps each agent to an integer priority. The weights of each agent are multiplied by WEIGHT_BASE^priority.
    :param capacities [optional]: maps each item to its number of units. Default is 1.
    :param sortkey [optional]: a key for additional sorting of the agents in the list for each item.
    :param maxcardinality: True to require maximum weight subject to maximum cardinality. False to require only maximum weight.

    :return two maps: the first maps an agent to the (single) item he got, and the second maps an item to the list of agents who got units of that item.

    >>> prefs = {"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}}
    >>> (map_agent_to_matched_good, map_good_to_matched_agent) = max_weight_matching(prefs)
    >>> stringify(map_agent_to_matched_good)
    '{avi:x, beni:y}'
    >>> stringify(map_good_to_matched_agent)
    "{x:['avi'], y:['beni']}"
    >>> prefs = {"avi": {"x":5, "y": -2}, "beni": {"x":2, "y":-3}}
    >>> stringify(max_weight_matching(prefs, maxcardinality=True)[0])
    '{avi:x, beni:y}'
    >>> stringify(max_weight_matching(prefs, maxcardinality=False)[0])
    '{avi:x}'
    >>> prefs = {"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}, "gadi": {"x":3, "y":2}}
    >>> capacities = {"x":2, "y":2}
    >>> (map_agent_to_matched_good, map_good_to_matched_agents) = max_weight_matching(prefs, capacities=capacities)
    >>> stringify(map_agent_to_matched_good)
    '{avi:x, beni:y, gadi:x}'
    >>> stringify(map_good_to_matched_agents)
    "{x:['avi', 'gadi'], y:['beni']}"
    """
    graph = prefs_to_graph(prefs, priorities=priorities, capacities=capacities)
    logger.info("Graph edges: %s", list(graph.edges.data()))
    matching = networkx.max_weight_matching(graph, maxcardinality=maxcardinality)
    logger.info("Matching: %s", matching)
    return matching_to_maps(matching, agents=prefs.keys(), priorities=priorities, sortkey=sortkey)


if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE)
    print("{} failures, {} tests".format(failures, tests))
