import unittest


class Data:
    def __init__(self,catagories:list, agents_evaluation:dict,items:set):
        self._catagories = catagories
        self._items = items
        self._agents_evaluation = agents_evaluation

def ef1_algorithm(agents_names:list, f: Data) :#-> bundles.Bundle
    allocation = {a:set() for a in agents_names}; allocation_sum = {a:0 for a in agents_names} ; sigma = [a for a in agents_names]
    for category in f._catagories:
        Bh = greedy_round_robin(category ,f._items, sigma , f._agents_evaluation)
        for agent in agents_names:
            allocation[agent].update(Bh[agent])
            allocation_sum[agent] += sum(value for key, value in f._agents_evaluation[agent][category].items() if key in allocation[agent])
        allocation, allocation_sum, sigma = envy_graph_l1(category, allocation, sigma)

def greedy_round_robin(category:str, items:set, agents:list, agents_evaluation:dict) -> dict:#-> bundles.Bundle
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