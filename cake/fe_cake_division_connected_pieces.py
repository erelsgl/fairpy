"""
Article name : Fair and Efficient Cake Division with Connected Pieces
Authors : Eshwar Ram Arunachaleswaran , Siddharth Barman , Rachitesh Kumar and Nidhi Rathi
Algorithm #1 : ALG
Programmer: Ori Zitzer
Since: 2019-12
"""

from cake.agents import *
from cake.allocations import *
import numpy as np
import random
import logging
logger = logging.getLogger(__name__)


def findRemainIntervals(allocation :Allocation)->List[tuple]:
    """
    Functoin that return the remain intervals from the allocation in (0,1)
    :param allocation: an Allocation
    :return: the remain intervals
    >>> Alice = PiecewiseConstantAgent([33, 33], "Alice")
    >>> George = PiecewiseConstantAgent([5,5],"George")
    >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
    >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
    >>> print(findRemainIntervals(Allocation([Alice,George,Abraham,Hanna])))
    [(0, 1)]
    >>> alloc = Allocation([Alice,George,Abraham,Hanna])
    >>> alloc.set_piece(1,[(0.2,0.3)])
    >>> print(findRemainIntervals(alloc))
    [(0, 0.2), (0.3, 1)]
    >>> alloc.set_piece(3,[(0.4,0.73),(0.92,1)])
    >>> print(findRemainIntervals(alloc))
    [(0, 0.2), (0.3, 0.4), (0.73, 0.92)]
    """
    remain = []
    pieces = allocation.get_pieces()
    piecesList = []
    #turn the pieces from list of lists of tuples into list of tuples
    for list in pieces:
        if list!= None :piecesList+=list
    if len(piecesList)==0:return [(0,1)]
    piecesList.sort(key=lambda ineterval: ineterval[0])
    start = 0
    if piecesList[0][0]==0:
        start = piecesList[0][1]
        piecesList.pop(0)
    for interval in piecesList:
        remain.append((start,interval[0]))
        start=interval[1]
    if start!=1:
        remain.append((start,1))

    return remain


def checkWhile(agents: List[Agent],allocation :Allocation,remain:List[tuple],epsilon:float)->tuple:
    """
    Check the while condition that in the algorithm
    :param agents: A list of agents
    :param allocation: An Allocation
    :param remain: The remain Intervals of the alloction
    :param epsilon: An constant between 0 to 1/3
    :return: An interval that uphold the condition

    >>> Alice = PiecewiseConstantAgent([33, 33], "Alice")
    >>> George = PiecewiseConstantAgent([5,5],"George")
    >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
    >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
    >>> alloc = Allocation([Alice,George,Abraham,Hanna])
    >>> agents = [Alice,George,Abraham,Hanna]
    >>> agents = agentNormalize(agents)
    >>> alloc.set_piece(1,[(0.2,0.3)])
    >>> alloc.set_piece(3,[(0.4,0.73),(0.92,1)])
    >>> print(checkWhile(agents,alloc,findRemainIntervals(alloc),0))
    (0, 0.2)
    >>> alloc.set_piece(0,[(0,0.2)])
    >>> print(checkWhile(agents,alloc,findRemainIntervals(alloc),0))
    (0.3, 0.4)
    >>> alloc.set_piece(2, [(0.73, 0.92)])
    >>> print(checkWhile(agents,alloc,findRemainIntervals(alloc),0))
    (0.3, 0.4)
    >>> newAlloc = Allocation(agents)
    >>> newAlloc.set_piece(1, [(0.1, 0.3)])
    >>> newAlloc.set_piece(3, [(0.3, 0.73)])
    >>> print(checkWhile(agents, newAlloc, findRemainIntervals(newAlloc), 0.1))
    (0.73, 1)
    >>> newAlloc.set_piece(0, [(0.73, 0.8)])
    >>> print(checkWhile(agents, newAlloc, findRemainIntervals(newAlloc), 0.1))
    (0, 0.1)
    >>> newAlloc.set_piece(2, [(0.01, 0.05)])
    >>> print(checkWhile(agents, newAlloc, findRemainIntervals(newAlloc), 0.1))
    (0.05, 0.1)
    >>> newAlloc = Allocation(agents)
    >>> newAlloc.set_piece(1, [(0.1, 0.3)])
    >>> newAlloc.set_piece(3, [(0.3, 0.73)])
    >>> print(checkWhile(agents, newAlloc, findRemainIntervals(newAlloc), 0.3))
    (0.73, 1)
    >>> newAlloc.set_piece(0, [(0.8,0.96)])
    >>> print(checkWhile(agents, newAlloc, findRemainIntervals(newAlloc), 0.3))
    None
    >>> newAlloc.set_piece(2, [(0, 0.05)])
    >>> print(checkWhile(agents, newAlloc, findRemainIntervals(newAlloc), 0.3))
    None
    """
    nSquared = len(agents)*len(agents)
    pieces = allocation.get_pieces()
    piecesList = []
    # turn the pieces from list of lists of tuples into list of tuples
    for list in pieces:
        if list != None: piecesList += list
    if len(piecesList)==0:
        return (0,1)
    for interval in remain:
        for agent,i in zip(agents,range(len(agents))):
            if (allocation.pieces[i] == None):
                continue
            if (agent.eval(allocation.get_piece(i)[0][0],allocation.get_piece(i)[0][1]) <
                    (agent.eval(interval[0],interval[1]) - (epsilon/nSquared))):
                return interval
    return None


def getC(agents: List[Agent],allocation :Allocation,epsilon:float,interval:tuple)->List[Agent]:
    """
    Get the C group from the Algorithm
    :param agents: A list of agents
    :param allocation: An Allocation
    :param epsilon: A constant between 0 to 1/3
    :param interval: The chosen interval out of the remain intervals
    :return: All the agents that their current evaluation to their piece is smaller than
                the evaluation to the interval - (epsilon/n^2) when n is the number of agents

    >>> Alice = PiecewiseConstantAgent([33, 33], "Alice")
    >>> George = PiecewiseConstantAgent([5,5],"George")
    >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
    >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
    >>> alloc = Allocation([Alice,George,Abraham,Hanna])
    >>> agents = [Alice,George,Abraham,Hanna]
    >>> agents = agentNormalize(agents)
    >>> alloc.set_piece(1,[(0.2,0.3)])
    >>> alloc.set_piece(3,[(0.4,0.7)])
    >>> interval = checkWhile(agents, alloc, findRemainIntervals(alloc), 0.2)
    >>> print([agent[0].name() for agent in getC(agents,alloc,0.2,interval)])
    ['Alice', 'George', 'Abraham']
    >>> alloc.set_piece(0,[(0.75,1)])
    >>> interval = checkWhile(agents, alloc, findRemainIntervals(alloc), 0)
    >>> print([agent[0].name() for agent in getC(agents,alloc,0.2,interval)])
    ['George', 'Abraham']
    """
    nSquared = len(agents) * len(agents)
    newAgents = []
    for agent, i in zip(agents, range(len(agents))):
        if(allocation.pieces[i]==None):
            newAgents.append((agent,i))
            continue
        if (agent.eval(allocation.pieces[i][0][0], allocation.pieces[i][0][1]) <
                agent.eval(interval[0], interval[1]) - (epsilon / nSquared)):
            newAgents.append((agent,i))
    return newAgents


def findRb(agent:Agent , allocation:Allocation,epsilon:float,index:int,interval:tuple,n:int)->float:
    """
    Find the leftmost number:Rb that hold the equation of evaluation to the agent piece + (epsilon/n^2)
              is equal to the evaluation to the [l,Rb] when l is the left of the interval
    :param agent: An agent
    :param allocation: An Allocation
    :param epsilon: A constant between 0 to 1/3
    :param index: the index of the agent
    :param interval: The chosen interval out of the remain intervals (l,r)
    :param n: The number of agents
    :return: The leftmost number:Rb that hold the equation of evaluation to the agent piece + (epsilon/n^2)
                is equal to the evaluation to the [l,Rb] when l is the left of the interval

    >>> Alice = PiecewiseConstantAgent([33, 33], "Alice")
    >>> George = PiecewiseConstantAgent([5,5],"George")
    >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
    >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
    >>> alloc = Allocation(agentNormalize([Alice,George,Abraham,Hanna]))
    >>> print(round(findRb(Hanna,alloc,0.1,3,(0,1),4),6))
    0.002083
    """
    currentPieceEval = 0
    if allocation.pieces[index]!=None:
        currentPiece = allocation.pieces[index][0]
        currentPieceEval = agent.eval(currentPiece[0],currentPiece[1])
    return agent.mark(interval[0],currentPieceEval + epsilon/(n*n))


def findPiece(reamin:List[tuple],attr:float , leftOrRight:int)->tuple:
    """
    Find the piece that her leftOrRight equal to attr
    :param reamin:The reamin intervals in (0,1)
    :param attr: the float we search
    :param leftOrRight: left or right
    :return:piece that her leftOrRight equal to attr
    >>> remain = [(0.1,0.2),(0.3,0.7),(0.9,1)]
    >>> print(findPiece(remain , 0.1,0))
    (0.1, 0.2)
    >>> print(findPiece(remain , 0.7,1))
    (0.3, 0.7)
    >>> print(findPiece(remain,0,0))
    None
    """
    for piece in reamin:
        if piece[leftOrRight]==attr:
            return piece
    return None


def setRemain(allocation:Allocation,agents: List[Agent])->List[List[tuple]]:
    """
    Set the remain intervals to the agents
    :param allocation: An partial allocation of (0,1)
    :param agents: A list of agents
    :return: A fully allocation of (0,1)
    >>> Alice = PiecewiseConstantAgent([33, 33], "Alice")
    >>> George = PiecewiseConstantAgent([5, 5], "George")
    >>> alloc = Allocation([Alice, George])
    >>> agents = [Alice, George]
    >>> alloc.set_piece(1, [(0.2, 0.3)])
    >>> alloc.set_piece(0, [(0.4, 0.73)])
    >>> print(alloc)
    > Alice gets [(0.4, 0.73)] with value 10.89
    > George gets [(0.2, 0.3)] with value 0.5
    <BLANKLINE>
    >>> setRemain(alloc,agents)
    [[(0.4, 0.73), (0.73, 1)], [(0.2, 0.3), (0.3, 0.4), (0, 0.2)]]
    >>> print(alloc)
    > Alice gets [(0.4, 0.73), (0.73, 1)] with value 19.8
    > George gets [(0.2, 0.3), (0.3, 0.4), (0, 0.2)] with value 2.0
    <BLANKLINE>
    """
    remain = findRemainIntervals(allocation)
    choice = random.choice(('Left', 'Right'))
    partialAlloc = allocation.get_pieces()

    for i,pieces in zip(range(partialAlloc.__len__()),partialAlloc):
        if(pieces==None):
            maxPiece , maxEval = 0,0
            for remainPiece in remain:
                if agents[i].eval(remainPiece[0],remainPiece[1])>=maxEval:
                    maxEval = agents[i].eval(remainPiece[0],remainPiece[1])
                    maxPiece = remainPiece
            remain.remove(maxPiece)
            allocation.set_piece(i,[maxPiece])
    partialAlloc = allocation.get_pieces()
    for pieces in partialAlloc:
        if(pieces==None):
            continue
        right = pieces[0][1]
        newPart = findPiece(remain, right,0)
        if newPart == None : continue
        pieces.append(newPart)
        remain.remove(newPart)
    partialAlloc = allocation.get_pieces()
    if len(remain) == 1:
        for pieces in partialAlloc:
            for piece in pieces:
                if (pieces == None):
                    continue
                if remain[0][1] == piece[0]:
                    pieces.append(remain[0])
                    break
            if(len(remain)==0):
                break

    return partialAlloc


def intervalUnionFromList(intervals:List[tuple])->tuple:
    """
    Uniting a list of intervals into one
    :param intervals: A list of adjacent intervals
    :return:A union of the intervals
    >>> print(intervalUnionFromList([(0.3,0.4),(0.4,0.7)]))
    (0.3, 0.7)
    >>> print(intervalUnionFromList([(0.3,0.4),(0.6,0.7),(0.4,0.7)]))
    (0.3, 0.7)
    """
    minimum = 1
    maximum = 0
    for interval in intervals:
        if interval[0] < minimum: minimum = interval[0]
        if interval[1] > maximum: maximum = interval[1]
    return (minimum,maximum)


def allocationToOnePiece(alloction:List[List[tuple]],agents:List[Agent])->Allocation:
    """
    Get a fully allocation of (0,1) that every agent have a list of adjacent pieces and return allocation
        of the union of each list
    :param alloction: An fully allocation of (0,1)
    :param agents: A list of agents
    :return: New alloction of (0,1)
    >>> Alice = PiecewiseConstantAgent([33, 33], "Alice")
    >>> George = PiecewiseConstantAgent([5, 5], "George")
    >>> alloc = Allocation([Alice, George])
    >>> agents = [Alice, George]
    >>> alloc.set_piece(1, [(0.2, 0.3)])
    >>> alloc.set_piece(0, [(0.4, 0.73)])
    >>> print(alloc)
    > Alice gets [(0.4, 0.73)] with value 10.89
    > George gets [(0.2, 0.3)] with value 0.5
    <BLANKLINE>
    >>> print(setRemain(alloc,agents),agents)
    [[(0.4, 0.73), (0.73, 1)], [(0.2, 0.3), (0.3, 0.4), (0, 0.2)]] [Alice is a piecewise-constant agent with values [33 33] and total value=66, George is a piecewise-constant agent with values [5 5] and total value=10]

    """
    I = Allocation(agents)
    for pieces,i in  zip(alloction,range(len(alloction))):
        if (pieces == None):
            continue
        I.set_piece(i,[intervalUnionFromList(pieces)])
    return I


def agentNormalize(agents: List[Agent])->List[Agent]:
    """
    replace all the agents with PiecewiseConstantAgent1Sgement that normalize to (0,1) segment
    :param agents: a list of agents that need to be normalized
    :return: a list of normalized agents


    >>> Alice = PiecewiseConstantAgent([3, 6, 3], name="Alice")
    >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
    >>> agents = [Alice, Hanna]
    >>> print("{} is {}".format(agents[0].name(), type(agents[0])))
    Alice is <class 'cake.agents.PiecewiseConstantAgent'>
    >>> agents = agentNormalize(agents)
    >>> print("{} is {}".format(agents[0].name(), type(agents[0])))
    Alice is <class 'cake.agents.PiecewiseConstantAgent1Sgement'>


    """
    for agent,i in zip(agents,range(len(agents))):
        agents[i] = PiecewiseConstantAgent1Sgement(agent)
    return agents


def ALG(agents: List[Agent], epsilon:float)->Allocation:
    """
        ALG: Algorithm that find Fair and Efficient Cake Division with Connected Pieces

        :param agents: a list that must contain at least 2 Agent objects.
                epsilon: constant between 0 to 1/3
        :return: a Fair and Efficient allocation.

        >>> Alice = PiecewiseConstantAgent([33,33], "Alice")
        >>> print(ALG([Alice],0.2))
        > Alice gets [(0, 1)] with value 1.0
        <BLANKLINE>
        >>> Alice = PiecewiseConstantAgent([3, 6, 3], name="Alice")
        >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
        >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
        >>> all_agents = [Alice,  Abraham, Hanna]
        >>> alloc = Allocation(all_agents)

        >>> remain = findRemainIntervals(alloc)
        >>> print(ALG(all_agents,0.2))
        > Alice gets [(0.429, 0.777)] with value 0.439
        > Abraham gets [(0, 0.429)] with value 0.739
        > Hanna gets [(0.777, 1)] with value 0.223
        <BLANKLINE>
    """
    logger.info(" Initialize partial allocation P = {P1, . . . , Pn} with empty interval")
    agents = agentNormalize(agents)
    allocation = Allocation(agents)
    interval = (checkWhile(agents,allocation,findRemainIntervals(allocation),epsilon))
    N = len(agents)
    while interval !=None:
        logger.info("\nThere exists an agent a∈[n] and an unassigned interval (%f,%f) from the remain intervals"
                    " such that Va(Pa) < Va(%f,%f) − epsilon/n^2",interval[0],interval[1],interval[0],interval[1])
        Rb = []
        C = getC(agents,allocation,epsilon,interval)
        names =[]
        for b in C:
            agent = b[0]
            names.append(agent.name())
            index = b[1]
            findRb(agent, allocation, epsilon, index, interval, N)
            Rb.append(findRb(agent,allocation,epsilon,index,interval,N))
        str =""
        for name in names:
            if name == names[0]:
                str+= name
            else:
                str+= " ,"+name
        logger.info("C = all agents satisfying the above condition = {%s}",str)
        a = C[np.argmin(np.asarray(Rb))]
        logger.info("%s is the chosen one with the minimum Rb = %s",a[0].my_name,Rb[np.argmin(Rb)])
        allocation.set_piece(a[1] ,[(interval[0],Rb[np.argmin(Rb)])])
        logger.info("Update partial allocation , Now the partial Allocation is:")
        logger.info(allocation)
        interval = (checkWhile(agents, allocation, findRemainIntervals(allocation), epsilon))
    logger.info("Associate unassigned intervals")
    return allocationToOnePiece(setRemain(allocation,agents),agents)


def efCheck(allocation:Allocation, epsilon:float)->str:
    """
    Check if tha allocation is (3 + o(1))-approximately envy-free allocation.
    :param allocation:the alloction we check
    :param epsilon:a constant between 0 to 1/3
    :return: A string that tell if the allocation is (3 + o(1))-approximately envy-free allocation.

    >>> Alice = PiecewiseConstantAgent([3, 6, 3], name="Alice")
    >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
    >>> epsilon  =0.1
    >>> all_agents = [Alice, Hanna]
    >>> alloc = Allocation(all_agents)
    >>> alloc.set_piece(0,[(0,0.9)])
    >>> alloc.set_piece(1,[(0.9,1)])
    >>> print(efCheck(alloc, 0.1))
    The Allocation isn't (3 + 9ε/n)approximately envy-free allocation
    >>> epsilon = 0.1
    >>> alloc = ALG(all_agents, epsilon)
    >>> print(efCheck(alloc, epsilon) )
    The Allocation is (3 + 9ε/n)approximately envy-free allocation

    """
    agents = allocation.agents
    o = (1/(3+(9*epsilon)/len(agents)))
    for i,a in zip(range(len(agents)),agents):
        x = allocation.get_piece(i)
        aPiece = allocation.get_piece(i)[0]
        for piece in allocation.get_pieces():
            if a.eval(aPiece[0],aPiece[1])<o*a.eval(piece[0][0],piece[0][1]):
                return "The Allocation isn't (3 + 9ε/n)approximately envy-free allocation"
    return "The Allocation is (3 + 9ε/n)approximately envy-free allocation"


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures,tests))
