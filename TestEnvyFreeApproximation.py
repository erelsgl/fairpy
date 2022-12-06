import unittest
from typing import List, Any

import numpy as np

from fairpy import Allocation, Valuation, ValuationMatrix, AllocationMatrix, compute_agent_bundle_value_matrix
from envy_free_approximation_division import envy_free_approximation


# import numpy as np


def calculateSW(res: dict, v: ValuationMatrix):
    """
    get social walfarm of allocation
    """
    items_values = payments = 0
    if isinstance(res, dict):
        payments = sum(res['payment'])
        items_values = sum(v[i, item] for i, item in zip(range(len(res)), [l[0] for l in res]))
    elif isinstance(res, Allocation):
        payments = 0
        items_values = sum(res.utility_profile())

    return items_values - payments


def bundle_value(idx: int, d: dict):
    return sum(d["bundles"][idx]) - d["payments"][idx]


def agent_is_EF(idx: int, d: dict):
    value = bundle_value(idx, d)
    for i in range(len(d["bundles"])):
        if bundle_value(i, d) <= value:
            return False
    return True


class TestApproximationDivison(unittest.TestCase):
    def setUp(self):
        self.v = [[15, 10, 90, 35],
                  [35, 21, 95, 48],
                  [9, 28, 5, 72],
                  [4, 25, 28, 75]]
        self.v2 = [[50, -10, 72, 22, -15, -30],
                   [-62, -24, 10, 71, 20, -10],
                   [10, 13, -45, 36, 41, -60],
                   [-34, 12, 10, -7, -6, -5]]
        self.a1 = np.zeros_like(self.v).tolist()
        for i in range(len(self.a1)):
            self.a1[i][i] = 1
        self.allocationBefore1 = Allocation(agents=ValuationMatrix(self.v),
                                            bundles=AllocationMatrix(self.a1))
        self.allocationResult1 = envy_free_approximation(self.allocationBefore1)
        self.a2 = np.zeros_like(self.v2).tolist()
        for i in range(len(self.a2)):
            self.a2[i][i] = 1
        self.allocationBefore2 = Allocation(agents=ValuationMatrix(self.v2),
                                            bundles=AllocationMatrix(self.a2))
        self.allocationResult2 = envy_free_approximation(self.allocationBefore2)

    def test_sw(self):
        self.assertLessEqual(calculateSW(self.allocationBefore1, self.v),
                             calculateSW(envy_free_approximation(self.allocationBefore1), self.v))
        self.assertLessEqual(calculateSW(self.allocationBefore2, self.v2),
                             calculateSW(envy_free_approximation(self.allocationBefore2), self.v2))

    def test_init(self):
        mat = [[1 + x + y * 50 for x in range(50)] for y in range(50)]
        amt = np.zeros_like(mat).tolist()
        for i in range(len(amt)):
            amt[i][i] = 1
        alloc = Allocation(agents=ValuationMatrix(mat),
                           bundles=AllocationMatrix(amt))
        self.assertIsNotNone(envy_free_approximation(alloc))
        mat2 = [[1 + x + y * 100 for x in range(100)] for y in range(100)]
        amt2 = np.zeros_like(mat).tolist()
        for i in range(len(amt2)):
            amt2[i][i] = 1
        alloc2 = Allocation(agents=ValuationMatrix(mat2),
                            bundles=AllocationMatrix(amt2))
        self.assertIsNotNone(envy_free_approximation(alloc2))

    def test_ef(self):
        for i in range(len(self.allocationResult1["bundles"])):
            self.assertTrue(agent_is_EF(i, self.allocationResult1))
        for i in range(len(self.allocationResult2["bundles"])):
            self.assertTrue(agent_is_EF(i, self.allocationResult2))

if __name__ == '__main__':
    unittest.main()
# v = [[15, 10, 90, 35],
#      [35, 21, 95, 48],
#      [9, 28, 5, 72],
#      [4, 25, 28, 75]]
# # z = ["X", "y", "z", "w"]
# # dic = {k: {v} for k in range(4), v in range(4)}
# agent_dict = {"A": {"x": 15, "y": 10, "z": 90, "w": 35},
#               "B": {"x": 35, "y": 21, "z": 95, "w": 48},
#               "C": {"x": 9, "y": 28, "z": 5, "w": 72},
#               "D": {"x": 4, "y": 25, "z": 28, "w": 75}}
# AllocationBefore = Allocation(agents=ValuationMatrix(v),
#                               bundles=AllocationMatrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))
# print(calculateSW(AllocationBefore,ValuationMatrix(v)))
# # print(AllocationBefore.utility_profile())
