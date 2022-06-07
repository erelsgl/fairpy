#!python3

"""
Find the Top tranding cycle houses allocation with indifference .
Based on:
Daniela Saban and Jay Sethuraman.
["House allocation with indifferences: a generalization and a unified view"](https://dl.acm.org/doi/abs/10.1145/2492002.2482574)
Programmer: Ishay Levy.
Since: 2022-05
"""
import fairpy
import operator
import networkx as nx
import unittest


from typing import Dict

# the Kosaraju’s algorithm i copy from https://www.geeksforgeeks.org/strongly-connected-components/

def top_trading_cycles_with_indifferences(owner_house: Dict, PreferenceLists: Dict):
    """
    the main fun that call all the func and return the owner houses after do this algo.
    :param owner_house:dictionary that connect between the houses to there owners.keys = agent, values = houses.
    :param PreferenceLists:dictionary with agent's keys and the values are order list houses from top to low choices.
    :return:owner houses after this algo.


    >>> PreferenceLists = {1: ['b', 'a'], 2: ['c', 'b'], 3: ['d', 'c'], 4: ['d']}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

    >>> PreferenceLists = {1: [{'a', 'b'}], 2: ['a', 'b']}
    >>> house = {1: 'a', 2: 'b'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'a'}

    >>> PreferenceLists = {1: {'a': 3, 'b': 3}, 2: {'a': 5, 'b': 1}}
    >>> house = {1: 'a', 2: 'b'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'a'}

    >>> PreferenceLists = {1: {'b': 3, 'a': 2}, 2: {'c': 5, 'b': 1}, 3:{'d':9, 'c':8},4:{'d':3}}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'a', 2: 'b', 3: 'c', 4: 'd'}

    >>> PreferenceLists = {1: ['b', 'a'], 2: ['c', 'b'], 3: ['d', 'c'], 4: ['a']}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'c', 3: 'd', 4: 'a'}

    >>> PreferenceLists = {1: {'b': 3, 'a': 2}, 2: {'c': 5, 'b': 1}, 3:{'d':9, 'c':8},4:{'a':3}}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'c', 3: 'd', 4: 'a'}

    >>> PreferenceLists = {1: ['b'], 2: ['a'], 3: ['c']}
    >>> house = {1: 'a', 2: 'b', 3: 'c'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'a', 3: 'c'}

    >>> PreferenceLists = {1: {'b': 3}, 2: {'a': 5}, 3:{'c':9}}
    >>> house = {1: 'a', 2: 'b', 3: 'c'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'a', 3: 'c'}

    >>> PreferenceLists = {1: [{'g', 'c'}], 2: [{'f', 'g', 'd'}], 3: [{'b', 'e'}, 'c'], 4: ['e'], 5: ['d'], 6: ['b', 'f'], 7: ['a']}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'g', 2: 'f', 3: 'c', 4: 'e', 5: 'd', 6: 'b', 7: 'a'}

    >>> PreferenceLists = {1: {'g': 3, 'c': 3}, 2: {'f': 2, 'g': 2, 'd': 2}, 3: {'b': 9, 'e':9, 'c': 3}, 4: {'e': 1}, 5: {'d': 5},6: {'b': 1, 'f': 0}, 7:{'a':3}}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'g', 2: 'f', 3: 'c', 4: 'e', 5: 'd', 6: 'b', 7: 'a'}

    >>> PreferenceLists = {1: [{'a', 'c'}],2: [{'a', 'b', 'd'}], 3: [{'c', 'e'}], 4: ['c'], 5: [{'a', 'f'}], 6: ['b']}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'a', 2: 'd', 3: 'e', 4: 'c', 5: 'f', 6: 'b'}

    >>> PreferenceLists = {1: {'a': 3, 'c': 3}, 2: {'a': 2, 'b': 2, 'd': 2}, 3: {'c': 9, 'e':9}, 4: {'c': 1}, 5: {'a': 5, 'f': 5},6: {'b': 1}}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'a', 2: 'd', 3: 'e', 4: 'c', 5: 'f', 6: 'b'}



    """



    for key, value in PreferenceLists.items():
        if isinstance(value, Dict):
            # this func change the data from rank with numbers to rank with order.
            PreferenceLists = get_all_values(owner_house, PreferenceLists)
            break

    graph = make_graph_begin(PreferenceLists, owner_house)
    # ----------------------------------------------1------------------------------------------------------------------
    # Repeat until no agent is left.
    while len(graph) != 0:
        jealous = []
        # ------------------------------------------1(a)--------------------------------------------------------------
        # connect between agents to there first
        # prefer object in the graph and also between the object to there owners.
        graph = make_graph(PreferenceLists, graph)

        # # if all agents in the graph are satisfied return the owner_house.
        # if if_all_satisfied(graph, owner_house):
        #     return owner_house

        # -------------------------------------------1(b)------------------------------------------------------------

        # if there is final scc remove all the node in this scc and update the graph and repeat.
        # over this until there is no final scc in the graph.
        graph = find_satisfied_SCC(graph, owner_house, PreferenceLists)
        # ------------------------------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------

        # ---------------------------------------------2--------------------------------------------------------------
        # keep all the jealous agens in list.
        for li in graph:
            if owner_house.keys().__contains__(li) and not graph.has_edge(li, owner_house[li]):
                jealous.append(li)

        labeled = []
        # ---------------------------------------------2(1.a)----------------------------------------------------------
        # connect jealous people to the min house they have edge to.
        graph = connect_jealous_agents_to_there_best(jealous, graph)
        # -------------------------------------------------------------------------------------------------------------

        for je in jealous:
            labeled.append(je)
            labeled.append(owner_house[je])
        # connect satisfied people to the closest label agent.
        # ---------------------------------------------2(1.b)----------------------------------------------------------
        graph = connect_satisfied_agents_to_there_best(graph, owner_house, labeled)

        # Change houses owners in SCC.
        graph = if_SCC_change_owners(graph, owner_house)

        # ------------------------------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------

    return owner_house

def stringify(d):
    """
    Returns a canonical string representation of the given dict,
    by sorting its items recursively.
    This is especially useful in doctests::
    >>> stringify({"a":1,"b":2,"c":{"e":4,"d":3}})
    '{a:1, b:2, c:{d:3, e:4}}'
    """
    d2 = {}
    for k, v in d.items():
        if isinstance(v, dict):
            d2[k] = stringify(v)
        else:
            d2[k] =str (v)

    return "{" + ", ".join(["{}:{}".format(k, v) for k, v in sorted(d2.items())]) + "}"

def make_graph(PreferenceLists: Dict, graph):
    """
    part 1(a)
    O(n^2)
    Update all the edges between agents and houses,with the PreferenceLists.
    :param PreferenceLists:dictionary that contain a order list houses from top to low choices prefer for all agents.
     keys = agent, values = prefer list of houses.
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :return: graph after update the edges.
    >>> PreferenceLists = {'1': [{'g', 'c'}],'2': [{'f', 'g', 'd'}],'3': [{'b', 'e'}, 'c'],'4': ['e'],'5': ['d'],'6': ['b', 'f'],'7': ['a']}
    >>> house = {'1': 'a','2': 'b','3': 'c','4': 'd','5': 'e','6': 'f','7': 'g'}
    >>> makeGraph = make_graph_begin(PreferenceLists, house)
    >>> makeGraph.remove_node('2')
    >>> makeGraph.remove_node('b')
    >>> G = make_graph(PreferenceLists, makeGraph)
    >>> G = nx.to_dict_of_dicts(G, edge_data=None)
    >>> stringify(G)
    '{1:{c:{}, g:{}}, 3:{e:{}}, 4:{e:{}}, 5:{d:{}}, 6:{f:{}}, 7:{a:{}}, a:{1:{}}, c:{3:{}}, d:{4:{}}, e:{5:{}}, f:{6:{}}, g:{7:{}}}'
    """


    newGraph = graph.copy()
    for i in newGraph:
        if i in PreferenceLists.keys():
            flag = 1
            m = 0
            while flag:
                for j in PreferenceLists[i][m]:
                    if j in graph:
                        if not graph[i].__contains__(j):
                            graph.add_edge(i, j)
                        flag = 0
                if flag:
                    m = m + 1
    return graph


def make_graph_begin(PreferenceLists: Dict, owner_house: Dict):
    """
    O(n^2)
    This func make graph with agents and houses nodes and connect between them with edges.
    The edges connect between agents to the houses they prefer and between the houses to agent owners.
    :param PreferenceLists:dictionary that give a order list from top to low choices prefer houses.
    keys = agent, values = prefer list of houses.
    :param owner_house:dictionary that connect between the houses to there owners.
     keys = agent, values = houses.
    :param graph:empty graph.
    :return:graph after add al the agents and houses and update the edges.

    >>> PreferenceLists = {'1': ['a', 'b'],'2': ['b', 'a'],'3': ['c']}
    >>> house = {'1': 'a', '2': 'b', '3': 'c'}
    >>> G = make_graph_begin(PreferenceLists, house)
    >>> G = nx.to_dict_of_dicts(G, edge_data=None)
    >>> stringify(G)
    '{1:{a:{}}, 2:{b:{}}, 3:{c:{}}, a:{1:{}}, b:{2:{}}, c:{3:{}}}'

    >>> PreferenceLists = {'1': [{'a', 'b', 'c'}], '2': [{'a', 'b', 'c'}], '3': [{'a', 'b', 'c'}]}
    >>> house = {'1': 'a', '2': 'b', '3': 'c'}
    >>> G = make_graph_begin(PreferenceLists, house)
    >>> G = nx.to_dict_of_dicts(G, edge_data=None)
    >>> stringify(G)
    '{1:{a:{}, b:{}, c:{}}, 2:{a:{}, b:{}, c:{}}, 3:{a:{}, b:{}, c:{}}, a:{1:{}}, b:{2:{}}, c:{3:{}}}'

    >>> PreferenceLists = {'1': [{'g', 'c'}],'2': [{'f', 'g', 'd'}],'3': [{'b', 'e'}, 'c'],'4': ['e'],'5': ['d'],'6': ['b', 'f'],'7': ['a']}
    >>> house = {'1': 'a','2': 'b','3': 'c','4': 'd','5': 'e','6': 'f','7': 'g'}
    >>> G = make_graph_begin(PreferenceLists, house)
    >>> G = nx.to_dict_of_dicts(G, edge_data=None)
    >>> stringify(G)
    '{1:{c:{}, g:{}}, 2:{d:{}, f:{}, g:{}}, 3:{b:{}, e:{}}, 4:{e:{}}, 5:{d:{}}, 6:{b:{}}, 7:{a:{}}, a:{1:{}}, b:{2:{}}, c:{3:{}}, d:{4:{}}, e:{5:{}}, f:{6:{}}, g:{7:{}}}'

    >>> PreferenceLists = {'1': [{'a', 'c'}],'2': ['c'],'3': ['d'],'4': [{'b', 'd'}]}
    >>> house = {'1': 'a','2': 'b','3': 'c','4': 'd'}
    >>> G = make_graph_begin(PreferenceLists, house)
    >>> G = nx.to_dict_of_dicts(G, edge_data=None)
    >>> stringify(G)
    '{1:{a:{}, c:{}}, 2:{c:{}}, 3:{d:{}}, 4:{b:{}, d:{}}, a:{1:{}}, b:{2:{}}, c:{3:{}}, d:{4:{}}}'

    >>> PreferenceLists = {'1': ['a', 'b', 'c', 'd'],'2': ['a', 'b', 'c', 'd'],'3': ['a', 'b', 'c', 'd'],'4': ['a', 'b', 'c', 'd']}
    >>> house = {'1': 'a','2': 'b','3': 'c','4': 'd'}
    >>> G = make_graph_begin(PreferenceLists, house)
    >>> G = nx.to_dict_of_dicts(G, edge_data=None)
    >>> stringify(G)
    '{1:{a:{}}, 2:{a:{}}, 3:{a:{}}, 4:{a:{}}, a:{1:{}}, b:{2:{}}, c:{3:{}}, d:{4:{}}}'
      """
    # add edge between the agents to the houses they prefer.
    graph = nx.DiGraph()
    for i in PreferenceLists.keys():
        for j in PreferenceLists[i][0]:
            graph.add_edge(i, j)

    # add edge between houses to the agent it belong to.
    for i in owner_house.keys():
        graph.add_edge(owner_house[i], i)
    return graph


def make_stack(graph, v, visited: list, stack: list):
    visited.append(v)
    for i in graph[v]:
        if i not in visited:
            make_stack(graph, i, visited, stack)
    stack.append(v)


def transpose_graph(graph):
    """
    Transpose the edges.
    if G contains an edge (u, v) then the transpose of G contains an edge (v, u) .
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :return:graph after transpose.

    >>> graph = {'1': {'a': {}}, '2': {'b': {}}, 'c': {'3': {}}}
    >>> graph = transpose_graph(graph)
    >>> graph = nx.to_dict_of_dicts(graph, edge_data=None)
    >>> stringify(graph)
    '{1:{}, 2:{}, 3:{c:{}}, a:{1:{}}, b:{2:{}}, c:{}}'


    >>> graph = {'1': {'a': {}, 'b' : {}}, '2': {'b': {}, 'a': {}}, 'c': {'3': {}}}
    >>> graph = transpose_graph(graph)
    >>> graph = nx.to_dict_of_dicts(graph, edge_data=None)
    >>> stringify(graph)
    '{1:{}, 2:{}, 3:{c:{}}, a:{1:{}, 2:{}}, b:{1:{}, 2:{}}, c:{}}'
    """
    TransposeG = nx.DiGraph()
    for i in graph:
        for j in graph[i]:
            TransposeG.add_edge(j, i)
    return TransposeG


def SCC(graph, v, visited: list, SCC_list):
    visited.append(v)
    SCC_list.append(v)

    for i in graph[v]:
        if i not in visited:
            SCC(graph, i, visited, SCC_list)

    return SCC_list


def if_all_satisfied(graph, owner_house: Dict):
    """
    O(n)
    check if there aren't jealous agents in the graph return 1 else 0.
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :param owner_house:dictionary that connect between the houses to there owners.keys = agent, values = houses.
    :return:true if all the agents in the graph are satisfied, else false.

    >>> PreferenceLists = {'1': [{'a', 'b', 'c'}],'2': [{'a', 'b', 'c'}],'3': [{'a', 'b', 'c'}]}
    >>> house = {'1': 'a','2': 'b','3': 'c'}
    >>> graph = make_graph_begin(PreferenceLists, house)
    >>> if_all_satisfied(graph, house)
    1

    >>> PreferenceLists = {'1': [{'b'}],'2': [{'a', 'b', 'c'}],'3': [{'a', 'b', 'c'}]}
    >>> house = {'1': 'a','2': 'b','3': 'c'}
    >>> graph = make_graph_begin(PreferenceLists, house)
    >>> if_all_satisfied(graph, house)
    0
    """
    for li in graph:
        if owner_house.keys().__contains__(li) and not graph.has_edge(li, owner_house[li]):
            return 0
    return 1


def if_SCC_change_owners(graph, owner_house: Dict):
    """
    part 2(1.b)
    this func run over all SCC in the graph and replace the houses owners in this SCC(that every agents in SCC will be satisfied) .
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :param owner_house:dictionary that connect between the houses to there owners.keys = agent, values = houses.
    :return: update graph.

    >>> PreferenceLists = {'1': ['b'], '2': ['a']}
    >>> house = {'1': 'a', '2': 'b'}
    >>> graph = make_graph_begin(PreferenceLists, house)
    >>> graph = if_SCC_change_owners(graph, house)
    >>> graph = nx.to_dict_of_dicts(graph, edge_data=None)
    >>> stringify(graph)
    '{1:{b:{}}, 2:{a:{}}, a:{2:{}}, b:{1:{}}}'

    >>> PreferenceLists = {'1': ['b'],'2': ['a'],'3': ['d'],'4': ['c']}
    >>> house = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}
    >>> graph = make_graph_begin(PreferenceLists, house)
    >>> graph = if_SCC_change_owners(graph, house)
    >>> graph = nx.to_dict_of_dicts(graph, edge_data=None)
    >>> stringify(graph)
    '{1:{b:{}}, 2:{a:{}}, 3:{d:{}}, 4:{c:{}}, a:{2:{}}, b:{1:{}}, c:{4:{}}, d:{3:{}}}'
    """
    HostHouse = []
    for i in owner_house.values():
        HostHouse.append(i)

    stack = []
    visited = []

    for i in graph:
        if i not in visited:
            visited.append(i)
            make_stack(graph, i, visited, stack)

    gr = transpose_graph(graph)
    visited = []
    HostHouse = []
    for o in owner_house.values():
        HostHouse.append(o)
    while stack:
        i = stack.pop()
        if not visited.__contains__(i):
            ListOfLists = []
            List = SCC(gr, i, visited, ListOfLists)
            if len(List) > 1:
                length = len(List)
                for mmm in range(length):
                    if HostHouse.__contains__(List[mmm]):
                        owner_house[List[(mmm + 1) % len(List)]] = List[mmm]
                        graph.remove_edge(List[mmm], List[mmm - 1])
                        graph.add_edge(List[mmm], List[(mmm + 1) % len(List)])
    return graph


def find_satisfied_SCC(graph, owner_house: Dict, PreferenceLists: Dict):
    """
    part 1(b)
    find SCC that all there agents are satisfied and point only to this SCC, if there is this SCC remove all the
    agents and houses that find in this SCC from the graph.update all the connected between the agents and houses and do
    this again until there is no END SCC.
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :param owner_house:dictionary that connect between the houses to there owners.keys = agent, values = houses.
    :param PreferenceLists:dictionary with agent's keys and the values are order list houses from top to low choices.
    :return: update graph.


    >>> PreferenceLists = {'1': ['a', 'b'], '2': ['b', 'a'], '3': ['d'], '4': ['c']}
    >>> house = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}
    >>> graph = make_graph_begin(PreferenceLists, house)
    >>> graph = find_satisfied_SCC(graph, house, PreferenceLists )
    >>> graph = nx.to_dict_of_dicts(graph, edge_data=None)
    >>> stringify(graph)
    '{3:{d:{}}, 4:{c:{}}, c:{3:{}}, d:{4:{}}}'

    >>> PreferenceLists = {'1': ['b'], '2': ['a'], '3': [{'c','d'}], '4': [{'c','d'}]}
    >>> house = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}
    >>> graph = make_graph_begin(PreferenceLists, house)
    >>> graph  = find_satisfied_SCC(graph, house, PreferenceLists )
    >>> graph = nx.to_dict_of_dicts(graph, edge_data=None)
    >>> stringify(graph)
    '{1:{b:{}}, 2:{a:{}}, a:{1:{}}, b:{2:{}}}'

    """
    change = 1
    while change:
        change = 0
        stack = []
        visited = []
        # O(n^2)
        # make stack with all agents.
        for i in graph:
            if i not in visited:
                visited.append(i)
                make_stack(graph, i, visited, stack)
        # O(n^2)
        # transpose the graph
        gr = transpose_graph(graph)

        visited = []
        while stack and not change:
            i = stack.pop()
            if i not in visited:
                if owner_house.keys().__contains__(i):
                    ListOfLists = []
                    # Strongly Connected Components
                    List = SCC(gr, i, visited, ListOfLists)
                    if len(List) > 1:
                        flag = 1
                        # check if List is "final" SCC
                        for li in List:
                            # if all node in List point doesn't point outside of the SCC.
                            for nodefromli in graph[li]:
                                if not List.__contains__(nodefromli):
                                    flag = 0
                            # if there is agent in SCC list that jealous.
                            if owner_house.keys().__contains__(li) and not graph.has_edge(li, owner_house[li]):
                                flag = 0
                        # if SCC "final".
                        if flag == 1:
                            for i in List:
                                graph.remove_node(i)
                            change = 1
                            graph = make_graph(PreferenceLists, graph)
    return graph


def connect_jealous_agents_to_there_best(jealous: list, graph):
    """
    part 1(a)
    part 2(1.a)
    # O(n^2)
    this func keep only one edge between all jealous agents to the house(the house that have already edge and also
    the house has the min "aski" value).
    :param jealous:list with all jealous agents.
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :return: update graph.


    >>> PreferenceLists = {'1': ['a', 'b'], '2': ['b', 'a'], '3': ['d'], '4': ['c']}
    >>> house = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}
    >>> graph = make_graph_begin(PreferenceLists, house)
    >>> graph = connect_jealous_agents_to_there_best([ '3', '4', 'd', 'c'], graph)
    >>> graph = nx.to_dict_of_dicts(graph, edge_data=None)
    >>> stringify(graph)
    '{1:{a:{}}, 2:{b:{}}, 3:{d:{}}, 4:{c:{}}, a:{1:{}}, b:{2:{}}, c:{3:{}}, d:{4:{}}}'

    >>> PreferenceLists = {'1': [{'b','c','d'}], '2': [{'a','c','d'}], '3': [{'c','d'}], '4': [{'c','d'}]}
    >>> house = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}
    >>> graph = make_graph_begin(PreferenceLists, house)
    >>> graph = connect_jealous_agents_to_there_best([ '3', '4', 'd', 'c'], graph)
    >>> graph = nx.to_dict_of_dicts(graph, edge_data=None)
    >>> stringify(graph)
    '{1:{b:{}, c:{}, d:{}}, 2:{a:{}, c:{}, d:{}}, 3:{c:{}}, 4:{c:{}}, a:{1:{}}, b:{2:{}}, c:{3:{}}, d:{4:{}}}'
    """
    # O(n)
    # run over all the jealous agents.
    for je in jealous:
        MinHouse = min(graph[je].keys())
        graphlllist = []
        for i in graph[je]:
            graphlllist.append(i)
        # O(n)
        # delete all the edges that go from jealous agents outside then MinHouse.
        for node in graphlllist:
            if node != MinHouse:
                if graph.has_edge(je, node):
                    graph.remove_edge(je, node)
    return graph


def connect_satisfied_agents_to_there_best(graph, owner_house: Dict, labeled: list):
    """
    part 2(1.b)
    O(n^2)
     keep only one edge between all satisfied agents to labeled agent.
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :param owner_house:dictionary that connect between the houses to there owners.keys = agent, values = houses.
    :param labeled:in begin it is all the jealous agents.and after that all the agents that connect to this labeled add
    to labeld.
    :return: update graph.


    >>> PreferenceLists = {'1': ['a', 'b'], '2': ['b', 'a'], '3': ['d'], '4': ['c']}
    >>> house = {'1': 'a', '2': 'b', '3': 'c', '4': 'd'}
    >>> graph = nx.DiGraph()
    >>> graph.add_edge('3','d')
    >>> graph.add_edge('d','4')
    >>> graph.add_edge('4','c')
    >>> graph.add_edge('c','3')
    >>> graph = connect_satisfied_agents_to_there_best(graph, house, [ '3', '4', 'd', 'c'])
    >>> graph = nx.to_dict_of_dicts(graph, edge_data=None)
    >>> stringify(graph)
    '{3:{d:{}}, 4:{c:{}}, c:{3:{}}, d:{4:{}}}'


    >>> PreferenceLists = {1: [{'b','c','d'}], 2: [{'a','c','d'}], 3: [{'c','d'}], 4: [{'c','d'}]}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> graph = nx.DiGraph()
    >>> graph.add_edge('1','b')
    >>> graph.add_edge('b','2')
    >>> graph.add_edge('2','a')
    >>> graph.add_edge('a','1')
    >>> graph = connect_satisfied_agents_to_there_best(graph, house, [ '1', '2', 'b', 'a'])
    >>> graph = nx.to_dict_of_dicts(graph, edge_data=None)
    >>> stringify(graph)
    '{1:{b:{}}, 2:{a:{}}, a:{1:{}}, b:{2:{}}}'
    """

    un_labeled = []
    ney_labeled = []
    labeled_houses = []
    # O(n)
    # put all the non labeled agents as un_labeled.
    for i in graph:
        if not labeled.__contains__(i):
            un_labeled.append(i)
    #  run until all the agents are labeled.
    while un_labeled:
        # keep all the Neighbors of labeled agents at ney_labeled (they are un_labeled).
        for i in labeled:
            if owner_house.keys().__contains__(i):
                house = owner_house[i]
                for j in graph:
                    if owner_house.keys().__contains__(j) and un_labeled.__contains__(j) and graph.has_edge(j, house) and not ney_labeled.__contains__(j):
                        ney_labeled.append(j)
        m = 0
        ney_labeled.sort()
        ney_labeled.reverse()
        for i in range(len(labeled)):
            if not owner_house.keys().__contains__(labeled[i - m]):
                labeled_houses.append(labeled[i - m])
                labeled.remove(labeled[i - m])
                m = m + 1
        labeled.sort()
        labeled.reverse()
        smallest_ney_labeled = ney_labeled.pop()
        listcheck = []

        # all the labeled houses put in list and sort.
        for i in graph[smallest_ney_labeled]:
            if labeled_houses.__contains__(i):
                listcheck.append(i)
        listcheck.sort()
        listcheck.reverse()
        min_house = listcheck.pop()
        graphlllist = []
        # delete all the edges between the Neighbors agent with the smallest value in the labeled list outside from
        # min_house he connect to in the labeled houses.
        for i in graph[smallest_ney_labeled]:
            graphlllist.append(i)
        for node in graphlllist:
            if node != min_house:
                if graph.has_edge(smallest_ney_labeled, node):
                    graph.remove_edge(smallest_ney_labeled, node)
        # remove smallest_ney_labeled from un_labeled list and add to labeled list.
        labeled.append(smallest_ney_labeled)
        labeled_houses.append(owner_house[smallest_ney_labeled])
        un_labeled.remove(smallest_ney_labeled)
        un_labeled.remove(owner_house[smallest_ney_labeled])
    return graph


def get_all_values(owner_house: Dict, PreferenceLists: Dict):
    """
    O(n^2*log(n))
    :param owner_house:dictionary that connect between the houses to there owners.
    keys = agent, values = houses.
    :param PreferenceLists:dictionary with agent's keys and the houses values with number how much the agent appraiser the houses.
    keys = agent, values = houses with number.
    :return:call top_trading_cycles_with_indifferences func with order PreferenceLists and owner houses.

    >>> PreferenceLists = {1: {'a': 3, 'b': 3}, 2: {'a': 5, 'b': 1}}
    >>> house = {1: 'a', 2: 'b'}
    >>> get_all_values(house, PreferenceLists)
    {1: [['a', 'b']], 2: ['a', 'b']}

    >>> PreferenceLists = {1: {'b': 3, 'a': 2}, 2: {'c': 5, 'b': 1}, 3:{'d':9, 'c':8},4:{'d':3}}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> get_all_values(house, PreferenceLists)
    {1: ['b', 'a'], 2: ['c', 'b'], 3: ['d', 'c'], 4: ['d']}

    >>> PreferenceLists = {1: {'b': 3, 'a': 2}, 2: {'c': 5, 'b': 1}, 3:{'d':9, 'c':8},4:{'a':3}}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> get_all_values(house, PreferenceLists)
    {1: ['b', 'a'], 2: ['c', 'b'], 3: ['d', 'c'], 4: ['a']}
    """
    ans = {}
    List = []
    ListName = []
    # run over all the agents.
    for x in PreferenceLists:
        # sort the preferences by the values that get all houses by this agent/
        sorted_x = sorted(PreferenceLists[x].items(), key=operator.itemgetter(1), reverse=True)
        ListName.append(x)
        List.append(sorted_x)
    # run over all sorted preferences.
    for i in range(len(List)):
        ListAns = []
        ListAns.append(List[i][0][0])
        for j in range(len(List[i]) - 1):
            # if the house i add to the list have same value to the last combine them to one list.
            if List[i][j][1].__eq__(List[i][j + 1][1]):
                if len(ListAns) > 0:
                    x = ListAns.pop()
                if type(x) is list:
                    x.append(List[i][j + 1][0])
                    ListAns.append(x)
                else:
                    ListAns.append([x, List[i][j + 1][0]])
            else:
                ListAns.append(List[i][j + 1][0])
        # ListAns.reverse()
        ans[ListName[i]] = ListAns
    return ans




if __name__ == '__main__':

    import doctest
    doctest.run_docstring_examples(stringify,  globals())
    doctest.run_docstring_examples(make_graph_begin, globals())
    doctest.run_docstring_examples(make_graph, globals())
    doctest.run_docstring_examples(if_SCC_change_owners, globals())
    doctest.run_docstring_examples(top_trading_cycles_with_indifferences, globals())
    doctest.run_docstring_examples(connect_satisfied_agents_to_there_best, globals())
    doctest.run_docstring_examples(connect_jealous_agents_to_there_best, globals())
    doctest.run_docstring_examples(find_satisfied_SCC, globals())
    doctest.run_docstring_examples(if_all_satisfied, globals())
    doctest.run_docstring_examples(transpose_graph, globals())
    doctest.run_docstring_examples(get_all_values, globals())










