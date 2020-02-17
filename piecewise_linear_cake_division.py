"""
Implementation of an envy-free cake cutting protocol for
agents with piecewise linear preferences in polynomial time.

References:

    David Kurokawa, John K. Lai, Ariel D Procaccia (2013). "How to Cut a Cake Before the Party Ends". Proceedings of AAAI 2013.

Programmer: Guy Wolf
Since: 2020-2
"""

from agents import *
from allocations import *
from typing import *

from itertools import permutations
import logging
logger = logging.getLogger(__name__)


def Cover(a: float, b: float, agents: List[Agent], roundAcc = 6)->List:
    """
    creates a cover of seperating intervals for a given interval.
    each interval in the cover is guarenteed to be worth at most proportionally
    for every agent and for every interval there is an agent for which the interval
    is worth exactly the proportional amount for them.

    :param a: the start of the given interval.
    :param b: the end of the given interval.
    :param agents: a list of agents.
    :return: a cover of [a,b].

    >>> Alice = PiecewiseUniformAgent([(0.5,0.7)], "Alice")
    >>> George = PiecewiseUniformAgent([(0.4,0.9)], "George")
    >>> print(str(Cover(0,1,[Alice,George])))
    [(0, 0.6), (0.6, 0.7), (0.65, 1)]

    """

    #1
    logger.info('covering from start point %f to end point %f.',a,b)
    agentNum = len(agents)
    ret = []
    start = a

    #2
    while start < b:
        #2a
        end = float('inf')
        #logger.info("start is %f.", start)
        for agent in agents:
            tmp = agent.mark(start, agent.eval(a, b)/agentNum)
            if tmp == None:
                continue
            tmp = round(tmp, roundAcc)
            #logger.info("end point from %s is %f", agent.name(), tmp)
            if tmp != None and tmp > start and tmp <= b and tmp < end:
                end = tmp

        #2b
        if(end == float('inf')):
            logger.info('no matching end point found. Exiting loop.')
            break

        logger.info('minimal end point found at %f.', end)

        #2c
        ret.append((start, end))

        #2d
        start = end

    #3
    final = -float('inf')
    for agent in agents:
        """we want to mark for [,b], but we can only mark for [a,].
        Since [x,b] is the same as [a,b]-[a,x], we will mark for [a,x] using
        1 - the value we need."""
        tmp = agent.mark(a, agent.eval(a,b)/agentNum)
        if tmp == None:
            continue
        tmp = round(tmp, roundAcc)
        if tmp <= b and tmp > final:
            final = tmp
    logger.info('maximal end point is %f.', final)

    #4
    ret.append((final, b))
    logger.info('cover complete.')
    return ret

def EFAllocate(agents: List[Agent], roundAcc = 2)->Allocation:
    """
    Envy Free cake cutting protocol for piecewise agents that runs
    in a polynomial time complexity.

    :param agents: a list of agents.
    :return: an envy-free allocation.

    >>> Alice = PiecewiseUniformAgent([(0.5,0.7)], "Alice")
    >>> George = PiecewiseUniformAgent([(0.4,0.9)], "George")
    >>> print(str(EFAllocate([Alice,George])))
    > George gets [(0.6, 0.7)] with value 0.1
    > Alice gets [(0.0, 0.3), (0.3, 0.6), (0.7, 0.85), (0.85, 1.0)] with value 0.1
    <BLANKLINE>
    """

    class MergableAllocation(Allocation):
        """
        an allocation with some extra helper methods, most notably:
        the ability to merge with other allocations,
        the ability to set all agents and pieces
        and the ability to check if it is envy free.
        """

        def merge(self, other):
            for i in range(len(self.pieces)):
                if(self.pieces[i] == None):
                    self.pieces[i] = []
                for j in range(len(other.pieces)):
                    if(other.agents[j].name() == self.agents[i].name()):
                        if(other.pieces[j] == None):
                            other.pieces[j] = []
                        self.pieces[i].extend(other.pieces[j])

        def setAgents(self, agents):
            self.agents = agents

        def setPieces(self, pieces):
            self.pieces = pieces

        def isEnvyFree(self):
            for i in range(len(self.agents)):
                selfVal = 0
                for piece in self.pieces[i]:
                    selfVal += self.agents[i].eval(piece[0], piece[1])
                for j in range(len(self.pieces)):
                    otherVal = 0
                    for otherPiece in self.pieces[j]:
                        otherVal += self.agents[i].eval(otherPiece[0], otherPiece[1])
                    if round(otherVal-selfVal, roundAcc) > 0:
                        #logger.info("allocation not envy free because %s prefers %d over %d", self.agents[i].name(), j, i)
                        #logger.info(self)
                        return False
            return True


    def sandwichAllocation(a, b, alpha, beta, n):
        """
        creates a sandwich allocation using the specified paramaters.
        :param a: starting point of the section to split.
        :param b: end point of the section to split.
        :param alpha: starting point of the internal interval.
        :param beta: end point of the internal interval.
        :param n: the amount of agents in the allocation.
        :return: a list of lists of intervals mathching the sandwich allocation.
        """
        gamma = round((alpha - a)/(2*(n-1)), roundAcc)
        delta = round((b - beta)/(2*(n-1)), roundAcc)
        ret = [[(alpha, beta)]]
        for j in range(1, n):
            toAdd = []
            toAdd.append((round(a + (j-1)*gamma, roundAcc), round(a + j*gamma, roundAcc)))
            toAdd.append((round(alpha - (j)*gamma, roundAcc), round(alpha - (j-1)*gamma, roundAcc)))
            toAdd.append((round(beta + (j-1)*delta, roundAcc), round(beta + j*delta, roundAcc)))
            toAdd.append((round(b - (j)*delta, roundAcc), round(b - (j-1)*delta, roundAcc)))
            ret.append(toAdd)
        return ret

    def EFAllocateRec(a: float, b: float)->Allocation:
        """
        exactly the same as EFAllocate, but creates the envy free allocation
        within a given interval.

        :param a: starting point of the interval to allocate.
        :param b: end point of the interval to allocate.
        :return: a list of lists of intervals mathching the sandwich allocation.
        """

        if round(a, roundAcc) == round(b, roundAcc):
            return MergableAllocation(agents)

        #1
        numAgents = len(agents)
        ret = MergableAllocation(agents)
        cover = Cover(a,b,agents)

        #2
        for inter in cover:
            ret.setPieces(sandwichAllocation(a,b,inter[0],inter[1],numAgents))
            for perm in permutations(agents):
                ret.setAgents(perm)
                if ret.isEnvyFree():
                    logger.info("allocation from %f to %f completed with sandwich allocation.",a,b)
                    return ret

        #3
        logger.info("no valid allocation without recursion from %f to %f.", a, b)
        logger.info("splitting to sub-allocations using the cover of the whole interval.")
        points = [a]
        for interval in cover:
            points.append(interval[1])
        points.sort()
        for i in range(1, len(points)):
            logger.info("creating allocation from %f to %f:", points[i-1], points[i])
            alloc = EFAllocateRec(points[i-1], points[i])
            ret.merge(alloc)
        logger.info("covered allocation from %f to %f using merging.",a,b)
        return ret

    #run the bounded function over the whole area - from 0 to 1.
    return EFAllocateRec(0, max([agent.cake_length() for agent in agents]))


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
