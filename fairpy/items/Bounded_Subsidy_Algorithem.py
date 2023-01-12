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

    >>> agents4 = AgentList({"Alice": {"a":3, "b":5}, "Bob": {"a":6, "b":7}})
    >>> print(Bounded_Subsidy(agents4))
    {'Alice': ['b'], 'Bob': ['a']}

    >>> agents5 = AgentList({"Alice": {"a":3, "b":2}, "Bob": {"a":4, "b":1}})
    >>> print(Bounded_Subsidy(agents5))
    {'Alice': ['b'], 'Bob': ['a']}

    >>> agents6 = AgentList([[3,2],[4,1]])
    >>> print(Bounded_Subsidy(agents6))
    {'Agent #0': [1], 'Agent #1': [0]}

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

def maximizes_allocation(agents: Dict[str,Agent], item_list: List[Any]):
   
    """
        
   # Allocate each agent with his highest item that has not been allocated.

    ##### test 1 #####
    >>> Alice = AdditiveAgent({"a": 1, "b": 5, "c": 3}, name="Alice")
    >>> Alice.aq_items = []
    >>> Bob = AdditiveAgent({"a": 1, "b": 3, "c": 2}, name="Bob")
    >>> Bob.aq_items = []
    >>> Eve = AdditiveAgent({"a": 3, "b": 2, "c": 1}, name="Eve")
    >>> Eve.aq_items = []
    >>> agents = {x.name():x for x in [Alice,Bob,Eve]}
    >>> items_list = list('abc')
    >>> maximizes_allocation(agents,items_list)
    >>> [(x.name(),sorted(x.aq_items)) for x in agents.values()]
    [('Alice', ['b']), ('Bob', ['c']), ('Eve', ['a'])]

    ##### test 2 #####
    >>> Alice = AdditiveAgent({"a": 1, "b": 5, "c": 3, "d":2}, name="Alice")
    >>> Alice.aq_items = []
    >>> Bob = AdditiveAgent({"a": 2, "b": 3, "c": 3, "d":1}, name="Bob")
    >>> Bob.aq_items = []
    >>> agents = {x.name():x for x in [Alice,Bob]}
    >>> items_list = list('abcd')
    >>> maximizes_allocation(agents,items_list)
    >>> [(x.name(),sorted(x.aq_items)) for x in agents.values()]
    [('Alice', ['b', 'd']), ('Bob', ['a', 'c'])]

    ##### test 3 #####
    >>> Alice = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6}, name="Alice")
    >>> Alice.aq_items = []
    >>> Bob = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6}, name="Bob")
    >>> Bob.aq_items = []
    >>> Eve = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6}, name="Eve")
    >>> Eve.aq_items = []
    >>> agents = {x.name():x for x in [Alice,Bob,Eve]}
    >>> items_list = list('abcdef')
    >>> maximizes_allocation(agents,items_list)
    >>> [(x.name(),sorted(x.aq_items)) for x in agents.values()]
    [('Alice', ['d', 'e']), ('Bob', ['a', 'f']), ('Eve', ['b', 'c'])]
   
    """

    agents_items = list(agents.items())
    while len(item_list) > 0:
        for name, val in (agents_items):
            max_item = max([x for x in val.valuation.desired_items if x[0] in item_list], key=lambda x: val.value(x))
            item_list.remove(max_item)
            val.aq_items.append(max_item)
        agents_items.reverse()


def create_Envy_Graph(agents: Dict[str, AdditiveAgent]) -> networkx.DiGraph:
    """
    This function creates an Envy Graph of agents, and maximizes the allocation
    for every two nodes representing agent u and v, 
    there will be an edge from u to v if agent u believes agent vs bundle is worth more then his.

    ##### test 1 #####
    >>> Alice = AdditiveAgent({"a": 5}, name="Alice")
    >>> Alice.aq_items = ['a']
    >>> Bob = AdditiveAgent({"a":4}, name="Bob")
    >>> Bob.aq_items = []
    >>> agents = {x.name():x for x in [Alice,Bob]}
    >>> list(create_Envy_Graph(agents).nodes)
    ['Alice', 'Bob']
    >>> list(create_Envy_Graph(agents).edges)
    [('Bob', 'Alice')]

    ##### test 2 #####
    >>> Alice = AdditiveAgent({"a": 1, "b": 5, "c": 3}, name="Alice")
    >>> Alice.aq_items = ['b']
    >>> Bob = AdditiveAgent({"a": 1, "b": 3, "c": 2}, name="Bob")
    >>> Bob.aq_items = ['c']
    >>> Eve = AdditiveAgent({"a": 3, "b": 2, "c": 1}, name="Eve")
    >>> Eve.aq_items = ['a']
    >>> agents = {x.name():x for x in [Alice,Bob,Eve]}
    >>> list(create_Envy_Graph(agents).nodes)
    ['Alice', 'Bob', 'Eve']
    >>> list(create_Envy_Graph(agents).edges)
    [('Bob', 'Alice')]

    ##### test 3 #####
    >>> Alice = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6}, name="Alice")
    >>> Alice.aq_items = ['d', 'e']
    >>> Bob = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6}, name="Bob")
    >>> Bob.aq_items = ['a', 'f']
    >>> Eve = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6}, name="Eve")
    >>> Eve.aq_items = ['b', 'c']
    >>> agents = {x.name():x for x in [Alice,Bob,Eve]}
    >>> list(create_Envy_Graph(agents).nodes)
    ['Alice', 'Bob', 'Eve']
    >>> list(create_Envy_Graph(agents).edges)
    [('Alice', 'Bob'), ('Alice', 'Eve')]

    """
    
    # DiGraph — Directed graphs with self loops
    # its stores nodes and edges with optional data, or attributes.
    # DiGraphs hold directed edges. Self loops are allowed but multiple (parallel) edges are not.
    envy_graph = networkx.DiGraph() 
    for i in agents.values():
        envy_graph.add_node(i.name())
        i_value = i.value(i.aq_items) # values of items of agent "i" from his eyes
        for k in agents.values():
            if i is k:
                continue
            k_value = i.value(k.aq_items) # values of items of agent "k" from eyes of agent "i"
            if k_value > i_value:
                envy_graph.add_edge(i.name(), k.name())
    return envy_graph


def check_positive_weight_directed_cycles(envy_graph: networkx.DiGraph, agents: Dict[str, AdditiveAgent]) -> bool:
    """
    This function checks if its envy graph does not contain a positive-weight directed cycle

    ##### test 1 #####
    >>> Alice = AdditiveAgent({"a": 5, "b": 3}, name="Alice")
    >>> Alice.aq_items = ['b']
    >>> Bob = AdditiveAgent({"a": 3, "b": 5}, name="Bob")
    >>> Bob.aq_items = ['a']
    >>> agents = {x.name():x for x in [Alice,Bob]}
    >>> envy_graph = create_Envy_Graph(agents)
    >>> check_positive_weight_directed_cycles(envy_graph, agents)
    True

    ##### test 2 #####
    >>> Alice = AdditiveAgent({"a": 3, "b": 2, "c": 1}, name="Alice")
    >>> Alice.aq_items = ['b']
    >>> Bob = AdditiveAgent({"a": 2, "b": 2, "c": 3}, name="Bob")
    >>> Bob.aq_items = ['a']
    >>> Eve = AdditiveAgent({"a": 1, "b": 3, "c": 2}, name="Eve")
    >>> Eve.aq_items = ['c']
    >>> agents = {x.name():x for x in [Alice,Bob,Eve]}
    >>> envy_graph = create_Envy_Graph(agents)
    >>> check_positive_weight_directed_cycles(envy_graph, agents)
    True

    ##### test 3 #####
    >>> Alice = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6}, name="Alice")
    >>> Alice.aq_items = ['d', 'e']
    >>> Bob = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6}, name="Bob")
    >>> Bob.aq_items = ['a', 'f']
    >>> Eve = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6}, name="Eve")
    >>> Eve.aq_items = ['b', 'c']
    >>> agents = {x.name():x for x in [Alice,Bob,Eve]}
    >>> envy_graph = create_Envy_Graph(agents)
    >>> check_positive_weight_directed_cycles(envy_graph, agents)
    False
    
    """

    try:
        # The cycle is a list of edges indicating the cyclic path. Orientation of directed edges is controlled
        networkx.find_cycle(envy_graph, orientation="original")
        return True

    except networkx.NetworkXNoCycle:
        return False


def Subsidy_calculation(agents: Dict[str, AdditiveAgent]):
    """
    This function calculates the subsidy

    ##### tets 1 #####
    >>> Alice = AdditiveAgent({"a": 1, "b": 5}, name="Alice")
    >>> Alice.aq_items = []
    >>> Bob = AdditiveAgent({"a": 2, "b": 3}, name="Bob")
    >>> Bob.aq_items = []
    >>> agents = {x.name():x for x in [Alice,Bob]}
    >>> Subsidy_calculation(agents)
    subsidy of: Bob is 1

    ##### tets 2 #####
    >>> Alice = AdditiveAgent({"a": 2, "b": 1}, name="Alice")
    >>> Alice.aq_items = []
    >>> Bob = AdditiveAgent({"a": 4, "b": 2}, name="Bob")
    >>> Bob.aq_items = []
    >>> agents = {x.name():x for x in [Alice,Bob]}
    >>> Subsidy_calculation(agents)
    subsidy of: Bob is 2

    ##### tets 3 #####
    >>> Alice = AdditiveAgent({"a": 1, "b": 5, "c": 3}, name="Alice")
    >>> Alice.aq_items = []
    >>> Bob = AdditiveAgent({"a": 1, "b": 3, "c": 2}, name="Bob")
    >>> Bob.aq_items = []
    >>> Eve = AdditiveAgent({"a": 3, "b": 2, "c": 1}, name="Eve")
    >>> Eve.aq_items = []
    >>> agents = {x.name():x for x in [Alice,Bob,Eve]}
    >>> Subsidy_calculation(agents)
    subsidy of: Bob is 1

    ##### test 4 #####
    >>> Alice = AdditiveAgent({"a":3, "b":4, "c":6}, name="Alice")
    >>> Alice.aq_items = []
    >>> Bob = AdditiveAgent({"a":4, "b":3, "c":1}, name="Bob")
    >>> Bob.aq_items = []
    >>> Eve = AdditiveAgent({"a":4, "b":5, "c":1}, name="Eve")
    >>> Eve.aq_items = []
    >>> agents_dict = {x.name():x for x in [Alice,Bob,Eve]}
    >>> Subsidy_calculation(agents_dict) # no subsidy

    ##### test 5 #####
    >>> Alice = AdditiveAgent({"a": 9, "b": 8, "c": 6, "d": 11, "e": 3, "f": 6}, name="Alice")
    >>> Alice.aq_items = []
    >>> Bob = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 5, "e": 3, "f": 6}, name="Bob")
    >>> Bob.aq_items = []
    >>> Eve = AdditiveAgent({"a": 9, "b": 8, "c": 7, "d": 11, "e": 3, "f": 6}, name="Eve")
    >>> Eve.aq_items = []
    >>> agents_dict = {x.name():x for x in [Alice,Bob,Eve]}
    >>> Subsidy_calculation(agents_dict)
    subsidy of: Alice is 1

    """

    for i in agents.values():
        all_items = list(i.all_items())
        break

    maximizes_allocation(agents, all_items)


    # DiGraph — Directed graphs with self loops
    # its stores nodes and edges with optional data, or attributes.
    # DiGraphs hold directed edges. Self loops are allowed but multiple (parallel) edges are not.
    envy_graph = networkx.DiGraph() 
    for i in agents.values():
        envy_graph.add_node(i.name())
        i_value = i.value(i.aq_items) # values of items of agent "i" from his eyes
        for k in agents.values():
            if i is k:
                continue
            k_value = i.value(k.aq_items) # values of items of agent "k" from eyes of agent "i"
            if k_value > i_value and check_positive_weight_directed_cycles(create_Envy_Graph(agents), agents) == False:
                envy_graph.add_edge(i.name(), k.name())
                print("subsidy of:",i.name(), "is", k_value-i_value)


#### MAIN

if __name__ == "__main__":
    import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)
    (failures, tests) = doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE)
    print("{} failures, {} tests".format(failures, tests))


   
