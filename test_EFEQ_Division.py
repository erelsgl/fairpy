import unittest
import numpy as np

from fairpy import Allocation, AllocationMatrix, ValuationMatrix
from envy_freeness_and_equitability_with_payments import envy_freeness_and_equitability_with_payments
from test_EnvyFreeApproximation import agent_is_EF, agent_is_EQ, calculateSW


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.v = [[0, 15, 23, 14],
                  [41, 17, 32, 68],
                  [35, 9, 16, 14],
                  [24, 32, 11, 3]]
        self.v2 = [[-14, 2, 54, -39, 4, 10],
                   [21, 85, -19, -28, -14, 26],
                   [10, 13, 36, 11, 36, 84],
                   [-34, 12, 10, -28, 18, 12],
                   [-10, 13, -8, 11, 18, -19],
                   [14, 41, 32, 14, -54, 52]]
        self.a1 = np.zeros_like(self.v).tolist()
        for i in range(len(self.a1)):
            self.a1[i][i] = 1
        self.allocationBefore1 = Allocation(agents=ValuationMatrix(self.v),
                                            bundles=AllocationMatrix(self.a1))
        self.allocationResult1 = envy_freeness_and_equitability_with_payments(self.allocationBefore1)
        self.a2 = np.zeros_like(self.v2).tolist()
        for i in range(len(self.a2)):
            self.a2[i][i] = 1
        self.allocationBefore2 = Allocation(agents=ValuationMatrix(self.v2),
                                            bundles=AllocationMatrix(self.a2))
        self.allocationResult2 = envy_freeness_and_equitability_with_payments(self.allocationBefore2)

    def test_sw(self):
        """
        check that SW of forst allocation <= SW of result allocation
        """
        self.assertLessEqual(calculateSW(self.allocationBefore1, self.v),
                             calculateSW(envy_freeness_and_equitability_with_payments(self.allocationBefore1), self.v))
        self.assertLessEqual(calculateSW(self.allocationBefore2, self.v2),
                             calculateSW(envy_freeness_and_equitability_with_payments(self.allocationBefore2), self.v2))

    def test_init(self):
        """
        check that algorithm run for many agents and bundles.
        """
        mat = [[1 + x + y * 50 for x in range(50)] for y in range(50)]
        amt = np.zeros_like(mat).tolist()
        for i in range(len(amt)):
            amt[i][i] = 1
        alloc = Allocation(agents=ValuationMatrix(mat),
                           bundles=AllocationMatrix(amt))
        self.assertIsNotNone(envy_freeness_and_equitability_with_payments(alloc))
        mat2 = [[1 + x + y * 100 for x in range(100)] for y in range(100)]
        amt2 = np.zeros_like(mat).tolist()
        for i in range(len(amt2)):
            amt2[i][i] = 1
        alloc2 = Allocation(agents=ValuationMatrix(mat2),
                            bundles=AllocationMatrix(amt2))
        self.assertIsNotNone(envy_freeness_and_equitability_with_payments(alloc2))

    def test_ef(self):
        """
        chaeck that all agents are envy-free.
        """
        for i in range(len(self.allocationResult1["bundles"])):
            self.assertTrue(agent_is_EF(i, self.allocationResult1, ValuationMatrix(self.v)))
        for i in range(len(self.allocationResult2["bundles"])):
            self.assertTrue(agent_is_EF(i, self.allocationResult2, ValuationMatrix(self.v2)))

    def test_eq(self):
        """
        check that utility of each agent equal to utility of each other agent.
        """
        for i in range(len(self.allocationResult1["bundles"])):
            assert agent_is_EQ(i, self.allocationResult1, ValuationMatrix(self.v))
        for i in range(len(self.allocationResult2["bundles"])):
            assert agent_is_EQ(i, self.allocationResult2, ValuationMatrix(self.v2))


if __name__ == '__main__':
    unittest.main()
