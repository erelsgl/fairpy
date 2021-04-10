#!python3

"""
Represents an allocation of a cake among agents ---  the output of a cake-cutting algorithm.
Used mainly for display purposes.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""

from typing import *
from fairpy.criteria import  is_envyfree
from fairpy.cake.agents import Agent, PiecewiseUniformAgent
from fairpy.cake.pieces import round_piece


class Allocation:
    """
    >>> Alice = PiecewiseUniformAgent([(2,3)], "Alice");George = PiecewiseUniformAgent([(0,10)], "George")
    >>> A = Allocation([Alice, George])
    >>> A.setPieces([[(1,2)],[(4,5)]]);
    >>> print(A)
    > Alice gets [(1, 2)] with value 0.0
    > George gets [(4, 5)] with value 1.0
    <BLANKLINE>
    >>> B = Allocation([George, Alice])
    >>> B.setPieces([[(0,1)],[(2,3)]]);
    >>> print(B)
    > George gets [(0, 1)] with value 1.0
    > Alice gets [(2, 3)] with value 1.0
    <BLANKLINE>
    >>> A.merge(B)
    >>> print(A)
    > Alice gets [(1, 2), (2, 3)] with value 1.0
    > George gets [(4, 5), (0, 1)] with value 2.0
    <BLANKLINE>
    >>> A.isEnvyFree(2)
    True
    """

    def __init__(self, agents:List[Agent], pieces:list=None):
        self.agents = agents
        if pieces is None:
            pieces = [None]*len(agents)
        self.pieces = pieces

    def get_piece(self, agent_index:int):
        return self.pieces[agent_index]

    def get_pieces(self):
        return self.pieces

    def set_piece(self, agent_index:int, piece:List[Tuple[float]]):
        """
        Sets the piece of the given index.

        :param agent_index: index of the agent.
        :param piece: a list of intervals.
        """
        self.pieces[agent_index] = piece


    def setAgents(self, agents):
        self.agents = agents

    def setPieces(self, pieces):
        self.pieces = pieces

    def isEnvyFree(self, roundAcc):
        """
        checks whether or not the allocation is envy free.

        :param roundAcc: the accuracy in digits of the envy free check.
        :return: True is the allocation is envy free, otherwise False.

        >>> Alice = PiecewiseUniformAgent([(2,3)], "Alice");George = PiecewiseUniformAgent([(0,10)], "George")
        >>> A = Allocation([Alice, George]);A.setPieces([[(1,2),(2,3)],[(4,5),(0,1)]]);
        >>> A.isEnvyFree(2)
        True
        """
        return is_envyfree(self.agents, self.pieces, roundAcc)

    def __repr__(self):
        s = ""
        for i in range(len(self.pieces)):
            agent = self.agents[i]
            piece = self.pieces[i]
            if piece is None:
                s += "> {} gets {} with value {}\n".format(agent.name(), None, round(agent.piece_value(piece),3))
            else:
                s += "> {} gets {} with value {}\n".format(agent.name(), round_piece(piece, digits=3), round(agent.piece_value(piece),3))
        return s


class OnePieceAllocation(Allocation):

    def __init__(self, agents: List[Agent]):
        super().__init__(agents)

    def set_piece(self, agent_index:int, piece:tuple):
        """
        Sets the piece of the given index.

        :param agent_index: index of the agent.
        :param piece: a list of intervals.
        """
        self.pieces[agent_index] = piece

    def get_piece(self,agent_index:int):
        return self.pieces[agent_index]






if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures,tests))
