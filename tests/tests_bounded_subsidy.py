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

        G1 = nx.DiGraph()
        G1.add_edge(1, 2, weight=3)
        res = check_positive_weight_directed_cycles(G1)
        self.assertEqual(res, False)

        G2 = nx.DiGraph()
        G2.add_edge(1, 2, weight=3)
        G2.add_edge(2, 1, weight=-2)
        res = check_positive_weight_directed_cycles(G2)
        self.assertEqual(res, True)

        G3 = nx.DiGraph()
        G3.add_edge(1, 2, weight=1)
        G3.add_edge(2, 3, weight=-1)
        G3.add_edge(3, 4, weight=1)
        G3.add_edge(4, 1, weight=-1)
        res = check_positive_weight_directed_cycles(G3)
        self.assertEqual(res, False)

        G4 = nx.DiGraph()
        G4.add_edge(2, 1, weight=4)
        G4.add_edge(1, 3, weight=-2)
        G4.add_edge(2, 3, weight=3)
        G4.add_edge(3, 4, weight=2)
        G4.add_edge(4, 2, weight=-1)
        res = check_positive_weight_directed_cycles(G4)
        self.assertEqual(res, True)

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
        

    def test_calculate_the_Subsidy(self):
        """
            tests for cal_the_Subsidy function, that calculates the Subsidy of the agentes
        """

        agents1 = AgentList({"Alice": {"a":3, "b":5}, "Bob": {"a":6, "b":7}})
        envy_graph1 = create_Envy_Graph(agents1)
        res = [0, 1]
        self.assertEqual(calculate_the_Subsidy(envy_graph1), res)

        agents2 = AgentList({"Alice": {"a":4, "b":10, "c":8, "d":7}, "Bob": {"a":5, "b":9, "c":5, "d":10}})
        envy_graph2 = create_Envy_Graph(agents2)
        res = [0, 0]
        self.assertEqual(calculate_the_Subsidy(envy_graph2), res)

        agents3 = AgentList({"Alice": {"a":1, "b":5, "c":3}, "Bob": {"a":1, "b":3, "c":2}, "Max": {"a":3, "b":2, "c":1}})
        envy_graph3 = create_Envy_Graph(agents3)
        res = [0, 1, 0]
        self.assertEqual(calculate_the_Subsidy(envy_graph3), res)

        agents4 = AgentList({"Alice": {"a":5, "b":6}, "Bob": {"a":3, "b":4}, "Max": {"a":2, "b":2}, "Nancy": {"a":2, "b":1}})
        envy_graph4 = create_Envy_Graph(agents4)
        res = [0, 1, 3, 3]
        self.assertEqual(calculate_the_Subsidy(envy_graph4), res)

        agents5 = AgentList({"Alice": {"a":4, "b":3, "c":2, "d":1}, "Bob": {"a":4, "b":3, "c":2, "d":1}, "Max": {"a":4, "b":3, "c":2, "d":1}, "Nancy": {"a":4, "b":3, "c":2, "d":1}})
        envy_graph5 = create_Envy_Graph(agents5)
        res = [3, 2, 1, 0]
        self.assertEqual(calculate_the_Subsidy(envy_graph5), res)

        agents6 = AgentList({"Alice": {"a":5, "b":6}, "Bob": {"a":5, "b":6}, "Max": {"a":4, "b":5}, "Nancy": {"a":4, "b":6}})    
        envy_graph6 = create_Envy_Graph(agents6)   
        res = [1, 6, 6, 0]
        self.assertEqual(calculate_the_Subsidy(envy_graph6), res)

        agents7 = AgentList({"Alice": {"a":5, "b":5}, "Bob": {"a":5, "b":5}, "Max": {"a":5, "b":5}, "Nancy": {"a":5, "b":5}})
        envy_graph7 = create_Envy_Graph(agents7)
        res = [5, 5, 0, 0]
        self.assertEqual(calculate_the_Subsidy(envy_graph7), res)


    def test_random_calculate_the_Subsidy(self):
        """
            tests of random number of agents and items
        """

        ############ create random number of agents and items ############
        num_of_agents = random.randint(2, 300)
        num_of_items = random.randint(2, 300)
        
        # create a list of random agents names
        list_of_agents = []
        for i in range(num_of_agents):
            random_agent = random.choice(string.ascii_uppercase)
            if random_agent not in list_of_agents:
                list_of_agents.append(str(random_agent))
        # print(list_of_agents)

        # create a list of random items names
        list_of_items = []
        for i in range(num_of_items):
            random_item = random.choice(string.ascii_lowercase)
            if random_item not in list_of_items:
                list_of_items.append(str(random_item))
        # print(list_of_items)
    
        # create list of dict of items and the weight
        list_of_items_and_values = []
        items_and_values = {}
        for i in range(len(list_of_agents)):
            for j in range(len(list_of_items)):
                random_item_weight = random.randint(0, 9)
                items_and_values[str(list_of_items[j])] = random_item_weight
            list_of_items_and_values.append(items_and_values.copy())
        # print(list_of_items_and_values)

        # create AgentList
        agents = AgentList(dict(zip(list_of_agents,list_of_items_and_values)))

        ############ Checks if the algorithm works correctly and efficiently  ############
        
        # list of the subsudy
        subsudy_list = calculate_the_Subsidy(create_Envy_Graph(agents))

        # maximum matching for all the agents
        maximum_matching = Bounded_Subsidy(agents) 

        # The items that allocated for the agent
        agent_items_allocated = list(maximum_matching.values()) 

        sum_item_and_subsudy = [] # The sum of the items and subsidy allocated to each agent
        result = True

        # Here we check if the value of the items that the agent received + the subsidy he received is at least as large as all the others
        for i, agent_i in enumerate(agents): 
            sum_item_and_subsudy.clear()
            for k,agent_k in enumerate(agents): 
                sum_item_and_subsudy.append(agent_i.value(agent_items_allocated[k]) + subsudy_list[k]) # The sum of the items and subsidy allocated to each agent
            max_sum = sum_item_and_subsudy[i]
            for l in range(len(sum_item_and_subsudy)): 
                if sum_item_and_subsudy[l] > max_sum:  # Check if there is an envy
                    result = False
                    break

        self.assertEqual(result, True)
   

def main():
    unittest.main()

if __name__ == "__main__":
    main()
