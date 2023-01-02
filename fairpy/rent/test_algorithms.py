import unittest
from fairpy.agentlist import AgentList
from fairpy.rent.Algorithms import maximum_rent_envy_free, optimal_envy_free


class TestMain(unittest.TestCase):
    def test_algo1(self):
        self.maxDiff = None
        ex1 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 500, '3': 250}})
        self.assertEqual(maximum_rent_envy_free(ex1, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}),
                         (709.99,
                          ([('Alice', '1'), ('Clair', '2'), ('Bob', '3')], [('1', 70.0), ('2', 320.0), ('3', 320.0)])))

        ex2 = AgentList({"Alice": {'1': 250, '2': 750}, "Bob": {'1': 250, '2': 750}})
        self.assertEqual(maximum_rent_envy_free(ex2, 1000, {'Alice': 600, 'Bob': 500}),
                         (500.0, ([('Alice', '1'), ('Bob', '2')], [('1', 0.0), ('2', 500.0)])))

        ex3 = AgentList({"Alice": {'1': 400, '2': 600}, "Bob": {'1': 300, '2': 700}})
        self.assertEqual(maximum_rent_envy_free(ex3, 1000, {'Alice': 450, 'Bob': 550}),
                         (800.0, ([('Alice', '1'), ('Bob', '2')], [('1', 250.0), ('2', 550.0)])))

        ex4 = AgentList({"Alice": {'1': 250, '2': 300, '3': 450}, "Bob": {'1': 300, '2': 250, '3': 450},
                         "Clair": {'1': 450, '2': 300, '3': 250}})
        self.assertEqual(maximum_rent_envy_free(ex4, 1000, {'Alice': 300, 'Bob': 320, 'Clair': 350}),
                         (810.01,
                          ([('Clair', '1'), ('Alice', '2'), ('Bob', '3')],
                           [('1', 320.0), ('2', 170.0), ('3', 320.0)])))

        ex5 = AgentList({"Alice": {'1': 300, '2': 400}, "Bob": {'1': 320, '2': 380}})
        self.assertEqual(maximum_rent_envy_free(ex5, 700, {'Alice': 310, 'Bob': 350}),
                         (540.0, ([('Bob', '1'), ('Alice', '2')], [('1', 230.0), ('2', 310.0)])))

        # Checking zero values
        ex6 = AgentList({"Alice": {'1': 0, '2': 0}, "Bob": {'1': 0, '2': 0}})
        self.assertEqual(maximum_rent_envy_free(ex6, 1000, {'Alice': 250, 'Bob': 250}),
                         (500.0, ([('Bob', '1'), ('Alice', '2')], [('1', 250.0), ('2', 250.0)])))

        # Checking wrong values
        ex7 = AgentList({"Alice": {'1': 300, '2': 250}, "Bob": {'1': 280, '2': 320}, "Clair": {'1': 400, '2': 370}})
        self.assertEqual(maximum_rent_envy_free(ex7, 700, {'Alice': 280, 'Bob': 290, 'Clair': 380}),
                         (565.0, ([('Clair', '1'), ('Bob', '2')], [('1', 320.0), ('2', 290.0)])))

        # Checking envy case
        ex8 = AgentList({"Alice": {'1': 400, '2': 250}, "Bob": {'1': 400, '2': 320}})
        self.assertEqual(maximum_rent_envy_free(ex8, 700, {'Alice': 420, 'Bob': 410}),
                         (760.0, ([('Alice', '1'), ('Bob', '2')], [('1', 420.0), ('2', 340.0)])))

        # Overload test
        agents = {"Alice": {str(i): i for i in range(1000)}, "Bob": {str(i): i for i in range(1000)}}
        ex9 = AgentList(agents)
        self.assertEqual(maximum_rent_envy_free(ex9, 10000, {'Alice': 500, 'Bob': 500}),
                         (999.0, ([('Alice', '998'), ('Bob', '999')], [('998', 499.0), ('999', 500.0)])))

        # Create a large number of agents and items with high values
        num_agents = 100
        num_items = 100
        agents = {f"Agent{i}": {f"Item{j}": (i + j) * 10 for j in range(num_items)} for i in range(num_agents)}
        ex10 = AgentList(agents)

        # Set the rent to a large value
        rent = num_agents * num_items * 10

        # Set the budgets to a high value
        budgets = {f"Agent{i}": (i + 1) * 100 for i in range(num_agents)}

        # Test the function
        result = maximum_rent_envy_free(ex10, rent, budgets)
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], tuple)
        self.assertIsInstance(result[1][0], list)
        self.assertIsInstance(result[1][1], list)

    def test_algo2(self):
        ex1 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 500, '3': 250}})
        self.assertEqual(optimal_envy_free(ex1, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}),
                         'no solution')

        ex2 = AgentList({"Alice": {'1': 250, '2': 750}, "Bob": {'1': 250, '2': 750}})
        self.assertEqual(optimal_envy_free(ex2, 1000, {'Alice': 600, 'Bob': 500}),
                         'no solution')

        # Negative values
        ex3 = AgentList({"Alice": {'1': -250, '2': 750}, "Bob": {'1': 350, '2': -650}})
        self.assertEqual(optimal_envy_free(ex3, 1000, {'Alice': 500, 'Bob': 600}),
                         ([('Alice', '2'), ('Bob', '1')], [('2', 500.0), ('1', 500.0)]))

        # Zero values
        ex4 = AgentList({"Alice": {'1': 0, '2': 0}, "Bob": {'1': 0, '2': 0}})
        self.assertEqual(optimal_envy_free(ex4, 1000, {'Alice': 250, 'Bob': 250}), 'no solution')

        # Overload test
        agents = {"Alice": {str(i): i for i in range(1000)}, "Bob": {str(i): i for i in range(1000)}}
        ex5 = AgentList(agents)
        self.assertEqual(optimal_envy_free(ex5, 10000, {'Alice': 500, 'Bob': 500}), 'no solution')

        # Overload test 2
        num_agents = 100
        num_items = 100
        agents = {f"Agent{i}": {f"Item{j}": (i + j) * 10 for j in range(num_items)} for i in range(num_agents)}
        rent = num_agents * num_items * 10
        budgets = {f"Agent{i}": (i + 1) * 100 for i in range(num_agents)}
        ex6 = AgentList(agents)
        self.assertEqual(optimal_envy_free(ex6, rent, budgets), 'no solution')


if __name__ == '__main__':
    unittest.main()
