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


from agents import *
from allocations import *
from typing import *
from networkx import *
import numpy as np

import logging
logger = logging.getLogger(__name__)

# naming for function: FPTAS for 3 agents. this function is about being recursive one.

class Simplex_Solver:
    def __init__(self, epsilon, n, agents):
        # finding a bit better approximation s.t its negative power of two
        x = 1/2
        while x > epsilon:
            x /= 2
        self.epsilon = x
        # reshape the size of base cell to be 1, and therefore the size is the cake size divide to the new epsilon
        self.N = n/x
        self.agents = agents

    def color(self, index_of_agent, triplet):
        """
        function that decide which color to assign to a specific vertex.
        :param index_of_agent: the agent's index, who need to 'color' (decide) the portion he prefer the most
        :param triplet: a triplet if indices, represent a vertex in the simplex, which is a partition of segment
        :return: a 'color', an integer between the group {0,1,2}, which part the agent prefer the most
        """
        # checking for validity of input
        if sum(triplet) != self.N or len(triplet) != 3 or index_of_agent < 0 or index_of_agent > 2:
            raise ValueError("Invalid triplet")

        # in order to get the right values and partition, the triplet is converted back to the right proportion
        partition = [i * self.epsilon for i in range(len(triplet))]

        return np.argmax(self.agents[index_of_agent].partition_values(partition))

    def label(self, triplet):
        """
        function that compute for a vertex who is the agent that who suppose to assign its color
        :param triplet: a triplet if indices, represent a vertex in the simplex, which is a partition of segment
        :return: a label, an integer between the group {0,1,2}, which represent the agents index
        """
        # checking for validity of input
        if sum(triplet) != self.N or len(triplet) != 3:
            raise ValueError("Invalid triplet")
        # according to the formula, sum up the product of i * Xi(the i'th element in a triplet), and then return mod 3
        return sum([i * triplet[i] for i in range(len(triplet))]) % 3

    def color_at_label(self, triplet):
        if sum(triplet) != self.N or len(triplet) != 3:
            raise ValueError("Invalid triplet")
        right_agent_index = self.label(triplet)
        return self.color(right_agent_index, triplet)

    def index(self, quartet):
        return 0

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
        """

        # if the indices we still check define a group of 4 vertices, find a proper triangle and return its
        if i2 - i1 == 1 and k2 - k1 == 1:
            print("end of recursive call, let's finally find a proper partition")
            vertex1_color = self.color_at_label([i1, self.N - i1 - k1, k1])
            vertex2_color = self.color_at_label([i1, self.N - i1 - k1 - 1, k1 + 1])
            vertex3_color = self.color_at_label([i1 + 1, self.N - i1 - k1 - 1, k1])
            # there is no need to develop the last vertex
            # if the triangle is the wrong triangle and two vertices is in same color, return vertex4 indices
            if vertex1_color == vertex2_color or vertex2_color == vertex3_color or vertex3_color == vertex1_color:
                return [i1 + 1, self.N - i1 - k1 - 2, k1 + 1]
            # if its the right triangle, return one of its vertices
            else:
                return [i1 + 1, self.N - i1 - k1 - 1, k1]
        else:
            # pick the max between the two, so we can cut by half the input size
            if i2 - i1 >= k2 - k1:
                i3 = int((i2 - i1) / 2)
                # compute the amount of swaps in the halved polygon, and if it has non-zero index then recurse on it
                if self.index(i1, i3, k1, k2) != 0:
                    self.recursive_algorithm1(i1, i3, k1, k2)
                # due to the induction in the essay, at least one of them is, and therefore, recurse on the second one
                else:
                    self.recursive_algorithm1(i3, i2, k1, k2)
            # the same routine, but with the third third index of the vertex.
            else:
                k3 = int((k2 - k1) / 2)
                if self.index(i1, i2, k1, k3) != 0:
                    self.recursive_algorithm1(i1, i2, k1, k3)
                else:
                    self.recursive_algorithm1(i1, i2, k3, k2)


def elaborate_simplex_solution(agents: List[Agent], epsilon) -> Allocation:
    """
    according to the algorithm in theirs essay, the algorithm will create class that solves the problem with simplex
    and return allocation.

    :param agents: a list that must contain exactly 3 Agent objects.
    :param epsilon: the approximation parameter
    :return: a proportional and envy-free-approximation allocation.

    """
    # checking parameters validity
    num_of_agents = len(agents)
    if num_of_agents != 3:
        raise ValueError("This simplex solution works only for three agents")

    allocation = Allocation(agents)
    n = max(agent.cake_length() for agent in agents)

    # init the solver with simplex, with the approximation value, cake length and agents's list
    solver = Simplex_Solver(epsilon, n, agents)

    # solver returns a partition of the segment
    triplet = solver.recursive_algorithm1(0, solver.N, 0, solver.N)
    or_indices = [solver.epsilon * index for index in triplet]
    first_index = solver.label(triplet)
    second_index = (first_index + 1) % 3
    third_index = (first_index + 2) % 3
    first_color_index = solver.color(first_index, triplet)
    if first_color_index == 0:
        # then allocate to him his choice
        allocation.set_piece(first_index, [(0, or_indices[0])])

        # find which of the next two has more enviness between the leftovers pieces, and let him be second
        options = [(or_indices[0], or_indices[1]), (or_indices[1], n)]
        sec_dif = agents[second_index].eval(or_indices[0], or_indices[1]) - agents[second_index].eval(or_indices[1], n)
        thr_dif = agents[third_index].eval(or_indices[0], or_indices[1]) - agents[third_index].eval(or_indices[1], n)
        second = second_index if abs(sec_dif) >= abs(thr_dif) else third_index
        third = second_index if abs(sec_dif) <= abs(thr_dif) else third_index

        # define which option goes to the second as first priority
        max_option = options[np.argmax(agents[second].eval(start, end) for (start,end) in options)]
        min_option = options[np.argmin(agents[second].eval(start, end) for (start, end) in options)]

        # allocate both players
        allocation.set_piece(second, options[max_option])
        allocation.set_piece(third, options[min_option])

    elif first_color_index == 1:
        # same things happens, just for another option
        allocation.set_piece(first_index, [(or_indices[0], or_indices[1])])

        # find which of the next two has more enviness between the leftovers pieces, and let him be second
        options = [(0, or_indices[0]), (or_indices[1], n)]
        sec_dif = agents[second_index].eval(0, or_indices[0]) - agents[second_index].eval(or_indices[1], n)
        thr_dif = agents[third_index].eval(0, or_indices[0]) - agents[third_index].eval(or_indices[1], n)
        second = second_index if abs(sec_dif) >= abs(thr_dif) else third_index
        third = second_index if abs(sec_dif) <= abs(thr_dif) else third_index

        # define which option goes to the second as first priority
        max_option = options[np.argmax(agents[second].eval(start, end) for (start, end) in options)]
        min_option = options[np.argmin(agents[second].eval(start, end) for (start, end) in options)]

        # allocate both players
        allocation.set_piece(second, options[max_option])
        allocation.set_piece(third, options[min_option])
    else:
        # same things happens, just for another option
        allocation.set_piece(first_index, [(or_indices[1], n)])

        # find which of the next two has more enviness between the leftovers pieces, and let him be second
        options = [(0, or_indices[0]), (or_indices[0], or_indices[1])]
        sec_dif = agents[second_index].eval(0, or_indices[0]) - agents[second_index].eval(or_indices[0], or_indices[1])
        thr_dif = agents[third_index].eval(0, or_indices[0]) - agents[third_index].eval(or_indices[0], or_indices[1])
        second = second_index if abs(sec_dif) >= abs(thr_dif) else third_index
        third = second_index if abs(sec_dif) <= abs(thr_dif) else third_index

        # define which option goes to the second as first priority
        max_option = options[np.argmax(agents[second].eval(start, end) for (start, end) in options)]
        min_option = options[np.argmin(agents[second].eval(start, end) for (start, end) in options)]

        # allocate both players
        allocation.set_piece(second, options[max_option])
        allocation.set_piece(third, options[min_option])
    return allocation
