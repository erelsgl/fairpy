"""
#-----------------------------------------------------
# name of the article: One Dollar Each Eliminates Envy
# authors: J. Brustle, J. Dippel, V.V. Narayan, M. Suzuki and A. Vetta
# link to the article: https://www.researchgate.net/publication/337781386_One_Dollar_Each_Eliminates_Envy

# Programmer: Eyad Amer
# Since : 2022-12
#-----------------------------------------------------
"""

import networkx as nx
import sys
import doctest
from typing import *

from fairpy import AgentList
from fairpy.items.utilitarian_matching import instance_to_graph, matching_to_allocation
from fairpy.agents import Agent, AdditiveAgent
import numpy as np

import matplotlib.pyplot as plt


import logging
logger = logging.getLogger(__name__)

##### algorithm 1 #####
def Bounded_Subsidy(agents: AgentList, items: Dict[str,int]=None, weights: Dict[str, int]=None):
    """
    The algorithm getting a list of agents, list of goods and array of the weights of the goods
    and it's returns a bundle of agents when each of the holds the best allocation to his valuation of the goods.

    Algorithem bounded_subsidy:
    --------------------------------------------------------------------------
    * I = {1, 2, . . . , n} => set of agents
    * J = {J1, J2, . . . , Jm} => set of  indivisible goods (items)
    * A = {A1, . . . , An}  => An allocation is an ordered partition of the set of items into n bundles. (The task is to construct an envy-freeable allocation A with maximum path weight 1 in the envy graph GA)
    * vi => Each agent i ∈ I has a valuation function vi over the set of items.
    * H[I, Jt] =>  The valuation graph H is the complete bipartite graph on vertex sets I and J, where edge (i, j) has weight vi(j).
    * Mt => a maximum-weight matching in H[I, Jt].
    * µti => If agent i is matched to item j = µti then we allocate item µti to that agent.


    Ai ← ∅ for all i ∈ I;
    t ← 1; J1 ← J; // For the first round, we set J1 = J
    while Jt != ∅ do: //  The process ends when every item has been allocated
        Compute a maximum-weight matching Mt = {(i, µti)}i∈I in H[I, Jt]; // we find a maximum-weight matching Mt in H[I, Jt]
        Set Ai ← Ai ∪ {µti} for all i ∈ I; //  If agent i is matched to item j = µti then we allocate item µti to that agent
        Set Jt+1 ← Jt \ ∪i∈I{µti}; // We recurse on the remaining items
        t ← t + 1;
    end
    ----------------------------------------------------------------------------
                                     Tests
    ----------------------------------------------------------------------------
    >>> agents1 = AgentList({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10}})
    >>> print(Bounded_Subsidy(agents1))
    {'Alice': ['b', 'c'], 'Bob': ['d', 'a']}

    >>> agents2 = AgentList({"Alice": {"a":10, "b":8, "c":5, "d":9, "e":3, "f":0}, "Bob": {"a":9, "b":2, "c":4, "d":7, "e":10, "f":0}})
    >>> alloc_max_weight_one = Bounded_Subsidy(agents2, items={"a":1, "b":1, "c":1, "d":1, "e":1, "f":1})
    >>> print(alloc_max_weight_one)
    {'Alice': ['a', 'b', 'c'], 'Bob': ['e', 'd', 'f']}

    >>> agents3 = AgentList([[5,4,3,2],[2,3,4,5]])
    >>> print(Bounded_Subsidy(agents3))
    {'Agent #0': [0, 1], 'Agent #1': [3, 2]}

    >>> agents4 = AgentList({"Alice": {"a":3, "b":6}, "Bob": {"a":5, "b":7}})
    >>> print(Bounded_Subsidy(agents4))
    {'Alice': ['b'], 'Bob': ['a']}

    >>> agents5 = AgentList({"Alice": {"a":3, "b":2}, "Bob": {"a":4, "b":1}})
    >>> print(Bounded_Subsidy(agents5))
    {'Alice': ['b'], 'Bob': ['a']}

    >>> agents6 = AgentList([[3,2],[4,1]])
    >>> print(Bounded_Subsidy(agents6))
    {'Agent #0': [1], 'Agent #1': [0]}

    >>> agents7 = AgentList({"Alice": {"a":5, "b":5}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
    >>> print(Bounded_Subsidy(agents7))
    {'Alice': ['a'], 'Bob': ['b'], 'Max': [], 'Nancy': []}

    """
    assert isinstance(agents, AgentList)
    allTheItems = agents[0].all_items() # list of all items
    if items is None:
        items = {item:1 for item in allTheItems}
    result = {agent.name(): [] for agent in agents} # empty list for the result => {agent.name: ['item.name']}
    # print(allTheItems)
    
    while len(items) > 0: # The process ends when every item has been allocated
        # The valuation graph H is the complete bipartite graph on vertex sets I and J, where edge (i, j) has weight vi(j)
        H = instance_to_graph(agents, agent_weights=weights, item_capacities=items) 
        # print(H)
        logger.info("Graph edges: %s", list(H.edges.data()))
        # a maximum weight matching in H[I, Jt]
        Mt = nx.max_weight_matching(H, maxcardinality=False) # H חשב התאמה משוקללת מקסימלית של .
        # print(Mt)
        logger.info("Matching: %s", Mt)
        # if agent i is matched to item j = µti then we allocate item µti to that agent
        agentsBundle = matching_to_allocation(Mt, agent_names=agents.agent_names()) # ממירה התאמה של אחד לרבים בגרף דו-חלקי
        # print(agentsBundle)
        for agent_name,item_name in agentsBundle.items():
            result[agent_name] += item_name
            # print(agent_name, item_name)
        # print(result)
        # The items that allocated to the agents in this round
        allocated_items = sum([item for item in agentsBundle.values()], []) 
        # print(allocated_items)
        # Remove the allocated items and recurse on the remaining items
        items = delete_items(items, allocated_items) # delete_items
    
    return result

Bounded_Subsidy.logger = logger

# helping function for algorithm 1
def delete_items(items:Dict[str,int], items_to_remove:List)->Dict[str,int]:
    """
    # This is help function that Remove the given items from the graph

    >>> print(delete_items({"a":4, "b":10, "c":8, "d":7}, ["a","b","d"]))
    {'a': 3, 'b': 9, 'c': 8, 'd': 6}

    >>> print(delete_items({"a":9, "b":2, "c":4, "d":7, "e":10, "f":0}, ["b","c"]))
    {'a': 9, 'b': 1, 'c': 3, 'd': 7, 'e': 10}

    >>> print(delete_items({"a":1, "b":2, "c":1}, ["a", "b", "c"]))
    {'b': 1}
    """
    for i in items_to_remove:
        items[i] -= 1

    return {item:newSize for item,newSize in items.items() if newSize > 0}

##### algorithm 2 #####
def create_Envy_Graph(agents: AgentList) -> nx.DiGraph():

    """
    The algorithm getting a Dict of agents, with Dict of goods and the weights of the goods
    and it returns an Envy Graph with maximum matching allocated

    ###### 2 agens, 1 items ######
    >>> agents0 = AgentList({"Alice": {"a":5}, "Bob": {"a":4}})
    >>> print(Bounded_Subsidy(agents0))
    {'Alice': ['a'], 'Bob': []}
    >>> print(create_Envy_Graph(agents0))
    DiGraph with 2 nodes and 2 edges
    >>> print(create_Envy_Graph(agents0).nodes)
    ['Alice', 'Bob']
    >>> print(create_Envy_Graph(agents0).edges.data())
    [('Alice', 'Bob', {'weight': -5}), ('Bob', 'Alice', {'weight': 4})]

    ###### 2 agens, 2 items ######
    >>> agents1 = AgentList({"Alice": {"a":3, "b":5}, "Bob": {"a":6, "b":7}})
    >>> print(Bounded_Subsidy(agents1))
    {'Alice': ['b'], 'Bob': ['a']}
    >>> print(create_Envy_Graph(agents1))
    DiGraph with 2 nodes and 2 edges
    >>> print(create_Envy_Graph(agents1).nodes)
    ['Alice', 'Bob']
    >>> print(create_Envy_Graph(agents1).edges.data())
    [('Alice', 'Bob', {'weight': -2}), ('Bob', 'Alice', {'weight': 1})]

    ###### 2 agens, 4 items ######
    >>> agents2 = AgentList({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10}})
    >>> print(Bounded_Subsidy(agents2))
    {'Alice': ['b', 'c'], 'Bob': ['d', 'a']}
    >>> print(create_Envy_Graph(agents2))
    DiGraph with 2 nodes and 2 edges
    >>> print(create_Envy_Graph(agents2).nodes)
    ['Alice', 'Bob']
    >>> print(create_Envy_Graph(agents2).edges.data())
    [('Alice', 'Bob', {'weight': -7}), ('Bob', 'Alice', {'weight': -1})]

    ###### 2 agens, 6 items ######
    >>> agents3 = AgentList({"Alice": {"a":10, "b":8, "c":5, "d":9, "e":3, "f":0}, "Bob": {"a":9, "b":2, "c":4, "d":7, "e":10, "f":1}})
    >>> print(Bounded_Subsidy(agents3))
    {'Alice': ['a', 'b', 'c'], 'Bob': ['e', 'd', 'f']}
    >>> print(create_Envy_Graph(agents3))
    DiGraph with 2 nodes and 2 edges
    >>> print(create_Envy_Graph(agents3).nodes)
    ['Alice', 'Bob']
    >>> print(create_Envy_Graph(agents3).edges.data())
    [('Alice', 'Bob', {'weight': -11}), ('Bob', 'Alice', {'weight': -3})]

    ###### 3 agents, 3 items ######
    >>> agents4 = AgentList({"Alice": {"a":3, "b":4, "c":6}, "Bob": {"a":4, "b":3, "c":1}, "Max": {"a":4, "b":5, "c":1}})
    >>> print(Bounded_Subsidy(agents4))
    {'Alice': ['c'], 'Bob': ['a'], 'Max': ['b']}
    >>> print(create_Envy_Graph(agents4))
    DiGraph with 3 nodes and 6 edges
    >>> print(create_Envy_Graph(agents4).nodes)
    ['Alice', 'Bob', 'Max']
    >>> print(create_Envy_Graph(agents4).edges.data())
    [('Alice', 'Bob', {'weight': -3}), ('Alice', 'Max', {'weight': -2}), ('Bob', 'Alice', {'weight': -3}), ('Bob', 'Max', {'weight': -1}), ('Max', 'Alice', {'weight': -4}), ('Max', 'Bob', {'weight': -1})]

    ###### 3 agents, 3 items ######
    >>> agents5 = AgentList({"Alice": {"a":1, "b":5, "c":3}, "Bob": {"a":2, "b":3, "c":2}, "Max": {"a":3, "b":4, "c":3}})
    >>> print(Bounded_Subsidy(agents5))
    {'Alice': ['b'], 'Bob': ['a'], 'Max': ['c']}
    >>> print(create_Envy_Graph(agents5))
    DiGraph with 3 nodes and 6 edges
    >>> print(create_Envy_Graph(agents5).nodes)
    ['Alice', 'Bob', 'Max']
    >>> print(create_Envy_Graph(agents5).edges.data())
    [('Alice', 'Bob', {'weight': -4}), ('Alice', 'Max', {'weight': -2}), ('Bob', 'Alice', {'weight': 1}), ('Bob', 'Max', {'weight': 0}), ('Max', 'Alice', {'weight': 1}), ('Max', 'Bob', {'weight': 0})]

    ###### 4 agents, 2 items ######
    >>> agents6 = AgentList({"Alice": {"a":5, "b":6}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
    >>> print(Bounded_Subsidy(agents6))
    {'Alice': ['b'], 'Bob': ['a'], 'Max': [], 'Nancy': []}
    >>> print(create_Envy_Graph(agents6))
    DiGraph with 4 nodes and 12 edges
    >>> print(create_Envy_Graph(agents6).nodes)
    ['Alice', 'Bob', 'Max', 'Nancy']
    >>> print(create_Envy_Graph(agents6).edges.data())
    [('Alice', 'Bob', {'weight': -1}), ('Alice', 'Max', {'weight': -6}), ('Alice', 'Nancy', {'weight': -6}), ('Bob', 'Alice', {'weight': 1}), ('Bob', 'Max', {'weight': -3}), ('Bob', 'Nancy', {'weight': -3}), ('Max', 'Alice', {'weight': 2}), ('Max', 'Bob', {'weight': 2}), ('Max', 'Nancy', {'weight': 0}), ('Nancy', 'Alice', {'weight': 1}), ('Nancy', 'Bob', {'weight': 2}), ('Nancy', 'Max', {'weight': 0})]

    ###### 5 agents, 3 items ######
    >>> agents7 = AgentList({"Alice": {"a":3, "b":5, "c":8}, "Bob": {"a":3, "b":10, "c":5}, "Max": {"a":1, "b":2, "c":10}, "Nancy": {"a":10, "b":10, "c":10}, "Eve": {"a":8, "b":7, "c":2}})
    >>> print(Bounded_Subsidy(agents7))
    {'Alice': [], 'Bob': ['b'], 'Max': ['c'], 'Nancy': ['a'], 'Eve': []}
    >>> print(create_Envy_Graph(agents7))
    DiGraph with 5 nodes and 20 edges
    >>> print(create_Envy_Graph(agents7).nodes)
    ['Alice', 'Bob', 'Max', 'Nancy', 'Eve']
    >>> print(create_Envy_Graph(agents7).edges.data())
    [('Alice', 'Bob', {'weight': 5}), ('Alice', 'Max', {'weight': 8}), ('Alice', 'Nancy', {'weight': 3}), ('Alice', 'Eve', {'weight': 0}), ('Bob', 'Alice', {'weight': -10}), ('Bob', 'Max', {'weight': -5}), ('Bob', 'Nancy', {'weight': -7}), ('Bob', 'Eve', {'weight': -10}), ('Max', 'Alice', {'weight': -10}), ('Max', 'Bob', {'weight': -8}), ('Max', 'Nancy', {'weight': -9}), ('Max', 'Eve', {'weight': -10}), ('Nancy', 'Alice', {'weight': -10}), ('Nancy', 'Bob', {'weight': 0}), ('Nancy', 'Max', {'weight': 0}), ('Nancy', 'Eve', {'weight': -10}), ('Eve', 'Alice', {'weight': 0}), ('Eve', 'Bob', {'weight': 7}), ('Eve', 'Max', {'weight': 2}), ('Eve', 'Nancy', {'weight': 8})]
    """

    # maximum matching for all the agents
    maximum_matching = Bounded_Subsidy(agents) 

    # The items that allocated for the agent
    agent_items_allocated = list(maximum_matching.values()) 

    # create an empty graph
    envy_graph = nx.DiGraph() # DiGraph — Directed graphs with self loops

    # create the nodes of the Envy Graph
    for agent_name in agents:
        envy_graph.add_node(agent_name.name())

    # create edges to the nodes in the Envy Graph
    for i,agent_i in enumerate(agents): 
        for k, agent_k in enumerate(agents):
            if agent_i.name() is agent_k.name():
                continue 
            # For any pair of agents i, k ∈ I the weight of arc (i, k) in GA is the envy agent i has for agent k under the allocation A, that is, wA(i, k) = vi(Ak) − vi(Ai).
            envy_graph.add_edge(agent_i.name(), agent_k.name(), weight=(agent_i.value(agent_items_allocated[k])) - agent_i.value(agent_items_allocated[i]))    

    return envy_graph


def check_positive_weight_directed_cycles(envy_graph: nx.DiGraph) -> bool:
    """
    This function checks if its envy graph does not contain a positive-weight directed cycle

    ###### 2 nodes, 1 edges ######
    >>> G = nx.DiGraph()
    >>> G.add_edge(1, 2, weight=3)
    >>> check_positive_weight_directed_cycles(G)
    False

    ###### 2 nodes, 2 edges ######
    >>> G = nx.DiGraph()
    >>> G.add_edge(1, 2, weight=3)
    >>> G.add_edge(2, 1, weight=-2)
    >>> check_positive_weight_directed_cycles(G)
    True

    ###### 3 nodes, 3 edges ######
    >>> G = nx.DiGraph()
    >>> G.add_edge(1, 3, weight=3)
    >>> G.add_edge(3, 2, weight=2)
    >>> G.add_edge(2, 1, weight=-6)
    >>> check_positive_weight_directed_cycles(G)
    False

    ###### 4 nodes, 4 edges ######
    >>> G = nx.DiGraph()
    >>> G.add_edge(1, 2, weight=1)
    >>> G.add_edge(2, 3, weight=-1)
    >>> G.add_edge(3, 4, weight=1)
    >>> G.add_edge(4, 1, weight=-1)
    >>> check_positive_weight_directed_cycles(G)
    False

    ###### 4 nodes, 5 edges ######
    >>> G = nx.DiGraph()
    >>> G.add_edge(2, 1, weight=4)
    >>> G.add_edge(1, 3, weight=-2)
    >>> G.add_edge(2, 3, weight=3)
    >>> G.add_edge(3, 4, weight=2)
    >>> G.add_edge(4, 2, weight=-1)
    >>> check_positive_weight_directed_cycles(G)
    True

    """

    # copy_envy_graph = envy_graph.copy() # copy the original graph
    nodes = envy_graph.nodes # nodes
    edges = envy_graph.edges.data() # edges

    # multiply by -1 for all the edges
    for edge in edges:
        edge[2]['weight'] *= -1  

    envy_graph.add_nodes_from(nodes) # add nodes to the graph
    envy_graph.add_edges_from(edges) # add edges to the graph
    
    try:
        nx.find_negative_cycle(envy_graph,list(nodes)[0])
        return True

    except nx.NetworkXError:
        return False


def calculate_the_Subsidy(envy_graph: nx.DiGraph) -> list:
    """
    This function calculates the Subsidy of the agentes

    ###### 2 agens, 1 items ######
    >>> agents0 = AgentList({"Alice": {"a":5}, "Bob": {"a":4}})
    >>> print(Bounded_Subsidy(agents0))
    {'Alice': ['a'], 'Bob': []}
    >>> envy_graph = create_Envy_Graph(agents0)
    >>> print(envy_graph.edges.data())
    [('Alice', 'Bob', {'weight': -5}), ('Bob', 'Alice', {'weight': 4})]
    >>> print(calculate_the_Subsidy(envy_graph))
    [0, 4]

    ###### 2 agens, 2 items ######
    >>> agents1 = AgentList({"Alice": {"a":3, "b":5}, "Bob": {"a":6, "b":7}})
    >>> print(Bounded_Subsidy(agents1))
    {'Alice': ['b'], 'Bob': ['a']}
    >>> print(create_Envy_Graph(agents1).edges.data())
    [('Alice', 'Bob', {'weight': -2}), ('Bob', 'Alice', {'weight': 1})]
    >>> print(calculate_the_Subsidy(create_Envy_Graph(agents1)))
    [0, 1]

    ###### 2 agens, 4 items ######
    >>> agents2 = AgentList({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10}})
    >>> print(Bounded_Subsidy(agents2))
    {'Alice': ['b', 'c'], 'Bob': ['d', 'a']}
    >>> print(create_Envy_Graph(agents2).edges.data())
    [('Alice', 'Bob', {'weight': -7}), ('Bob', 'Alice', {'weight': -1})]
    >>> print(calculate_the_Subsidy(create_Envy_Graph(agents2)))
    [0, 0]

    ###### 3 agents, 3 items ######
    >>> agents3 = AgentList({"Alice": {"a":1, "b":5, "c":3}, "Bob": {"a":1, "b":3, "c":2}, "Max": {"a":3, "b":2, "c":1}})
    >>> print(Bounded_Subsidy(agents3))
    {'Alice': ['b'], 'Bob': ['c'], 'Max': ['a']}
    >>> print(create_Envy_Graph(agents3).edges.data())
    [('Alice', 'Bob', {'weight': -2}), ('Alice', 'Max', {'weight': -4}), ('Bob', 'Alice', {'weight': 1}), ('Bob', 'Max', {'weight': -1}), ('Max', 'Alice', {'weight': -1}), ('Max', 'Bob', {'weight': -2})]
    >>> print(calculate_the_Subsidy(create_Envy_Graph(agents3)))
    [0, 1, 0]

    ###### 4 agents, 2 items ######
    >>> agents4 = AgentList({"Alice": {"a":5, "b":6}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
    >>> print(Bounded_Subsidy(agents4))
    {'Alice': ['b'], 'Bob': ['a'], 'Max': [], 'Nancy': []}
    >>> print(create_Envy_Graph(agents4).edges.data())
    [('Alice', 'Bob', {'weight': -1}), ('Alice', 'Max', {'weight': -6}), ('Alice', 'Nancy', {'weight': -6}), ('Bob', 'Alice', {'weight': 1}), ('Bob', 'Max', {'weight': -3}), ('Bob', 'Nancy', {'weight': -3}), ('Max', 'Alice', {'weight': 2}), ('Max', 'Bob', {'weight': 2}), ('Max', 'Nancy', {'weight': 0}), ('Nancy', 'Alice', {'weight': 1}), ('Nancy', 'Bob', {'weight': 2}), ('Nancy', 'Max', {'weight': 0})]
    >>> print(calculate_the_Subsidy(create_Envy_Graph(agents4)))
    [0, 1, 3, 3]

    ###### 4 agents, 4 items ######
    >>> agents5 = AgentList({"Alice": {"a":4, "b":3, "c":2, "d":1}, "Bob": {"a":4, "b":3, "c":2, "d":1}, "Max": {"a":4, "b":3, "c":2, "d":1}, "Nancy": {"a":4, "b":3, "c":2, "d":1}})
    >>> print(Bounded_Subsidy(agents5))
    {'Alice': ['d'], 'Bob': ['c'], 'Max': ['b'], 'Nancy': ['a']}
    >>> print(create_Envy_Graph(agents5).edges.data())
    [('Alice', 'Bob', {'weight': 1}), ('Alice', 'Max', {'weight': 2}), ('Alice', 'Nancy', {'weight': 3}), ('Bob', 'Alice', {'weight': -1}), ('Bob', 'Max', {'weight': 1}), ('Bob', 'Nancy', {'weight': 2}), ('Max', 'Alice', {'weight': -2}), ('Max', 'Bob', {'weight': -1}), ('Max', 'Nancy', {'weight': 1}), ('Nancy', 'Alice', {'weight': -3}), ('Nancy', 'Bob', {'weight': -2}), ('Nancy', 'Max', {'weight': -1})]
    >>> print(calculate_the_Subsidy(create_Envy_Graph(agents5)))
    [3, 2, 1, 0]

    """

    subsedy_list = [] # list of the values of the subsudy of the agents in order 
    nodes = envy_graph.nodes # nodes

    if check_positive_weight_directed_cycles(envy_graph): # if the graph have a positive cycles
        logger.info("The graph has positive weight directed cycles") 
        return

    for node in nodes:
        p = nx.single_source_bellman_ford(envy_graph, source=node, weight='weight') # Compute shortest path length and predecessors on shortest paths in weighted graphs. O(V*E)
        path_weight = list(p[0].values()) # The weight of the path
        path_nodes = list(p[1].values()) # The nodes of the path

        min_path_weight = path_weight[0] # min path weight
        min_path_nodes = path_nodes[0] # min path nodes
        for i in range(1, len(p[0])): # search of shortest path of all targets node
            if path_weight[i] < min_path_weight:
                min_path_weight = path_weight[i]
                min_path_nodes = path_nodes[i]

        logger.info("maximum path: %s", (str(min_path_nodes) + " ==> " + str(min_path_weight*(-1))))
        subsedy_list.append(min_path_weight*(-1))

    return subsedy_list

calculate_the_Subsidy.logger = logger

def print_results(agents: AgentList):
    """
    This is the main function, it's received an Agent List and print the result

    ###### 2 agens, 1 items ######
    >>> agents0 = AgentList({"Alice": {"a":5}, "Bob": {"a":4}})
    >>> print_results(agents0)
    Alice gets ['a'] with Subsudy of: 0
    Bob gets [] with Subsudy of: 4

    ###### 2 agens, 2 items ######
    >>> agents1 = AgentList({"Alice": {"a":3, "b":5}, "Bob": {"a":6, "b":7}})
    >>> print_results(agents1)
    Alice gets ['b'] with Subsudy of: 0
    Bob gets ['a'] with Subsudy of: 1

    ###### 2 agens, 4 items ######
    >>> agents2 = AgentList({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10}})
    >>> print_results(agents2)
    Alice gets ['b', 'c'] with Subsudy of: 0
    Bob gets ['d', 'a'] with Subsudy of: 0

    ###### 3 agents, 3 items ######
    >>> agents3 = AgentList({"Alice": {"a":1, "b":5, "c":3}, "Bob": {"a":1, "b":3, "c":2}, "Max": {"a":3, "b":2, "c":1}})
    >>> print_results(agents3)
    Alice gets ['b'] with Subsudy of: 0
    Bob gets ['c'] with Subsudy of: 1
    Max gets ['a'] with Subsudy of: 0

    ###### 4 agents, 2 items ######
    >>> agents4 = AgentList({"Alice": {"a":5, "b":6}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
    >>> print_results(agents4)
    Alice gets ['b'] with Subsudy of: 0
    Bob gets ['a'] with Subsudy of: 1
    Max gets [] with Subsudy of: 3
    Nancy gets [] with Subsudy of: 3

    ###### 4 agents, 4 items ######
    >>> agents5 = AgentList({"Alice": {"a":4, "b":3, "c":2, "d":1}, "Bob": {"a":4, "b":3, "c":2, "d":1}, "Max": {"a":4, "b":3, "c":2, "d":1}, "Nancy": {"a":4, "b":3, "c":2, "d":1}})
    >>> print_results(agents5)
    Alice gets ['d'] with Subsudy of: 3
    Bob gets ['c'] with Subsudy of: 2
    Max gets ['b'] with Subsudy of: 1
    Nancy gets ['a'] with Subsudy of: 0
    
    """
    # list of the items that allocated to the agents
    items = list(Bounded_Subsidy(agents).values()) 

    # create Envy Graph
    envy_graph = create_Envy_Graph(agents)

    # calculate the Subsidy
    subsidy = calculate_the_Subsidy(envy_graph)

    # print the results
    for index,agent in enumerate(agents):
        print(str(agent.name()) + " gets " + str(items[index]) + " with Subsudy of: " + str(subsidy[index]))
    

#### MAIN

if __name__ == "__main__":
    import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)
    (failures, tests) = doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE)
    print("{} failures, {} tests".format(failures, tests))

    
