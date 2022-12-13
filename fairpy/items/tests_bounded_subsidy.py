import unittest

from items.Bounded_Subsidy import bounded_subsidy


class TestMain(unittest.TestCase):
    
    def test_goods(self):
        """
        This test passes without implementation of Bounded Subsidy algorithem
        """
        agents1 = ["Alice", "Bob"]
        goods1 = ["a", "b", "c", "d", "e", "f", "g"]
        weights1 = {agents1[0]: {"a": 2, "b": 6, "c": 3, "d":1,"e":4,"f":7,"g":12}, 
                   agents1[1]: {"a": 3, "b": 5, "c": 4, "d":1,"e":2,"f":10,"g":15}}
        
        ans1 = bounded_subsidy(agents1, goods1, weights1)
        self.assertEqual(ans1, {"Alice": ["b", "c"], "Bob": ["a", "d"]})


        agents2 = ["Alice", "Bob"]
        goods2 = ["a", "b", "c", "d", "e", "f"]
        weights2 = {agents2[0]: {"a":1, "b":0.8, "c":0.5, "d":1, "e":0.3, "f":0}, agents2[1]: {"a":0.9, "b":0.2, "c":0.4, "d":0.7, "e":1, "f":0}}

        ans2 = bounded_subsidy(agents2, goods2, weights2)
        self.assertEqual(ans2, {"Alice": ["a", "b", "c"], "Bob": ["d", "e", "f"]})


        ### nothing to allocate
        agents3 = ["Alice", "Bob"]
        goods3 = []
        weights3 = {agents3[0]: {}, agents3[1]: {}}

        ans3 = bounded_subsidy(agents3, goods3, weights3)
        self.assertEqual(ans3, {"Alice": [], "Bob": []})


    if __name__ == '__main__':
        unittest.main()

