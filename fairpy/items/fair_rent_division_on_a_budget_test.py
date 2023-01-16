import unittest
from fairpy.agentlist import AgentList
from fairpy.items.fair_rent_division_on_a_budget import maximum_rent_envy_free, optimal_envy_free


class TestMain(unittest.TestCase):
    def test_algo1(self):
        self.maxDiff = None
        ex1 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 500, '3': 250}})
        self.assertEqual(maximum_rent_envy_free(ex1, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}),
                         (1249.99,
                          ([('Alice', '1'), ('Clair', '2'), ('Bob', '3')],
                           [('1', 250.0), ('2', 500.0), ('3', 500.0)])))

        ex2 = AgentList({"Alice": {'1': 250, '2': 750}, "Bob": {'1': 250, '2': 750}})
        self.assertEqual(maximum_rent_envy_free(ex2, 1000, {'Alice': 600, 'Bob': 500}),
                         (1700.0, ([('Alice', '1'), ('Bob', '2')], [('1', 600.0), ('2', 1100.0)])))

        ex3 = AgentList({"Alice": {'1': 400, '2': 600}, "Bob": {'1': 300, '2': 700}})
        self.assertEqual(maximum_rent_envy_free(ex3, 1000, {'Alice': 450, 'Bob': 550}),
                         (1200.0, ([('Alice', '1'), ('Bob', '2')], [('1', 450.0), ('2', 750.0)])))

        ex4 = AgentList({"Alice": {'1': 250, '2': 300, '3': 450}, "Bob": {'1': 300, '2': 250, '3': 450},
                         "Clair": {'1': 450, '2': 300, '3': 250}})
        self.assertEqual(maximum_rent_envy_free(ex4, 1000, {'Alice': 300, 'Bob': 320, 'Clair': 350}),
                         (1200.01,
                          ([('Clair', '1'), ('Alice', '2'), ('Bob', '3')],
                           [('1', 450.0), ('2', 300.0), ('3', 450.0)])))

        ex5 = AgentList({"Alice": {'1': 300, '2': 400}, "Bob": {'1': 320, '2': 380}})
        self.assertEqual(maximum_rent_envy_free(ex5, 700, {'Alice': 310, 'Bob': 350}),
                         (780.0, ([('Bob', '1'), ('Alice', '2')], [('1', 350.0), ('2', 430.0)])))

        # Checking zero values
        ex6 = AgentList({"Alice": {'1': 0, '2': 0}, "Bob": {'1': 0, '2': 0}})
        self.assertEqual(maximum_rent_envy_free(ex6, 1000, {'Alice': 250, 'Bob': 250}),
                         (500.0, ([('Bob', '1'), ('Alice', '2')], [('1', 250.0), ('2', 250.0)])))

        # Checking wrong values
        ex7 = AgentList({"Alice": {'1': 300, '2': 250}, "Bob": {'1': 280, '2': 320}, "Clair": {'1': 400, '2': 370}})
        self.assertEqual(maximum_rent_envy_free(ex7, 700, {'Alice': 280, 'Bob': 290, 'Clair': 380}),
                         (745.0, ([('Clair', '1'), ('Bob', '2')], [('1', 380.0), ('2', 350.0)])))

        # Checking envy case
        ex8 = AgentList({"Alice": {'1': 400, '2': 250}, "Bob": {'1': 400, '2': 320}})
        self.assertEqual(maximum_rent_envy_free(ex8, 700, {'Alice': 420, 'Bob': 410}),
                         (900.0, ([('Alice', '1'), ('Bob', '2')], [('1', 490.0), ('2', 410.0)])))

        # Overload test
        agents = {"Alice": {str(i): i for i in range(1000)}, "Bob": {str(i): i for i in range(1000)}}
        ex9 = AgentList(agents)
        self.assertEqual(maximum_rent_envy_free(ex9, 10000, {'Alice': 500, 'Bob': 500}),
                         (1001.0, ([('Alice', '998'), ('Bob', '999')], [('998', 500.0), ('999', 501.0)])))

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

        ex2 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 250, '3': 500}})
        self.assertEqual(optimal_envy_free(ex2, 1000, {'Alice': 300, 'Bob': 300, 'Clair': 300}), 'no solution')

        ex3 = AgentList({"Alice": {'1': 250, '2': 750}, "Bob": {'1': 250, '2': 750}})
        self.assertEqual(optimal_envy_free(ex3, 1000, {'Alice': 600, 'Bob': 500}),
                         'no solution')

        ex4 = AgentList({"Alice": {'1': 250, '2': 750}, "Bob": {'1': 350, '2': 650}})
        self.assertEqual(optimal_envy_free(ex4, 1000, {'Alice': 500, 'Bob': 600}),
                         'no solution')

        # No Strongly connected component
        ex5 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 250, '3': 500}})
        self.assertEqual(optimal_envy_free(ex5, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}), "no solution")

        # Negative values
        ex6 = AgentList({"Alice": {'1': -250, '2': 750}, "Bob": {'1': 350, '2': -650}})
        self.assertEqual(optimal_envy_free(ex6, 1000, {'Alice': 500, 'Bob': 600}),
                         ([('Alice', '2'), ('Bob', '1')], [('2', 500.0), ('1', 500.0)])
                         )

        # Zero values
        ex7 = AgentList({"Alice": {'1': 0, '2': 0}, "Bob": {'1': 0, '2': 0}})
        self.assertEqual(optimal_envy_free(ex7, 1000, {'Alice': 250, 'Bob': 250}), "no solution")

        ex8 = AgentList(
            {"a": {'1': 100, '2': 200, '3': 300, '4': 400, '5': 500, '6': 600, '7': 700, '8': 800, '9': 900,
                   '10': 1000},
             "b": {'1': 1000, '2': 900, '3': 800, '4': 700, '5': 600, '6': 500, '7': 400, '8': 300, '9': 200,
                   '10': 100},
             "c": {'1': 100, '2': 1000, '3': 200, '4': 300, '5': 400, '6': 500, '7': 600, '8': 700, '9': 800,
                   '10': 900},
             "d": {'1': 200, '2': 100, '3': 1000, '4': 400, '5': 300, '6': 500, '7': 600, '8': 700, '9': 800,
                   '10': 900},
             "e": {'1': 300, '2': 200, '3': 400, '4': 1000, '5': 500, '6': 600, '7': 700, '8': 800, '9': 900,
                   '10': 100},
             "f": {'1': 400, '2': 300, '3': 200, '4': 100, '5': 1000, '6': 800, '7': 600, '8': 500, '9': 700,
                   '10': 900},
             "g": {'1': 500, '2': 900, '3': 800, '4': 700, '5': 100, '6': 1000, '7': 200, '8': 300, '9': 600,
                   '10': 400},
             "h": {'1': 600, '2': 200, '3': 300, '4': 400, '5': 500, '6': 100, '7': 1000, '8': 800, '9': 700,
                   '10': 900},
             "i": {'1': 700, '2': 900, '3': 800, '4': 200, '5': 300, '6': 400, '7': 100, '8': 1000, '9': 500,
                   '10': 600},
             "j": {'1': 800, '2': 900, '3': 100, '4': 200, '5': 300, '6': 400, '7': 500, '8': 600, '9': 1000,
                   '10': 700},
             })
        self.assertEqual(optimal_envy_free(ex8, 5500, {
            'a': 1000,
            'b': 1000,
            'c': 1000,
            'd': 1000,
            'e': 1000,
            'f': 1000,
            'g': 1000,
            'h': 1000,
            'i': 1000,
            'j': 1000
        }), ([('a', '10'),
              ('b', '1'),
              ('c', '2'),
              ('d', '3'),
              ('e', '4'),
              ('f', '5'),
              ('g', '6'),
              ('h', '7'),
              ('i', '8'),
              ('j', '9')],
             [('10', 550.0), ('1', 550.0), ('2', 550.0), ('3', 550.0), ('4', 550.0), ('5', 550.0), ('6', 550.0),
              ('7', 550.0), ('8', 550.0), ('9', 550.0)]))

        # Overload test
        agents = {"Alice": {str(i): i for i in range(1000)}, "Bob": {str(i): i for i in range(1000)}}
        ex9 = AgentList(agents)
        self.assertEqual(optimal_envy_free(ex9, 10000, {'Alice': 500, 'Bob': 500}), 'no solution')

        # Overload test 2
        num_agents = 100
        num_items = 100
        agents = {f"Agent{i}": {f"Item{j}": (i + j) * 10 for j in range(num_items)} for i in range(num_agents)}
        rent = num_agents * num_items * 10
        budgets = {f"Agent{i}": (i + 1) * 100 for i in range(num_agents)}
        ex10 = AgentList(agents)
        self.assertEqual(optimal_envy_free(ex10, rent, budgets), 'no solution')


if __name__ == '__main__':
    unittest.main()
