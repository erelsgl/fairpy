from typing import List, Dict, Callable, Set, Any
from fairpy.items.valuations import ValuationMatrix
import numpy as np

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

    Example 1: simple example.
    >>> course_allocation(ValuationMatrix([[60,30,6,4],[62,32,4,2]]),neighbors,score,0,[1.1,1.0],[1.1,0.9,0.1,0.0],[1,1,1,1])
    # ValuationMatrix([1, 0, 0, 1], [0, 1, 1, 0])

    Example 2: input that cannot be divided equally.
    >>> course_allocation(ValuationMatrix(np.array([[30, 70], [55, 45], [80, 20]])), neighbors, score, 0, [1.0, 1.1, 1.2], [1.2, 1.0], [1, 1])
    ValuationMatrix([0, 0], [0, 1], [1, 0])

    Example 3: input that can be divided equally.
    >>> course_allocation(ValuationMatrix(np.array([[36, 35, 13, 10, 4, 2], [1, 3, 43, 37, 7, 9], [5, 13, 12, 17, 25, 28]])), neighbors, score, 0, [1.5, 1.1, 1.3], [0.9, 0.3, 0.9, 1.1, 1.0, 0.2], [1,1,1,1,1,1])
    ValuationMatrix([1, 1, 0, 0, 0, 0], [0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 1])

    Example 4: input with popular courses.
    >>> course_allocation(ValuationMatrix([[49, 40, 10, 1], [53, 29, 15, 3], [61, 30, 7, 2]]), neighbors, score, 0, [1.3, 1.2, 1.0], [0.2, 0.5, 0.4, 0.6], [2,2,2,2])
    ValuationMatrix([0, 0, 1, 1], [1, 0, 1, 0], [1, 1, 0, 0])

    """
    pass


def neighbors(prices: List[float]) -> List[List[float]]:
    pass


def score(prices: List[float]) -> float:
    pass
