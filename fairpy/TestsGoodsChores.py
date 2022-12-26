import unittest
import sys
from random import randint

from fairpy import *
from fairpy.agentlist import AgentList
from fairpy.goods_chores import Double_RoundRobin_Algorithm, Generalized_Adjusted_Winner_Algorithm, Generalized_Moving_knife_Algorithm


def is_continuous(allocation:list):
    # print(allocation)
    for i in range(0,len(allocation) -1):
        if not (int(allocation[i])+1) == int(allocation[i+1]):
            return False
    return True


def is_PO(param):
    pass


class Mytes(unittest.TestCase):
        # ---------------------------------------------------Tests for algo 1-----------------------------------------
    def test1(self):
        #only good chores
        exm = AgentList({"Agent1": {"1": 1, "2": 8, "3": 1, "4": 2}, "Agent2": {"1": 2, "2": 6, "3": 7, "4": 6},
                          "Agent3": {"1": 4, "2": 2, "3": 2, "4": 2}})
        res = Double_RoundRobin_Algorithm(exm)
        self.assertEqual(res, {"Agent1": ["2","4"], "Agent2": ["3"], "Agent3": ["1"]})

    def test2(self):
        # only bad chores
        exm = AgentList({"Agent1": {"1": -1, "2": -5, "3": -1, "4": 0}, "Agent2": {"1": -5, "2": -4, "3": -7, "4": -6},
                          "Agent3": {"1": -4, "2": 0, "3": -2, "4": 0}})
        res = Double_RoundRobin_Algorithm(exm)
        self.assertEqual(res, {"Agent1": ["3", "4"], "Agent2": ["1"], "Agent3": ["2"]})


    def test3(self):
        exm = AgentList({"Agent1": {"1": 1, "2": 0, "3": -1, "4": 2}, "Agent2": {"1": 2, "2": 6, "3": 0, "4": 0},
                          "Agent3": {"1": 0, "2": 2, "3": -2, "4": 2}})
        res = Double_RoundRobin_Algorithm(exm)
        self.assertEqual(res, {"Agent1": ["1","3"], "Agent2": ["2"], "Agent3": ["4"]})

    # ---------------------------------------------------Tests for algo 2 -----------------------------------------


    def test4(self):
        exm = AgentList({"Agent1": {"1": 1, "2": 0, "3": -1, "4": 2}, "Agent2": {"1": 2, "2": 6, "3": 0, "4": 0}})
        res = Generalized_Adjusted_Winner_Algorithm(exm)
        self.assertEqual(res, {"Agent1": ["4", "1"], "Agent2": ["3", "2"]})


    def test5(self):
        exm = AgentList({"Agent1":{"1":1,"2":-1,"3":-2,"4":3,"5":5,"6":0,"7":0,"8":-1,"9":2,"10":3},"Agent2":{"1":-3,"2":4,"3":-6,"4":2,"5":4,"6":-3,"7":2,"8":-2,"9":4,"10":5}})
        res = Generalized_Adjusted_Winner_Algorithm(exm)
        self.assertEqual(res, {"Agent1": ["6","1","4","10","5"], "Agent2": ["2","7","8","3","9"]})

    def test6(self):
        exm = AgentList({"Agent1": {"1": -1, "2": 0, "3": -1, "4": -2},

                         "Agent2": {"1": -2, "2": -6, "3": 0, "4": 0}})

        res = Generalized_Adjusted_Winner_Algorithm(exm)

        self.assertEqual(res, {"Agent1": ["2"], "Agent2": ["1", "3", "4"]})

    def test7(self):
        exm = AgentList({"Agent1": {"1": -1, "2": 0, "3": -1, "4": -2},

                         "Agent2": {"1": -2, "2": -6, "3": 0, "4": 0}})

        res = Generalized_Adjusted_Winner_Algorithm(exm)

        self.assertTrue(is_PO(AgentList({"Agent1": ["2"], "Agent2": ["1", "3", "4"]})))

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
        # print(agents)
        res = Generalized_Moving_knife_Algorithm(AgentList(agents) , prop_values=prop, remain_interval=[0,1000] , result=result)
        for allocation in res:
            self.assertTrue(is_continuous(res[allocation]))

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
        res = Generalized_Moving_knife_Algorithm(AgentList(agents) , prop_values=prop, remain_interval=[0,1000] , result=result)
        for i in range(100):
            maxim = -10
            minim = 10
            agentI = "Agent" + str(i)
            for j in range(1,1001):
                if str(j) not in res[agentI] and agents[agentI][str(j)] >= maxim:
                    maxim = int(agents[agentI][str(j)])
                if str(j) in res[agentI] and agents[agentI][str(j)] <= minim:
                    minim = int(agents[agentI][str(j)])
            plus1 = prop[agentI] + (maxim/10)
            minus1 = prop[agentI] - (minim/10)
            sum_res_i = sum([int(x) for x in res[agentI]])
            self.assertTrue(sum_res_i >= prop[agentI] or sum_res_i >= plus1 or sum_res_i >= minus1)


if __name__ == '__main__':
    unittest.main()
