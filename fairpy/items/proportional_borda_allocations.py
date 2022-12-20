#!python3
"""
The "Proportional Borda Allocations" algorithm for item allocation.

Authors: Andreas Darmann and Christian Klamler. See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5075029/
Publishing the article: 2016

Programmer: Shlomo Glick
Since:  2022-12
"""

from fairpy import AgentList
from fairpy.allocations import Allocation
from typing import List, Tuple
import networkx as nx

agents_to_test_0 = AgentList({"Shlomo": {"A": 0, "B": 1, "C": 2, "D": 3},"Shira": {"A": 2, "B": 0, "C": 1, "D": 3},"Hadar": {"A": 2, "B": 0, "C": 1, "D": 3},"Or": {"A": 3, "B": 2, "C": 1, "D": 0}})
def proportional_division_equal_number_of_items_and_players(agents: AgentList) -> Allocation:
    """
    Proposition 2 from "Proportional Borda Allocations":
    Finds a proportional division for the items 
    
    :param agents: represents the n agents.
    :param items: n the items that are allocated.
    :return: the proportional allocation, or none if no proportional allocation exists.
    Notes: 
        1. len(items) must be equal to len(agents)
        2. Valuation of agents is defined by "Borda scores" see https://en.wikipedia.org/wiki/Borda_count

    >>> proportional_division_equal_number_of_items_and_players(agents=agents_to_test_0).map_agent_to_bundle()
    {'Shlomo': ['C'], 'Shira': ['D'], 'Hadar': ['A'], 'Or': ['B']}
    >>> proportional_division_equal_number_of_items_and_players(agents=AgentList([[1,3,2,0],[3,2,1,0],[3,2,1,0],[0,1,3,2]])).map_agent_to_bundle()
    {'Agent #0': [2], 'Agent #1': [1], 'Agent #2': [0], 'Agent #3': [3]}
    >>> proportional_division_equal_number_of_items_and_players(agents=AgentList([[1,0],[0,1]])).map_agent_to_bundle()
    {'Agent #0': [0], 'Agent #1': [1]}
    >>> proportional_division_equal_number_of_items_and_players(agents=AgentList([[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3]])) is None
    True
    >>> proportional_division_equal_number_of_items_and_players(agents=AgentList([[0]])).map_agent_to_bundle()
    {'Agent #0': [0]}
    """
    if not isBordaCount(agents):
        raise ValueError(f'Evaluation of items by the agents must be defined by "Board scores". but it is not')
    items = list(agents.all_items())
    k = len(items)
    if k != len(agents):
        raise ValueError(f"Numbers of agents and items must be identical, but they are not: {len(agents)}, {k}")
    threshold = (k-1)/2
    G = reduction_to_graph(agents, items, threshold)
    match = nx.max_weight_matching(G)
    if len(match) < k:
        return  # There is no proportional allocation
    bundles = bundles_from_edges(match, G)
    return Allocation(agents, bundles)

def proportional_division_with_p_even(agents: AgentList) -> Allocation:
    """
    Proposition 3 from "Proportional Borda Allocations":
    Finds a proportional division for the items
    :param agents: represents the agents.
    :param items: The items which are being allocated.
    :return: the proportional allocation, There is always a proportional allocation
    Notes: 
        1. p:= len(items)/len(agents) must be an even positive integer
        2. Valuation of agents is defined by "Borda scores" see https://en.wikipedia.org/wiki/Borda_count

    >>> proportional_division_with_p_even(agents=AgentList([[0,1,2,3],[2,0,1,3]])).map_agent_to_bundle()
    {'Agent #0': [1, 3], 'Agent #1': [0, 2]}
    """
    n = len(agents)
    k = len(agents.all_items())
    if k % n != 0:
        raise ValueError(f"The number of items must be multiple of the number of agents, but they are not: {k}, {n}")
    if not isBordaCount(agents):
        raise ValueError(f'Evaluation of items by the agents must be defined by "Board scores". but it is not')
    p = k/n
    if not isEven(p):
        raise ValueError(f"The number of items divided by the number of agents must be even but it is not:{k}/{n}={p}")
    unselected_items = list(agents.all_items())
    allocation = [[] for i in range(n)]
    _, allocation = selection_by_order(agents=agents, items=unselected_items ,allocation=allocation, num_iteration=int(p/2))
    return Allocation(agents, allocation)

agents_to_test_1 = AgentList([[14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],[14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],[14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]])
def proportional_division_with_number_of_agents_odd(agents: AgentList) -> Allocation:
    """
    Theorem 1 from "Proportional Borda Allocations":
    Finds a proportional division for the items
    :param agents: represents the agents.
    :param items: The items which are being allocated.
    :return: the proportional allocation, There is always a proportional allocation
    Notes: 
        1. len(agents) must be an odd positive integer and  len(items)/len(agents) must be a positive integer of at least 3
        2. Valuation of agents is defined by "Borda scores" see https://en.wikipedia.org/wiki/Borda_count
    
    >>> proportional_division_with_number_of_agents_odd(agents=agents_to_test_1).map_agent_to_bundle()
    {'Agent #0': [0, 4, 8, 9, 14], 'Agent #1': [1, 5, 6, 10, 13], 'Agent #2': [2, 3, 7, 11, 12]}
    """
    n = len(agents)
    if isEven(n):
        raise ValueError(f"The number of agents must be odd but it is not: {n}")
    # If n is even, there is a proportional division and the proportional_division function returns it
    return proportional_division(agents)  

def proportional_division(agents: AgentList) -> Allocation:
    """
    Theorem 3 from "Proportional Borda Allocations":
    Finds a proportional division for the items
    :param agents: represents the agents.
    :param items: The items which are being allocated.
    :return the proportional allocation, 
        or an approximately proportional allocation if no proportional allocation exists.

    Notes: 
    1. len(items)/len(agents) must be an positive integer and len(items)/len(agents) ≥ 3
    2. approximately proportional allocation If and only if  
            valuation[i][items of agent[i]]  ≥  |  valuation[i](items)/len(agents) | for each agent i
                                                |__                              __|
    3. There is always an approximately proportional allocation
    4. Valuation of agents is defined by "Borda scores" see https://en.wikipedia.org/wiki/Borda_count

    >>> proportional_division(agents=AgentList([[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9]])).map_agent_to_bundle()
    {'Agent #0': [0, 3, 5, 6, 9], 'Agent #1': [1, 2, 4, 7, 8]}
    >>> proportional_division(agents= AgentList({"Shlomo": [0,1,2,3],"Dani": [2,0,1,3]})).map_agent_to_bundle()
    {'Shlomo': [1, 3], 'Dani': [0, 2]}

    """
    n = len(agents)
    k = len(agents.all_items())
    if not k % n == 0:
        raise ValueError(f"The number of items must be multiple of the number of agents, but they are not: {k}, {n}")
    if isEven(k/n):
        return proportional_division_with_p_even(agents)
    if k/n == 1:
            raise ValueError(f"len(items)/len(agents) must be at least 3, but {k}/{n} == 1")
    if not isBordaCount(agents):
        raise ValueError(f'Evaluation of items by the agents must be defined by "Board scores". but it is not')
    p = k/n - 3     # 3 ≤ k/n is odd
    q1 = [i for i in range(n)]
    q2 = [i-1 for i in range(n, 0, -2)]
    q3 = [i-1 for i in range(n-1, 0, -2)]
    order = q1 + q2 + q3 + q3 + q2
    items = list(agents.all_items())
    allocation = [[] for i in range(n)]
    unselected_items, allocation = selection_by_order(agents, items=items, allocation=allocation, order=order)
    _, allocation = selection_by_order(agents, items=unselected_items, allocation=allocation, num_iteration=int(p/2))
    return Allocation(agents, allocation)



#################    Helper function    #################
def bundles_from_edges(match:set, G:nx.Graph) -> dict:
    bundles = {}
    for edge in match:
        first_node = edge[0]
        second_node = edge[1]
        if G.nodes[first_node].get('isAgent', False):
            bundles[first_node] = [second_node]
        else:
            bundles[second_node] = [first_node]
    return bundles

def reduction_to_graph(agents:AgentList, items:List, threshold:float) -> nx.Graph:
    G = nx.Graph()
    G.add_nodes_from(agents.agent_names())
    nx.set_node_attributes(G, True, 'isAgent')
    G.add_nodes_from(items)
    for agent in agents:
        for item in items:
            val_item = agent.value(item)
            if val_item >= threshold:
                G.add_edge(agent.name(), item)
    return G

def isBordaCount(agents:AgentList) -> bool:
    for agent in agents:
        agent_values = {agent.value(item) for item in agents.all_items()}
        if len (agent_values) < len(agents.all_items()):
            return False
        for val in range(len(agents.all_items())):
            if val not in agent_values:
                return False
    return True

def selection_by_order(agents:AgentList, items:list, allocation:List[list], num_iteration:int=1, order:list=None) -> Tuple[list,List[list]]:
    if not order:
        order = [i for i in range(len(agents))]
        order += reversed(order)

    for iter in range(num_iteration):
        for i in order:
            agent = agents[i]
            favorite_index = agent.best_index(items)
            favorite = items[favorite_index]
            allocation[i].append(favorite)
            items.remove(favorite)
    return items, allocation

def isEven(n):
    return n % 2 == 0


### MAIN

if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))