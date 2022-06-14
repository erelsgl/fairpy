#!python3

from .undercut_procedure import undercut
import unittest
import fairpy


class TestAlgo(unittest.TestCase):
    def setUp(self):
        self.allocation={}
        
    def test_normal_cases(self):
        
        Alice = ({"a": 7, "b": 4, "c": 3, "d":2})
        Bob = ({"a": 1, "b": 7, "c": 3, "d":2})
        items=['a','b','c','d']
        
        A = fairpy.agents.AdditiveAgent({"a": 7, "b": 4, "c": 3, "d":2}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 1, "b": 7, "c": 3, "d":2}, name="Bob")
        allocation = undercut([Alice,Bob],items)
        self.assertEqual(allocation, "Alice gets ['a', 'd'] with value 9.\nBob gets ['b', 'c'] with value 10.\n")
        
        
        A = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Bob")
        allocation = undercut([{"a": 8, "b": 7, "c": 6, "d":3},{"a": 8, "b": 7, "c": 6, "d":3}],['a','b','c','d'])
        self.assertEqual(allocation, "There is no envy-free division")
    

    def test_special_cases(self):
        
        #no objects
        A = fairpy.agents.AdditiveAgent({}, name="Alice")
        B = fairpy.agents.AdditiveAgent({}, name="Bob")
        allocation = undercut([{},{}],[])
        self.assertEqual(allocation, "Alice gets [] with value 0.\nBob gets [] with value 0.\n")
        
        #same values
        A = fairpy.agents.AdditiveAgent({"a": 4, "b": 4, "c": 4, "d":4}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 4, "b": 4, "c": 4, "d":4}, name="Bob")
        allocation = undercut([{"a": 4, "b": 4, "c": 4, "d":4},{"a": 4, "b": 4, "c": 4, "d":4}],['a','b','c','d'])
        self.assertEqual(allocation, "Alice gets ['a', 'd'] with value 8.\nBob gets ['b', 'c'] with value 8.\n")
        
        
        A = fairpy.agents.AdditiveAgent({"a": 1,"b": 2, "c": 3, "d":4,"e": 5, "f":14}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a":1,"b": 1, "c": 1, "d":1,"e": 1, "f":7}, name="Bob")
        allocation = undercut([{"a": 1,"b": 2, "c": 3, "d":4,"e": 5, "f":14},{"a":1,"b": 1, "c": 1, "d":1,"e": 1, "f":7}],['a','b','c','d','e','f'])  
        self.assertEqual(allocation, "Alice gets ['a', 'b', 'c', 'd', 'e'] with value 15.\nBob gets ['f'] with value 7.\n")
        
        #no allocation
        A = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Bob")
        allocation = undercut([{"a": 8, "b": 7, "c": 6, "d":3},{"a": 8, "b": 7, "c": 6, "d":3}],['a','b','c','d'])
        self.assertEqual(allocation, "There is no envy-free division")

    def test_envy_free(self):
      
        
        A = fairpy.agents.AdditiveAgent({"a": 7, "b": 4, "c": 3, "d":2}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 1, "b": 7, "c": 3, "d":2}, name="Bob")
        self.assertTrue(A.is_EF({'a', 'c', 'd'}, [{"b"},{"a","d"},{"b","c"}]))
        self.assertTrue(B.is_EF({"b"}, [{'a', 'c', 'd'},{"a","d"},{"c"}]))
        self.assertFalse(B.is_EF({"a","d"}, [{"a","d"},{"b","c"}]))

        A = fairpy.agents.AdditiveAgent({"a": 7, "b": 4, "c": 3, "d":2}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 7, "b": 1, "c": 3, "d":2}, name="Bob")
        self.assertTrue(A.is_EF({"b","c","d"}, [{"a"},{"b","c","d"}]))
        self.assertTrue(B.is_EF({"a"}, [{"a"},{"b","c","d"}]))

        A = fairpy.agents.AdditiveAgent({"a": 5, "b": 5, "c": 5, "d":5}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 5, "b": 5, "c": 5, "d":5}, name="Bob")
        self.assertTrue(A.is_EF({"a","b"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]))
        self.assertTrue(B.is_EF({"c","d"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]))

        A = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Bob")
        self.assertFalse(A.is_EF({"a","b"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]) and B.is_EF({"d","c"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]))
        self.assertFalse(B.is_EF({"a","c"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]) and  A.is_EF({"b","d"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]))

        A = fairpy.agents.AdditiveAgent({"a": 5}, name="Alice")
        B = fairpy.agents.AdditiveAgent({"a": -4}, name="Bob")
        self.assertTrue(A.is_EF({"a"}, [{},{"a"}]))
        self.assertTrue(B.is_EF({},[{},{"a"}]))

        A = fairpy.agents.AdditiveAgent({}, name="Alice")
        B = fairpy.agents.AdditiveAgent({}, name="Bob")
        self.assertTrue(A.is_EF({}, [{}]))
        self.assertTrue(B.is_EF({}, [{}]))

if __name__ == '__main__':
    unittest.main()