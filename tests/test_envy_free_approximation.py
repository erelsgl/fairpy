import unittest, pytest
import numpy as np
from fairpy import Allocation, ValuationMatrix, AllocationMatrix
from fairpy.items.envy_free_approximation_with_payments import make_envy_free_approximation_with_payments, find_envy_free_approximation_with_payments


def calculateSW(res: dict, v: ValuationMatrix):
    """
    get social walfarm of allocation
    """
    if isinstance(res, dict):
        bundles = res['allocation']
        items_values = [v[i][item] for i, item in zip(range(len(bundles)), [l[0] for l in bundles])]
        return sum(items_values)
    elif isinstance(res, Allocation):
        items_values = res.utility_profile()
        return sum(items_values)


def bundle_value(idx: int, d: dict, v: ValuationMatrix):
    """
    get value of bundle by valuation function of idx agent.
    """
    ans = 0
    if d["allocation"][idx]:
        ans = sum(v[idx][i] for i in d["allocation"][idx])
    return ans - d["payments"][idx]


def bundle_value_subjective(own: int, other: int, d: dict, v: ValuationMatrix):
    """
    get value of bundle of other agent by valuation function of own agent.
    """
    ans = 0
    if d["allocation"][other]:
        ans = sum(v[own][i] for i in d["allocation"][other])
    return ans - d["payments"][other]


def agent_is_EF(idx: int, d: dict, v: ValuationMatrix):
    """
    check if idx agent is envy-free.
    """
    value = bundle_value(idx, d, v)
    for i in range(len(d["allocation"])):
        if bundle_value_subjective(idx, i, d, v) > value:
            return False
    return True


class TestApproximationDivison(unittest.TestCase):
    def setUp(self) -> None:
        self.v = [[15, 10, 90, 35],
                  [35, 21, 95, 48],
                  [9, 28, 5, 72],
                  [4, 25, 28, 75]]
        self.v2 = [[50, -10, 72, 22, -15, -30],
                   [-62, -24, 10, 71, 20, -10],
                   [10, 13, -45, 36, 41, -60],
                   [-34, 12, 10, -14, -6, -5],
                   [-11, -20, 10, 38, 17, 12],
                   [14, 32, 5, -7, -9, 15]]  # 50-24-45-14+17+15

        self.a1 = np.eye(len(self.v), len(self.v[0]))
        self.allocationBefore1 = Allocation(agents=ValuationMatrix(self.v),
                                            bundles=AllocationMatrix(self.a1))
        self.allocationResult1 = make_envy_free_approximation_with_payments(self.allocationBefore1)
        self.a2 = np.eye(len(self.v2), len(self.v2[0]))
        self.allocationBefore2 = Allocation(agents=ValuationMatrix(self.v2),
                                            bundles=AllocationMatrix(self.a2))
        x = self.allocationBefore2.utility_profile()
        self.allocationResult2 = make_envy_free_approximation_with_payments(self.allocationBefore2)

    def test_sw(self):
        """
        check that SW of forst allocation <= SW of result allocation
        """
        self.assertLessEqual(calculateSW(self.allocationBefore1, self.v),
                             calculateSW(make_envy_free_approximation_with_payments(self.allocationBefore1), self.v))
        self.assertLessEqual(calculateSW(self.allocationBefore2, self.v2),
                             calculateSW(self.allocationResult2, self.v2))

    @pytest.mark.skip("takes too long for pytest")
    def test_init(self):
        """
        check that algorithm run for many agents and bundles.
        """
        for i in range(1, 11):
            shape = (i * 10, i * 10)
            v = np.random.randint(-i * 10, i * 10, size=shape)
            self.assertIsNotNone(find_envy_free_approximation_with_payments(ValuationMatrix(v), eps=0.1))

    def test_ef(self):
        """
        chaeck that all agents are envy-free.
        """
        for i in range(len(self.allocationResult1["allocation"])):
            self.assertTrue(agent_is_EF(i, self.allocationResult1, ValuationMatrix(self.v)))
        for i in range(len(self.allocationResult2["allocation"])):
            self.assertTrue(agent_is_EF(i, self.allocationResult2, ValuationMatrix(self.v2)))

    def test_edge_cases(self):
        # 0 bundles
        matrix = np.zeros((10, 10))
        self.assertIsNotNone(find_envy_free_approximation_with_payments(ValuationMatrix(matrix), eps=0.1))

        # 1 bundle
        for i in range(1, 21):
            matrix = np.random.randint(-1 * 10, i * 10, i * 5).reshape(-1, 1)
            self.assertIsNotNone(find_envy_free_approximation_with_payments(ValuationMatrix(matrix), eps=0.1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
