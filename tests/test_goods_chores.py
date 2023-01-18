"""
    "Fair allocation of indivisible goods and chores" by  Ioannis Caragiannis ,
    Ayumi Igarashi, Toby Walsh and Haris Aziz.(2021) ,
    Programmers: Yair Raviv , Rivka Strilitz
"""

import unittest
from random import randint

from fairpy.items.goods_chores import *
import itertools


def is_continuous(allocation:list , items : list):
    """
    >>> is_continuous([], ['a'])
    True

    >>> is_continuous(['a'], [])
    False

    >>> is_continuous(['a', 'b', 'c'], ['f', 'a', 'b', 'c'])
    True

    >>> is_continuous(['a', 'b', 'c'], ['f', 'a', 'b', 'd', 'c'])
    False
    """
    # print(allocation)
    if len(allocation) == 0:
        return True
    index = -1
    item1 = allocation[0]
    # find the first item of the agent in the items list
    for i in range(len(items)):
        if item1 == items[i]:
            index = i
            break
    if index == -1:
        return False
    # check if the agent's bundle is continuous
    for item in allocation:
        if not item == items[index]:
            return False
        index += 1
    return True


def is_PO(agents: AgentList, result: dict):
    """
    This function checks for 2 agents if the given allocation is Paretto optimal or not.
    The algorithm compare the allocation to the all other allocations and check if there is another allocation
    That provides Paretto improvement.
    >>> is_PO(AgentList({"Agent1":{"item_1":0}, "Agent2":{"item_1":1}}), {'Agent1': [], 'Agent2': ["item_1"]})
    True

    >>> is_PO(AgentList({"Agent1":{"item_1":0}, "Agent2":{"item_1":1}}), {'Agent1': ["item_1"], 'Agent2': []})
    False

    >>> is_PO(AgentList({"Agent1":{"item_1":0,"item_2":-1}, "Agent2":{"item_1":1,"item_2":3}}), {'Agent1': [], 'Agent2': ["item_1", "item_2"]})
    True

    >>> is_PO(AgentList({"Agent1":{"item_1":1,"item_2":-1}, "Agent2":{"item_1":-1,"item_2":1}}), {'Agent1': ["item_1"], 'Agent2': ["item_2"]})
    True

    >>> is_PO(AgentList({"Agent1":{"item_1":1,"item_2":-1}, "Agent2":{"item_1":-1,"item_2":1}}), {'Agent1': ["item_2"], 'Agent2': ["item_1"]})
    False
    """

    try:
        winner = agents[0]
        looser = agents[1]
        winner_utility = sum([winner.value(item) for item in result['Agent1']])
        looser_utility = sum([looser.value(item) for item in result['Agent2']])
    except:
        raise 'Invalid arguments'
    all_items = set(result['Agent1'] + result['Agent2'])
    for i in range(len(all_items) +1):
        for bundle in itertools.combinations(all_items, i):
            W_utility = sum([winner.value(item) for item in bundle])
            L_utility = sum([looser.value(item) for item in all_items if item not in bundle])
            notPoWinner = W_utility > winner_utility and L_utility >= looser_utility
            notPoLooser = W_utility >= winner_utility and L_utility > looser_utility
            if notPoWinner or notPoLooser:
                return False
    return True


class Goods_Chores_Tests(unittest.TestCase):
        # ---------------------------------------------------Tests for algo 1-----------------------------------------
    def test1(self):
        #only good chores
        exm = AgentList({"Agent1": {"item_1": 1, "item_2": 8, "item_3": 1, "item_4": 2}, "Agent2": {"item_1": 2, "item_2": 6, "item_3": 7, "item_4": 6},"Agent3": {"item_1": 4, "item_2": 2, "item_3": 2, "item_4": 2}})
        res = Double_RoundRobin_Algorithm(exm)
        self.assertEqual(res, {'Agent1': ['item_2'], 'Agent2': ['item_3'], 'Agent3': ['item_1', 'item_4']})

    def test2(self):
        # only bad chores
        exm = AgentList({"Agent1": {"item_1": -1, "item_2": -5, "item_3": -1, "item_4": 0}, "Agent2": {"item_1": -5, "item_2": -4, "item_3": -7, "item_4": -6},
                          "Agent3": {"item_1": -4, "item_2": 0, "item_3": -2, "item_4": 0}})
        res = Double_RoundRobin_Algorithm(exm)
        self.assertEqual(res, {'Agent1': ['item_4', 'item_1'], 'Agent2': ['item_2'], 'Agent3': ['item_3']})


    def test3(self):
        exm = AgentList({"Agent1": {"item_1": 1, "item_2": 0, "item_3": -1, "item_4": 2}, "Agent2": {"item_1": 2, "item_2": 6, "item_3": 0, "item_4": 0},
                          "Agent3": {"item_1": 0, "item_2": 2, "item_3": -2, "item_4": 2}})
        res = Double_RoundRobin_Algorithm(exm)
        self.assertEqual(res, {'Agent1': ['item_3', 'item_4'], 'Agent2': ['item_1'], 'Agent3': ['item_2']})


    # ---------------------------------------------------Tests for algo 2 -----------------------------------------


    def test4(self):
        exm = AgentList({"Agent1": {"item_1": 1, "item_2": 0, "item_3": -1, "item_4": 2}, "Agent2": {"item_1": 2, "item_2": 6, "item_3": 0, "item_4": 0}})
        res = Generalized_Adjusted_Winner_Algorithm(exm)
        self.assertEqual(res, {'Agent1': ["item_1", "item_4"], 'Agent2': ["item_2", "item_3"]})


    def test5(self):
        exm = AgentList({"Agent1":{"item_1":1,"item_2":-1,"item_3":-2,"item_4":3,"item_5":5,"item_6":0,"item_7":0,"item_8":-1,"item_9":2,"item_10":3},"Agent2":{"item_1":-3,"item_2":4,"item_3":-6,"item_4":2,"item_5":4,"item_6":-3,"item_7":2,"item_8":-2,"item_9":4,"item_10":5}})
        res = Generalized_Adjusted_Winner_Algorithm(exm)
        self.assertEqual(res, {'Agent1': ["item_1" , "item_4", "item_5", "item_6", "item_9", "item_10"], 'Agent2': ["item_2", "item_3", "item_7", "item_8"]})

    def test6(self):
        exm = AgentList({"Agent1": {"item_1": -1, "item_2": 0, "item_3": -1, "item_4": -2},"Agent2": {"item_1": -2, "item_2": -6, "item_3": 0, "item_4": 0}})

        res = Generalized_Adjusted_Winner_Algorithm(exm)

        self.assertEqual(res, {'Agent1': ["item_2"], 'Agent2': ["item_1", "item_3", "item_4"]})

    def test7(self):
        exm = AgentList({"Agent1": {"item_1": -1, "item_2": 0, "item_3": -1, "item_4": -2},"Agent2": {"item_1": -2, "item_2": -6, "item_3": 0, "item_4": 0}})
        res = Generalized_Adjusted_Winner_Algorithm(exm)
        self.assertTrue(is_PO(exm , res))

        # --------------------------------------------------- Tests for algo 3 -----------------------------------------

    # large input and continuous validation
    def test8(self):
        agents = {}
        prop = {}
        result = {}
        prop_shares = []
        for i in range(1,100):
            agentI = "Agent" + str(i)
            agents[agentI] = {}
            sum = 0
            for j in range(1, 1001):
                agents[agentI][str(j)] = randint(-10, 10)
                sum += agents[agentI][str(j)]
            prop[agentI] = sum/100
            result[agentI] = []
        res = Generalized_Moving_knife_Algorithm(agent_list=AgentList(agents) ,items =  [str(i) for i in range(1,1001)])
        for allocation in res:
            self.assertTrue(is_continuous(res[allocation] , items =  [str(i) for i in range(1,1001)]))

    # large random input and prop1 validation
    def test9(self):
        agents = {}
        prop = {}
        result = {}
        prop_shares = []
        for i in range(100):
            agentI = "Agent"+str(i)
            agents[agentI] = {}
            s = 0
            for j in range(1,1001):
                agents[agentI][str(j)] = randint(-10,10)
                s += agents[agentI][str(j)]
            prop[agentI] = s / 1000
            result[agentI] = []
            prop_shares.append(sum(list(agents[agentI].values()))/1000)
        res = Generalized_Moving_knife_Algorithm(agent_list=AgentList(agents) ,items =  [str(i) for i in range(1,1001)])
        for i in range(100):
            maxim = -10
            minim = 10
            agentI = "Agent" + str(i)
            for j in range(1,1001):
                if str(j) not in res[agentI] and agents[agentI][str(j)] >= maxim:
                    maxim = int(agents[agentI][str(j)])
                if str(j) in res[agentI] and agents[agentI][str(j)] <= minim:
                    minim = int(agents[agentI][str(j)])
            plus1 = prop[agentI] + (maxim/100)
            minus1 = prop[agentI] - (minim/100)
            sum_res_i = sum([int(x) for x in res[agentI]])
            self.assertTrue(sum_res_i >= prop[agentI] or sum_res_i >= plus1 or sum_res_i >= minus1)





if __name__ == '__main__':
    unittest.main()
