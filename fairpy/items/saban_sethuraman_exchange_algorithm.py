#!python3

"""
Find the Top tranding cycle houses allocation with indifference .
Based on:
Daniela Saban and Jay Sethuraman.
["House allocation with indifferences: a generalization and a unified view"](https://dl.acm.org/doi/abs/10.1145/2492002.2482574)
Programmer: Ishay Levy.
Since: 2022-05
"""
import operator
import sys

import networkx as nx
import logging
# saban_sethuraman_exchange_algorithm
logger = logging.getLogger("project")
from typing import Dict
logger.addHandler(logging.StreamHandler(sys.stdout))

def top_trading_cycles_with_indifferences(owner_house: Dict, PreferenceLists: Dict) -> Dict:
    """
    the main fun that call all the func and return the owner houses after do this algo.
    :param owner_house:dictionary that connect between the houses to their owners.keys = agent, values = houses.
    :param PreferenceLists:dictionary with agent's keys and the values are order list houses from top to low choices.
    :return:owner houses after this algorithm.
    # >>> logger.addHandler(logging.StreamHandler())

    >>> logger.setLevel(logging.INFO)
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: [{'a', 'b'}], 2: ['a', 'b']}
    >>> house = {1: 'a', 2: 'b'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'a'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: ['b', 'a'], 2: ['c', 'b'], 3: ['d', 'c'], 4: ['d']}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: {'a': 3, 'b': 3}, 2: {'a': 5, 'b': 1}}
    >>> house = {1: 'a', 2: 'b'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'a'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: {'b': 3, 'a': 2}, 2: {'c': 5, 'b': 1}, 3:{'d':9, 'c':8},4:{'d':3}}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: ['b', 'a'], 2: ['c', 'b'], 3: ['d', 'c'], 4: ['a']}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'c', 3: 'd', 4: 'a'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: {'b': 3, 'a': 2}, 2: {'c': 5, 'b': 1}, 3:{'d':9, 'c':8},4:{'a':3}}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'c', 3: 'd', 4: 'a'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: ['b'], 2: ['a'], 3: ['c']}
    >>> house = {1: 'a', 2: 'b', 3: 'c'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'a', 3: 'c'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: {'b': 3}, 2: {'a': 5}, 3:{'c':9}}
    >>> house = {1: 'a', 2: 'b', 3: 'c'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'b', 2: 'a', 3: 'c'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: [{'g', 'c'}], 2: [{'f', 'g', 'd'}], 3: [{'b', 'e'}, 'c'], 4: ['e'], 5: ['d'], 6: ['b', 'f'], 7: ['a']}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'g', 2: 'f', 3: 'c', 4: 'e', 5: 'd', 6: 'b', 7: 'a'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: {'g': 3, 'c': 3}, 2: {'f': 2, 'g': 2, 'd': 2}, 3: {'b': 9, 'e':9, 'c': 3}, 4: {'e': 1}, 5: {'d': 5},6: {'b': 1, 'f': 0}, 7:{'a':3}}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'g', 2: 'f', 3: 'c', 4: 'e', 5: 'd', 6: 'b', 7: 'a'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: [{'a', 'c'}],2: [{'a', 'b', 'd'}], 3: [{'c', 'e'}], 4: ['c'], 5: [{'a', 'f'}], 6: ['b']}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'a', 2: 'd', 3: 'e', 4: 'c', 5: 'f', 6: 'b'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")
    >>> logger.info("----------------------------------------begin----------------------------------------------------")
    >>> PreferenceLists = {1: {'a': 3, 'c': 3}, 2: {'a': 2, 'b': 2, 'd': 2}, 3: {'c': 9, 'e':9}, 4: {'c': 1}, 5: {'a': 5, 'f': 5},6: {'b': 1}}
    >>> house = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f'}
    >>> top_trading_cycles_with_indifferences(house, PreferenceLists)
    {1: 'a', 2: 'd', 3: 'e', 4: 'c', 5: 'f', 6: 'b'}
    >>> logger.info("----------------------------------------end----------------------------------------------------")

    """


    logger.info("Top trading cycles with indifferences algorithm")
    logger.info("List with all the preference lists of all agents: %s ", PreferenceLists)
    logger.info("List with agents and their own house: %s ", owner_house)

    for key, value in PreferenceLists.items():
        if isinstance(value, Dict):
            logger.info("this func change the data from rank with numbers to rank with order.")
            PreferenceLists = Change_preferences_by_numbers_to_preferences_by_order(PreferenceLists)
            break

    graph = make_graph_begin(PreferenceLists, owner_house)

    logger.info("----------------------------------------------1------------------------------------------------------")
    logger.info("Repeat until no agent is left.")

    while len(graph) != 0:
        jealous = []

        logger.info("------------------------------------------1(a)---------------------------------------------------")
        logger.info("connect between agents to there first preference and also between the object to their owners.")
        graph = make_graph(PreferenceLists, graph)
        logger.info(nx.to_dict_of_dicts(graph, edge_data=None))
        # I add this func to the algorithm
        if are_all_agents_satisfied(graph, owner_house):
            logger.info("if all agents in the graph are satisfied return the owner_house. %s \n", owner_house)
            return owner_house

        logger.info("------------------------------------------1(b)---------------------------------------------------")
        logger.info(" if there is final scc remove all the node in this scc and update the graph and repeat.")
        logger.info("over this until there is no final scc in the graph.")

        graph = find_satisfied_SCC(graph, owner_house, PreferenceLists)
        logger.info("the find_satisfied_SCC is : %s ", nx.to_dict_of_dicts(graph, edge_data=None))


        logger.info("-------------------------------------------------------------------------------------------------")
        logger.info("-------------------------------------------------------------------------------------------------")

        logger.info("----------------------------------------------2--------------------------------------------------")
        logger.info("keep all the jealous agens in list.")
        for li in graph:
            if owner_house.keys().__contains__(li) and not graph.has_edge(li, owner_house[li]):
                jealous.append(li)
        logger.info("jealous agents are:")
        logger.info(jealous)

        labeled = []
        logger.info("----------------------------------------------2(1.a)---------------------------------------------")
        logger.info("connect jealous people to the min house they have edge to.")
        graph = connect_jealous_agents_to_there_best(jealous, graph)
        logger.info(nx.to_dict_of_dicts(graph, edge_data=None))
        logger.info("-------------------------------------------------------------------------------------------------")

        for je in jealous:
            labeled.append(je)
            labeled.append(owner_house[je])
        logger.info("----------------------------------------------2(1.b)---------------------------------------------")
        logger.info("connect satisfied agents to the closest label agent.")
        graph = connect_satisfied_agents_to_their_preferred_house(graph, owner_house, labeled)
        logger.info(nx.to_dict_of_dicts(graph, edge_data=None))

        logger.info("Change houses owners in SCC.")
        graph = if_SCC_change_owners(graph, owner_house)
        logger.info(nx.to_dict_of_dicts(graph, edge_data=None))

        logger.info("-------------------------------------------------------------------------------------------------")
        logger.info("-------------------------------------------------------------------------------------------------")
    logger.info("List with agents and their new house after redistribution: %s \n", owner_house)
    return owner_house





top_trading_cycles_with_indifferences.logger = logger


def stringify(d: Dict) -> str:
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


def make_graph_begin(PreferenceLists: Dict, owner_house: Dict) -> nx.DiGraph:
    """
    O(n^2)
    This func make graph with agents and houses nodes and connect between them with edges.
    The edges connect between agents to the houses they prefer and between the houses to agent owners.
    :param PreferenceLists:dictionary that give a order list from top to low choices prefer houses.
    keys = agent, values = prefer list of houses.
    :param owner_house:dictionary that connect between the houses to their owners.
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


def make_stack(graph: nx.DiGraph, node, visited: list, stack: list):
    """
    start with one node in the graph ,add to stack him and all the nodes
    that connected components to him.
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :param visited:list with all the nodes that already visited.
    :param node: node in the graph that we run over all this Neighbors and call this func(make_stack) with them.
    :return:stack with all connected components nodes to the first node.
    """

    visited.append(node)
    for i in graph[node]:
        if i not in visited:
            make_stack(graph, i, visited, stack)
    stack.append(node)


def DFS(graph: nx.DiGraph, node, visited: list, DFS_list: list) -> list:
    """
    O(|V|+|E|)
    this func return list of dfs nodes.
    this func run in recurs and add to DFS_list all the nodes that are in the same dfs.
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :param node:node in the graph.
    :param visited:list with all the nodes we already visited.
    :param DFS_list:dfs list nodes that begin in node.
    :return:DFS_list .
    >>> graph = {'1': {'a': {}}, 'b': {'3': {}}, '2': {'b': {}}, 'c': {'1': {}}, '3': {'c': {}}, 'a': {'2': {}}}
    >>> node = '1'
    >>> visited = []
    >>> DFS_list = []
    >>> DFS(graph, node, visited, DFS_list)
    ['1', 'a', '2', 'b', '3', 'c']
    >>> graph = {'1': {'a': {}}, 'b': {'3': {}}, '2': {'b': {}}, 'c': {'1': {}}, '3': {'c': {}}, 'a': {'2': {}}}
    >>> node = '3'
    >>> visited = []
    >>> DFS_list = []
    >>> DFS(graph, node, visited, DFS_list)
    ['3', 'c', '1', 'a', '2', 'b']
    >>> graph = {'1': {'a': {}}, 'b': {}, '2': {'b': {}}, 'a': {'2': {}}, '3': {'c': {}}, 'c': {'3': {}}}
    >>> node = '1'
    >>> visited = []
    >>> DFS_list = []
    >>> DFS(graph, node, visited, DFS_list)
    ['1', 'a', '2', 'b']
    >>> graph = {'1': {'a': {}}, 'b': {}, '2': {'b': {}}, 'a': {'2': {}}, '3': {'c': {}}, 'c': {'3': {}}}
    >>> node = '3'
    >>> visited = []
    >>> DFS_list = []
    >>> DFS(graph,node,visited,DFS_list)
    ['3', 'c']
    """
    # Mark the current node as visited and print it
    visited.append(node)
    DFS_list.append(node)
    # Recur for all the vertices adjacent to this vertex
    for i in graph[node]:
        if i not in visited:
            DFS(graph, i, visited, DFS_list)
    return DFS_list


def are_all_agents_satisfied(graph, owner_house: Dict) -> bool:
    """
    O(n)
    check if there aren't jealous agents in the graph return 1 else 0.
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :param owner_house:dictionary that connect between the houses to their owners.keys = agent, values = houses.
    :return:true if all the agents in the graph are satisfied, else false.
    >>> PreferenceLists = {'1': [{'a', 'b', 'c'}],'2': [{'a', 'b', 'c'}],'3': [{'a', 'b', 'c'}]}
    >>> house = {'1': 'a','2': 'b','3': 'c'}
    >>> graph = make_graph_begin(PreferenceLists, house)
    >>> are_all_agents_satisfied(graph, house)
    True
    >>> PreferenceLists = {'1': [{'b'}],'2': [{'a', 'b', 'c'}],'3': [{'a', 'b', 'c'}]}
    >>> house = {'1': 'a','2': 'b','3': 'c'}
    >>> graph = make_graph_begin(PreferenceLists, house)
    >>> are_all_agents_satisfied(graph, house)
    False
    """
    for li in graph:
        if owner_house.keys().__contains__(li) and not graph.has_edge(li, owner_house[li]):
            return False
    return True


def if_SCC_change_owners(graph, owner_house: Dict) -> nx.DiGraph:
    """
    part 2(1.b)
    this func run over all SCC in the graph and replace the houses owners in this SCC(that every agents in SCC will be satisfied) .
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :param owner_house:dictionary that connect between the houses to their owners.keys = agent, values = houses.
    :return: update graph.
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

    gr = graph.reverse()
    visited = []
    HostHouse = []
    for o in owner_house.values():
        HostHouse.append(o)
    while stack:
        i = stack.pop()
        if not visited.__contains__(i):
            ListOfLists = []
            List = DFS(gr, i, visited, ListOfLists)
            if len(List) > 1:
                length = len(List)
                for mmm in range(length):
                    if HostHouse.__contains__(List[mmm]):
                        owner_house[List[(mmm + 1) % len(List)]] = List[mmm]
                        graph.remove_edge(List[mmm], List[mmm - 1])
                        graph.add_edge(List[mmm], List[(mmm + 1) % len(List)])
    return graph


def find_satisfied_SCC(graph: nx.DiGraph, owner_house: Dict, PreferenceLists: Dict) -> nx.DiGraph:
    """
    part 1(b)
    find SCC that all the agents are satisfied and point only to this SCC, if this SCC maintains this remove all the
    agents and houses that find in this SCC from the graph.update all the connected between the agents and houses and do
    this again until there is no END SCC.
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :param owner_house:dictionary that connect between the houses to their owners.keys = agent, values = houses.
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
        gr = graph.reverse()

        visited = []
        while stack and not change:
            i = stack.pop()
            if i not in visited:
                if owner_house.keys().__contains__(i):
                    ListOfLists = []
                    # Strongly Connected Components
                    List = DFS(gr, i, visited, ListOfLists)
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


def connect_jealous_agents_to_there_best(jealous: list, graph: nx.DiGraph) -> nx.DiGraph:
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



def connect_satisfied_agents_to_their_preferred_house(graph: nx.DiGraph, owner_house: Dict, labeled: list) -> nx.DiGraph:
    """
    part 2(1.b)
    O(n^2)
     keep only one edge between all satisfied agents to labeled agent.
    :param graph:diGraph with agents and houses nodes and edges that connect between them.
    :param owner_house:dictionary that connect between the houses to their owners.keys = agent, values = houses.
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
    >>> graph = connect_satisfied_agents_to_their_preferred_house(graph, house, [ '3', '4', 'd', 'c'])
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
    >>> graph = connect_satisfied_agents_to_their_preferred_house(graph, house, [ '1', '2', 'b', 'a'])
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


def Change_preferences_by_numbers_to_preferences_by_order(PreferenceLists: Dict) -> Dict:
    """
    O(n^2*log(n))
    :param owner_house:dictionary that connect between the houses to their owners.
    keys = agent, values = houses.
    :param PreferenceLists:dictionary with agent's keys and the houses values with number how much the agent appraiser the houses.
    keys = agent, values = houses with number.
    :return:call top_trading_cycles_with_indifferences func with order PreferenceLists and owner houses.
    >>> PreferenceLists = {1: {'a': 3, 'b': 3}, 2: {'a': 5, 'b': 1}}
    >>> Change_preferences_by_numbers_to_preferences_by_order(PreferenceLists)
    {1: [['a', 'b']], 2: ['a', 'b']}
    >>> PreferenceLists = {1: {'b': 3, 'a': 2}, 2: {'c': 5, 'b': 1}, 3:{'d':9, 'c':8},4:{'d':3}}
    >>> Change_preferences_by_numbers_to_preferences_by_order(PreferenceLists)
    {1: ['b', 'a'], 2: ['c', 'b'], 3: ['d', 'c'], 4: ['d']}
    >>> PreferenceLists = {1: {'b': 3, 'a': 2}, 2: {'c': 5, 'b': 1}, 3:{'d':9, 'c':8},4:{'a':3}}
    >>> Change_preferences_by_numbers_to_preferences_by_order(PreferenceLists)
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
    logger.setLevel(logging.INFO)

    import doctest
    doctest.run_docstring_examples(DFS, globals())
    doctest.run_docstring_examples(stringify,  globals())
    doctest.run_docstring_examples(make_graph_begin, globals())
    doctest.run_docstring_examples(make_graph, globals())
    doctest.run_docstring_examples(if_SCC_change_owners, globals())
    doctest.run_docstring_examples(top_trading_cycles_with_indifferences, globals())
    doctest.run_docstring_examples(connect_satisfied_agents_to_their_preferred_house, globals())
    doctest.run_docstring_examples(connect_jealous_agents_to_there_best, globals())
    doctest.run_docstring_examples(find_satisfied_SCC, globals())
    doctest.run_docstring_examples(are_all_agents_satisfied, globals())
    doctest.run_docstring_examples(Change_preferences_by_numbers_to_preferences_by_order, globals())
