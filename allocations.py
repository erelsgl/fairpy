"""
Defines cake-allocations.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""

from typing import *
from agents import Agent


class Allocation:
    """
    An allocation of a cake among agents.
    This is the output of a cake-cutting algorithm.
    """

    def __init__(self, agents:List[Agent]):
        self.agents = agents
        self.pieces = [None]*len(agents)

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
            s += "> {} gets {} with value {:.2f}\n".format(agent.name(), self.pieces[i], agent.piece_value(piece))
        return s

