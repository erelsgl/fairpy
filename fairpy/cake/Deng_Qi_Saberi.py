#!python3

"""
Simplex robust algorithm for Divisible continuous segment of goods, with an approximation.
References:
    Xiaotie Deng, Qi Qi, Amin Saberi (2012):
    "Algorithmic Solutions for Envy-Free Cake Cutting"
    Algorithm 1.
Programmer: Dvir Fried
Since: 2020-01
"""

from fairpy.agents import *
from fairpy import Allocation

from typing import *
import numpy as np

import logging

logger = logging.getLogger(__name__)


# naming for function: FPTAS for 3 agents. this function is about being recursive one.


class SimplexSolver:
    def __init__(self, epsilon, n, agents):
        # finding a bit better approximation s.t its negative power of two
        x = 0.5
        while x > epsilon:
            x *= 0.5
        self.epsilon = x
        # reshape the size of base cell to be 1, and therefore the size is the cake size divide by the new epsilon
        self.N = int(n / x)
        self.agents = agents
        logger.info("finish initializing the simplex solver")

    def color(self, index_of_agent, triplet):
        """
        function that decide which color to assign to a specific vertex.
        :param index_of_agent: the agent's index, who need to 'color' (decide) the portion he prefer the most
        :param triplet: a triplet if indices, represent a vertex in the simplex, which is a partition of segment
        :return: a 'color', an integer between the group {0,1,2}, which part the agent prefer the most

        >>> George = PiecewiseConstantAgent([0, 2, 4, 6], name="George")
        >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
        >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
        >>> agents = [George, Abraham, Hanna]
        >>> solver = SimplexSolver(1/31, 4, agents)
        >>> right_index = solver.label([19, 29, 80])
        >>> solver.color(right_index, [19,29,80])
        2

        """
        # checking for validity of input
        if sum(triplet) != self.N or len(triplet) != 3 or index_of_agent < 0 or index_of_agent > 2:
            raise ValueError("Invalid triplet")

        # in order to get the right values and partition, the triplet is converted back to the right proportion
        partition = []
        counter = 0
        for i in range(len(triplet)):
            partition.append(self.epsilon * (triplet[i] + counter))
            counter += triplet[i]
        result = np.argmax(self.agents[index_of_agent].partition_values(partition))
        logger.info("agent %s picked piece num %d, in partition (%d, %d, %d)", self.agents[index_of_agent].name(),
                    result, triplet[0], triplet[1], triplet[2])
        return result

    def label(self, triplet):
        """
        function that compute for a vertex who is the agent that who suppose to assign its color
        :param triplet: a triplet if indices, represent a vertex in the simplex, which is a partition of segment
        :return: a label, an integer between the group {0,1,2}, which represent the agents index

        >>> George = PiecewiseConstantAgent([0, 2, 4, 6], name="George")
        >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
        >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
        >>> agents = [George, Abraham, Hanna]
        >>> solver = SimplexSolver(1/31, 4, agents)
        >>> solver.label([19, 29, 80])
        0

        """
        # checking for validity of input
        if sum(triplet) != self.N or len(triplet) != 3:
            raise ValueError("Invalid triplet")
        # according to the formula, sum up the product of i * Xi(the i'th element in a triplet), and then return mod 3
        label = sum([i * triplet[i] for i in range(len(triplet))]) % 3
        logger.info("the vertex(%d,%d,%d) is labeled for agent %s", triplet[0], triplet[1], triplet[2],
                    self.agents[label].name())
        return label

    def color_at_label(self, triplet):
        """
        function that gets a triplet representing a vertex in the simplex, and returns the color it gets from
        the right agent, the one's who has the same label.
        :param triplet: triplet of integers, represent a partition of the cake.
        :return: a color, an integer between the group {0,1,2}, which represent the cake piece number

        >>> George = PiecewiseConstantAgent([0, 2, 4, 6], name="George")
        >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
        >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
        >>> agents = [George, Abraham, Hanna]
        >>> solver = SimplexSolver(1/31, 4, agents)
        >>> solver.color_at_label([19, 29, 80])
        2
        >>> George = PiecewiseConstantAgent([0, 2, 4, 6], name="George")
        >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
        >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
        >>> agents = [George, Abraham, Hanna]
        >>> solver = SimplexSolver(1/2, 4, agents)
        >>> solver.color_at_label([0,8,0])
        1

        """

        if sum(triplet) != self.N or len(triplet) != 3:
            raise ValueError("Invalid triplet")
        right_agent_index = self.label(triplet)
        return self.color(right_agent_index, triplet)

    def index(self, i1, i2, k1, k2):
        """
        this function calculate how much swaps there is from color num. 0 to color num. 1, and return 0 if its
        sums to zero, and 1 otherwise.

        :param i1: the lower boundary of the first index polygon.
        :param i2: the upper boundary of the first index polygon.
        :param k1: the lower boundary of the third index polygon.
        :param k2: the upper boundary of the third index polygon.
        :return: 1 if it has non-zero index, and 0 if it has zero index

        >>> George = PiecewiseConstantAgent([4, 6], name="George")
        >>> Abraham = PiecewiseConstantAgent([6, 4], name="Abraham")
        >>> Hanna = PiecewiseConstantAgent([3, 3], name="Hanna")
        >>> agents = [George, Abraham, Hanna]
        >>> solver = SimplexSolver(1/2, 2, agents)
        >>> solver.index(0, solver.N, 0, solver.N)
        1

        >>> George = PiecewiseConstantAgent([4, 6], name="George")
        >>> Abraham = PiecewiseConstantAgent([6, 4], name="Abraham")
        >>> Hanna = PiecewiseConstantAgent([3, 3], name="Hanna")
        >>> agents = [George, Abraham, Hanna]
        >>> solver = SimplexSolver(1/2, 2, agents)
        >>> solver.index(0, 2, 0, 1)
        0

        """

        counter = 0
        # as the essay says, listing an array with proper j, which related to the segment we going to iterate over
        # this is where we deciding over which i's side to go, so the k1 gonna be fixed and the i's gonna change

        # when k1 is fixed
        proper_js_k1 = [j for j in range(self.N - i1 - k1 + 1) if j >= self.N - i2 - k2 and self.N - j - k1 <= i2]
        proper_js_k1.sort(reverse=True)
        # when i2 is fixed
        proper_js_i2 = [j for j in range(self.N - i2 - k1 + 1) if j >= self.N - i2 - k2]
        proper_js_i2.sort(reverse=True)
        # when k2 is fixed
        proper_js_k2 = [j for j in range(self.N - k2 - i1 + 1) if j >= self.N - k2 - i2]
        proper_js_k2.sort()
        # when i1 is fixed
        proper_js_i1 = [j for j in range(self.N - i1 - k1 + 1) if j >= self.N - i1 - k2]
        proper_js_i1.sort()

        last_color = self.color_at_label([self.N - max(proper_js_k1) - k1, max(proper_js_k1), k1])

        for j in proper_js_k1:
            # check the next vertex in the segment, and update the counter according to changes of colors
            check_color = self.color_at_label([self.N - j - k1, j, k1])
            if last_color == 0 and check_color == 1:
                counter += 1
            elif last_color == 1 and check_color == 0:
                counter -= 1
            last_color = check_color
        for j in proper_js_i2:
            check_color = self.color_at_label([i2, j, self.N - i2 - j])
            if last_color == 0 and check_color == 1:
                counter += 1
            elif last_color == 1 and check_color == 0:
                counter -= 1
            last_color = check_color
        if len(proper_js_k2) > 1:
            for j in proper_js_k2:
                check_color = self.color_at_label([self.N - k2 - j, j, k2])
                if last_color == 0 and check_color == 1:
                    counter += 1
                elif last_color == 1 and check_color == 0:
                    counter -= 1
                last_color = check_color
        else:
            j_min = min(proper_js_i2)
            i2_to_k2 = [self.N - i2 - j_min + t for t in range(k2 - k1 + 1) if self.N - i2 - j_min + t <= self.N]
            i2_to_k2.sort()
            for k in i2_to_k2:
                check_color = self.color_at_label([self.N - k - proper_js_k2[0], proper_js_k2[0], k])
                if last_color == 0 and check_color == 1:
                    counter += 1
                elif last_color == 1 and check_color == 0:
                    counter -= 1
                last_color = check_color
        for j in proper_js_i1:
            check_color = self.color_at_label([i1, j, self.N - i1 - j])
            if last_color == 0 and check_color == 1:
                counter += 1
            elif last_color == 1 and check_color == 0:
                counter -= 1
            last_color = check_color

        return 0 if counter == 0 else 1

    def recursive_algorithm1(self, i1, i2, k1, k2):
        """
        in the references, listed as 'Algorithm 1', a recursive function that cuts unnecessary vertices in the polygon,
        and by the recursive call we will get to a base triangle at the end, which its vertices can be return as proper
        partition.

        according to the essay, there is no need in having limits to all three, and during implementing its decided to
        leave it as close as possible to the essay, and therefore the middle index had left outside
        :param i1: the lower bound of the first index.
        :param i2: the upper bound of the first index.
        :param k1: the lower bound of the third index.
        :param k2: the upper bound of the third index.
        :return: a triplet, which represent a vertex that has a proper approximation for an envy-free cake cutting

        >>> George = PiecewiseConstantAgent([4, 6], name="George")
        >>> Abraham = PiecewiseConstantAgent([6, 4], name="Abraham")
        >>> Hanna = PiecewiseConstantAgent([3, 3], name="Hanna")
        >>> agents = [George, Abraham, Hanna]
        >>> solver = SimplexSolver(1/2, 2, agents)
        >>> solver.recursive_algorithm1(0, solver.N, 0, solver.N)
        [2, 1, 1]

        """

        # if the indices we still check define a group of 4 vertices, find a proper triangle and return its
        if i2 - i1 == 1 and k2 - k1 == 1:
            logger.info("end of recursive call, let's finally find a proper partition")
            vertex1_color = self.color_at_label([i1, self.N - i1 - k1, k1])
            vertex2_color = self.color_at_label([i1, self.N - i1 - k1 - 1, k1 + 1])
            vertex3_color = self.color_at_label([i1 + 1, self.N - i1 - k1 - 1, k1])
            # there is no need to develop the last vertex
            # if the triangle is the wrong triangle and two vertices is in same color, return vertex4 indices
            if vertex1_color == vertex2_color or vertex2_color == vertex3_color or vertex3_color == vertex1_color:
                logger.info("we found a division that is envy-free-approximation")
                arr = [i1 + 1, self.N - i1 - k1 - 2, k1 + 1]
                return arr
            # if its the right triangle, return one of its vertices
            else:
                logger.info("we found a division that is envy-free-approximation")
                arr = [i1 + 1, self.N - i1 - k1 - 1, k1]
                return arr
        else:
            # pick the max between the two, so we can cut by half the input size
            logger.info("we are checking for the next polygon to recurse on it")
            if i2 - i1 >= k2 - k1:
                i3 = int((i2 + i1) / 2)
                # compute the amount of swaps in the halved polygon, and if it has non-zero index then recurse on it
                if self.index(i1, i3, k1, k2) != 0:
                    return self.recursive_algorithm1(i1, i3, k1, k2)
                # due to the induction in the essay, at least one of them is, and therefore, recurse on the second one
                else:
                    return self.recursive_algorithm1(i3, i2, k1, k2)
            # the same routine, but with the third third index of the vertex.
            else:
                k3 = int((k2 + k1) / 2)
                if self.index(i1, i2, k1, k3) != 0:
                    return self.recursive_algorithm1(i1, i2, k1, k3)
                else:
                    return self.recursive_algorithm1(i1, i2, k3, k2)


def elaborate_simplex_solution(agents: List[Agent], epsilon) -> Allocation:
    """
    according to the algorithm in theirs essay, the algorithm will create class that solves the problem with simplex
    and return allocation.

    :param agents: a list that must contain exactly 3 Agent objects.
    :param epsilon: the approximation parameter
    :return: a proportional and envy-free-approximation allocation.

    >>> George = PiecewiseConstantAgent([4, 6], name="George")
    >>> Abraham = PiecewiseConstantAgent([6, 4], name="Abraham")
    >>> Hanna = PiecewiseConstantAgent([3, 3], name="Hanna")
    >>> agents = [George, Abraham, Hanna]
    >>> elaborate_simplex_solution(agents, 1/2)
    George gets {(0, 1.0)} with value 4.
    Abraham gets {(1.0, 1.5)} with value 2.
    Hanna gets {(1.5, 2)} with value 1.5.
    <BLANKLINE>
    """
    # checking parameters validity
    num_of_agents = len(agents)
    if num_of_agents != 3 or epsilon == 0:
        raise ValueError("This simplex solution works only for 3 agents, with approximation epsilon greater than 0")

    pieces = num_of_agents*[None]
    n = max([agent.cake_length() for agent in agents])

    # init the solver with simplex, with the approximation value, cake length and agents's list
    solver = SimplexSolver(epsilon, n, agents)

    # solver returns a vertex, which represent a proper partition of the segment
    triplet = solver.recursive_algorithm1(0, solver.N, 0, solver.N)
    # reversing the indices to a proper partition
    logger.info("we found a triplet of indices that represent a proper envy-free-approximation partition")
    or_indices = []
    counter = 0
    for i in range(len(triplet)):
        or_indices.append(solver.epsilon * (triplet[i] + counter))
        counter += triplet[i]
    first_index = solver.label(triplet)
    second_index = (first_index + 1) % 3
    third_index = (first_index + 2) % 3
    first_color_index = solver.color(first_index, triplet)

    if first_color_index == 0:
        # then allocate to him his choice
        pieces[first_index] = [(0, or_indices[0])]
        logger.info("%s gets the the piece [%f,%f].", solver.agents[first_index].name(), 0, or_indices[0])
        # find which of the next two has more envious between the leftovers pieces, and let him be second
        options = [(or_indices[0], or_indices[1]), (or_indices[1], n)]
        sec_dif = agents[second_index].eval(or_indices[0], or_indices[1]) - agents[second_index].eval(or_indices[1], n)
        thr_dif = agents[third_index].eval(or_indices[0], or_indices[1]) - agents[third_index].eval(or_indices[1], n)
        second = second_index if abs(sec_dif) >= abs(thr_dif) else third_index
        third = second_index if abs(sec_dif) < abs(thr_dif) else third_index

        # define which option goes to the second as first priority
        max_option = options[np.argmax(agents[second].eval(start, end) for (start, end) in options)]
        options.remove(max_option)
        min_option = options[np.argmin(agents[second].eval(start, end) for (start, end) in options)]

        # allocate both players

        pieces[second] = [max_option]
        logger.info("%s gets the the piece [%f,%f].", solver.agents[second].name(), max_option[0], max_option[1])
        pieces[third] = [min_option]
        logger.info("%s gets the the piece [%f,%f].", solver.agents[third].name(), min_option[0], min_option[1])

    elif first_color_index == 1:
        # same things happens, just for another option
        pieces[first_index] = [(or_indices[0], or_indices[1])]
        logger.info("%s gets the the piece [%f,%f].", solver.agents[first_index].name(), or_indices[0], or_indices[1])

        # find which of the next two has more envious between the leftovers pieces, and let him be second
        options = [(0, or_indices[0]), (or_indices[1], n)]
        sec_dif = agents[second_index].eval(0, or_indices[0]) - agents[second_index].eval(or_indices[1], n)
        thr_dif = agents[third_index].eval(0, or_indices[0]) - agents[third_index].eval(or_indices[1], n)
        second = second_index if abs(sec_dif) >= abs(thr_dif) else third_index
        third = second_index if abs(sec_dif) <= abs(thr_dif) else third_index

        # define which option goes to the second as first priority
        max_option = options[np.argmax(agents[second].eval(start, end) for (start, end) in options)]
        options.remove(max_option)
        min_option = options[np.argmin(agents[second].eval(start, end) for (start, end) in options)]

        # allocate both players

        pieces[second] = [max_option]
        logger.info("%s gets the the piece [%f,%f].", solver.agents[second].name(), max_option[0], max_option[1])
        pieces[third] = [min_option]
        logger.info("%s gets the the piece [%f,%f].", solver.agents[third].name(), min_option[0], min_option[1])
    else:
        # same things happens, just for another option
        pieces[first_index] = [(or_indices[1], n)]
        logger.info("%s gets the the piece [%f,%f].", solver.agents[first_index].name(), or_indices[1], n)

        # find which of the next two has more envious between the leftovers pieces, and let him be second
        options = [(0, or_indices[0]), (or_indices[0], or_indices[1])]
        sec_dif = agents[second_index].eval(0, or_indices[0]) - agents[second_index].eval(or_indices[0], or_indices[1])
        thr_dif = agents[third_index].eval(0, or_indices[0]) - agents[third_index].eval(or_indices[0], or_indices[1])
        second = second_index if abs(sec_dif) >= abs(thr_dif) else third_index
        third = second_index if abs(sec_dif) <= abs(thr_dif) else third_index

        # define which option goes to the second as first priority
        max_option = options[np.argmax(agents[second].eval(start, end) for (start, end) in options)]
        options.remove(max_option)
        min_option = options[np.argmin(agents[second].eval(start, end) for (start, end) in options)]

        # allocate both players
        pieces[second] = [max_option]
        logger.info("%s gets the the piece [%f,%f].", solver.agents[second].name(), max_option[0], max_option[1])
        pieces[third] = [min_option]
        logger.info("%s gets the the piece [%f,%f].", solver.agents[third].name(), min_option[0], min_option[1])

    return Allocation(agents, pieces)


if __name__ == '__main__':
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

