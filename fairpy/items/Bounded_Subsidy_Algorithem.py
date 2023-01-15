"""
#-----------------------------------------------------
# name of the article: One Dollar Each Eliminates Envy
# authors: J. Brustle, J. Dippel, V.V. Narayan, M. Suzuki and A. Vetta
# link to the article: https://www.researchgate.net/publication/337781386_One_Dollar_Each_Eliminates_Envy

# Programmer: Eyad Amer
# Since : 2022-12
#-----------------------------------------------------
"""

import networkx
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
        Mt = networkx.max_weight_matching(H, maxcardinality=False) # H חשב התאמה משוקללת מקסימלית של .
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
def create_Envy_Graph(agents: AgentList)->networkx.DiGraph():
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
    >>> agents5 = AgentList({"Alice": {"a":1, "b":5, "c":3}, "Bob": {"a":1, "b":3, "c":2}, "Max": {"a":3, "b":2, "c":1}})
    >>> print(Bounded_Subsidy(agents5))
    {'Alice': ['b'], 'Bob': ['c'], 'Max': ['a']}
    >>> print(create_Envy_Graph(agents5))
    DiGraph with 3 nodes and 6 edges
    >>> print(create_Envy_Graph(agents5).nodes)
    ['Alice', 'Bob', 'Max']
    >>> print(create_Envy_Graph(agents5).edges.data())
    [('Alice', 'Bob', {'weight': -2}), ('Alice', 'Max', {'weight': -4}), ('Bob', 'Alice', {'weight': 1}), ('Bob', 'Max', {'weight': -1}), ('Max', 'Alice', {'weight': -1}), ('Max', 'Bob', {'weight': -2})]

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

    """

    # list of all items
    allTheItems = list(agents[0].all_items())
     
    # maximum matching for all the agents
    maximum_matching = Bounded_Subsidy(agents)
   
    # calculate the values of the items that allocate to the agent
    agent_names = list(maximum_matching.keys()) # agent names
    agent_items_allocated = list(maximum_matching.values()) # The items that allocated for the agent
    items_values_for_agent = {} # Dict of the values of the items that allocate to the agent

    # indexes for the loops
    i,j = 0,0
    while i < len(agent_names):
        item_value = 0
        j = 0
        while j < len(allTheItems):
            name = agent_names[i]
            if allTheItems[j] in agent_items_allocated[i]:
                item_value += agents[i].value(allTheItems[j])
            j += 1
            items_values_for_agent[name] = item_value
        i += 1

    # calculate the values of the edges in the Envy Graph
    list_to_create_Envy_Graph = [] # list of values of the edges in the Envy Graph
    list_of_subsidy_value = {} # list of subsidy value

    # index for the loop
    k = 0
    while k < len(agent_names):
        i = 0
        while i < len(items_values_for_agent):
            subsidy_value = 0
            j = 0
            while j < len(allTheItems):
                name = agent_names[i]
                if allTheItems[j] in agent_items_allocated[i]:
                    subsidy_value += agents[k].value(allTheItems[j])
                j += 1
            list_of_subsidy_value[name] = subsidy_value - list(items_values_for_agent.values())[k]
            i += 1
        list_to_create_Envy_Graph.append(list_of_subsidy_value.copy()) 
        k += 1

    # create an empty graph
    envy_graph = networkx.DiGraph() # DiGraph — Directed graphs with self loops

    # create nodes of the Envy Graph
    for name_node in agent_names:
        envy_graph.add_node(name_node)
    
    # create edges to the nodes in the Envy Graph
    i=0
    while i < len(agent_names):
        j=0
        while j < len(list_to_create_Envy_Graph):
            node1 = agent_names[i]
            node2 = list(list_to_create_Envy_Graph[i].keys())[j]
            if node1 is node2:
                j += 1
                continue 
            envy_graph.add_edge(agent_names[i], list(list_to_create_Envy_Graph[i].keys())[j], weight=list(list_to_create_Envy_Graph[i].values())[j])
            j += 1
        i += 1
    
    # ########## show Envy Graph ##########
    # # positions for all nodes - seed for reproducibility
    # pos = networkx.spring_layout(envy_graph, seed=1)

    # # nodes
    # networkx.draw_networkx_nodes(envy_graph, pos, node_size=500)

    # # edges
    # networkx.draw_networkx_edges(envy_graph, pos, connectionstyle="arc3,rad=-0.3")
    # networkx.draw_networkx_edges(envy_graph, pos, alpha=0.5, edge_color="b", style="dashed")

    # # node labels
    # networkx.draw_networkx_labels(envy_graph, pos, font_size=10, font_family="sans-serif")

    # # edge weight labels
    # edge_labels = networkx.get_edge_attributes(envy_graph, "weight")
    # networkx.draw_networkx_edge_labels(envy_graph, pos, edge_labels)

    # ax = plt.gca()
    # ax.margins(0.08)
    # plt.axis("off")
    # plt.tight_layout()
    # plt.show()

    return envy_graph

create_Envy_Graph.logger = logger

def check_positive_weight_directed_cycles(envy_graph: networkx.DiGraph)->bool:
    """
    This function checks if its envy graph does not contain a positive-weight directed cycle

    ###### 2 agens, 2 items ######
    >>> agents1 = AgentList({"Alice": {"a":5, "b":3}, "Bob": {"a":4, "b":1}})
    >>> print(Bounded_Subsidy(agents1))
    {'Alice': ['b'], 'Bob': ['a']}
    >>> envy_graph = create_Envy_Graph(agents1)
    >>> print(envy_graph)
    DiGraph with 2 nodes and 2 edges
    >>> print(envy_graph.nodes)
    ['Alice', 'Bob']
    >>> print(envy_graph.edges.data())
    [('Alice', 'Bob', {'weight': 2}), ('Bob', 'Alice', {'weight': -3})]
    >>> check_positive_weight_directed_cycles(envy_graph)
    False

    ###### 3 agens, 3 items ######
    >>> agents2 = AgentList({"Alice": {"a": 3, "b": 2, "c": 1}, "Bob": {"a": 2, "b": 2, "c": 3}, "Max": {"a": 1, "b": 3, "c": 2}})
    >>> print(Bounded_Subsidy(agents2))
    {'Alice': ['a'], 'Bob': ['c'], 'Max': ['b']}
    >>> envy_graph = create_Envy_Graph(agents2)
    >>> print(envy_graph)
    DiGraph with 3 nodes and 6 edges
    >>> print(envy_graph.nodes)
    ['Alice', 'Bob', 'Max']
    >>> print(envy_graph.edges.data())
    [('Alice', 'Bob', {'weight': -2}), ('Alice', 'Max', {'weight': -1}), ('Bob', 'Alice', {'weight': -1}), ('Bob', 'Max', {'weight': -1}), ('Max', 'Alice', {'weight': -2}), ('Max', 'Bob', {'weight': -1})]
    >>> check_positive_weight_directed_cycles(envy_graph)
    False

    ###### 4 agens, 2 items ######
    >>> agents3 = AgentList({"Alice": {"a":5, "b":6}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
    >>> print(Bounded_Subsidy(agents3))
    {'Alice': ['b'], 'Bob': ['a'], 'Max': [], 'Nancy': []}
    >>> envy_graph = create_Envy_Graph(agents3)
    >>> print(envy_graph)
    DiGraph with 4 nodes and 12 edges
    >>> print(envy_graph.nodes)
    ['Alice', 'Bob', 'Max', 'Nancy']
    >>> print(envy_graph.edges.data())
    [('Alice', 'Bob', {'weight': -1}), ('Alice', 'Max', {'weight': -6}), ('Alice', 'Nancy', {'weight': -6}), ('Bob', 'Alice', {'weight': 1}), ('Bob', 'Max', {'weight': -3}), ('Bob', 'Nancy', {'weight': -3}), ('Max', 'Alice', {'weight': 2}), ('Max', 'Bob', {'weight': 2}), ('Max', 'Nancy', {'weight': 0}), ('Nancy', 'Alice', {'weight': 1}), ('Nancy', 'Bob', {'weight': 2}), ('Nancy', 'Max', {'weight': 0})]
    >>> check_positive_weight_directed_cycles(envy_graph)
    False
    
    """

    nodes = envy_graph.nodes
    edges = envy_graph.edges.data()
    G = networkx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    cycles = networkx.simple_cycles(G)
    weights = networkx.get_edge_attributes(G, 'weight')
    for cycle in cycles:
        cycle.append(cycle[0])
        cycle_weight = sum([weights[(cycle[i-1], cycle[i])] for i in range(1, len(cycle))])
        # print (cycle,cycle_weight)
        if cycle_weight > 0:
            return True

    return False


def cal_the_Subsidy(agents: AgentList):
    """
    This function calculates the Subsidy of the agentes
    ###### 2 agens, 1 items ######
    >>> agents0 = AgentList({"Alice": {"a":5}, "Bob": {"a":4}})
    >>> print(Bounded_Subsidy(agents0))
    {'Alice': ['a'], 'Bob': []}
    >>> print(create_Envy_Graph(agents0).edges.data())
    [('Alice', 'Bob', {'weight': -5}), ('Bob', 'Alice', {'weight': 4})]
    >>> cal_the_Subsidy(agents0)
    Bob is envious of Alice with a subsidy of: 4

    ###### 2 agens, 2 items ######
    >>> agents1 = AgentList({"Alice": {"a":3, "b":5}, "Bob": {"a":6, "b":7}})
    >>> print(Bounded_Subsidy(agents1))
    {'Alice': ['b'], 'Bob': ['a']}
    >>> print(create_Envy_Graph(agents1).edges.data())
    [('Alice', 'Bob', {'weight': -2}), ('Bob', 'Alice', {'weight': 1})]
    >>> cal_the_Subsidy(agents1)
    Bob is envious of Alice with a subsidy of: 1

    ###### 2 agens, 4 items ######
    >>> agents2 = AgentList({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10}})
    >>> print(Bounded_Subsidy(agents2))
    {'Alice': ['b', 'c'], 'Bob': ['d', 'a']}
    >>> print(create_Envy_Graph(agents2).edges.data())
    [('Alice', 'Bob', {'weight': -7}), ('Bob', 'Alice', {'weight': -1})]
    >>> cal_the_Subsidy(agents2)
    There is no envy in this graph

    
    ###### 3 agents, 3 items ######
    >>> agents3 = AgentList({"Alice": {"a":1, "b":5, "c":3}, "Bob": {"a":1, "b":3, "c":2}, "Max": {"a":3, "b":2, "c":1}})
    >>> print(Bounded_Subsidy(agents3))
    {'Alice': ['b'], 'Bob': ['c'], 'Max': ['a']}
    >>> print(create_Envy_Graph(agents3).edges.data())
    [('Alice', 'Bob', {'weight': -2}), ('Alice', 'Max', {'weight': -4}), ('Bob', 'Alice', {'weight': 1}), ('Bob', 'Max', {'weight': -1}), ('Max', 'Alice', {'weight': -1}), ('Max', 'Bob', {'weight': -2})]
    >>> cal_the_Subsidy(agents3)
    Bob is envious of Alice with a subsidy of: 1

    ###### 4 agents, 2 items ######
    >>> agents4 = AgentList({"Alice": {"a":5, "b":6}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
    >>> print(Bounded_Subsidy(agents4))
    {'Alice': ['b'], 'Bob': ['a'], 'Max': [], 'Nancy': []}
    >>> print(create_Envy_Graph(agents4).edges.data())
    [('Alice', 'Bob', {'weight': -1}), ('Alice', 'Max', {'weight': -6}), ('Alice', 'Nancy', {'weight': -6}), ('Bob', 'Alice', {'weight': 1}), ('Bob', 'Max', {'weight': -3}), ('Bob', 'Nancy', {'weight': -3}), ('Max', 'Alice', {'weight': 2}), ('Max', 'Bob', {'weight': 2}), ('Max', 'Nancy', {'weight': 0}), ('Nancy', 'Alice', {'weight': 1}), ('Nancy', 'Bob', {'weight': 2}), ('Nancy', 'Max', {'weight': 0})]
    >>> cal_the_Subsidy(agents4)
    Bob is envious of Alice with a subsidy of: 1
    Max is envious of Alice with a subsidy of: 2
    Max is envious of Bob with a subsidy of: 2
    Nancy is envious of Alice with a subsidy of: 1
    Nancy is envious of Bob with a subsidy of: 2

    """

    envy_graph = create_Envy_Graph(agents) # create Envy Graph

    if check_positive_weight_directed_cycles(envy_graph): # if the graph have a positive cycles
        print("The graph has positive weight directed cycles")
        return

    i=0
    flag = False
    while i < len(envy_graph.edges.data()):
        first_agent = list(envy_graph.edges.data())[i][0]
        second_agent = list(envy_graph.edges.data())[i][1]
        subside = list(list(envy_graph.edges.data())[i][2].values())[0]
        if subside > 0: # יש קנאה
            flag = True
            print(first_agent, "is envious of", second_agent, "with a subsidy of:", subside)
        i += 1

    if flag == False:
        print("There is no envy in this graph")


#### MAIN

if __name__ == "__main__":
    import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)
    (failures, tests) = doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE)
    print("{} failures, {} tests".format(failures, tests))


  
   
