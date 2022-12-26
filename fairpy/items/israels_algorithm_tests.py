from israels_MinMakespan_algorithm import *
import unittest
from time import perf_counter

'''see test examples.pdf for farther info'''


class TestMinMakespanAlgos(unittest.TestCase):

    def test_basics(self):
        
        '''quick sanity check'''

        arr = np.array([[1, 1], [1, 1]])

        scd = scedual_assignment()
        scd.build(arr)

        assert isinstance(scd, scedual)
        assert isinstance(scd.extract_result(), np.ndarray.astype(bool))

        scd = scedual_makespan()
        scd.build(arr)

        assert isinstance(scd, scedual)
        assert isinstance(scd.extract_result(), float)

    def test_aprrx_lim(self):

        self.assertTrue(MinMakespan(apprx, apprx_lim_exm1(100), scedual_makespan) < 201)
        self.assertTrue(MinMakespan(apprx, apprx_lim_exm1(200), scedual_makespan) < 401)

        self.assertTrue(MinMakespan(apprx, apprx_lim_exm2(1000), scedual_makespan) < 1000.1)
        self.assertTrue(MinMakespan(apprx, apprx_lim_exm2(2000), scedual_makespan) < 2000.1)

        ans = MinMakespan(apprx, apprx_lim_exm2(100), scedual_assignment)

        self.assertTrue(ans[1, 0])
        self.assertTrue((ans[0, 1] and ans[2, 2]) or (ans[0, 2] and ans[2, 1]))

    def origional(self):

        # uniformally different mechines
        uniformally_diff = np.array([[2, 2, 3],
                                     [4, 6, 7],
                                     [1, 10, 11]])

        # example that elustrates the trickyness of the problome
        tradeof = np.array([[10, 10, 1], [5, 2, 6], [7, 5, 6]])

        self.assertTrue(MinMakespan(apprx, uniformally_diff, scedual_makespan) <= 10)
        self.assertTrue(MinMakespan(apprx, tradeof, scedual_makespan) <= 10)

    def test_supiriorty(self):

        start = perf_counter()
        apprx_preformance = sum([makespan for makespan in RandomTesting(apprx, scedual_makespan, 1000)])
        print('the approximation algorithm took ' + (perf_counter() - start) + 'seconds to complete a 1000 random examples')
        start = perf_counter()
        greedy_preformance = sum([makespan for makespan in RandomTesting(greedy, scedual_makespan, 1000)])
        print('the greedy algorithm took ' + (perf_counter() - start) + 'seconds to complete a 1000 random examples')

        assert apprx_preformance < greedy_preformance

        print('approximations algorithm \'s avarage result: ' + apprx_preformance / 1000)
        print('greedy algorithm \'s avarage result: ' + greedy_preformance / 1000)


if __name__ == '__main__':

    def apprx_lim_exm1(m: int) -> ValuationMatrix:

        '''
        first example to show strictness of the
        approximiation factor of the algorithm, 2
        '''

        return ValuationMatrix([ [1] + [1 / m] * (m - 1) ] * (m * (m - 1)))

    def apprx_lim_exm2(t: int) -> ValuationMatrix:

        '''
        second example to show strictness of the
        approximiation factor of the algorithm, 2
        '''

        return ValuationMatrix([[1, t], [t, t + 1], [t + 1, 2*t + 2]])


    unittest.main()