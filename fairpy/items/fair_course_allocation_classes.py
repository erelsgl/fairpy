from typing import List, Dict, Callable, Set, Any
from fairpy.items.valuations import ValuationMatrix


class Agent:

    def __init__(self, utility: List[int], effect_variable: Dict[Set, int], constraint: Dict[Set, int], budget: float):
        self.utility = utility
        self.effect_variable = effect_variable
        self.constraint = constraint
        self.budget = budget

    def max_utility(self, prices: List[float]) -> List[bool]:
        """
        Given a price vector for the courses, the program will return
        the most affordable course package for the student,
        according to the student's budget limitations and constraints.
        The returned placement vector is binary: contains 1 in index i if the student's package
        includes course i, and contains 0 in index i if the student's package does not include course i.


        :param: courses price vector
        :return: optimal placement of courses for the student.
        """
        pass


class FairCourseAllocation:

    def __init__(self, students: List[Any], courses: List[Any], utilities: ValuationMatrix,
                 effect_variables: List[Dict[Set, int]], constraint: List[Dict[Set, int]]):
        """
        Note: A valuation matrix is a matrix v in which each row represents an agent,
        each column represents an object, and v[i][j] is the value of agent i to object j.
        """

        self.students = students
        self.courses = courses
        self.utilities = utilities
        self.effect_variables = effect_variables
        self.constraint = constraint
        self.agentList = list()

    def initialization(self) -> None:
        """
        The function initializes a list of agents, according to the received values.
        In addition, the function randomly selects a budget for each agent,
        and in addition the function initializes an initial price vector

        """
        pass

    def neighbors(self, prices: List[float]) -> List[List[float]]:
        """
        The neighbors function receives a current price vector, and produces for it a list of
        price vectors that are close to it according to the algorithm described in the article,
        where the goal is to produce a price vector that will reduce the gap between the demand
        and supply of the courses as much as possible.

        :param prices:
        :return: neighbors prices vectors.
        """
        pass

    def tabu_search(self, neighbors: Callable, score: Callable, bound: float) -> List[List[bool]]:
        """
        The main function.
        The tabu search aims to find the price vector P for which the gap between demand and supply
        will be as small as possible, thus allowing for an optimal and fair distribution of the courses.
        The search uses the neighbors function to find the optimal price vectors, and the score function
        that calculates the gap between demand and supply for a given price vector.
        The search continues as long as the SCORE is greater than the desired bound.
        At the end of the search, the vector will determine the optimal price, according to which the
        program will output the optimal course package for each student.

        :param neighbors:
        :param score:
        :param bound:
        :return:
        """
        pass
