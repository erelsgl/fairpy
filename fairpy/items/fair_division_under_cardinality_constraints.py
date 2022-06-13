import unittest
import networkx as nx
import copy
import pprint
import doctest
import itertools

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
        self._agents_evaluation = a_evaluation
        

def ef1_algorithm(agents_names:list, f: Data) -> dict:
    """
    in paper - Algorithm 1 ALG 1
    this algorithm returns a bundel of agents when each of the holds the best allocation to his valuation of the goods.
    :param m a list of items
    :param f data obj, hold all other information about agents, evaluation, and items.
    :return a bundel of agents each containing a fair allocation of the goods that said agent desired the most.(that is ef1 fair)

    >>> agents_evaluation ={"a": {"trees": {"oak":9,"sprouce":8,"mango":2},"doors":{"white":8,"black":1,"green":5}}, "b":{"trees": {"oak":10,"sprouce":5,"mango":0},"doors":{"white":1,"black":4,"green":9}},"c":{"trees": {"oak":0,"sprouce":10,"mango":6},"doors":{"white":4,"black":6,"green":7}}}
    >>> catagories  = ["trees", "doors"]
    >>> items = {"trees":{"oak","sprouce","sakoia","mango"},"doors":{"white","black","red","green"}}
    >>> agents_names = ['a','b','c']
    >>> answer =  ef1_algorithm(agents_names , Data(catagories, agents_evaluation, items))
    >>> answer['a']
    {'trees': {'oak'}, 'doors': {'white'}}
    >>> answer['b']
    {'trees': {'sprouce'}, 'doors': {'black'}}
    >>> answer['c']
    {'trees': {'mango'}, 'doors': {'green'}}
    """
    # Initialize parameters, each to zero-values. 
    allocation, sigma= {a:{k:set() for k in f._catagories} for a in agents_names}, [a for a in agents_names]
    for category in f._catagories:
        envy_graph = nx.DiGraph()
        # As stated in the paper, iterating over each category 
        Bh = greedy_round_robin(category ,f._items, sigma , f._agents_evaluation)
        # Bh an allocation returned from Greedy-Round-Robin algorithm, stated in the paper.
        {key:allocation[key][category].update(Bh[key]) for key in allocation.keys()}
        # coping results for later uses.
        for agent in agents_names:
            # adding nodes to envy graph, initialize the graph. 
            envy_graph.add_node( agent ,bundel = allocation[agent])
        #changing the order of the agents, using the topology of the envy graph.
        sigma = lemma_1(envy_graph, f._agents_evaluation, allocation, category, sigma, f._items)
    # this for loop is to assign the total amount of value each agent got for each category (from all items)
    return allocation   

def greedy_round_robin(category:str, items:set, agents:list, agents_evaluation:dict) -> dict:
    """
    in paper - Algorithm 2 Greedy-Round-Robin (ALG 2)
    this algorithm divides all of the item in each category.
    :param catag the category that will be divided.
    :param Vi hold all of the agents and their preferences.
    :return an updated bundel of the agents.
    >>> agents_evaluation ={"a": {"trees": {"oak":9,"sprouce":8,"mango":2},"doors":{"white":8,"black":1,"green":5}}, "b":{"trees": {"oak":10,"sprouce":5,"mango":0},"doors":{"white":1,"black":4,"green":9}},"c":{"trees": {"oak":0,"sprouce":10,"mango":6},"doors":{"white":4,"black":6,"green":7}}}
    >>> catagories  = ["trees", "doors"]
    >>> items = {"trees":{"oak","sprouce","sakoia","mango"},"doors":{"white","black","red","green"}}
    >>> agents_names = ['a','b','c']

    >>> greedy_round_robin('trees', items, agents_names, agents_evaluation)
    {'a': {'oak'}, 'b': {'sprouce'}, 'c': {'mango'}}

    >>> greedy_round_robin('doors', items, agents_names, agents_evaluation)
    {'a': {'white'}, 'b': {'green'}, 'c': {'black'}}
    """
    # Greedy-Round-Robin from paper, 
    index =0
    allocation, M = {a:set() for a in agents}, {k for k in agents_evaluation[agents[index]][category].keys()}
    while len(M) != 0:
        # while M is not empty try to give each agent by the order given, the item he hold dearest in the current category.
        for i in range(len(set(M))):
            agent_name = agents[index % len(agents)]
            evaluation_arr = dict({key:value for key, value in agents_evaluation[agent_name][category].items() if key in M})
            max_item = max(evaluation_arr, key =lambda x: evaluation_arr[x])
            allocation[agent_name].add(max_item)
            M.discard(max_item)
            index += 1
    return allocation

def lemma_1(envy_graph:nx.DiGraph, evaluation:dict, allocation:dict, category:str, sigma:list, items:set) -> list:
    """
    this method is being called from the main algorithm, to achieve EF1 allocation we must make sure there are no 
    cycles in the envy graph. 
    :param bun_agents a bundel of agents.
    >>> import networkx as nx
    >>> envy_graph = nx.DiGraph()
    >>> for agent in agents_names:
    ...     envy_graph.add_node(agent)
    >>> evaluation ={"a": {"trees": {"oak":9,"sprouce":8,"mango":2},"doors":{"white":8,"black":1,"green":5}}, "b":{"trees": {"oak":10,"sprouce":5,"mango":0},"doors":{"white":1,"black":4,"green":9}},"c":{"trees": {"oak":0,"sprouce":10,"mango":6},"doors":{"white":4,"black":6,"green":7}}}
    >>> category  = "trees" 
    >>> items = {"trees":{"oak","sprouce","sakoia","mango"},"doors":{"white","black","red","green"}}
    >>> sigma = ['a','b','c']
    >>> allocation ={'a': {'trees': {'oak'}, 'doors': set()}, 'b': {'trees': {'sprouce'}, 'doors': set()}, 'c': {'trees': {'mango'}, 'doors': set()}}
    >>> generate_envy(envy_graph, evaluation, category, allocation)
    >>> lemma_1(envy_graph, evaluation, allocation, category, sigma, items)
    ['c', 'b', 'a']


    >>> envy_graph = nx.DiGraph()
    >>> for agent in agents_names:
    ...     envy_graph.add_node(agent)
    >>> agents_evaluation = {"a": {"trees": {"oak":9,"sprouce":8,"sakoia":0,"mango":2},"doors":{"white":8,"black":1,"red":4,"green":5}},"b":{"trees": {"oak":10,"sprouce":5,"sakoia":0,"mango":0},"doors":{"white":1,"black":4,"red":2,"green":9}},"c":{"trees": {"oak":0,"sprouce":10,"sakoia":9,"mango":0},"doors":{"white":4,"black":6,"red":3,"green":7}}}
    >>> category  = "trees" 
    >>> items = {"trees":{"oak","sprouce","sakoia","mango"},"doors":{"white","black","red","green"}}
    >>> sigma = ['a','b','c']
    >>> allocation ={'a': {'trees': {'oak'}, 'doors': set()}, 'b': {'trees': {'sprouce'}, 'doors': set()}, 'c': {'trees': {'mango'}, 'doors': set()}}
    >>> generate_envy(envy_graph, evaluation, category, allocation)
    >>> lemma_1(envy_graph, evaluation, allocation, category, sigma, items)
    ['c', 'b', 'a']
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
        permutations = [list(x) for x in itertools.permutations(sigma)]
        permutations.remove(sigma)
        for p in list(permutations):
            somthing = greedy_round_robin(category ,items, p , evaluation)
            envy_graph.clear_edges()
            for key in allocation.keys():
                allocation[key][category] = set()
            {key:allocation[key][category].update(somthing[key]) for key in allocation.keys()}
            generate_envy(envy_graph, evaluation, category, allocation)
            if (list(nx.simple_cycles(envy_graph))):
                permutations.remove(p)
            else: return list(nx.topological_sort(envy_graph))
    else: 
        return list(nx.topological_sort(envy_graph))

def generate_envy(envy_graph:nx.DiGraph, evaluation:dict, category:str, allocation:dict):
    # simple method for loop on all agents, checking each agent as follows:
    # allocation = {'alice' : {'oak'}, 'bob':{'sakoia'}, 'eve':{"sprouce"}}
    # we define envy as alice's evaluation of her allocations,
    # so if eval(alice(oak)) < eval(alice(sakoia)) then alice is envious of bob, and so one.  

    for agent_u in allocation.keys():
        for agent_v in allocation.keys():
            if agent_u != agent_v:
                u_eval = sum_values(agent_u, evaluation, category, allocation[agent_u])
                v_eval = sum_values(agent_u, evaluation, category, allocation[agent_v])
                if v_eval > u_eval :
                    envy_graph.add_edge(agent_u, agent_v)

def sum_values(agent_name:str, evaluation:dict, category:str, allocations:set) -> int:
    #simple method for calculating the sum of all values (values of one agent from the PERSPECTIVE of another)
    return sum([sum(evaluation[agent_name][category][item] for x in evaluation[agent_name][category] if x == item )for item in allocations[category]])

if __name__ == "__main__":
    # this is a test for branching
    agents_evaluation = {
                "a": {"trees": {"oak":9,"sprouce":8,"sakoia":0,"mango":2},"doors":{"white":8,"black":1,"red":4,"green":5}}, 
                "b":{"trees": {"oak":10,"sprouce":5,"sakoia":0,"mango":0},"doors":{"white":1,"black":4,"red":2,"green":9}},
                "c":{"trees": {"oak":0,"sprouce":10,"sakoia":9,"mango":0},"doors":{"white":4,"black":6,"red":3,"green":7}}
                    }
    catagories  = ["trees", "doors"]
    items = {"trees":{"oak","sprouce","sakoia","mango"},"doors":{"white","black","red","green"}}
    agents_names = ['a','b','c']
    d = Data(catagories, agents_evaluation, items)
    allocation = ef1_algorithm(agents_names,d)
    doctest.testmod()
    # pprint.pprint(allocation)

 