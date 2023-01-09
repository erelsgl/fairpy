import heapq
import logging
import math
import sys
from typing import List, Dict, Callable, Set, Any

import numpy as np
from fairpy.items.valuations import ValuationMatrix
from queue import PriorityQueue
import cvxpy as cp
from cvxopt import matrix



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

logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

# console = logging.StreamHandler()  # writes to stderr (= cerr)
# logger.handlers = [console]
# logger.setLevel(logging.INFO)

Epsilon = 0.01


def general_course_allocation(utilities: ValuationMatrix, capacity: List[int], num_of_courses: int,
                      effect_variables: List[Dict[Set, int]] = None, constraint: List[Dict[Set, int]] = None) \
        -> ValuationMatrix:

    """
    This function find the optimal course package for each student.
    The function inserts random values for the price of each course (between 0 and 1)
    and for the budget of each student (between 1 and 2).

    """

    budgets = []
    prices = []

    for student in utilities.agents():
        budgets.append(1 + np.random.randint(1, 100)/100)

    for course in utilities.objects():
        prices.append(np.random.randint(1, 100)/100)

    return course_allocation(utilities, budgets, prices, capacity, num_of_courses, effect_variables, constraint)


def course_allocation(utilities: ValuationMatrix, budgets: List[float], prices: List[float], capacity: List[int],
                      num_of_courses: int, bound = 0,
                      effect_variables: List[Dict[Set, int]] = None, constraint: List[Dict[Set, int]] = None) \
        -> ValuationMatrix:
    """
    The main function.
    The tabu search aims to find the price vector P for which the gap between demand and supply
    will be as small as possible, thus allowing for an optimal and fair distribution of the courses.
    The search uses the neighbors function to find the optimal price vectors, and the score function
    that calculates the gap between demand and supply for a given price vector.
    The search continues as long as the SCORE is greater than the desired bound.
    At the end of the search, the vector will determine the optimal price, according to which the
    program will output the optimal course package for each student.

    Example 1: simple example.
    >>> course_allocation(ValuationMatrix([[60,30,6,4],[62,32,4,2]]),[1.1,1.0],[1.1,0.9,0.1,0.0],[1,1,1,1], 2)
    [[1, 0, 0, 1], [0, 1, 1, 0]]

    Example 2: input that cannot be divided equally.
    >>> course_allocation(ValuationMatrix([[30, 70], [55, 45], [80, 20]]), [1.0, 1.1, 1.2], [1.2, 1.0], [1, 1], 1)
    [[0, 0], [0, 1], [1, 0]]

    Example 3: input that can be divided equally.
    >>> course_allocation(ValuationMatrix([[36, 35, 13, 10, 4, 2], [1, 3, 43, 37, 7, 9], [5, 13, 12, 17, 25, 28]]), [1.3, 1.1, 1.5], [0.9, 0.3, 0.9, 1.1, 1.0, 0.2], [1,1,1,1,1,1], 2)
    [[1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1]]

    Example 4: input with popular courses.
    >>> course_allocation(ValuationMatrix([[49, 40, 8, 3], [53, 29, 15, 3], [61, 30, 7, 2]]), [0.7, 1.2, 1.3], [0.2, 0.4, 0.2, 0.6], [2,2,2,2], 2)
    [[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 0]]
    """

    logger.info('course_allocation function')

    q = PriorityQueue()
    tabu = []
    curr_node: Course_Bundle = Course_Bundle(utilities, budgets, prices, capacity, num_of_courses)
    best_node = curr_node

    counter = 0
    max_iterations = 100

    while best_node.score() > bound:

        if counter == max_iterations:
            break

        tabu.append(curr_node)
        for p in curr_node.neighbors():
            q.put(Course_Bundle(utilities, budgets, p, capacity, num_of_courses))

        curr_node = q.get()
        while tabu.__contains__(curr_node):
            curr_node = q.get()

        if curr_node.score() < best_node.score():
            logger.debug('The new best_node score is: %g', best_node.score())
            best_node = curr_node

        counter += 1

    return best_node.placement


def neighbors(utilities: ValuationMatrix, budgets: List[float], prices: List[float], capacity: List[int],
              num_of_courses: int,
              effect_variables: List[Dict[Set, int]] = None, constraint: List[Dict[Set, int]] = None) \
        -> List[List[float]]:
    """
    The neighbors function receives a current price vector, and produces for it a list of
    price vectors that are close to it according to the algorithm described in the article,
    where the goal is to produce a price vector that will reduce the gap between the demand
    and supply of the courses as much as possible.

    Example 1:
    >>> neighbors(ValuationMatrix([[30, 70], [55, 45], [80, 20]]), [1.0, 1.1, 1.2], [1.2, 1.0], [1, 1], 1)
    [[0, 1], [1.2, 1.01]]

    Example 2:
    >>> neighbors(ValuationMatrix([[36, 35, 13, 10, 4, 2], [1, 3, 43, 37, 7, 9], [5, 13, 12, 17, 25, 28]]), [1.3, 1.1, 1.5], [0.9, 0.3, 0.9, 1.1, 1.0, 0.2], [1,1,1,1,1,1], 2)
    [[0, 0, 0, -1, 0, 1], [0.9, 0.3, 0.9, 1.1, 1.0, 0.21000000000000002]]

    Example 3:
    >>> neighbors(ValuationMatrix([[49, 40, 8, 3], [53, 29, 15, 3], [61, 30, 7, 2]]), [1.0, 1.2, 1.3], [0.2, 0.5, 0.4, 0.6], [2,2,2,2], 2)
    [[1, 1, -2, -2], [1.01, 0.5, 0.4, 0.6], [0.2, 0.81, 0.4, 0.6]]
    """

    logger.info('neighbors function')

    neighbors_list = []
    placement = max_utilities(utilities, budgets, prices, num_of_courses)
    placement_sum = np.sum(placement, axis=0)

    # 1) find neighbor by gradiant:
    gradiant = []

    for index, size in enumerate(placement_sum):
        if prices[index] > 0:
            gradiant.append(size - capacity[index])
        else:
            gradiant.append(max(size - capacity[index], 0))
    neighbors_list.append(gradiant)

    # 2) find neighbors for each individual price:
    courses_num = len(prices)
    students_num = len(budgets)

    for course in range(0, courses_num):
        # Checking whether the course has excess demand:
        if capacity[course] < placement_sum[course]:

            pi = math.inf

            for student in range(0, students_num):
                # Checking whether the course belongs to the student's bundle:
                if placement[student][course] == 1:

                    # 2.1) Looking for the package with the maximum value that *does not* contain the current course:
                    x1 = cp.Variable(shape=(courses_num, 1), boolean=True)
                    objective1 = cp.Maximize(np.array(utilities[student]) @ x1)
                    constraints = [sum(np.array(prices) @ x1) <= budgets[student],
                                   x1[course] == 0,
                                   sum(x1) <= num_of_courses]
                    prob = cp.Problem(objective1, constraints)
                    prob.solve()
                    # The maximum value of the package without the current course for the current student:
                    O1 = prob.value
                    logger.debug('The maximum value without course %g for student %g is: %g', course, student, O1)

                    # 2.2) Looking for the package with the minimum price whose value is greater than O1 and contains the current course:
                    x2 = cp.Variable(shape=(courses_num, 1), boolean=True)
                    objective2 = cp.Minimize(np.array(prices) @ x2)
                    constraints = [sum(np.array(utilities[student]) @ x2) >= O1 + Epsilon,
                                   x2[course] == 1,
                                   sum(x2) <= num_of_courses]
                    prob = cp.Problem(objective2, constraints)
                    prob.solve()
                    O2 = prob.value
                    logger.debug('The minimum price with course %g for student %g is: %g', course, student, O2)

                    if (budgets[student] - O2 + Epsilon) < pi:
                        pi = budgets[student] - O2 + Epsilon

            new_prices = prices.copy()
            new_prices[course] = prices[course] + pi
            neighbors_list.append(new_prices)

    return neighbors_list


def score(placement: List[List[bool]], capacity: List[int]) -> float:
    """
    The function receives the course packages assigned to the students and a vector with
    the number of places for all courses, and returns the gap between demand and supply.

    Example 1: min score.
    >>> score([[0, 1],[1, 0]],[1,1])
    0.0

    Example 2:
    >>> score([[0, 1, 1, 0],[0, 1, 1, 0], [0, 1, 1, 0]],[1,1,1,1])
    2.8284271247461903

    Example 3:
    >>> score([[0, 1, 0, 0],[0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0]],[2,2,2,2])
    1.0
    """

    logger.info('score function')

    ans = 0
    placement_sum = np.sum(placement, axis=0)
    for index, size in enumerate(placement_sum):
        if capacity[index] < size:
            ans += (size - capacity[index]) ** 2

    return math.sqrt(ans)


def max_utility(utility: List[float], budget: float, prices: List[float], num_of_courses: int,
                effect_variables: List[Dict[Set, int]] = None, constraint: List[Dict[Set, int]] = None) \
        -> List[bool]:
    """
    Given a price vector for the courses, the program will return
    the most affordable course package for the student,
    according to the student's budget limitations and constraints.
    The returned placement vector is binary: contains 1 in index i if the student's package
    includes course i, and contains 0 in index i if the student's package does not include course i.


    Example 1: best courses
    >>> max_utility([60,30,6,4],1.1,[1.1,0.9,0.1,0.0], 2)
    [1, 0, 0, 1]

    Example 2: not enough budget
    >>> max_utility([99, 1], 1.0, [1.2, 1.0], 1)
    [0, 1]

    Example 3: not enough budget
    >>> max_utility([36, 35, 13, 10, 4, 2], 1.0, [0.9, 0.3, 0.9, 1.1, 1.0, 0.2], 2)
    [0, 1, 0, 0, 0, 1]
    """

    size = len(utility)
    # Create binary variables
    x = cp.Variable(shape=(size, 1), boolean=True)
    # Define the objective function
    objective = cp.Maximize(np.array(utility) @ x)
    # Add constraints
    constraints = [sum(np.array(prices) @ x) <= budget,
                   sum(x) <= num_of_courses]
    # Form and solve the problem
    prob = cp.Problem(objective, constraints)
    prob.solve()
    return x.value.ravel().astype(int).tolist()


def max_utilities(utilities: ValuationMatrix, budgets: List[float], prices: List[float], num_of_courses: int,
                  effect_variables: List[Dict[Set, int]] = None, constraint: List[Dict[Set, int]] = None) \
        -> List[List[bool]]:

    """
    The function receives a ValuationMatrix containing utilities of several students,
    and calculates with the help of the max_utility function for each of the students
    the most affordable course package for him.
    Finally the function returns a matrix containing all the placements for all the students.

    Example 1:
    >>> max_utilities(ValuationMatrix([[60,30,6,4],[62,32,4,2]]),[1.1,1.0],[1.1,0.9,0.1,0.0], 2)
    [[1, 0, 0, 1], [0, 1, 1, 0]]

    Example 2:
    >>> max_utilities(ValuationMatrix([[30, 70], [55, 45], [80, 20]]), [1.0, 1.1, 1.2], [1.2, 1.0], 1)
    [[0, 1], [0, 1], [1, 0]]

    Example 3:
    (after tabu search the output will be: [[1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1]] )
    >>> max_utilities(ValuationMatrix([[36, 35, 13, 10, 4, 2], [1, 3, 43, 37, 7, 9], [5, 13, 12, 17, 25, 28]]), [1.3, 1.1, 1.5], [0.9, 0.3, 0.9, 1.1, 1.0, 0.2], 2)
    [[1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 1], [0, 0, 0, 0, 1, 1]]

    """

    logger.info('max_utilities function')

    placements = []

    for student in utilities.agents():
        placement: List[bool] = max_utility(utilities[student], budgets[student], prices, num_of_courses)
        placements.append(placement)

    return placements


class Course_Bundle:
    """
    Structure for a bundle of courses.
    The structure is intended to be used by the main function,
    which contains a priority queue, which needs to implement for
    the queue a comparison function between price vectors of packages.

    >>> course_bundle1 = Course_Bundle(ValuationMatrix([[60,30,6,4],[62,32,4,2]]),[1.1,1.0],[1.1,0.9,0.1,0.0],[1,1,1,1], 2)
    >>> course_bundle2 = Course_Bundle(ValuationMatrix([[36, 35, 13, 10, 4, 2], [1, 3, 43, 37, 7, 9], [5, 13, 12, 17, 25, 28]]), [1.3, 1.1, 1.5], [0.9, 0.3, 0.9, 1.1, 1.0, 0.2], [1,1,1,1,1,1], 2)

    >>> course_bundle1.score()
    0.0
    >>> course_bundle2.score()
    1.0
    >>> course_bundle1.neighbors()
    [[0, 0, 0, 0]]
    >>> course_bundle2.neighbors()
    [[0, 0, 0, -1, 0, 1], [0.9, 0.3, 0.9, 1.1, 1.0, 0.21000000000000002]]
    >>> course_bundle1 < course_bundle2
    True

    """

    def __init__(self, utilities: ValuationMatrix, budgets: List[float],
                 prices: List[float], capacity: List[int], num_of_courses: int):
        self.utilities = utilities
        self.budgets = budgets
        self.prices = prices
        self.capacity = capacity
        self.num_of_courses = num_of_courses
        self.placement = max_utilities(self.utilities, self.budgets, self.prices, self.num_of_courses)

    def score(self):
        return score(self.placement, self.capacity)

    def neighbors(self):
        return neighbors(self.utilities, self.budgets, self.prices, self.capacity, self.num_of_courses)

    def __lt__(self, other):
        return self.score() < other.score()

    def __eq__(self, other):
        return np.array_equal(np.array(self.prices), np.array(other.prices))


if __name__ == '__main__':

    import doctest

    doctest.testmod()

    # print(general_course_allocation( ValuationMatrix([[30, 70], [55, 45], [80, 20]]), [1, 1], 1))

    # utilities = ValuationMatrix([[3, 7, 1, 13, 34, 23, 24, 5, 77, 32, 12, 22, 34, 18, 51],
    #                              [5, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [76, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [22, 3, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [56, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [28, 7, 1, 64, 34, 23, 24, 5, 77, 32, 12, 22, 34, 18, 51],
    #                              [50, 2, 7, 33, 14, 58, 95, 33, 2, 2, 77, 90, 34, 21, 63],
    #                              [59, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 9, 34, 21, 63],
    #                              [23, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 93, 34, 21, 63],
    #                              [86, 2, 7, 33, 14, 9, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [33, 7, 1, 64, 34, 23, 24, 5, 77, 32, 12, 22, 34, 18, 51],
    #                              [53, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [22, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [40, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [86, 2, 7, 33, 14, 9, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [33, 7, 1, 64, 34, 23, 24, 5, 77, 32, 12, 22, 34, 18, 51],
    #                              [53, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [22, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [40, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63],
    #                              [5, 2, 7, 33, 14, 58, 95, 33, 5, 2, 77, 90, 34, 21, 63]])
    #
    # bound: float = 0
    # budgets: List[float] = [1.0, 1.11, 1.2, 1.22, 1.43, 1.32, 1.65, 1.222, 1.7, 1.56, 1.3, 1.41, 1.62, 1.52, 1.435,
    #                         1.932, 1.685, 1.24, 1.27, 1.666]
    # prices: List[float] = [1.0, 0.0, 1.2, 1.22, 0.3, 1.32, 1.65, 1.222, 1.7, 0.2, 0.2, 0.6, 0.66, 1.4, 2.1]
    # capacity: List[int] = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    # num_of_courses = 4
    #
    #
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

    bound: float = 0
    budgets: List[float] = [1.0, 1.11, 1.2, 1.7, 1.56, 1.3, 1.41, 1.62, 1.52, 1.435]
    prices: List[float] = [1.9, 0.3, 1.6, 1.2, 0.8]
    capacity: List[int] = [2, 2, 2, 2, 2]
    num_of_courses = 2

    placements = []
    for i in utilities.agents():
        placements.append(max_utility(utilities[i], budgets[i], prices, num_of_courses))

    # course_allocation test:
    print("course_allocation:")
    print(np.array(course_allocation(utilities, budgets, prices, capacity, num_of_courses)))
    # neighbors test:
    print("neighbors:")
    print(neighbors(utilities, budgets, prices, capacity, num_of_courses))
    # score test:
    print("score:")
    print(score(placements, capacity))
    # max_utility test:
    print("max_utility")
    print(max_utility(utilities[0], budgets[0], prices, num_of_courses))
