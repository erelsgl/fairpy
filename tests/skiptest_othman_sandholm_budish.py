"""
Article Name:
"Finding Approximate Competitive Equilibria: Efficient and Fair Course Allocation" (2010)

Authors:
Abraham Othman, Tuomas Sandholm and Eric Budish.

Link:
https://dl.acm.org/doi/abs/10.5555/1838206.1838323

Programmer:
Tahel Zecharia.

The algorithm performs a fair and equal allocation as much as possible
between courses for students given a list of preferences for each student.

"""

import pytest
from typing import List
from fairpy.courses.othman_sandholm_budish import course_allocation, neighbors, score, max_utility
from fairpy.valuations import ValuationMatrix

"""
    Since the definition of fairness is not unambiguous in this algorithm,
    and mainly depends on the budget given to each of the agents,
    it is very difficult to find the results of the algorithm.
    That's why I prepared tests for large inputs in order to make sure that the algorithm does not get stuck.
"""


def test_big_input1():
    """
    5 courses and 10 students:
    """

    utilities = ValuationMatrix([[1, 2, 33, 44, 34],
                                 [4, 9, 90, 6, 8],
                                 [1, 2, 7, 3, 14],
                                 [58, 95, 9, 5, 2],
                                 [77, 7, 14, 21, 63],
                                 [3, 6, 1, 64, 3],
                                 [88, 2, 4, 6, 78],
                                 [5, 1, 7, 3, 14],
                                 [58, 95, 33, 5, 2],
                                 [7, 8, 34, 21, 28]])

    budgets: List[float] = [1.0, 1.11, 1.2, 1.7, 1.56, 1.3, 1.41, 1.62, 1.52, 1.435]
    prices: List[float] = [1.9, 0.3, 1.6, 1.2, 0.8]
    capacity: List[int] = [2, 2, 2, 2, 2]
    num_of_courses = 2

    placements = []
    for i in utilities.agents():
        placements.append(max_utility(utilities[i], budgets[i], prices, num_of_courses))

    # course_allocation test:
    assert course_allocation(utilities, budgets, prices, capacity, num_of_courses) == \
           [[0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0]]

    # neighbors test:
    assert neighbors(utilities, budgets, prices, capacity, num_of_courses) == \
           [[-2, 6, -2, 1, 5],
            [1.9, 0.41, 1.6, 1.2, 0.8],
            [1.9, 0.3, 1.6, 1.23, 0.8],
            [1.9, 0.3, 1.6, 1.2, 0.82]]

    # score test:
    """
    the placement is:
    [0, 0, 0, 0, 1]
    [0, 1, 0, 0, 1]
    [0, 1, 0, 0, 1]
    [0, 1, 0, 1, 0]
    [0, 1, 0, 0, 1]
    [0, 0, 0, 1, 0]
    [0, 1, 0, 0, 1]
    [0, 1, 0, 0, 1]
    [0, 1, 0, 1, 0]
    [0, 1, 0, 0, 1]

    the capacity of eac course is 2.
    in the placement, 8 students were placed in course 2,
    3 students were placed in course 4 and 7 students were placed in course 5.
    Therefore, the score will be calculated as follows:
    sqrt( (8 - 2)**2 + (3 - 2)**2 + (7 - 2)**2 ) = sqrt(62) = 7.874...
    """
    assert score(placements, capacity) == 7.874
    # max_utility test:
    assert max_utility(utilities[0], budgets[0], prices, num_of_courses) == [0, 0, 0, 0, 1]


def test_big_input2():
    """
    5 courses and 15 students:
    """

    utilities = ValuationMatrix([[3, 7, 1, 64, 34],
                                 [88, 2, 4, 6, 8],
                                 [5, 2, 7, 33, 14],
                                 [58, 95, 33, 5, 2],
                                 [77, 90, 34, 21, 63],
                                 [3, 7, 1, 64, 34],
                                 [88, 2, 4, 6, 8],
                                 [5, 2, 7, 33, 14],
                                 [58, 95, 33, 5, 2],
                                 [77, 90, 34, 21, 63],
                                 [3, 7, 1, 64, 34],
                                 [88, 2, 4, 6, 8],
                                 [5, 2, 7, 33, 14],
                                 [58, 95, 33, 5, 2],
                                 [77, 90, 34, 21, 63]])

    budgets: List[float] = [1.5, 1.11, 1.222, 1.7, 1.56, 1.3, 1.41, 1.62, 1.52, 1.435, 1.932, 1.685, 1.24, 1.27, 1.666]
    prices: List[float] = [1.0, 0.0, 1.2, 1.22, 0.3]
    capacity: List[int] = [3, 3, 3, 3, 3]
    num_of_courses = 3

    placements = []
    for i in utilities.agents():
        placements.append(max_utility(utilities[i], budgets[i], prices, num_of_courses))

    # course_allocation test:
    assert course_allocation(utilities, budgets, prices, capacity, num_of_courses) == \
           [[0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0]]

    # neighbors test:
    assert neighbors(utilities, budgets, prices, capacity, num_of_courses) == \
           [[6, 12, -3, 3, 6],
            [1.12, 0.0, 1.2, 1.22, 0.3],
            [1.0, 0.012, 1.2, 1.22, 0.3],
            [1.0, 0.0, 1.2, 1.232, 0.3],
            [1.0, 0.0, 1.2, 1.22, 0.41]]

    # score test:
    assert score(placements, capacity) == 15.0
    # max_utility test:
    assert max_utility(utilities[0], budgets[0], prices, num_of_courses) == [0, 1, 0, 1, 0]


def test_big_input3():
    """
    15 courses and 20 students:
    """

    utilities = ValuationMatrix([[3, 7, 1, 13, 34, 23, 24, 5, 77, 32, 12, 22, 34, 18, 51],
                                 [5, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [76, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [22, 3, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [56, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [28, 7, 1, 64, 34, 23, 24, 5, 77, 32, 12, 22, 34, 18, 51],
                                 [50, 2, 7, 33, 14, 58, 95, 33, 2, 2, 77, 90, 34, 21, 63],
                                 [59, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 9, 34, 21, 63],
                                 [23, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 93, 34, 21, 63],
                                 [86, 2, 7, 33, 14, 9, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [33, 7, 1, 64, 34, 23, 24, 5, 77, 32, 12, 22, 34, 18, 51],
                                 [53, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [22, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [40, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [86, 2, 7, 33, 14, 9, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [33, 7, 1, 64, 34, 23, 24, 5, 77, 32, 12, 22, 34, 18, 51],
                                 [53, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [22, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [40, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
                                 [5, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63]])

    budgets: List[float] = [1.0, 1.11, 1.2, 1.22, 1.43, 1.32, 1.65, 1.222, 1.7, 1.56, 1.3, 1.41, 1.62, 1.52, 1.435,
                            1.932, 1.685, 1.24, 1.27, 1.666]
    prices: List[float] = [1.0, 0.0, 1.2, 1.22, 0.3, 1.32, 1.65, 1.222, 1.7, 0.2, 0.2, 0.6, 0.66, 1.4, 2.1]
    capacity: List[int] = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    num_of_courses = 3

    placements = []
    for i in utilities.agents():
        placements.append(max_utility(utilities[i], budgets[i], prices, num_of_courses))

    # course_allocation test:
    # assert course_allocation(utilities, budgets, prices, capacity, num_of_courses) == \
    #        [[0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
    #         [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    #         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    #         [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    #         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    #         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #         [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    #         [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    #         [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    #         [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]]

    # neighbors test:
    assert neighbors(utilities, budgets, prices, capacity, num_of_courses) == \
           [[0, 0, -1, -1, 11, -2, -1, -2, -1, 2, 16, 13, 8, -2, -1],
            [1.0, 0.0, 1.2, 1.22, 0.32, 1.32, 1.65, 1.222, 1.7, 0.2, 0.2, 0.6, 0.66, 1.4, 2.1],
            [1.0, 0.0, 1.2, 1.22, 0.3, 1.32, 1.65, 1.222, 1.7, 0.41, 0.2, 0.6, 0.66, 1.4, 2.1],
            [1.0, 0.0, 1.2, 1.22, 0.3, 1.32, 1.65, 1.222, 1.7, 0.2, 0.51, 0.6, 0.66, 1.4, 2.1],
            [1.0, 0.0, 1.2, 1.22, 0.3, 1.32, 1.65, 1.222, 1.7, 0.2, 0.2, 0.92, 0.66, 1.4, 2.1],
            [1.0, 0.0, 1.2, 1.22, 0.3, 1.32, 1.65, 1.222, 1.7, 0.2, 0.2, 0.6, 0.73, 1.4, 2.1]]

    # score test:
    assert score(placements, capacity) == 24.779
    # max_utility test:
    assert max_utility(utilities[0], budgets[0], prices, num_of_courses) == [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0,
                                                                             0]


if __name__ == '__main__':
    pytest.main([__file__])
