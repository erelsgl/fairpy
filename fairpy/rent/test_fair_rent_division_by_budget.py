import unittest
from fairpy.agentlist import AgentList
from fair_rent_division_by_budget import algorithm1, algorithm2


class TestMain(unittest.TestCase):
    def test_algo1(self):
        ex1 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 500, '3': 250}})
        self.assertEqual(algorithm1(ex1, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}),
                         (709.99, {"Alice": {1: 70}, "Bob": {2: 320}, "Clair": {3: 320}}))

        ex2 = AgentList({"Alice": {'1': 250, '2': 750}, "Bob": {'1': 250, '2': 750}})
        self.assertEqual(algorithm1(ex2, 1000, {'Alice': 600, 'Bob': 500}),
                         (918.75, {"Alice": {1: 600}, "Bob": {2: 318.75}}))

        ex3 = AgentList({"Alice": {'1': 400, '2': 600}, "Bob": {'1': 300, '2': 700}})
        self.assertEqual(algorithm1(ex3, 1000, {'Alice': 450, 'Bob': 550}),
                         (900, {"Alice": {1: 350}, "Bob": {2: 550}}))

        ex4 = AgentList({"Alice": {'1': 250, '2': 300, '3': 450}, "Bob": {'1': 300, '2': 250, '3': 450},
                         "Clair": {'1': 450, '2': 300, '3': 250}})
        self.assertEqual(algorithm1(ex4, 1000, {'Alice': 300, 'Bob': 320, 'Clair': 350}),
                         (822.25, {"Alice": {2: 180}, "Bob": {3: 300}, "Clair": {3: 342.25}}))

        ex5 = AgentList({"Alice": {'1': 300, '2': 400}, "Bob": {'1': 320, '2': 380}})
        self.assertEqual(algorithm1(ex5, 700, {'Alice': 310, 'Bob': 350}),
                         (660, {"Alice": {2: 310}, "Bob": {1: 350}}))

        # Checking zero values
        ex6 = AgentList({"Alice": {'1': 0, '2': 0}, "Bob": {'1': 0, '2': 0}})
        self.assertEqual(algorithm1(ex6, 1000, {'Alice': 250, 'Bob': 250}), {})

        # Checking wrong values
        ex7 = AgentList({"Alice": {'1': 300, '2': 250}, "Bob": {'1': 280, '2': 320}, "Clair": {'1': 400, '2': 370}})
        self.assertEqual(algorithm1(ex7, 700, {'Alice': 280, 'Bob': 290,'Clair': 380}), {})

        # Checking envy case
        ex8 = AgentList({"Alice": {'1': 400, '2': 250}, "Bob": {'1': 400, '2': 320}})
        self.assertEqual(algorithm1(ex8, 700, {'Alice': 420, 'Bob': 410}),
                         (680, {"Alice": {1: 400}, "Bob": {2: 280}}))

    def test_algo2(self):
        ex1 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 500, '3': 250}})
        self.assertEqual(algorithm2(ex1, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}),
                         {"Alice": {1: 130}, "Bob": {2: 270}, "Clair": {3: 520}})

        ex2 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 250, '3': 500}})
        self.assertEqual(algorithm2(ex2, 1000, {'Alice': 300, 'Bob': 300, 'Clair': 300}), "no solution")

        ex3 = AgentList({"Alice": {'1': 250, '2': 750}, "Bob": {'1': 250, '2': 750}})
        self.assertEqual(algorithm2(ex3, 1000, {'Alice': 600, 'Bob': 500}),
                         {"Alice": {1: 600}, "Bob": {2: 318.75}})

        ex4 = AgentList({"Alice": {'1': 250, '2': 750}, "Bob": {'1': 350, '2': 650}})
        self.assertEqual(algorithm2(ex4, 1000, {'Alice': 500, 'Bob': 600}),
                         {{"Alice": {2: 520}, "Bob": {1: 350}}})

        # No Strongly connected component
        ex5 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 250, '3': 500}})
        self.assertEqual(algorithm2(ex5, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}), "no solution")

        # Negative values
        ex6 = AgentList({"Alice": {'1': -250, '2': 750}, "Bob": {'1': 350, '2': -650}})
        self.assertEqual(algorithm2(ex6, 1000, {'Alice': 500, 'Bob': 600}), "no solution")

        # Zero values
        ex7 = AgentList({"Alice": {'1': 0, '2': 0}, "Bob": {'1': 0, '2': 0}})
        self.assertEqual(algorithm2(ex7, 1000, {'Alice': 250, 'Bob': 250}), "no solution")


if __name__ == '__main__':
    unittest.main()
