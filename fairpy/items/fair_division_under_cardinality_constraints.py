# from fairpy import bundles 
# from fairpy import agents
# from fairpy import allocations 
import unittest
import networkx as nx
import copy
import pprint
"""
This Python file represent the paper named  Fair Division Under Cardinality Constraints
Authors - Arpita Biswas, Siddharth Barman
At - https://arxiv.org/pdf/1804.09521.pdf
"""

class Data:
    """
    data should hold all given catagories of item, including each Agenets name and his evaluation for each item.
    """
    def __init__(self,catagories:list, a_evaluation:dict,items:set):
        """"
        :param catagories, a list (of strings).
        :param goods_and_values, a specification dictionary for each agent. 

        """
        self._catagories = catagories
        self._items = items
        self._agents_evaluation = agents_evaluation
        

def ef1_algorithm(agents_names:list, f: Data) -> dict:
    """
    in paper - Algorithm 1 ALG 1
    this algorithm returns a bundel of agents when each of the holds the best allocation to his valuation of the goods.
    :param m a list of items
    :param f data obj, hold all other information about agents, evaluation, and items.
    :return a bundel of agents each containing a fair allocation of the goods that said agent desired the most.(that is ef1 fair)

    >>> agents_names
    ["a","b"]
    >>> catagories  = ["trees", "doors"]
    >>> dict_goods ={"a": {"trees": {"oak":6,"sprouce":9,"sakoia":4,"mango":2},"doors":{"white":8,"black":1,"red":4,"green":5}}, 
                "b":{"trees": {"oak":7,"sprouce":6,"sakoia":7,"mango":5},"doors":{"white":1,"black":4,"red":2,"green":9}}
            }
    >>> data = Data(catagories,dict_goods)
    >>> answer =  ef1_algorithm(agents_names ,data)
    >>> answer['a'] 
    {{"trees":["sprouce","skoia"],"doors":["white","red"]}}
    >>> answer['b']
    {{"trees":["oak","mango"],"doors":["green","black"]}}
    """
    # Initialize parameters, each to zero-values. 
    allocation, sigma, envy_graph, value = {a:{k:set() for k in f._catagories} for a in agents_names}, [a for a in agents_names], nx.DiGraph(), 0
    for category in f._catagories:
        # As stated in the paper, iterating over each category 
        Bh = greedy_round_robin(category ,f._items, sigma , f._agents_evaluation)
        # Bh an allocation returned from Greedy-Round-Robin algorithm, stated in the paper.
        {key:allocation[key][category].update(Bh[key]) for key in allocation.keys()}
        # coping results for later uses.
        for agent in agents_names:
            # adding nodes to envy graph, initialize the graph. 
            envy_graph.add_node( agent ,bundel = allocation[agent])
        #changing the order of the agents, using the topology of the envy graph.
        sigma = lemma_1(envy_graph, f._agents_evaluation, allocation, category, sigma)
    # this for loop is to assign the total amount of value each agent got for each category (from all items)
    for agent in agents_names:
        for category in f._agents_evaluation[agent].keys():
            for item in f._agents_evaluation[agent][category]:
                if item in allocation[agent][category]:
                    value += f._agents_evaluation[agent][category][item]
            allocation[agent]['total'] = {category:value}
            value = 0
    return allocation   


def greedy_round_robin(category:str, items:set, agents:list, agents_evaluation:dict) -> dict:#-> bundles.Bundle
    """
    in paper - Algorithm 2 Greedy-Round-Robin (ALG 2)
    this algorithm divides all of the item in each category.
    :param catag the category that will be divided.
    :param Vi hold all of the agents and their preferences.
    :return an updated bundel of the agents.

    >>> agents
    {"a":[],"b":[]}
    >>> items
    {"trees":{"oak","sprouce","sakoia","mango"},"doors":{"white","black","red","green"}}

    iteration 1:
    >>> agents
    {"a":["sprouce"],"b":[]}

    iteration 2:
    >>> agents
    {"a":["sprouce"],"b":["oak"]}

    iteration 3:
    >>> agents
    {"a":["sprouce","sakoia"],"b":["oak"]}

    iteration 4:
    >>> agents
    {"a":["sprouce","sakoia"],"b":["oak","mango"]}

    >>> isenvy = envy_graph_l1(bundles.Bundle(agents))
    (two agents cant envy)
    isenvy ={}}
    """
    # Greedy-Round-Robin from paper, 
    index =0
    allocation, M = {a:set() for a in agents}, {k for k in agents_evaluation[agents[index]][category].keys()}
    while len(M) != 0:
        # while M is not empty try to give each agent by the order given, the item he hold dearest in the current category.
        for i in range(len(set(M))):
            agent_name = agents[index % len(agents)]
            evaluation_arr = dict({key:value for key, value in agents_evaluation[agent_name][category].items() if key in M})
            max_item =  max(evaluation_arr, key =lambda x: evaluation_arr[x])
            allocation[agent_name].add(max_item)
            M.discard(max_item)
            index += 1
    return allocation

def lemma_1(envy_graph:nx.DiGraph, evaluation:dict, allocation:dict, category:str, sigma:list) -> list:
    """
    this method is being called from the main algorithm, to achieve EF1 allocation we must make sure there are no 
    cycles in the envy graph. 
    :param bun_agents a bundel of agents.

    # agents = {"a":["sprouce","sakoia"],"b":["oak","mango"]}
    # catag = {"trees": {"oak":6,"sprouce":9,"sakoia":4,"mango":2}}
    >>> if len(agnets.keys()) > 3:
    >>> sums = {}
    >>> envy = 0
    >>> for agnt in agents.keys():
    >>>     for val in agents[angt]:  
    >>>         sums[agnt] += val    
    >>> else: return []
    """
    # lemma_1 - remove cycles from graph using networkx, and changing the order of the agents byt the topology of the graph.  
    # algorithm:
        # if graph has cycles:
            # check what node is not in loop(can be more then one)
            # choose one node (that is not in the loop) at random, and one that is (at radom)
            # change their allocations.
            # if graph has cycles:
                # didn't work change back
                # else : return this graph and order.  
    generate_envy(envy_graph, evaluation, category, allocation)
    if (list(nx.simple_cycles(envy_graph))):
        cycles = list(nx.simple_cycles(envy_graph))
        for loop in cycles:
            for node in loop:
                rest_of_nodes = set(sigma).difference(set(loop))
                for other in rest_of_nodes:
                    if not envy_graph.has_edge(node, other):
                        current_g = nx.DiGraph(envy_graph)
                        current_a = allocation
                        change_allocation(envy_graph, node, other, evaluation, allocation, category)
                        if(list(nx.simple_cycles(envy_graph))):
                            envy_graph = current_g
                            allocation = current_a
                        else:
                            # from networkx return the order for next allocations.
                            return list(nx.topological_sort(envy_graph))
        sigma = lemma_1(envy_graph, evaluation, allocation, category, sigma)
    else:   
        return sigma

def change_allocation(envy_graph:nx.DiGraph, src:str, dst:str, evaluation:dict, allocation, category:str) -> dict:
    # simple method to switch allocations without losing any values.
    place_holder = allocation[dst][category]
    allocation[dst][category] = allocation[src][category]
    allocation[src][category] = place_holder
    generate_envy(envy_graph, evaluation, category, allocation)


def generate_envy(envy_graph:nx.DiGraph, evaluation:dict, category:str, allocation:dict):
    # first we remove all edges from graph so we wont have duplicates,
    # if agent named u envy'es an agent named v, add an edge (as stated in paper.)
    envy_graph.remove_edges_from(list(envy_graph.edges()))
    for agent_u in allocation.keys():
        for agent_v in allocation.keys():
            if agent_u != agent_v:
                u_eval = sum_values(agent_u, evaluation, category, allocation[agent_u])
                v_eval = sum_values(agent_v, evaluation, category, allocation[agent_u])
                if v_eval > u_eval :
                    envy_graph.add_edge(agent_u, agent_v)

def sum_values(agent_name:str, evaluation:dict, category:str, allocations:set) -> int:
    #simple method for calculating the sum of all values (values of one agent from the PERSPECTIVE of another)
    return sum([sum(evaluation[agent_name][category][item] for x in evaluation[agent_name][category] if x == item )for item in allocations[category]])

if __name__ == "__main__":
    agents_evaluation ={
                "a": {"trees": {"oak":8,"sprouce":9,"sakoia":9,"mango":2},"doors":{"white":8,"black":1,"red":4,"green":5}}, 
                "b":{"trees": {"oak":2,"sprouce":2,"sakoia":2,"mango":2},"doors":{"white":1,"black":4,"red":2,"green":9}},
                "c":{"trees": {"oak":2,"sprouce":5,"sakoia":8,"mango":7},"doors":{"white":4,"black":6,"red":3,"green":7}
            }}
    catagories  = ["trees", "doors"]
    items = {"trees":{"oak","sprouce","sakoia","mango"},"doors":{"white","black","red","green"}}
    agents_names = ['a','b','c']
    d = Data(catagories,agents_evaluation,items)
    pprint.pprint(ef1_algorithm(agents_names,d))