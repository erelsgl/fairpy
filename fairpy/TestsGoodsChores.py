import unittest
import sys
from random import randint

from fairpy import *
from fairpy.agentlist import AgentList
from fairpy.goods_chores import Double_RoundRobin_Algorithm, Generalized_Adjusted_Winner_Algorithm, Generalized_Moving_knife_Algorithm


def is_continuous(allocation):
    for i in range(len(allocation) -1):
        if not (int(allocation[i]) == (int(allocation[i+1])+1)):
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
    def test6(self):
        agents = {}
        prop_shares = []
        for i in range(10000):
            agentI = "Agent" + str(i)
            agents[agentI] = {}
            for j in range(1, 6):
                agents[agentI][str(j)] = randint(-10, 10)
        res = Generalized_Moving_knife_Algorithm(agents)
        for allocation in res:
            self.assertTrue(is_continuous(allocation))

    # large random input and prop1 validation
    def test7(self):
        agents = {}
        prop_shares = []
        for i in range(10000):
            agentI = "Agent"+str(i)
            agents[agentI] = {}
            for j in range(1,6):
                agents[agentI][str(j)] = randint(-10,10)
            prop_shares.append((sum(agents[agentI].values()))/10000)
        res = Generalized_Moving_knife_Algorithm(agents)
        for i in range(10000):
            max = -10
            min = 10
            agentI = "Agent" + str(i)
            for j in range(1,6):
                if j not in res[i] and agents[agentI][j] >= max:
                    max = agents[agentI][j]
                if j in res[i] and agents[agentI][j] <= min:
                    min = agents[agentI][j]
            plus1 = prop_shares[i] + max/10000
            minus1 = prop_shares[i] - min/10000
            self.assertTrue(sum(res[i]) >= prop_shares[i] or sum(res[i]) >= plus1 or sum(res[i]) <= minus1)


if __name__ == '__main__':
    unittest.main()