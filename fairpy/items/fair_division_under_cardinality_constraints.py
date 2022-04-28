from fairpy import bundles 
from fairpy import agents
from fairpy import allocations 
import unittest

"""
This Python file represent the paper named  Fair Division Under Cardinality Constraints
Authors - Arpita Biswas, Siddharth Barman
At - https://arxiv.org/pdf/1804.09521.pdf
"""

class Data:
    """
    data should hold all given catagories of item, including each Agenets name and his evaluation for each item.
    """
    def __init__(self,catagories:list, goods_and_values:dict):
        """"
        :param catagories, a list (of strings).
        :param goods_and_values, a specification dictionary for each agent. 

        """
        self._catagories = catagories
        self._goods = goods_and_values

def ef1_algorithm(m:list, f: Data) -> bundles.Bundle:
    """
    in paper - Algorithm 1 ALG 1
    this algorithm returns a bundel of agents when each of the holds the best allocation to his valuation of the goods.
    :param m a list of items
    :param f data obj, hold all other information about agents, evaluation, and items.
    :return a bundel of agents each containing a fair allocation of the goods that said agent desired the most.(that is ef1 fair)

    >>> catagories = catalog1 = ["trees", "doors"]
    >>> dict_goods1 = {"trees": {"oak":6,"sprouce":9,"sakoia":4,"mango":2},"doors":{"white":8,"black":1,"red":4,"green":5}}
    >>> data = Data(catagories,dict_goods1)
    >>> m
    ["a","b"]
    >>> answer =  ef1_algorithm(m ,data)
    >>> answer['a'] 
    {{"trees":["sprouce","skoia"],"doors":["white","red"]}}
    >>> answer['b']
    {{"trees":["oak","mango"],"doors":["green","black"]}}
    """
    pass

def greedy_round_robin(catag :dict, Vi:dict, agents:dict) -> bundles.Bundle:
    """
    in paper - Algorithm 2 Greedy-Round-Robin (ALG 2)
    this algorithm divides all of the item in each category.
    :param catag the category that will be divided.
    :param Vi hold all of the agents and their preferences.
    :return an updated bundel of the agents.

    >>> agents
    {"a":[],"b":[]}
    >>> catag
    {"trees": {"oak":6,"sprouce":9,"sakoia":4,"mango":2}}

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
    isenvy =[]

    """
    pass

def envy_graph_l1(agents:dict,catag :dict) -> bundles.Bundle:
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
    pass