from typing import List, Dict, Callable, Set, Any
from fairpy.items.valuations import ValuationMatrix


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


def course_allocation(utilities: ValuationMatrix, neighbors_func: Callable, score_func: Callable,
                      bound: float, budgets: List[float], prices: List[float], capacity: List[int],
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
    >>> course_allocation(ValuationMatrix([[60,30,6,4],[62,32,4,2]]),neighbors,score,0,[1.1,1.0],[1.1,0.9,0.1,0.0],[1,1,1,1])
    ValuationMatrix([1, 0, 0, 1], [0, 1, 1, 0])

    Example 2: input that cannot be divided equally.
    >>> course_allocation(ValuationMatrix([[30, 70], [55, 45], [80, 20]]), neighbors, score, 0, [1.0, 1.1, 1.2], [1.2, 1.0], [1, 1])
    ValuationMatrix([0, 0], [0, 1], [1, 0])

    Example 3: input that can be divided equally.
    >>> course_allocation(ValuationMatrix([[36, 35, 13, 10, 4, 2], [1, 3, 43, 37, 7, 9], [5, 13, 12, 17, 25, 28]]), neighbors, score, 0, [1.5, 1.1, 1.3], [0.9, 0.3, 0.9, 1.1, 1.0, 0.2], [1,1,1,1,1,1])
    ValuationMatrix([1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1])

    Example 4: input with popular courses.
    >>> course_allocation(ValuationMatrix([[49, 40, 10, 1], [53, 29, 15, 3], [61, 30, 7, 2]]), neighbors, score, 0, [1.3, 1.2, 1.0], [0.2, 0.5, 0.4, 0.6], [2,2,2,2])
    ValuationMatrix([0, 0, 1, 1], [1, 0, 1, 0], [1, 1, 0, 0])
    """

    pass


def neighbors(utilities: ValuationMatrix, budgets: List[float], prices: List[float], capacity: List[int],
              effect_variables: List[Dict[Set, int]] = None, constraint: List[Dict[Set, int]] = None)\
        -> List[List[float]]:
    """
    The neighbors function receives a current price vector, and produces for it a list of
    price vectors that are close to it according to the algorithm described in the article,
    where the goal is to produce a price vector that will reduce the gap between the demand
    and supply of the courses as much as possible.

    Example 1:
    >>> neighbors(ValuationMatrix([[30, 70], [55, 45], [80, 20]]), [1.0, 1.1, 1.2], [1.2, 1.0], [1, 1])
    [[0, 1], [1.2, 1.01]]

    Example 2:
    >>> neighbors(ValuationMatrix([[36, 35, 13, 10, 4, 2], [1, 3, 43, 37, 7, 9], [5, 13, 12, 17, 25, 28]]), [1.5, 1.1, 1.3], [0.9, 0.3, 0.9, 1.1, 1.0, 0.2], [1,1,1,1,1,1])
    [[0, 0, 0, -1, 0 ,1], [0.9, 0.3, 0.9, 1.11, 1.0, 0,2]]

    Example 3:
    >>> neighbors(ValuationMatrix([[49, 40, 10, 1], [53, 29, 15, 3], [61, 30, 7, 2]]), [1.3, 1.2, 1.0], [0.2, 0.5, 0.4, 0.6], [2,2,2,2])
    [[1, 1, 0, 0], [0.61, 0.5, 0.4, 0.6], [0.2, 0.81, 0.4, 0.6]]
    """

    pass


def score(placement: ValuationMatrix, capacity: List[int]) -> float:
    """
    The function receives the course packages assigned to the students and a vector with
    the number of places for all courses, and returns the gap between demand and supply.

    Example 1: min score.
    >>> score(ValuationMatrix([[0, 1],[1, 0]]),[1,1])
    0.0

    Example 2:
    >>> score(ValuationMatrix([[0, 1, 1, 0],[0, 1, 1, 0], [0, 1, 1, 0]]),[1,1,1,1])
    math.sqrt(8)

    Example 3:
    >>> score(ValuationMatrix([[0, 1, 0, 0],[0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 1, 0]]),[2,2,2,2])
    1.0
    """

    pass


def max_utility(utility: List[float], budget: float, prices: List[float],
                effect_variables: List[Dict[Set, int]] = None, constraint: List[Dict[Set, int]] = None) \
        -> List[bool]:
    """
    Given a price vector for the courses, the program will return
    the most affordable course package for the student,
    according to the student's budget limitations and constraints.
    The returned placement vector is binary: contains 1 in index i if the student's package
    includes course i, and contains 0 in index i if the student's package does not include course i.


    Example 1: best courses
    >>> max_utility([60,30,6,4],1.1,[1.1,0.9,0.1,0.0])
    [1, 1, 0, 0]

    Example 2: not enough budget
    >>> max_utility([99, 1], 1.0, [1.2, 1.0])
    [0, 1]

    Example 3: not enough budget
    >>> max_utility([36, 35, 13, 10, 4, 2], 1.0, [0.9, 0.3, 0.9, 1.1, 1.0, 0.2])
    [1, 0, 0, 0, 0, 0]
    """

    pass
