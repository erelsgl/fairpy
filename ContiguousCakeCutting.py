"""
Contiguous Cake Cutting: Hardness Results and Approximation Algorithms∗
Programmers: prof. Erel Segal-Halevi for Agent
and          Shalev Goldshtein for algor1
Since: 2020-03
"""

from abc import ABC, abstractmethod
from typing import Optional, Any

import numpy as np
from typing import *

import logging
logger = logging.getLogger(__name__)

class Agent(ABC):
    """
    An abstract class that describes a participant in a cake-cutting algorithm.
    It can answer the standard "mark" and "eval" queries.
    It may also have a name, which is used only in demonstrations and for tracing. The name may be left blank (None).
    """

    def __init__(self, name: str = None):
        if name is not None:
            self.my_name = name

    def name(self):
        if hasattr(self, 'my_name') and self.my_name is not None:
            return self.my_name
        else:
            return "Anonymous"

    @abstractmethod
    def cake_value(self):
        """
        :return: the value of the entire cake for the agent.
        """
        pass

    @abstractmethod
    def cake_length(self):
        """
        :return: the total length of the cake that the agent cares about.
        """
        pass

    @abstractmethod
    def eval(self, start: float, end: float):
        """
        Answer an Eval query: return the value of the interval [start,end].
        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]
        """
        pass

    @abstractmethod
    def mark(self, start: float, targetValue: float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is targetValue.
        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of targetValue.
        """
        pass

    def piece_value(self, piece: List[tuple]):
        """
        Evaluate a piece made of several intervals.
        :param piece: a list of tuples [(start1,end1), (start2,end2),...]
        :return:
        """
        if (piece == None):
            return 0
        return sum([self.eval(*interval) for interval in piece])

    def partition_values(self, partition: List[float]):
        """
        Evaluate all the pieces in the given partition.
        :param partition: a list of k cut-points [cut1,cut2,...]
        :return: a list of k+1 values: eval(0,cut1), eval(cut1,cut2), ...
        >>> a = PiecewiseConstantAgent([1,2,3,4])
        >>> a.partition_values([1,2])
        [0.1, 0.2, 0.7]
        >>> a.partition_values([3,3])
        [0.6, 0.0, 0.4]
        """

        values = []
        values.append(self.eval(0, partition[0]))
        for i in range(len(partition) - 1):
            values.append(self.eval(partition[i], partition[i + 1]))
        values.append(self.eval(partition[-1], self.cake_length()))
        return values


class PiecewiseConstantAgent(Agent):


    # the init of the agent
    def __init__(self, values: list, name: str = None):
        super().__init__(name)

        # the len of the values list
        self.length = len(values)
        self.total_value_cache = sum(values)
        # self.values = np.array(values)
        ls = [None] * len(values)
        # normalize the cake to values between 0.0 and 1.0
        # by dividing the values by there sum
        for i in range(len(values)):
            ls[i] = values[i] / self.total_value_cache

        # the list of the values
        self.values = np.array(ls)

        self.normal = 1 / self.total_value_cache

    def __repr__(self):
        return "{} is a piecewise-constant agent with values {} (((NORMALIZED)))".format(self.my_name, self.values)

    def cake_value(self):
        return self.total_value_cache

    def cake_length(self):
        return self.length

    # the evaluation of the agents
    def eval(self, start: float, end: float):
        """
        Answer an Eval query: return the value of the interval [start,end] {{{[(NORMALIZED)]}}}.

        :param start: Location on cake where the calculation starts.
        :param end:   Location on cake where the calculation ends.
        :return: Value of [start,end]

        >>> a = PiecewiseConstantAgent([11,22,33,44])
        >>> a.eval(0.5,1)
        0.7
        >>> a.eval(0.25,1)
        0.9
        >>> a.eval(0,0.25)
        0.1
        >>> a.eval(0,0.375)
        0.2

        """
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, min(start * self.length, self.length))
        end = max(0, min(end * self.length, self.length))
        if end <= start:
            return 0.0  # special case not covered by loop below

        fromFloor = int(np.floor(start))
        fromFraction = (fromFloor + 1 - start)
        toCeiling = int(np.ceil(end))
        toCeilingRemovedFraction = (toCeiling - end)

        val = 0.0
        val += (self.values[fromFloor] * fromFraction)
        val += self.values[fromFloor + 1:toCeiling].sum()
        val -= (self.values[toCeiling - 1] * toCeilingRemovedFraction)

        return val

    # the mark is for finding the point where it's equals to  the target value
    def mark(self, start: float, target_value: float):
        """
        Answer a Mark query: return "end" such that the value of the interval [start,end] is target_value  {[(NORMALIZED)]}.

        :param start: Location on cake where the calculation starts.
        :param targetValue: required value for the piece [start,end]
        :return: the end of an interval with a value of target_value.
        If the value is too high - returns None.

        >>> a = PiecewiseConstantAgent([11,22,33,44])
        >>> a.mark(0.5, 0.7)
        1
        >>> a.mark(0.375, 0.1)
        0.5
        >>> a.mark(0, 0.2)
        0.375
        >>> a.mark(0.25, 0.2)
        0.5
        >>> a.mark(0, 0.9)
        0.9375

        """
        # the cake to the left of 0 and to the right of length is considered worthless.
        start = max(0, start * self.length)
        if start >= self.length:
            return None  # value is too high

        if target_value < 0:
            raise ValueError("sum out of range (should be positive): {}".format(sum))

        start_floor = int(np.floor(start))
        if start_floor >= len(self.values):
            raise ValueError(
                "mark({},{}): start_floor ({}) is >= length of values ({})".format(start, target_value, start_floor,
                                                                                   self.values))

        start_fraction = (start_floor + 1 - start)

        value = self.values[start_floor]
        if value * start_fraction >= target_value:
            # i added the division by self.length for normalzing
            return ((start + (target_value / value)) / self.length)
        target_value -= (value * start_fraction)
        for i in range(start_floor + 1, self.length):
            value = self.values[i]
            if target_value <= value:
                # i added the division by self.length for normalzing
                return ((i + (target_value / value)) / self.length)
            target_value -= value

        # Value is too high: return None
        return None

# line 5. 'some agent in N values [`, 1] at least 1/3'
# agentN - indexes of all existing agents
# agentL - all agents
def hasBiggerThanThird(left, agentN, agentL):
    """
    Answer if there is part that is bigger then 1/3 till the end of the cake.

    :param left: Our Location on this moment.
    :param agentN: the number of agents.
    :param agentL: the agents themselves.
    :return: true if there is at list one the has value more then 1/3 .
    & false where there is no one that has value that is more or equal to 1/3.

    >>> c1 = PiecewiseConstantAgent([2, 8, 2])
    >>> c2 = PiecewiseConstantAgent([4, 2, 6])
    >>> lsC = [c1,c2]
    >>> hasBiggerThanThird(0,2,lsC)
    True
    >>> hasBiggerThanThird(0.85,2,lsC)
    False
    >>> hasBiggerThanThird(0.6,2,lsC)
    True

    """
    # for every agent
    for agentIndex in agentN:
        # if the segment [left,1] is evaluated >= 1/3
        if (agentL[agentIndex].eval(left, 1.0) >= (1 / 3)):
            logger.info("There is a agent with more then 1/3 value - Therefore and accordingly we are doing another round in the loop")
            return True
    logger.info("There isn't a agent with more then 1/3 value - we are exist the loop")
    return False


# Algorithm 1 1/3-Envy-Free Algorithm
# AgentList is all agents
def algor1(AgentList):
    """
    Answer a Mark query: return "end" such that the value of the interval [start,end] is target_value  {[(NORMALIZED)]}.

    :param start: Location on cake where the calculation starts.
    :param targetValue: required value for the piece [start,end]
    :return: the end of an interval with a value of target_value.
    If the value is too high - returns None.

    >>> aa = ContiguousCakeCutting.PiecewiseConstantAgent([2, 8, 2], name="aa")
    >>> bb = ContiguousCakeCutting.PiecewiseConstantAgent([4, 2, 6], name="bb")
    >>> lstba = [aa,bb]
    >>> algor1(lstba)
    > Agent aa gets the segment: [0.3333333333333333, 1.0]
    > Agent bb gets the segment: [0.0, 0.3333333333333333]

    >>> a0 = ContiguousCakeCutting.PiecewiseConstantAgent([4, 10, 20], name="a0")
    >>> a1 = ContiguousCakeCutting.PiecewiseConstantAgent([14, 42, 9, 17], name="a1")
    >>> a2 = ContiguousCakeCutting.PiecewiseConstantAgent([30, 1, 12], name="a2")
    >>> lstaaa = [a0,a1,a2]
    >>> algor1(lstaaa)
    > Agent a0 gets the segment: [0.3824514991181658, 1.0]
    > Agent a1 gets the segment: [0.15925925925925924, 0.3824514991181658]
    > Agent a2 gets the segment: [0.0, 0.15925925925925924]

    """
    l = 0.00
    lenAgents = len(AgentList)
    # N = list(range(0, lenAgents))
    N = [i for i in range(lenAgents)]


    # Mlist is the list who save the M Parts of the cake
    Mlist = [None] * lenAgents

    # the leftest point of each of the agent to fulfill the condition of the 1/3
    rList = [None] * lenAgents

    # for saving who was the last agent to remove
    lastAgentRemove = -1

    # the main loop
    while hasBiggerThanThird(l, N, AgentList):
        for i in N:
            if AgentList[i].eval(l, 1.0) >= (1 / 3):
                #where it equal 1/3
                rList[i] = (AgentList[i].mark(l, (1 / 3)))
            else:
                rList[i] = 1
        # j - agent with smallest rList value (r[i])
        j = N[0]
        # r - smallest rList value (r[i])
        r = rList[N[0]]
        # find j and r (finds minimum)
        for k in N:
            if rList[k] < r:
                j = k
                r = rList[k]
        logger.info("From The agents who remained The agent (%s) is with the leftest point - which is %s.", AgentList[j].name(),str(r))
        # gives agent j this segment , moves l to the right (r)
        Mlist[j] = [l, r]
        l = r

        # remove j
        N.remove(j)

        lastAgentRemove = j
        if len(N) == 0:
            break
    # if N is not empty
    if N:
        # arbitrary agent in N

        j = N[0]
        logger.info(" (%s) is getting the rest. %s till 1.0",AgentList[j].name(), str(l))
        Mlist[j] = [l, 1.0]
    else:
        logger.info("There is no agents that remained")
        j = lastAgentRemove
        logger.info(" we are adding to (%s) the rest. %s till 1.0", AgentList[j].name(), str(l))
        # [a, l] unite with [l, 1] => [a, 1]
        Mlist[j][1] = 1.0
    logger.info("")
    for i, allocation in enumerate(Mlist):
        #print("> Agent " + str(i) + " gets the segment: " + str(allocation))
        logger.info("> Agent %s gets the segment: %s", AgentList[i].name(), str(allocation))


