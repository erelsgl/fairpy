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

import logging

logger = logging.getLogger(__name__)


def equally_sized_pieces(agents: List[Agent], piece_size: float) -> Allocation:
    """
    Algorithm 1.
    Compute an approximation algorithm of auction for uniform-size pieces.

    :param agents: A list of Agent objects.
    :param piece_size: Size of an equally sized piece.
    :return: A proportional cake-allocation.

    >>> Alice = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([2, 90], "Bob")
    >>> equally_sized_pieces([Alice, Bob], 0.5)
    > Alice gets (0,0.5) with value 100
    > Bob gets (0.5, 1) with value 90
    """
    num_of_agents = len(agents)
    if num_of_agents == 0:
        raise ValueError("There must be at least one agent")
    if not 0 < piece_size <= 1:
        raise ValueError("Piece size must be between 0 and 1")
    delta = 1 - int(1 / piece_size) * piece_size
    allocation = Allocation(agents)

    return allocation


def discrete_setting(agents: List[Agent], pieces: List[tuple]) -> Allocation:
    """
    Algorithm 2.
    Compute an approximation algorithm of auction for number of pieces with known sizes.

    :param agents: A list of Agent objects.
    :param pieces: List of sized pieces.
    :return: A proportional cake-allocation.

    >>> Alice = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Bob = PiecewiseConstantAgent([2, 90], "Bob")
    >>> discrete_setting([Alice, Bob], [(0, 0.5), (0.5, 1)])
    > Alice gets (0,0.5) with value 100
    > Bob gets (0.5, 1) with value 90
    """
    pass


def continuous_setting(agents: List[Agent]) -> Allocation:
    """
    Algorithm 3.
    Compute an approximation algorithm of auction for a continuous cake.

    :param agents: A list of Agent objects.
    :return: A proportional cake-allocation.

    >>> Alice1 = PiecewiseConstantAgent([100, 1], "Alice")
    >>> Alice2 = PiecewiseConstantAgent([100, 1], "Alice")
    >>> continuous_setting([Alice1, Alice2])
    > Alice gets (0,1) with value 101
    """
    pass
