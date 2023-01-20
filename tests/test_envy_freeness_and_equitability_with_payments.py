import unittest
from fairpy import Allocation
from fairpy.items.envy_freeness_and_equitability_with_payments import make_envy_freeness_and_equitability_with_payments


class MyTestCase(unittest.TestCase):
    def test_make_envy_freeness_and_equitability_with_payments(self):
        # test1
        self.eval_1 = {"a": {"x": 40, "y": 20, "r": 30, "xy":65, "rx": 80, "rxy": 100}, "b": {"x": 10, "y":30, "r": 70, "xy":55, "rx": 79, "rxy": 90}}
        self.allocation_1 = {"a": ["y"], "b": ["x", "r"]}
        self.ans1 = make_envy_freeness_and_equitability_with_payments(evaluation=self.eval_1,
                                                               allocation=Allocation(agents=["a", "b"],
                                                                                     bundles=self.allocation_1))
        self.assertEqual(self.ans1, {'allocation': {'a': ['y', 'r', 'x'], 'b': []}, 'payments': {'a': 50.0, 'b': -50.0}})

        # test2
        self.eval_2 = {"A": {"x": 70}, "B": {"x": 60}, "C": {"x": 40}, "D": {"x": 80}, "E": {"x": 55}}
        self.allocation_2 = {"A": ["x"], "B": [], "C": [], "D": [], "E": []}
        self.ans2 = make_envy_freeness_and_equitability_with_payments(evaluation=self.eval_2,
                                                               allocation=Allocation(agents=["A", "B", "C", "D", "E"],
                                                                                     bundles=self.allocation_2))
        self.assertEqual(self.ans2, {'allocation': {'A': [], 'B': [], 'C': [], 'D': ['x'], 'E': []},
                                        'payments': {'A': -16.0, 'B': -16.0, 'C': -16.0, 'D': 64.0, 'E': -16.0}})

        # test3
        eq_value = {"x": 10, "y": 5, "z": 15, "xy": 15, "yz": 20, "xz": 25}
        self.eval_3 = {"A": eq_value, "B": eq_value, "C": eq_value, "D": eq_value}
        self.allocation_3 = {"A": ["x"], "B": ["y"], "C": ["z"], "D": []}
        self.ans3 = make_envy_freeness_and_equitability_with_payments(evaluation=self.eval_3,
                                                               allocation=Allocation(agents=["A", "B", "C", "D"],
                                                                                     bundles=self.allocation_3))
        self.assertEqual(self.ans3, {'allocation': {'A': ['x'], 'B': ['y'], 'C': ['z'], 'D': []},
                                    'payments': {'A': 2.5, 'B': -2.5, 'C': 7.5, 'D': -7.5}})

        #test4
        a = {"x": 15, "y": 20, "z": 10, "w": 5, "xy": 45, "xz": 25, "wx": 20, "yz": 30, "yw": 30, "zw": 20,
                   "xyz": 50, "xyw": 50, "xzw": 30, "yzw": 40, "wxyz": 50}
        b = {"x": 30, "y": 35, "z": 22, "w": 7, "xy": 65, "xz": 55, "wx": 40, "yz": 60, "yw": 45, "zw": 30,
                   "xyz": 90, "xyw": 75, "xzw": 65, "yzw": 65, "wxyz": 95}
        c = {"x": 40, "y": 12, "z": 13, "w": 21, "xy": 55, "xz": 55, "wx": 65, "yz": 25, "yw": 35, "zw": 35,
                  "xyz": 65, "xyw": 75, "xzw": 75, "yzw": 50, "wxyz": 90}
        d = {"x": 5, "y": 7, "z": 17, "w": 19, "xy": 12, "xz": 25, "wx": 25, "yz": 25, "yw": 30, "zw": 36,
                   "xyz": 30, "xyw": 35, "xzw": 45, "yzw": 45, "wxyz": 50}
        self.eval_4 = {"A": a, "B": b, "C": c, "D": d}
        self.allocation_4 = {"A": ["x"], "B": ["y"], "C": ["z"], "D": ["w"]}
        self.ans4 = make_envy_freeness_and_equitability_with_payments(evaluation= self.eval_4,
                                                               allocation=Allocation(agents=["A", "B", "C", "D"],
                                                                                     bundles= self.allocation_4))
        self.assertEqual(self.ans4, {'allocation': {'A': [], 'B': ['y', 'x', 'z'], 'C': ['w'], 'D': []},
                                    'payments': {'A': -27.75, 'B': 62.25, 'C': -6.75, 'D': -27.75}})


if __name__ == '__main__':
    unittest.main()