#!python3

"""
Truthful auction of Heterogeneous Divisible Goods with an approximation algorithm.
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
        # checking for validity of input
        if sum(triplet) != self.N or len(triplet) != 3 or index_of_agent < 0 or index_of_agent > 2:
            raise ValueError("Invalid triplet")
        # in order to get the right values and partition, the triplet is converted back to the right proportion
        partition = [i * self.epsilon for i in range(len(triplet))]
        return np.argmax(self.agents[index_of_agent].partition_values(partition))

    def label(self, triplet):
        # checking for validity of input
        if sum(triplet) != self.N or len(triplet) != 3:
            raise ValueError("Invalid triplet")
        return sum([i * triplet[i] for i in range(len(triplet))]) % 3

    def color_at_label(self, triplet):
        if sum(triplet) != self.N or len(triplet) != 3:
            raise ValueError("Invalid triplet")
        right_agent_index = self.label(triplet)
        return self.color(right_agent_index, triplet)

    def index(self, quartet):
        return 0

    def recursive_algorithm1(self, i1, i2, k1, k2):
        if i2 - i1 == 1 and k2 - k1 == 1:
            print("end of recursive call, let's finally find a proper partition")
            vertex1_color = self.color_at_label(i1, self.N - i1 - k1, k1)
            vertex2_color = self.color_at_label(i1, self.N - i1 - k1 - 1, k1 + 1)
            vertex3_color = self.color_at_label(i1 + 1, self.N - i1 - k1 - 1, k1)
            if vertex1_color != vertex2_color and vertex2_color != vertex3_color and vertex3_color != vertex1_color:
                return i1, self.N - i1 - k1, k1
            else:
                return i1 + 1, self.N - i1 - k1 - 2, k1 + 1
        else:
            if i2 - i1 >= k2 - k1:
                i3 = int((i2 - i1) / 2)
                if self.index(i1, i3, k1, k2) != 0:
                    self.recursive_algorithm1(i1, i3, k1, k2)
                else:
                    self.recursive_algorithm1(i3, i2, k1, k2)
            else:
                k3 = int((k2 - k1) / 2)
                if self.index(i1, i2, k1, k3) != 0:
                    self.recursive_algorithm1(i1, i2, k1, k3)
                else:
                    self.recursive_algorithm1(i1, i2, k3, k2)


def robust_simplex_solution(agents: List[Agent], epsilon) -> Allocation:
    """
    according to the algorithm in theirs essay, the algorithm will create class that gonna solve with simplex
    and return allocation.

    :param agents: a list that must contain exactly 2 Agent objects.
    :param epsilon: the approximation parameter
    :return: a proportional and envy-free-approximation allocation.

    >>> Alice = PiecewiseConstantAgent([33,33], "Alice")
    >>> George = PiecewiseConstantAgent([11,55], "George")
    >>> asymmetric_protocol([Alice, George])
    > Alice gets [(0, 1.0)] with value 33.00
    > George gets [(1.0, 2)] with value 55.00
    <BLANKLINE>
    >>> asymmetric_protocol([George, Alice])
    > George gets [(1.4, 2)] with value 33.00
    > Alice gets [(0, 1.4)] with value 46.20
    <BLANKLINE>

    >>> Alice = PiecewiseConstantAgent([33,33,33], "Alice")
    >>> asymmetric_protocol([Alice, George])
    > Alice gets [(1.5, 3)] with value 49.50
    > George gets [(0, 1.5)] with value 38.50
    <BLANKLINE>
    >>> asymmetric_protocol([George, Alice])
    > George gets [(0, 1.4)] with value 33.00
    > Alice gets [(1.4, 3)] with value 52.80
    <BLANKLINE>
    """

    num_of_agents = len(agents)
    if num_of_agents != 3:
        raise ValueError("This simplex solution works only for three agents")

    allocation = Allocation(agents)


    # logger.info("The cutter (%s) cuts at %.2f.", cutter.name(), cut)



    return allocation



# naming for function inside: index(V(i_1, i_2, k_1, k_2).
# this function is the one who divides V to subsets under those boundaries.
