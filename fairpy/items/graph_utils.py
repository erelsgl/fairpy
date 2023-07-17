"""
Utility functions for converting an instance to a (networkx) graph,
and for converting a matching to an allocation.

Author: Erel Segal-Halevi
Since : 2021-04
"""

import networkx
from fairpy import AgentList
from typing import *
from collections import defaultdict


def instance_to_graph(agents: AgentList,  agent_weights: Dict[str, int]=None, item_capacities: Dict[str,int]=None, agent_capacities: Dict[str,int]=None)->networkx.Graph:
    """
    Converts agents' preferences to a bipartite graph (a networkx object).
    :param agents: maps each agent to a map from an item's name to its value for the agent.
    :param agent_weights [optional]: maps each agent to a weight. The values of each agent are multiplied by the agent's weight.
    :param item_capacities [optional]: maps each item to its number of units. Default is 1.

    >>> prefs = AgentList({"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}})
    >>> graph = instance_to_graph(prefs) 
    >>> list(graph.edges.data())
    [('avi', 'x', {'weight': 5}), ('avi', 'y', {'weight': 4}), ('x', 'beni', {'weight': 2}), ('y', 'beni', {'weight': 3})]
    >>> graph = instance_to_graph(prefs, item_capacities={"x":1, "y":2}) 
    >>> list(graph.edges.data())
    [('avi', 'x', {'weight': 5}), ('avi', ('y', 0), {'weight': 4}), ('avi', ('y', 1), {'weight': 4}), ('x', 'beni', {'weight': 2}), (('y', 0), 'beni', {'weight': 3}), (('y', 1), 'beni', {'weight': 3})]
    >>> graph = instance_to_graph(prefs, agent_weights={"avi":1, "beni":100}) 
    >>> list(graph.edges.data())
    [('avi', 'x', {'weight': 5}), ('avi', 'y', {'weight': 4}), ('x', 'beni', {'weight': 200}), ('y', 'beni', {'weight': 300})]
    >>> graph = instance_to_graph(prefs, agent_capacities={"avi":2, "beni":1}) 
    >>> list(graph.edges.data())
    [(('avi', 0), 'x', {'weight': 5}), (('avi', 0), 'y', {'weight': 4}), ('x', ('avi', 1), {'weight': 5}), ('x', 'beni', {'weight': 2}), (('avi', 1), 'y', {'weight': 4}), ('y', 'beni', {'weight': 3})]
    >>> graph = instance_to_graph(prefs, item_capacities={"x":1, "y":2}, agent_capacities={"avi":2, "beni":1}) 
    >>> list(graph.edges.data())
    [(('avi', 0), 'x', {'weight': 5}), (('avi', 0), ('y', 0), {'weight': 4}), (('avi', 0), ('y', 1), {'weight': 4}), ('x', ('avi', 1), {'weight': 5}), ('x', 'beni', {'weight': 2}), (('avi', 1), ('y', 0), {'weight': 4}), (('avi', 1), ('y', 1), {'weight': 4}), (('y', 0), 'beni', {'weight': 3}), (('y', 1), 'beni', {'weight': 3})]

    >>> prefs = AgentList([[5,4],[2,3]])
    >>> graph = instance_to_graph(prefs) 
    >>> list(graph.edges.data())
    [('Agent #0', 0, {'weight': 5}), ('Agent #0', 1, {'weight': 4}), (0, 'Agent #1', {'weight': 2}), (1, 'Agent #1', {'weight': 3})]
    """
    assert isinstance(agents, AgentList)

    # Utility function to get the capacity from a capacity map if it exists:
    def _get_capacity(map_item_to_capacity:Dict[str,int], item:str):
        if map_item_to_capacity is None:
            return 1
        elif item not in map_item_to_capacity:
            return 0
        else:
            return map_item_to_capacity[item]

    graph = networkx.Graph()
    for agent in agents:
        agent_name = agent.name()
        num_of_agent_clones = _get_capacity(agent_capacities, agent_name)
        for item in agent.all_items():
            weight = agent.value(item)
            if agent_weights is not None:
                weight *= agent_weights.get(agent_name,1)
            num_of_item_units = _get_capacity(item_capacities, item)

            if num_of_item_units==1 and num_of_agent_clones==1:
                graph.add_edge(agent_name, item, weight=weight)
            elif num_of_item_units!=1 and num_of_agent_clones==1:
                for unit in range(num_of_item_units):
                    graph.add_edge(agent_name, (item,unit), weight=weight)
            elif num_of_item_units==1 and num_of_agent_clones!=1:
                for clone in range(num_of_agent_clones):
                    graph.add_edge((agent_name,clone), item, weight=weight)
            else:
                for clone in range(num_of_agent_clones):
                    for unit in range(num_of_item_units):
                        graph.add_edge((agent_name,clone), (item,unit), weight=weight)
    return graph



def matching_to_allocation(matching: list, agent_names:list)->Dict[str,str]:
    """
    Converts a one-to-many matching in a bipartite graph (output of networkx) to an allocation (given as a dict)
    :param matching: a list of pairs (agent,item).
    :param agent_names: the names of the agents. Used for distinguishing, in each edge, between the agent and the item (since the edges are not ordered).

    :return a dict, mapping an agent name to its bundle.

    >>> from dicttools import stringify
    >>> matching = [("a", "xxx"), ("yyy", "b"), ("c", "yyy")]
    >>> map_agent_name_to_bundle = matching_to_allocation(matching, ["a","b","c"])
    >>> stringify(map_agent_name_to_bundle)
    "{a:['xxx'], b:['yyy'], c:['yyy']}"
    >>> matching = [("a", ("xxx",0)), ("b", ("xxx",1)), ("c", "yyy")]
    >>> map_agent_name_to_bundle = matching_to_allocation(matching, ["a","b","c"])
    >>> stringify(map_agent_name_to_bundle)
    "{a:['xxx'], b:['xxx'], c:['yyy']}"
    >>> matching = [(("a",0), "xxx"), ("yyy", ("a",1)), ("c", "yyy")]
    >>> map_agent_name_to_bundle = matching_to_allocation(matching, ["a","b","c"])
    >>> stringify(map_agent_name_to_bundle)
    "{a:['xxx', 'yyy'], c:['yyy']}"
    >>> matching = [(("a",0), ("xxx",0)), ("yyy", ("a",1)), ("c", ("xxx",1))]
    >>> map_agent_name_to_bundle = matching_to_allocation(matching, ["a","b","c"])
    >>> stringify(map_agent_name_to_bundle)
    "{a:['xxx', 'yyy'], c:['xxx']}"
    """
    # utility function to remove the unit-index from a tuple representing a single unit of an item or agent
    def _remove_unit_index(id):
        if isinstance(id, tuple):  # when there are several units of the same item or agent...
            return id[0]           # ... 0 is the item/agent, 1 is the unit-number. 
        else:
            return id

    map_agent_name_to_bundle = defaultdict(list)
    for edge in matching:
        edge = (_remove_unit_index(edge[0]), _remove_unit_index(edge[1]))
        if edge[0] in agent_names:  
            (agent,good)=edge
        elif edge[1] in agent_names:
            (good,agent)=edge
        else:
            raise ValueError(f"Cannot find an agent in {edge}")
        map_agent_name_to_bundle[agent].append(good)
    for agent,bundle in map_agent_name_to_bundle.items():
        bundle.sort()
    return map_agent_name_to_bundle
    

if __name__ == "__main__":
    import doctest
    print(doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE))
