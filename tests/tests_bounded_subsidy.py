import unittest
from fairpy.items.Bounded_Subsidy_Algorithem import *
from fairpy.agentlist import AgentList
import random
import string

class TestMain(unittest.TestCase):

    
    def test_Bounded_Subsidy(self):
        """
        Bounded Subsidy Algorithem tests
        """

        agents1 = AgentList({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10}})
        ans1 = Bounded_Subsidy(agents1)
        self.assertEqual(ans1, {"Alice": ["b", "c"], "Bob": ["d", "a"]})

        agents2 = AgentList({"Alice": {"a":10, "b":8, "c":5, "d":9, "e":3, "f":0}, "Bob": {"a":9, "b":2, "c":4, "d":7, "e":10, "f":0}}) 
        ans2 = Bounded_Subsidy(agents2)
        self.assertEqual(ans2, {'Alice': ['a', 'b', 'c'], 'Bob': ['e', 'd', 'f']})

        agents3 = AgentList({"Alice": {"a":5, "b":5}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
        ans3 = Bounded_Subsidy(agents3)
        self.assertEqual(ans3, {'Alice': ['a'], 'Bob': ['b'], 'Max': [], 'Nancy': []})

        ### nothing to allocate
        agents4 = AgentList({"Alice": {}, "Bob": {}})
        ans4 = Bounded_Subsidy(agents4)
        self.assertEqual(ans4, {"Alice": [], "Bob": []})

    def test_create_Envy_Graph(self):
        """
            tests for create_Envy_Graph function, that creates a Envy Graph
        """

        agents1 = AgentList({"Alice": {"a":3, "b":5}, "Bob": {"a":6, "b":7}})
        envy_graph1 = create_Envy_Graph(agents1)
        self.assertEqual(list(envy_graph1.edges.data()), [('Alice', 'Bob', {'weight': -2}), ('Bob', 'Alice', {'weight': 1})])
        
        agents2 = AgentList({"Alice": {"a":1, "b":5, "c":3}, "Bob": {"a":1, "b":3, "c":2}, "Max": {"a":3, "b":2, "c":1}})
        envy_graph2 = create_Envy_Graph(agents2)
        self.assertEqual(list(envy_graph2.edges.data()), [('Alice', 'Bob', {'weight': -2}), ('Alice', 'Max', {'weight': -4}), ('Bob', 'Alice', {'weight': 1}), ('Bob', 'Max', {'weight': -1}), ('Max', 'Alice', {'weight': -1}), ('Max', 'Bob', {'weight': -2})])

        agents3 = AgentList({"Alice": {"a":5, "b":6}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
        envy_graph3 = create_Envy_Graph(agents3)
        self.assertEqual(list(envy_graph3.edges.data()), [('Alice', 'Bob', {'weight': -1}), ('Alice', 'Max', {'weight': -6}), ('Alice', 'Nancy', {'weight': -6}), ('Bob', 'Alice', {'weight': 1}), ('Bob', 'Max', {'weight': -3}), ('Bob', 'Nancy', {'weight': -3}), ('Max', 'Alice', {'weight': 2}), ('Max', 'Bob', {'weight': 2}), ('Max', 'Nancy', {'weight': 0}), ('Nancy', 'Alice', {'weight': 1}), ('Nancy', 'Bob', {'weight': 2}), ('Nancy', 'Max', {'weight': 0})])

        agents4 = AgentList({"Alice": {"a":3, "b":5, "c":8}, "Bob": {"a":3, "b":10, "c":5}, "Max": {"a":1, "b":2, "c":10}, "Nancy": {"a":10, "b":10, "c":10}, "Eve": {"a":8, "b":7, "c":2}})
        envy_graph4 = create_Envy_Graph(agents4)
        self.assertEqual(list(envy_graph4.edges.data()), [('Alice', 'Bob', {'weight': 5}), ('Alice', 'Max', {'weight': 8}), ('Alice', 'Nancy', {'weight': 3}), ('Alice', 'Eve', {'weight': 0}), ('Bob', 'Alice', {'weight': -10}), ('Bob', 'Max', {'weight': -5}), ('Bob', 'Nancy', {'weight': -7}), ('Bob', 'Eve', {'weight': -10}), ('Max', 'Alice', {'weight': -10}), ('Max', 'Bob', {'weight': -8}), ('Max', 'Nancy', {'weight': -9}), ('Max', 'Eve', {'weight': -10}), ('Nancy', 'Alice', {'weight': -10}), ('Nancy', 'Bob', {'weight': 0}), ('Nancy', 'Max', {'weight': 0}), ('Nancy', 'Eve', {'weight': -10}), ('Eve', 'Alice', {'weight': 0}), ('Eve', 'Bob', {'weight': 7}), ('Eve', 'Max', {'weight': 2}), ('Eve', 'Nancy', {'weight': 8})])

    def test_check_positive_weight_directed_cycles(self):
        """
            tests for check_positive_weight_directed_cycles function, that checks if its envy graph does not contain a positive-weight directed cycle
        """

        agents1 = AgentList({"Alice": {"a":5, "b":3}, "Bob": {"a":4, "b":1}})
        envy_graph1 = create_Envy_Graph(agents1)
        res = check_positive_weight_directed_cycles(envy_graph1)
        self.assertEqual(res, False)

        agents2 = AgentList({"Alice": {"a": 3, "b": 2, "c": 1}, "Bob": {"a": 2, "b": 2, "c": 3}, "Max": {"a": 1, "b": 3, "c": 2}})
        envy_graph2 = create_Envy_Graph(agents2)
        res = check_positive_weight_directed_cycles(envy_graph2)
        self.assertEqual(res, False)

        agents3 = AgentList({"Alice": {"a":5, "b":6}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
        envy_graph3 = create_Envy_Graph(agents3)
        res = check_positive_weight_directed_cycles(envy_graph3)
        self.assertEqual(res, False)

        agents4 = AgentList({"Alice": {"a":4, "b":3, "c":2, "d":1}, "Bob": {"a":4, "b":3, "c":2, "d":1}, "Max": {"a":4, "b":3, "c":2, "d":1}, "Nancy": {"a":4, "b":3, "c":2, "d":1}})
        envy_graph4 = create_Envy_Graph(agents4)
        res = check_positive_weight_directed_cycles(envy_graph4)
        self.assertEqual(res, False)
        

    def test_cal_the_Subsidy(self):
        """
            tests for cal_the_Subsidy function, that calculates the Subsidy of the agentes
        """

        agents1 = AgentList({"Alice": {"a":3, "b":5}, "Bob": {"a":6, "b":7}})
        res = "Alice gets ['b'] with No Subsudy" + "\n" + "Bob gets ['a'] and it is envious of Alice with Subsudy of: 1" + "\n"
        self.assertEqual(cal_the_Subsidy(agents1), res)

        agents2 = AgentList({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10}})
        res = "Alice gets ['b', 'c'] with No Subsudy" + "\n" + "Bob gets ['d', 'a'] with No Subsudy" + "\n"
        self.assertEqual(cal_the_Subsidy(agents2), res)

        agents3 = AgentList({"Alice": {"a":1, "b":5, "c":3}, "Bob": {"a":1, "b":3, "c":2}, "Max": {"a":3, "b":2, "c":1}})
        res = "Alice gets ['b'] with No Subsudy" + "\n" + "Bob gets ['c'] and it is envious of Alice with Subsudy of: 1" + "\n" + "Max gets ['a'] with No Subsudy" + "\n"
        self.assertEqual(cal_the_Subsidy(agents3), res)

        agents4 = AgentList({"Alice": {"a":5, "b":6}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
        res = "Alice gets ['b'] with No Subsudy" + "\n" + "Bob gets ['a'] and it is envious of Alice with Subsudy of: 1" + "\n" + "Max gets [] and it is envious of Bob with Subsudy of: 3" + "\n" + "Nancy gets [] and it is envious of Bob with Subsudy of: 3" + "\n"
        self.assertEqual(cal_the_Subsidy(agents4), res)

        agents5 = AgentList({"Alice": {"a":4, "b":3, "c":2, "d":1}, "Bob": {"a":4, "b":3, "c":2, "d":1}, "Max": {"a":4, "b":3, "c":2, "d":1}, "Nancy": {"a":4, "b":3, "c":2, "d":1}})
        res = "Alice gets ['d'] and it is envious of Bob with Subsudy of: 3" + "\n" + "Bob gets ['c'] and it is envious of Alice with Subsudy of: 2" + "\n" + "Max gets ['b'] and it is envious of Alice with Subsudy of: 1" + "\n" + "Nancy gets ['a'] with No Subsudy" + "\n"
        self.assertEqual(cal_the_Subsidy(agents5), res)

    ############ random number of agents and items ############
        random_item = random.choice(string.ascii_lowercase)
        random_item_weight = random.randint(0, 9)
        num_of_agents = random.randint(2, 9)
        num_of_items = random.randint(1, 9)

        
        # # create a list of random agents name
        # list_of_agents = []
        # for i in range(num_of_agents):
        #     random_agent = random.choice(string.ascii_uppercase)
        #     if random_agent not in list_of_agents:
        #         list_of_agents.append(random_agent)


        # # create a list of Dict of random items with values
        # list_of_items = []
        # for i in range(num_of_items):
        #     random_item = random.choice(string.ascii_lowercase)
        #     random_item_weight = random.randint(0, 9)
        #     if random_item not in list_of_items:
        #         list_of_items.append(dict({random_item:random_item_weight}))


        # print(list_of_agents)
        # print(list_of_items)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
