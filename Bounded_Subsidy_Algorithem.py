
"""
#-----------------------------------------------------
# name of the article: One Dollar Each Eliminates Envy
# authors: J. Brustle, J. Dippel, V.V. Narayan, M. Suzuki and A. Vetta
# link to the article: https://www.researchgate.net/publication/337781386_One_Dollar_Each_Eliminates_Envy

# Programmer: Eyad Amer
# Since : 2022-12
#-----------------------------------------------------
"""

import fairpy
import networkx
from typing import *
from fairpy.items.utilitarian_matching import instance_to_graph, matching_to_allocation
from fairpy import AgentList
from dicttools import stringify

import logging
logger = logging.getLogger(__name__)



def Bounded_Subsidy(agents: Dict[str, Dict[str, int]], items: Dict[str,int], weights: Dict[str,int]):
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

    >>> agents1 = ({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10})
    >>> alloc_max_weight_one = iterated_maximum_matching(agents1, items={"a":1,"b":1,"c":1,"d":1})
    >>> stringify(alloc_max_weight_one)
    "{Alice: ['b', 'c'], Bob: ['a', 'd']}"


    >>>  agents2 = ({"Alice": {"a":10, "b":8, "c":5, "d":10, "e":3, "f":0}, "Bob": {"a":9, "b":2, "c":4, "d":7, "e":10, "f":0})
    >>>  alloc_max_weight_one = iterated_maximum_matching(agents2, items={"a":1, "b":1, "c":1, "d":1, "e":1, "f":1})
    >>> stringify(alloc_max_weight_one)
    "{Alice: ['a', 'b', 'c'], Bob: ['d', 'e', 'f']}"

    """ 
    items = None
    weights = None

    listOfAgents = fairpy.agents_from(agents) # list of agents
    NamesOfAgent = fairpy.agent_names_from(agents) # names of agents

    allTheItems = listOfAgents[0].all_items() # list of items
    if items is None:
        items = {item:1 for item in allTheItems} 
    result = {agent.name(): [] for agent in agents} # list for the result

    while len(items) >= 1: # The process ends when every item has been allocated
        # The valuation graph H is the complete bipartite graph on vertex sets I and J, where edge (i, j) has weight vi(j)
        H = instance_to_graph(agents, weights=weights, items=items) 
        logger.info("Graph edges: %s", list(H.edges.data()))
        # a maximum weight matching in H[I, Jt]
        Mt = networkx.max_weight_matching(H, maxcardinality=False)
        logger.info("Matching: %s", Mt)
        # if agent i is matched to item j = µti then we allocate item µti to that agent
        agentsBundle = matching_to_allocation(Mt, agent_names=NamesOfAgent)
        for agent,bundle in agentsBundle.items():
            result[agent] += bundle
        # Remove the given items and recurse on the remaining items
        allocated_items = sum([bundle for bundle in agentsBundle.values()], []) # the number of the items that allocated to the agents
        items = delete_items(items, allocated_items) # delete_items

    return result

Bounded_Subsidy.logger = logger


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

    for item,newSize in items.items():
        if newSize > 0:
            return {item:newSize}


# Main Function
if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True,optionflags=doctest.NORMALIZE_WHITESPACE)
    print("{} failures, {} tests".format(failures, tests))