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
from typing import List, Any, Dict
import networkx as nx
import matplotlib.pyplot as plt

agents_to_test_0 = AgentList({"Shlomo": {"A": 0, "B": 1, "C": 2, "D": 3},"Shira": {"A": 2, "B": 0, "C": 1, "D": 3},"Hadar": {"A": 2, "B": 0, "C": 1, "D": 3},"Or": {"A": 3, "B": 2, "C": 1, "D": 0}})
def proportional_division_equal_number_of_items_and_players(agents: AgentList, items: List[Any]=None) -> Allocation:
    """
    Proposition 2 from "Proportional Borda Allocations":
    Finds a proportional distribution for the items 
    
    :param agents: represents the n agents.
    :param items: n the items that are allocated.
    :return: the proportional allocation, or none if no proportional allocation exists.
    Notes: 
        1. len(items) must be equal to len(agents)
        2. Valuation of agents is defined by "Borda scores" see https://en.wikipedia.org/wiki/Borda_count

    >>> proportional_division_equal_number_of_items_and_players(agents=agents_to_test_0,items=['A','B','C','D']).map_agent_to_bundle()
    {'Shlomo': ['C'], 'Shira': ['D'], 'Hadar': ['A'], 'Or': ['B']}
    >>> proportional_division_equal_number_of_items_and_players(agents=AgentList([[1,3,2,0],[3,2,1,0],[3,2,1,0],[0,2,3,1]]),items=[0,1,2,3]).map_agent_to_bundle()
    {'Agent #0': [2], 'Agent #1': [0], 'Agent #2': [1], 'Agent #3': [3]}
    >>> proportional_division_equal_number_of_items_and_players(agents=AgentList([[1,0],[0,1]]),items=[0,1]).map_agent_to_bundle()
    {'Agent #0': [0], 'Agent #1': [1]}    
    >>> proportional_division_equal_number_of_items_and_players(agents=AgentList([[0,1,2,3],[0,1,2,3],[0,1,2,3],[0,1,2,3]]),items=[0,1,2,3]) is None
    True
    >>> proportional_division_equal_number_of_items_and_players(agents=AgentList([[0]]),items=[0]).map_agent_to_bundle()
    {'Agent #0': [0]}
    """

    items = list(agents.all_items())
    n = len(agents)
    k = len(items)
    if k != n:
        print('errror')
        return

    G = nx.Graph()
    G.add_nodes_from(items)
    G.add_nodes_from(agents.agent_names())
    threshold = (k-1)/2
    for agent in agents:
        for item in items:
            val_item = agent.value(item)
            if val_item > threshold:
                G.add_edge(item, agent.name())

    ans = nx.maximal_matching(G)
    print(ans)
    # if len(ans) < len(agents):
    #     print('not exists')
    #     return

    # names = []
    # aloc = []
    # for a in ans:
    #     print(agents.agent_names().index(a[1]))

        # names.append(a[1])
        # print(a[0])
        # agents.
        # aloc.append(a[1],agents[a[1]].value(a[0]))
    
    # print(G)
    # draw_options = {
    #     "font_size": 10,
    #     "node_size": 700,
    #     "node_color": "yellow",
    #     "edgecolors": "black",
    #     "linewidths": 1,
    #     "width": 1,
    #     "with_labels": True
    # }
    # nx.draw(G,  **draw_options)
    # print('ddd')
    # plt.show()
    
    return Allocation([''],[['']])

def proportional_division_with_p_even(agents: AgentList, items: List[Any]=None) -> Allocation:
    """
    Proposition 3 from "Proportional Borda Allocations":
    Finds a proportional distribution for the items
    :param agents: represents the agents.
    :param items: The items which are being allocated.
    :return: the proportional allocation, There is always a proportional allocation
    Notes: 
        1. p:= len(items)/len(agents) must be an even positive integer
        2. Valuation of agents is defined by "Borda scores" see https://en.wikipedia.org/wiki/Borda_count

    >>> proportional_division_with_p_even(agents=AgentList([[0,1,2,3],[2,0,1,3]]),items=[0,1,2,3]).map_agent_to_bundle()
    {'Agent #0': [1,3], 'Agent #1': [0,2]}
    """
    return Allocation([''],[['']])

agents_to_test_1 = AgentList([[14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],[14,13,12,11,10,9,8,7,6,5,4,3,2,1,0],[14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]])
def proportional_division_with_number_of_agents_odd(agents: AgentList, items: List[Any]=None) -> Allocation:
    """
    Theorem 1 from "Proportional Borda Allocations":
    Finds a proportional distribution for the items
    :param agents: represents the agents.
    :param items: The items which are being allocated.
    :return: the proportional allocation, There is always a proportional allocation
    Notes: 
        1. len(agents) must be an odd positive integer and len(items)/len(agents) must be an positive integer
        2. Valuation of agents is defined by "Borda scores" see https://en.wikipedia.org/wiki/Borda_count
    
    >>> proportional_division_with_number_of_agents_odd(agents=agents_to_test_1,items=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]).map_agent_to_bundle()
    {'Agent #0': [0,4,8,9,14], 'Agent #1': [1,5,6,10,13], 'Agent #2': [2,3,7,11,12]}
    """
    return Allocation([''],[['']])

def proportional_division(agents: AgentList, items: List[Any]=None) -> Allocation:
    """
    Theorem 3 from "Proportional Borda Allocations":
    Finds a proportional distribution for the items
    :param agents: represents the agents.
    :param items: The items which are being allocated.
    :return the proportional allocation, 
        or an approximately proportional allocation if no proportional allocation exists.

    Notes: 
    1. len(items)/len(agents) must be an positive integer
    2. approximately proportional allocation If and only if  
            valuation[i][items of agent[i]]  ≥  |  valuation[i](items)/len(agents) | for each agent i
                                                |__                              __|
    3. There is always an approximately proportional allocation
    4. Valuation of agents is defined by "Borda scores" see https://en.wikipedia.org/wiki/Borda_count

    >>> proportional_division(agents=AgentList([[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9]]),items=[0,1,2,3,4,5,6,7,8,9]).map_agent_to_bundle()
    {'Agent #0': [0,3,4,6,9], 'Agent #1': [1,2,5,7,8]}
    >>> proportional_division(agents= AgentList({"Shlomo": [0,1,2,3],"Dani": [2,0,1,3]}),items=[0,1,2,3]).map_agent_to_bundle()
    {'Shlomo': [1,3], 'Dani': [0,2]} 

    """
    return Allocation([''],[['']])

### MAIN

if __name__ == "__main__":
<<<<<<< HEAD






    # proportional_division_equal_number_of_items_and_players(agents=agents_to_test_0, items=['A','B','C','D']).map_agent_to_bundle()
    agents_to_test_0 = AgentList({"Shlomo": {"A": 0, "B": 1, "C": 2, "D": 3},"Shira": {"A": 2, "B": 0, "C": 1, "D": 3},"Hadar": {"A": 2, "B": 0, "C": 1, "D": 3},"Or": {"A": 3, "B": 2, "C": 1, "D": 0}})
    
    # print(len(agents_to_test_0))
    # print()
    tt = proportional_division_equal_number_of_items_and_players(agents=agents_to_test_0, items=['A','B','C','D'])
    print(tt)


    # import doctest
    # # (failures,tests) = doctest.testmod(report=True)
    # print(doctest.testmod())
    # print ("{} failures, {} tests".format(failures,tests))
    
=======
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
    
>>>>>>> 1aa126ce664ae49214ed02a036e19ffd1efbce8d
