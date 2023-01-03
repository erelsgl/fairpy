'''
Main testing module for bidding_for_envy_freeness.py.

Programmers: Barak Amram, Adi Dahari.
Since: 2022-12.
'''
import numpy as np

from fairpy.items.valuations import ValuationMatrix
from fairpy.items.bidding_for_envy_freeness import BiddingForEnvyFreeness, bidding_for_envy_freeness

def test_find_best_matching():
    '''
    Test the find_best_matching function.
    '''
    matrix = [[50, 40, 35], [25, 25, 25], [10, 20, 25]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_best_matching(ValuationMatrix(matrix)) == [0, 1, 2]
    
    matrix = [[25, 25, 25], [50, 40, 35], [10, 20, 25]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_best_matching(ValuationMatrix(matrix)) == [1, 0, 2]
    
    matrix = [[25, 25, 25], [10, 20, 25], [50, 40, 35]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_best_matching(ValuationMatrix(matrix)) == [2, 0, 1]
    
    matrix = [[50, 20, 10, 20], [60, 40, 15, 10], [0, 40, 25, 35], [50, 35, 10, 30]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_best_matching(ValuationMatrix(matrix)) == [0, 1, 2, 3]
    
    matrix = [[60, 40, 15, 10], [50, 20, 10, 20], [0, 40, 25, 35], [50, 35, 10, 30]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_best_matching(ValuationMatrix(matrix)) == [1, 0, 2, 3]
    
    matrix = [[60, 40, 15, 10], [50, 35, 10, 30], [0, 40, 25, 35], [50, 20, 10, 20]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_best_matching(ValuationMatrix(matrix)) == [3, 0, 2, 1]
    

def test_find_m_c():
    '''
    Test the find_m_c function.
    '''
    matrix = [[50, 40, 35], [25, 25, 25], [10, 20, 25]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_m_c() == (100, 55, 45)
    
    matrix = [[25, 25, 25], [50, 40, 35], [10, 20, 25]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_m_c() == (100, 55, 45)
    
    matrix = [[25, 25, 25], [10, 20, 25], [50, 40, 35]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_m_c() == (100, 55, 45)
    
    matrix = [[50, 20, 10, 20], [60, 40, 15, 10], [0, 40, 25, 35], [50, 35, 10, 30]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_m_c() == (145, 100, 45)
    
    matrix = [[60, 40, 15, 10], [0, 40, 25, 35], [50, 20, 10, 20], [50, 35, 10, 30]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_m_c() == (145, 100, 45)
    
    matrix = [[0, 40, 25, 35], [60, 40, 15, 10], [50, 20, 10, 20], [50, 35, 10, 30]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_m_c() == (145, 100, 45)

    matrix = [[0, 40, 25, 35], [50, 35, 10, 30], [60, 40, 15, 10], [50, 20, 10, 20]]
    bfef = BiddingForEnvyFreeness(matrix)
    assert bfef.find_m_c() == (145, 100, 45)

def assert_matrix_equal(expected, actual):
    '''
    Assert that two matrices are equal.
    '''
    for i in range(len(expected)):
        for j in range(len(expected[0])):
            assert expected[i][j] == actual[i][j]

def test_initialize_assessment_matrix():
    '''
    Test the initialize_assessment_matrix function.
    '''
    matrix = [[50, 40, 35], [25, 25, 25], [10, 20, 25]]
    bfef = BiddingForEnvyFreeness(matrix)
    expected = np.array([[0, 15, 10], [-25, 0, 0], [-40, -5, 0], [0, 0, 0]])
    actual = bfef.initialize_assessment_matrix()
    assert_matrix_equal(expected, actual)
    
    matrix = [[25, 25, 25], [50, 40, 35], [10, 20, 25]]
    bfef = BiddingForEnvyFreeness(matrix)
    expected = np.array([[0, 15, 10], [-25, 0, 0], [-40, -5, 0], [0, 0, 0]])
    actual = bfef.initialize_assessment_matrix()
    assert_matrix_equal(expected, actual)
    
    matrix = [[50, 20, 10, 20], [60, 40, 15, 10], [0, 40, 25, 35], [50, 35, 10, 30]]
    bfef = BiddingForEnvyFreeness(matrix)
    expected = np.array([[  0, -20, -15, -10], [ 10,   0, -10, -20], [-50,   0,   0,   5], [  0,  -5, -15,   0], [  0,   0,   0,   0]])
    actual = bfef.initialize_assessment_matrix()
    assert_matrix_equal(expected, actual)
    
    matrix = [[60, 40, 15, 10], [50, 35, 10, 30], [0, 40, 25, 35], [50, 20, 10, 20]]
    bfef = BiddingForEnvyFreeness(matrix)
    expected = np.array([[  0, -20, -15, -10], [ 10,   0, -10, -20], [-50,   0,   0,   5], [  0,  -5, -15,   0], [  0,   0,   0,   0]])
    actual = bfef.initialize_assessment_matrix()
    assert_matrix_equal(expected, actual)
    
    
def test_compensation_procedure():
    '''
    As the compensation procedure returns the final assessment matrix, we can use it to test the
    correctness of the procedure.
    '''
    matrix = [[50, 40, 35], [25, 25, 25], [10, 20, 25]]
    bfef = BiddingForEnvyFreeness(matrix)
    expected = np.array([[ 15,  15,  10], [-10,   0,   0], [-25,  -5,   0], [ 25,  10,  10]])
    actual = bfef.assessment_matrix
    
    assert_matrix_equal(expected, actual)
    
    matrix = [[10, 20, 25], [25, 25, 25], [50, 40, 35]]
    bfef = BiddingForEnvyFreeness(matrix)
    expected = np.array([[ 15,  15,  10], [-10,   0,   0], [-25,  -5,   0], [ 25,  10,  10]])
    actual = bfef.assessment_matrix
    
    assert_matrix_equal(expected, actual)
    
    matrix = [[50, 20, 10, 20], [60, 40, 15, 10], [0, 40, 25, 35], [50, 35, 10, 30]]
    bfef = BiddingForEnvyFreeness(matrix)
    expected = np.array([[  0, -10,  -5,  -5], [ 10,  10,   0, -15], [-50,  10,  10,  10], [  0,   5,  -5,   5], [  5,  15,  15,  10]])
    actual = bfef.assessment_matrix
    
    assert_matrix_equal(expected, actual)
    
    matrix = [[0, 40, 25, 35], [60, 40, 15, 10], [50, 35, 10, 30], [50, 20, 10, 20]]
    bfef = BiddingForEnvyFreeness(matrix)
    expected = np.array([[  0, -10,  -5,  -5], [ 10,  10,   0, -15], [-50,  10,  10,  10], [  0,   5,  -5,   5], [  5,  15,  15,  10]])
    actual = bfef.assessment_matrix
    
    assert_matrix_equal(expected, actual)


def test_full_cases():
    '''
    Test full cases.
    '''
    matrix = [[50, 40, 35], [25, 25, 25], [10, 20, 25]]
    expected = {0: {'bundle': 0, 'discount': 25},
                1: {'bundle': 1, 'discount': 10},
                2: {'bundle': 2, 'discount': 10}}
    
    assert bidding_for_envy_freeness(matrix) == expected
    
    matrix = [[25, 25, 25], [50, 40, 35], [10, 20, 25]]
    expected = {0: {'bundle': 1, 'discount': 10},
                1: {'bundle': 0, 'discount': 25},
                2: {'bundle': 2, 'discount': 10}}
    
    assert bidding_for_envy_freeness(matrix) == expected
    
    matrix = [[50, 20, 10, 20], [60, 40, 15, 10], [0, 40, 25, 35], [50, 35, 10, 30]]
    expected = {0: {'bundle': 0, 'discount': 5},
                1: {'bundle': 1, 'discount': 15},
                2: {'bundle': 2, 'discount': 15},
                3: {'bundle': 3, 'discount': 10}}
    
    assert bidding_for_envy_freeness(matrix) == expected
    
    matrix = [[60, 40, 15, 10], [50, 35, 10, 30], [0, 40, 25, 35], [50, 20, 10, 20]]
    expected = {0: {'bundle': 1, 'discount': 15},
                1: {'bundle': 3, 'discount': 10},
                2: {'bundle': 2, 'discount': 15},
                3: {'bundle': 0, 'discount': 5}}
    
    assert bidding_for_envy_freeness(matrix) == expected
    