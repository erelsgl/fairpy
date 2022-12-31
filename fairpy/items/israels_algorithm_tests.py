from israels_MinMakespan_algorithm import *
import unittest


class TestScedualing(unittest.TestCase):

    def setUp(self):
        
        self.scd1 : scedual = scedual_assignment()
        self.scd2 : scedual = scedual_makespan()
        self.mat = ValuationMatrix([[1, 1], [-1, -1]])
        self.scd1.build(self.mat)
        self.scd2.build(self.mat)

        self.scd1.scedual(0, 0)
        self.scd2.scedual(1, 1)

        assert isinstance(self.scd1, scedual)
        assert isinstance(self.scd2, scedual)
        assert isinstance(self.scd1.costs, ValuationMatrix)
        assert isinstance(self.scd2.costs, ValuationMatrix)

        self.assertEqual(id(self.scd1.costs), id(self.scd2.costs))


    def testBase(self):

        # properties

        self.assertEqual(2, self.scd1.Jobs)
        self.assertEqual(2, self.scd1.Mechines)
        self.assertEqual((2, 2), self.scd1.shape)

        # iterator

        self.assertEqual(4, len([(mechine, job) for mechine, job in self.scd1]))

        for mechine, job in self.scd1:
            self.assertEqual(self.scd1.costs[mechine, job], self.mat[mechine, job])

        # scedualing

        self.assertTrue(self.scd1.assignments[0, 0])
        self.assertFalse(self.scd2.assignments[0, 0])
        with self.assertRaises(KeyError): self.scd1.scedual(0, 0)
        self.scd2.scedual(0, 0)

    def testDerived1(self):

        self.assertEqual({(0, 0)}, self.scd1.extract_result())

    def testDerived2(self):

        self.assertEqual(0, self.scd2.extract_result())
        self.scd2.scedual(0, 0)
        self.assertEqual(1, self.scd2.extract_result())




class TestMinMakespanAlgos(unittest.TestCase):

    def test_aprrx_lim(self):

        for m in range(1, 10):
            self.assertTrue(MinMakespan(apprx, apprx_lim_exm1(m), scedual_makespan()) < 2*m)

        for t in range(1, 13):
            self.assertTrue(MinMakespan(apprx, apprx_lim_exm2(1000 * t), scedual_makespan()) <= 2000 * t + 2)

    def origionalTests(self):


        # uniformally different mechines
        uniformally_diff = ValuationMatrix([[2, 4, 1],
                                            [2, 6, 10],
                                            [3, 7, 11]])

        # example that elustrates the trickyness of the problome
        tradeof = ValuationMatrix([[10, 5, 7],
                                   [10, 2, 5],
                                   [1, 6, 6]])

        self.assertEqual(5, MinMakespan(apprx, uniformally_diff, scedual_makespan))
        self.assertEqual(7, MinMakespan(greedy, uniformally_diff, scedual_makespan))
        self.assertEqual(5, MinMakespan(apprx, tradeof, scedual_makespan))
        self.assertEqual(7, MinMakespan(greedy, tradeof, scedual_makespan))

    def test_supiriorty(self):


        print('avg makespan for the approximation algorithm: ', sum(res for res in RandomTesting(apprx, scedual_makespan(), 30)) / 30)
        print('----------')
        print('avg makespan for the greedy algorithm: ', sum(res for res in RandomTesting(greedy, scedual_makespan(), 30)) / 30)


if __name__ == '__main__':

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