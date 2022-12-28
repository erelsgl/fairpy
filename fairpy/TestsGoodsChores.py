import unittest
import sys
from random import randint

from fairpy import *
from fairpy.agentlist import AgentList
from fairpy.goods_chores import *
import itertools


def is_continuous(allocation:list , items : list):
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


def is_PO(agents:AgentList , result:dict):
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
            L_utility = sum([winner.value(item) for item in all_items if item not in bundle])
            notPoWinner = W_utility > winner_utility and L_utility >= looser_utility
            notPoLooser = W_utility >= winner_utility and L_utility > looser_utility
            if notPoWinner or notPoLooser:
                return False
    return True


class Mytes(unittest.TestCase):
        # ---------------------------------------------------Tests for algo 1-----------------------------------------
    def test1(self):
        #only good chores
        exm = AgentList({"Agent1": {"1": 1, "2": 8, "3": 1, "4": 2}, "Agent2": {"1": 2, "2": 6, "3": 7, "4": 6},"Agent3": {"1": 4, "2": 2, "3": 2, "4": 2}})
        res = Double_RoundRobin_Algorithm(exm)
        self.assertEqual(res, {'Agent1': [2], 'Agent2': [3], 'Agent3': [1, 4]})

    def test2(self):
        # only bad chores
        exm = AgentList({"Agent1": {"1": -1, "2": -5, "3": -1, "4": 0}, "Agent2": {"1": -5, "2": -4, "3": -7, "4": -6},
                          "Agent3": {"1": -4, "2": 0, "3": -2, "4": 0}})
        res = Double_RoundRobin_Algorithm(exm)
        self.assertEqual(res, {'Agent1': [4, 1], 'Agent2': [2], 'Agent3': [3]})


    def test3(self):
        exm = AgentList({"Agent1": {"1": 1, "2": 0, "3": -1, "4": 2}, "Agent2": {"1": 2, "2": 6, "3": 0, "4": 0},
                          "Agent3": {"1": 0, "2": 2, "3": -2, "4": 2}})
        res = Double_RoundRobin_Algorithm(exm)
        self.assertEqual(res, {'Agent1': [3, 4], 'Agent2': [1], 'Agent3': [2]})


    # ---------------------------------------------------Tests for algo 2 -----------------------------------------


    def test4(self):
        exm = AgentList({"Agent1": {"1": 1, "2": 0, "3": -1, "4": 2}, "Agent2": {"1": 2, "2": 6, "3": 0, "4": 0}})
        res = Generalized_Adjusted_Winner_Algorithm(exm)
        self.assertEqual(res, {'Agent1': ['1', '4'], 'Agent2': ['2', '3']})


    def test5(self):
        exm = AgentList({"Agent1":{"1":1,"2":-1,"3":-2,"4":3,"5":5,"6":0,"7":0,"8":-1,"9":2,"10":3},"Agent2":{"1":-3,"2":4,"3":-6,"4":2,"5":4,"6":-3,"7":2,"8":-2,"9":4,"10":5}})
        res = Generalized_Adjusted_Winner_Algorithm(exm)
        self.assertEqual(res, {'Agent1': ['1' , '4', '5', '6', '9', '10'], 'Agent2': ['2', '3', '7', '8']})

    def test6(self):
        exm = AgentList({"Agent1": {"1": -1, "2": 0, "3": -1, "4": -2},"Agent2": {"1": -2, "2": -6, "3": 0, "4": 0}})

        res = Generalized_Adjusted_Winner_Algorithm(exm)

        self.assertEqual(res, {'Agent1': ['2'], 'Agent2': ['1', '3', '4']})

    def test7(self):
        exm = AgentList({"Agent1": {"1": -1, "2": 0, "3": -1, "4": -2},"Agent2": {"1": -2, "2": -6, "3": 0, "4": 0}})
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
