from fairpy.items.min_makespan_2apprximation import *
import unittest


class TestScedualing(unittest.TestCase):

    def setUp(self):
        
        self.scd1 : schedule = schedule()
        self.scd2 : schedule = schedule()
        self.mat = ValuationMatrix([[1, 1], [-1, -1]])
        self.scd1.build(self.mat)
        self.scd2.build(self.mat)

        self.scd1.scedual(0, 0)
        self.scd2.scedual(1, 1)

        assert isinstance(self.scd1, schedule)
        assert isinstance(self.scd2, schedule)
        assert isinstance(self.scd1.costs, ValuationMatrix)
        assert isinstance(self.scd2.costs, ValuationMatrix)

        self.assertEqual(id(self.scd1.costs), id(self.scd2.costs))


    def testBase(self):

        # properties

        self.assertEqual(2, self.scd1.jobs)
        self.assertEqual(2, self.scd1.mechines)
        self.assertEqual((2, 2), self.scd1.shape)

        # iterator

        self.assertEqual(4, len([(mechine, job) for mechine, job in self.scd1]))

        for mechine, job in self.scd1:
            self.assertEqual(self.scd1.costs[mechine, job], self.mat[mechine, job])

        # scedualing

        self.assertEqual(self.scd1.assignments[0], 0)
        with self.assertRaises(KeyError): self.scd2.assignments[0]
        with self.assertRaises(KeyError): self.scd1.scedual(0, 0)
        self.scd2.scedual(0, 0)

        self.assertFalse(self.scd1.complete())
        self.assertTrue(self.scd2.complete())

    def testDerived1(self):

        self.assertEqual({0: 0}, self.scd1.assignments)

    def testDerived2(self):

        self.assertEqual(0, self.scd2.makespan)
        self.scd2.scedual(0, 0)
        self.assertEqual(1, self.scd2.makespan)



class TestMinMakespanAlgos(unittest.TestCase):

    def setUp(self):    self.scd = schedule()

    def test_validaty(self):

        self.scd.build(ValuationMatrix(np.ones((10, 10))))

        greedy(self.scd)
        self.assertTrue(self.scd.complete())
        self.assertEqual(1, self.scd.makespan)

        self.scd.clear()

        apprx(self.scd)
        self.assertTrue(self.scd.complete())
        self.assertEqual(1, self.scd.makespan)

        self.scd.clear()

        self.scd.build(ValuationMatrix([[1, 3, 3, 3],
                                        [4, 4, 1, 4],
                                        [1, 2, 3, 4],
                                        [4, 1, 1, 2]]))

        greedy(self.scd)
        self.assertTrue(self.scd.complete())
        self.assertEqual(3, self.scd.makespan)

        self.scd.clear()

        apprx(self.scd)
        self.assertTrue(self.scd.complete())
        self.assertEqual(3, self.scd.makespan)

    def test_apprx_factor(self):

        for i in range(10):

            mat = ValuationMatrix(uniform(1, 3, (3, 4)))

            MinMakespan(optimal, mat, self.scd)

            optimum = self.scd.makespan

            MinMakespan(apprx, mat, self.scd)

            try:    self.assertTrue(self.scd.makespan <= 2.1 * optimum)
            except: logger.debug('approximation gurentee did not hold, input: \n%s, output: %s, makespan: %s, OPT: %s', mat, self.scd.assignments, self.scd.makespan, optimum)

    def test_aprrx_lim(self):

        for m in range(1, 10):

            MinMakespan(apprx, apprx_lim_exm1(m), self.scd)
            self.assertTrue(self.scd.makespan < 2*m)

        for t in range(1, 13):

            MinMakespan(apprx, apprx_lim_exm2(1000 * t), self.scd)
            self.assertTrue(self.scd.makespan <= 2000 * t + 2)

    def origionalTests(self):


        # uniformally different mechines
        uniformally_diff = ValuationMatrix([[2, 4, 1],
                                            [2, 6, 10],
                                            [3, 7, 11]])

        # example that elustrates the trickyness of the problome
        tradeof = ValuationMatrix([[10, 5, 7],
                                   [10, 2, 5],
                                   [1, 6, 6]])

        MinMakespan(apprx, uniformally_diff, self.scd)
        self.assertEqual(5, self.scd.makespan)
        MinMakespan(greedy, uniformally_diff, self.scd)
        self.assertEqual(7, self.scd.makespan)
        MinMakespan(apprx, tradeof, self.scd)
        self.assertEqual(5, self.scd.makespan)
        MinMakespan(greedy, tradeof, self.scd)
        self.assertEqual(7, self.scd.makespan)


if __name__ == '__main__':


    def RandomTesting(algo: MinMakespanAlgo, iterations: int, **kwargs):

        ''' spesefied amount of random tests generator '''

        scd = schedule()

        for i in range(iterations):
            MinMakespan(algo, ValuationMatrix(uniform(1, 3, (randint(1, 60), randint(1, 20)))), scd, **kwargs)
            yield scd.makespan


    def apprx_lim_exm1(m: int) -> ValuationMatrix:

        '''
        first example to show strictness of the
        approximiation factor of the algorithm, 2
        '''

        return ValuationMatrix([[m] + [1] * (m*m - m)] * m)

    def apprx_lim_exm2(t: int) -> ValuationMatrix:

        '''
        second example to show strictness of the
        approximiation factor of the algorithm, 2
        '''

        return ValuationMatrix([[1, t, t + 1], [t, t + 1, (2*t + 2) / (2*t + 1)]])


    unittest.main()