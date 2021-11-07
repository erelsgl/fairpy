#!python3
"""
Implementation of an envy-free cake cutting protocol for
agents with piecewise linear preferences in polynomial time.

References:

    David Kurokawa, John K. Lai, Ariel D Procaccia (2013). "How to Cut a Cake Before the Party Ends". Proceedings of AAAI 2013.

Programmer: Guy Wolf
Since: 2020-2
"""

from fairpy.criteria import is_envyfree
from fairpy import Allocation
from fairpy.agents import Agent
from typing import *

from itertools import permutations
import logging
logger = logging.getLogger(__name__)

"""
important note:
these algorithms are susceptible to python floating point math errors.
In Python, for instance, 0.1+0.2>0.3. This creates a situation where, for instance,
a cut that should be envy free is not seen as one to calculation errors when
creating it.

Therefore, both algorithms use a paramater called roundAcc to round values
in order to prevent fragmentation caused due to these errors. Furthermore,
it is recommended that when using these algorithms the cake will be in a large
size, in order to prevent calculation errors as much as possible.
"""

def Cover(a: float, b: float, agents: List[Agent], roundAcc = 6)->List:
    """
    creates a cover of seperating intervals for a given interval.
    each interval in the cover is guarenteed to be worth at most proportionally
    for every agent and for every interval there is an agent for which the interval
    is worth exactly the proportional amount for them.

    :param a: the start of the given interval.
    :param b: the end of the given interval.
    :param agents: a list of agents.
    :param roundAcc: the rounding accuracy of the algorithm in decimal digits.
    :return: a cover of [a,b].

    >>> from fairpy.agents import PiecewiseUniformAgent
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
            if tmp > start and tmp <= b and tmp < end:
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
    :param roundAcc: the rounding accuracy of the algorithm in decimal digits.
    :return: an envy-free allocation.

    >>> from fairpy.agents import PiecewiseUniformAgent
    >>> Alice = PiecewiseUniformAgent([(5,7)], "Alice")
    >>> George = PiecewiseUniformAgent([(4,9)], "George")
    >>> print(str(EFAllocate([Alice,George])))
    Alice gets {(0, 6.0)} with value 1.
    George gets {(6.0, 7.5),(7.5, 9.0)} with value 3.
    <BLANKLINE>
    >>> Alice = PiecewiseUniformAgent([(2,3), (9,10)], "Alice")
    >>> George = PiecewiseUniformAgent([(1,2), (6,7)], "George")
    >>> print(str(EFAllocate([Alice,George])))
    Alice gets {(2.0, 6.0),(6.0, 10.0)} with value 2.
    George gets {(0, 2.0)} with value 1.
    <BLANKLINE>
    """
    num_of_agents = len(agents)

    def sandwichAllocation(a, b, alpha, beta, n)->List[List[Tuple[float,float]]]:
        """
        creates a sandwich allocation using the specified paramaters.
        :param a: starting point of the section to split.
        :param b: end point of the section to split.
        :param alpha: starting point of the internal interval.
        :param beta: end point of the internal interval.
        :param n: the amount of agents in the allocation.
        :return: a list of lists of intervals mathching the sandwich allocation.

        >>>sandwichAllocation(0,1,0.4,0.6,2)
        [[(0.4, 0.6)], [(0,0.2), (0.2, 0.4), (0.6, 0.8), (0.8, 1)]]
        """
        gamma = round((alpha - a)/(2*(n-1)), roundAcc)
        delta = round((b - beta)/(2*(n-1)), roundAcc)
        tmp = [[(alpha, beta)]]
        for j in range(1, n):
            toAdd = []
            toAdd.append((round(a + (j-1)*gamma, roundAcc), round(a + j*gamma, roundAcc)))
            toAdd.append((round(alpha - (j)*gamma, roundAcc), round(alpha - (j-1)*gamma, roundAcc)))
            toAdd.append((round(beta + (j-1)*delta, roundAcc), round(beta + j*delta, roundAcc)))
            toAdd.append((round(b - (j)*delta, roundAcc), round(b - (j-1)*delta, roundAcc)))
            tmp.append(toAdd)

        #clear useless points where the start equals to the end
        ret = []
        for piece in tmp:
            ret.append([])
            for inter in piece:
                if round(inter[1]-inter[0], roundAcc) > 0.0:
                    ret[-1].append(inter)
        return ret

    def EFAllocateRec(a: float, b: float)->List[List[Tuple[float,float]]]:
        """
        exactly the same as EFAllocate, but creates the envy free allocation
        within a given interval.

        :param a: starting point of the interval to allocate.
        :param b: end point of the interval to allocate.
        :return: a list of lists of intervals mathching the sandwich allocation.
        """

        if round(a, roundAcc) == round(b, roundAcc):
            return Allocation(agents, len(agents)*[[]])

        #1
        numAgents = len(agents)
        ret = Allocation(agents, len(agents)*[[]])
        cover = Cover(a,b,agents,roundAcc=roundAcc)

        #2
        for inter in cover:
            pieces = sandwichAllocation(a,b,inter[0],inter[1],numAgents)
            for permuted_pieces in permutations(pieces):
                if is_envyfree(agents, permuted_pieces, roundAcc):
                    logger.info("allocation from %f to %f completed with sandwich allocation.",a,b)
                    return permuted_pieces

        #3
        logger.info("no valid allocation without recursion from %f to %f.", a, b)
        logger.info("splitting to sub-allocations using the cover of the whole interval.")
        points = [a]
        for interval in cover:
            points.append(interval[1])
        points.sort()
        ret = num_of_agents*[[]]
        for i in range(1, len(points)):
            logger.info("creating allocation from %f to %f:", points[i-1], points[i])
            alloc = EFAllocateRec(points[i-1], points[i])
            # merge the existing allocation with the new allocation:
            merged_alloc = [ret[i_agent]+alloc[i_agent] for i_agent in range(num_of_agents)]
            ret = merged_alloc
        logger.info("covered allocation from %f to %f using merging.",a,b)
        return ret

    #run the bounded function over the whole area - from 0 to 1.
    alloc = EFAllocateRec(0, max([agent.cake_length() for agent in agents]))
    return Allocation(agents, alloc)


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
