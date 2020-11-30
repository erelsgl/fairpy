"""
Defines cake-allocations.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""

# import repackage
# repackage.up()

from typing import *
from cake.agents import Agent, PiecewiseUniformAgent

def round_piece(piece:list, digits:int):
    """
    Round the numbers in the given piece. For presentation purposes.
    :param piece:   A list of intervals.
    :param digits:  How many digits after the decimal point.

    >>> round_piece([(0.1999999, 0.300001), (0.40000001, 0.599999)], 3)
    [(0.2, 0.3), (0.4, 0.6)]
    """
    return [(round(interval[0],digits),round(interval[1],digits)) for interval in piece]



class Allocation:
    """
    An allocation of a cake among agents.
    This is the output of a cake-cutting algorithm.

    >>> Alice = PiecewiseUniformAgent([(2,3)], "Alice");George = PiecewiseUniformAgent([(0,10)], "George")
    >>> A = Allocation([Alice, George]);A.setPieces([[(1,2)],[(4,5)]]);
    >>> B = Allocation([George, Alice]);B.setPieces([[(0,1)],[(2,3)]]);
    >>> A.merge(B);print(A)
    > Alice gets [(1, 2), (2, 3)] with value 1.0
    > George gets [(4, 5), (0, 1)] with value 2.0
    <BLANKLINE>
    >>> A.isEnvyFree(2)
    True
    """

    def __init__(self, agents:List[Agent]):
        self.agents = agents
        self.pieces = [None]*len(agents)

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

    def merge(self, other):
        """
        merges this allocation with another allocation in place.

        :param other: the other allocation to merge with.

        >>> Alice = PiecewiseUniformAgent([(2,3)], "Alice");George = PiecewiseUniformAgent([(0,10)], "George")
        >>> A = Allocation([Alice, George]);A.setPieces([[(1,2)],[(4,5)]]);
        >>> B = Allocation([George, Alice]);B.setPieces([[(0,1)],[(2,3)]]);
        >>> A.merge(B);print(A)
        > Alice gets [(1, 2), (2, 3)] with value 1.0
        > George gets [(4, 5), (0, 1)] with value 2.0
        <BLANKLINE>
        """

        for i in range(len(self.pieces)):
            if(self.pieces[i] == None):
                self.pieces[i] = []
            for j in range(len(other.pieces)):
                #merge the same agents.
                if(other.agents[j].name() == self.agents[i].name()):
                    if(other.pieces[j] == None):
                        other.pieces[j] = []
                    self.pieces[i].extend(other.pieces[j])

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
        for i in range(len(self.agents)):
            selfVal = 0
            for piece in self.pieces[i]:
                selfVal += self.agents[i].eval(piece[0], piece[1])
            for j in range(len(self.pieces)):
                otherVal = 0
                for otherPiece in self.pieces[j]:
                    otherVal += self.agents[i].eval(otherPiece[0], otherPiece[1])
                if round(otherVal-selfVal, roundAcc) > 0:
                    return False
        return True

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
