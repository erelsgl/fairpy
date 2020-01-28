"""
Defines cake-allocations.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""

from typing import *
from agents import Agent

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
    """

    def __init__(self, agents:List[Agent]):
        self.agents = agents
        self.pieces = [None]*len(agents)

    def get_piece(self,agent_index:int):
        return self.pieces[agent_index]
    def get_pieces(self):
        return self.pieces

    def set_piece(self, agent_index:int, piece:List[tuple]):
        """
        Sets the piece of the given index.

        :param agent_index: index of the agent.
        :param piece: a list of intervals.
        """
        self.pieces[agent_index] = piece


    def __repr__(self):
        s = ""
        for i in range(len(self.pieces)):
            agent = self.agents[i]
            piece = self.pieces[i]
            s += "> {} gets {} with value {}\n".format(agent.name(), round_piece(self.pieces[i], digits=3), round(agent.piece_value(piece),3))
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
