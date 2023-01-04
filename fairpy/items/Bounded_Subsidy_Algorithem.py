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
from fairpy import AdditiveAgent

import logging
logger = logging.getLogger(__name__)


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


def allocate_items_with_Subsidy(agents: AgentList, items: Dict[str,int]=None, weights: Dict[str, int]=None):
    """
    The algorithm getting a list of agents, list of goods and array of the weights of the goods
    and it returns a bundle of agents each holding the best allocation for their own valuation,
    with the subsidy that eliminates envy

    >>> agents1 = AgentList({"Alice": {"a":3, "b":5}, "Bob": {"a":6, "b":7}})
    >>> allocate_items_with_Subsidy(agents1)
    Alice gets ['b'] ,Bob gets ['a'] and subsidy of 1

    >>> agents2 = AgentList({"Alice": {"a":3, "b":2}, "Bob": {"a":4, "b":1}})
    >>> allocate_items_with_Subsidy(agents2)
    Alice gets ['b'] and subsidy of 1 ,Bob gets ['a']

    >>> agents3 = AgentList({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10}})
    >>> allocate_items_with_Subsidy(agents3)
    Alice gets ['b', 'c'] ,Bob gets ['d', 'a'] .No subsidy

    >>> agents4 = AgentList({"Alice": {"a":10, "b":8, "c":5, "d":9, "e":3, "f":0}, "Bob": {"a":9, "b":2, "c":4, "d":7, "e":10, "f":1}})
    >>> allocate_items_with_Subsidy(agents4)
    Alice gets ['a', 'b', 'c'] ,Bob gets ['e', 'd', 'f'] .No subsidy

    """


    assert isinstance(agents, AgentList)
    allTheItems = agents[0].all_items() # list of all items

    sum_of_all_values_Alice = agents[0].value(list(allTheItems))
    sum_of_all_values_bob = agents[1].value(list(allTheItems))

    if items is None:
        items = {item:1 for item in allTheItems}
    result = {agent.name(): [] for agent in agents} # empty list for the result => {agent.name: ['item.name']}
    # print(allTheItems)
    
    sum_Alice = 0
    sum_Bob = 0

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
        agent1 = (list(agentsBundle.keys())[0])
        # agent2 = (list(agentsBundle.keys())[1])
        
        Alice = agents[0].name()
        # Bob = agents[1].name()

        for agent_name,item_name in agentsBundle.items():
            result[agent_name] += item_name
            
        # The items that allocated to the agents in this round
        allocated_items = sum([item for item in agentsBundle.values()], []) 

        if(agent1 == Alice):
            sum_Alice += agents[0].value(allocated_items[0])
            sum_Bob += agents[1].value(allocated_items[1])
        else:
            sum_Alice += agents[0].value(allocated_items[1])
            sum_Bob += agents[1].value(allocated_items[0])
        
        # Remove the allocated items and recurse on the remaining items
        items = delete_items(items, allocated_items) # delete_items
    
    # subsid value 
    subsid_alice = ((2 * sum_Alice)-sum_of_all_values_Alice) 
    subsid_Bob = ((2 * sum_Bob)-sum_of_all_values_bob)

    if (subsid_alice < 0):
        print("Alice gets", list(result.values())[0], "and subsidy of",subsid_alice*-1, ",Bob gets", list(result.values())[1])
    elif (subsid_Bob < 0):
        print("Alice gets", list(result.values())[0], ",Bob gets", list(result.values())[1],"and subsidy of",subsid_Bob*-1)
    else:
        print("Alice gets", list(result.values())[0], ",Bob gets", list(result.values())[1],".No subsidy")

allocate_items_with_Subsidy.logger = logger


def delete_items(items:Dict[str,int], items_to_remove:List)->Dict[str,int]:
    """
    # This is help function that Remove the given items from the graph

    >>> stringify(delete_items({"a":4, "b":10, "c":8, "d":7}, ["a","b","d"]))
    '{a:3, b:9, c:8, d:6}'

    >>> stringify(delete_items({"a":9, "b":2, "c":4, "d":7, "e":10, "f":0}, ["b","c"]))
    '{a:9, b:1, c:3, d:7, e:10}'

    >>> stringify(delete_items({"a":1, "b":2, "c":1}, ["a", "b", "c"]))
    '{b:1}'
    """
    for i in items_to_remove:
        items[i] -= 1

    return {item:newSize for item,newSize in items.items() if newSize > 0}



#### MAIN

if __name__ == "__main__":
    # import sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)
    (failures, tests) = doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE)
    print("{} failures, {} tests".format(failures, tests))
    # agents4 = AgentList({"Alice": {"a":3, "b":5}, "Bob": {"a":6, "b":7}})
    # agents1 = AgentList({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10}})
    # agents5 = AgentList({"Alice": {"a":3, "b":2}, "Bob": {"a":4, "b":1}})
    # agents2 = AgentList({"Alice": {"a":10, "b":8, "c":5, "d":9, "e":3, "f":0}, "Bob": {"a":9, "b":2, "c":4, "d":7, "e":10, "f":1}})

    # Bounded_Subsidy(agents1)
    # allocate_items_with_Subsidy(agents2)
