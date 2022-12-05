import unittest
from fairpy.agentlist import AgentList
from main import algorithm1, algorithm2


class TestMain(unittest.TestCase):
    def test_algo1(self):
        ex1 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 500, '3': 250}})
        self.assertEqual(algorithm1(ex1, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}),
                         (709.99, "(Alice gets {1} with rent 70, Bob gets {2} with rent 320,"
                                  "Clair gets {3} with rent 320))"))

        ex2 = AgentList({"Alice": {'1': 250, '2': 750}, "Bob": {'1': 250, '2': 750}})
        self.assertEqual(algorithm1(ex2, 1000, {'Alice': 600, 'Bob': 500}),
                         (918.75, "(Alice gets {1} with rent 600, Bob gets {2} with rent 318.75)"))

        ex3 = AgentList({"Alice": {'1': 400, '2': 600}, "Bob": {'1': 300, '2': 700}})
        self.assertEqual(algorithm1(ex3, 1000, {'Alice': 450, 'Bob': 550}),
                         (900, "(Alice gets {1} with rent 350, Bob gets {2} with rent 550)"))

        ex4 = AgentList({"Alice": {'1': 250, '2': 300, '3': 450}, "Bob": {'1': 300, '2': 250, '3': 450},
                         "Clair": {'1': 450, '2': 300, '3': 250}})
        self.assertEqual(algorithm1(ex4, 1000, {'Alice': 300, 'Bob': 320, 'Clair': 350}),
                         (822.25, "(Alice gets {2} with rent 180, Bob gets {3} with rent 300,"
                                  "Clair gets {3} with rent 342.25))"))

        ex5 = AgentList({"Alice": {'1': 300, '2': 400}, "Bob": {'1': 320, '2': 380}})
        self.assertEqual(algorithm1(ex5, 700, {'Alice': 310, 'Bob': 350}),
                         (660, "(Alice gets {2} with rent 310, Bob gets {1} with rent 350)"))

        # Checking zero values
        ex6 = AgentList({"Alice": {'1': 0, '2': 0}, "Bob": {'1': 0, '2': 0}})
        self.assertEqual(algorithm1(ex6, 1000, {'Alice': 250, 'Bob': 250}),
                         "no solution")

        # Checking wrong values
        ex7 = AgentList({"Alice": {'1': 300, '2': 250}, "Bob": {'1': 280, '2': 320}, "Clair": {'1': 400, '2': 370}})
        self.assertEqual(algorithm1(ex7, 700, {'Alice': 280, 'Bob': 290,'Clair': 380}),
                         "no solution")

        # Checking envy case
        ex8 = AgentList({"Alice": {'1': 400, '2': 250}, "Bob": {'1': 400, '2': 320}})
        self.assertEqual(algorithm1(ex8, 700, {'Alice': 420, 'Bob': 410}),
                         (680, "(Alice gets {1} with rent 400, Bob gets {2} with rent 280)"))

    def test_algo2(self):
        ex1 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 500, '3': 250}})
        self.assertEqual(algorithm2(ex1, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}),
                         (920, "(Alice gets {1} with rent 130, Bob gets {2} with rent 270,"
                               "Clair gets {3} with rent 520)"))

        ex2 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 250, '3': 500}})
        self.assertEqual(algorithm2(ex2, 1000, {'Alice': 300, 'Bob': 300, 'Clair': 300}),
                         "no solution")

        ex3 = AgentList({"Alice": {'1': 250, '2': 750}, "Bob": {'1': 250, '2': 750}})
        self.assertEqual(algorithm2(ex3, 1000, {'Alice': 600, 'Bob': 500}),
                         (918.75, "(Alice gets {1} with rent 600, Bob gets {2} with rent 318.75)"))

        # Need to continue from here
        ex4 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 500, '3': 250}})
        self.assertEqual(algorithm2(ex4, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}),
                         (920, "(Alice gets {1} with rent 130, Bob gets {2} with rent 270,"
                               "Clair gets {3} with rent 520)"))

        ex5 = AgentList({"Alice": {'1': 250, '2': 250, '3': 500}, "Bob": {'1': 250, '2': 250, '3': 500},
                         "Clair": {'1': 250, '2': 500, '3': 250}})
        self.assertEqual(algorithm2(ex5, 1000, {'Alice': 250, 'Bob': 320, 'Clair': 430}),
                         (920, "(Alice gets {1} with rent 130, Bob gets {2} with rent 270,"
                               "Clair gets {3} with rent 520)"))


if __name__ == '__main__':
    unittest.main()
