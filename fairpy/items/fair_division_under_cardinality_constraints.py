# from fairpy import bundles 
# from fairpy import agents
# from fairpy import allocations 
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
    def __init__(self,catagories:list, a_evaluation:dict,items:set):
        """"
        :param catagories, a list (of strings).
        :param goods_and_values, a specification dictionary for each agent. 

        """
        self._catagories = catagories
        self._items = items
        self._agents_evaluation = agents_evaluation
        

def ef1_algorithm(agents_names:list, f: Data) :#-> bundles.Bundle
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
    allocation = {a:set() for a in agents_names}; allocation_sum = {a:0 for a in agents_names} ; sigma = [a for a in agents_names]
    for category in f._catagories:
        Bh = greedy_round_robin(category ,f._items, sigma , f._agents_evaluation)
        for agent in agents_names:
            allocation[agent].update(Bh[agent])
            allocation_sum[agent] += sum(value for key, value in f._agents_evaluation[agent][category].items() if key in allocation[agent])
        allocation, allocation_sum, sigma = envy_graph_l1(category, allocation, sigma)

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
    index = 0;allocation ={a:set() for a in agents} ;M = {k for k in agents_evaluation[agents[index]][category].keys()}
    while len(M) != 0:
        for i in range(len(set(M))):
            agent = agents[index % len(agents)]
            temp = dict({k:v for k,v in agents_evaluation[agent][category].items() if k in M})
            item =  max(temp, key =lambda x: temp[x])
            allocation[agent].add(item)
            M.discard(item)
            index += 1
    return allocation

def envy_graph_l1(category:str, allocation:dict, sigma:list) -> (dict, dict, list):#  -> bundles.Bundle
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

if __name__ == "__main__":
    agents_evaluation ={"a": {"trees": {"oak":6,"sprouce":9,"sakoia":4,"mango":2},"doors":{"white":8,"black":1,"red":4,"green":5}}, 
                "b":{"trees": {"oak":7,"sprouce":6,"sakoia":7,"mango":5},"doors":{"white":1,"black":4,"red":2,"green":9}}
            }
    catagories  = ["trees", "doors"]
    items = {"trees":{"oak","sprouce","sakoia","mango"},"doors":{"white","black","red","green"}}
    agents_names = ['a','b']
    d = Data(catagories,agents_evaluation,items)
    ef1_algorithm(agents_names,d)
    pass