#!python3

"""
Truthful auction of Heterogeneous Divisible Goods with an approximation algorithm.

References:

    Yonatan Aumann, Yair Dombb, Avinatan Hassidim (2015):
    "Auctioning time: Truthful auctions of heterogeneous divisible goods"
    ACM Transactions on Economics and Computation, 4(1).

Programmers: Naama Berman and Yonatan Lifshitz
Since: 2019-12
"""

from agents import *
from allocations import *
from typing import *
from networkx import *
from math import *

import logging

logger = logging.getLogger(__name__)


def equally_sized_pieces(agents: List[Agent], piece_size: float) -> Allocation:
    """
    Algorithm 1.
    Approximation algorithm of the optimal auction for uniform-size pieces.

    :param agents: A list of Agent objects.
    :param piece_size: Size of an equally sized piece.
    :return: A cake-allocation, not necessarily all the cake will be allocated.

    >>> Alice = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([2, 90], "Bob")
    >>> equally_sized_pieces([Alice, Bob], 0.5)
    > Alice gets [(0, 1)] with value 100.00
    > Bob gets [(1, 2)] with value 90.00

    >>> Alice = PiecewiseConstantAgent([1, 1, 1, 1, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([3, 3, 3, 1, 1], "Bob")
    >>> equally_sized_pieces([Alice, Bob], 3 / 5)
    > Bob gets [(0, 3)] with value 9.00
    """
    num_of_agents = len(agents)
    if num_of_agents == 0:
        raise ValueError("There must be at least one agent")
    if not 0 < piece_size <= 1:
        raise ValueError("Piece size must be between 0 and 1")
    delta = 1 - int(1 / piece_size) * piece_size
    allocation = Allocation(agents)

    partition_0_l = create_partition(piece_size)
    partition_delta_l = create_partition(piece_size, start=delta)
    all_partitions = partition_0_l + partition_delta_l

    length = max([a.cake_length() for a in agents])
    normalize_partitions = [(int(p[0] * length), int(p[1] * length)) for p in all_partitions]

    evaluations = {}
    for piece in normalize_partitions:
        for agent in agents:
            evaluations[(agent, piece)] = agent.eval(start=piece[0], end=piece[1])

    g = create_matching_graph(agents, normalize_partitions, evaluations)
    edges_set = max_weight_matching(g)

    for edge in edges_set:
        allocation.set_piece(agent_index=agents.index(edge[1]), piece=[edge[0]])

    return allocation


def discrete_setting(agents: List[Agent], pieces: List[tuple]) -> Allocation:
    """
    Algorithm 2.
    Approximation algorithm of the optimal auction for a discrete cake with known piece sizes.

    :param agents: A list of Agent objects.
    :param pieces: List of sized pieces.
    :return: A cake-allocation.

    >>> Alice = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([2, 90], "Bob")
    >>> discrete_setting([Alice, Bob], [(0, 1), (1, 2)])
    > Alice gets [(0, 1)] with value 100.00
    > Bob gets [(1, 2)] with value 90.00
    """
    m = len(pieces)
    r = int(log(m, 2))
    allocation = Allocation(agents)

    max_weight = 0
    max_match = None
    for t in range(0, r):
        partition_i = change_partition(pieces, t)

        evaluations = {}
        for piece in partition_i:
            for agent in agents:
                evaluations[(agent, piece)] = agent.eval(start=piece[0], end=piece[1])

        g_i = create_matching_graph(agents, partition_i, evaluations)
        edges_set = max_weight_matching(g_i)
        weight = calculate_weight(g_i, edges_set)

        if weight > max_weight:
            max_match = edges_set

    for edge in max_match:
        allocation.set_piece(agent_index=agents.index(edge[1]), piece=[edge[0]])

    return allocation


def change_partition(partition:List[tuple], t: int) -> List[tuple]:
    ret = []
    for start in range(0, len(partition) - 2 ** t + 1, 2 ** t):
        end = start + 2 ** t - 1
        ret.append((partition[start][0], partition[end][1]))
    return ret


def calculate_weight(g: Graph, edges_set) -> float:
    ret = 0
    for edge in edges_set:
        ret += g.get_edge_data(edge[0], edge[1])['weight']
    return ret


def continuous_setting(agents: List[Agent]) -> Allocation:
    """
    Algorithm 3.
    Approximation algorithm of the optimal auction for a continuous cake.

    :param agents: A list of Agent objects.
    :return: A cake-allocation.

    >>> Alice1 = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Alice2 = PiecewiseConstantAgent([100, 1], "Alice")
    >>> continuous_setting([Alice1, Alice2])
    > Alice gets (0, 1) with value 101
    """
    pass


def create_partition(size:float, start: float=0) -> List[Tuple[float, float]]:
    """

    :param size:
    :param start:
    :return:
    """
    res = []
    end = start + size
    while end <= 1:
        res.append((start, end))
        start = end
        end = start + size
    return res


def create_matching_graph(left: List[Agent], right: List[Tuple[float, float]],
                          weights: Dict[Tuple[Agent, Tuple[float, float]], float])-> nx.Graph:
    """

    :param left:
    :param right:
    :param weights:
    :return:
    """
    g = nx.Graph()
    g.add_nodes_from(left, bipartite=0)
    g.add_nodes_from(right, bipartite=1)

    for key, value in weights.items():
        g.add_edge(key[0], key[1], weight=value)
    return g


if __name__ == '__main__':
    Alice = PiecewiseConstantAgent([100, 1], "Alice")
    Bob = PiecewiseConstantAgent([2, 90], "Bob")
    print(discrete_setting([Alice, Bob], [(0, 1), (1, 2)]))
    # print(equally_sized_pieces([Alice, Bob], 0.5))
