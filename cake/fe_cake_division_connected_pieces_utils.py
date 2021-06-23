#!python3
"""
Article name : Fair and Efficient Cake Division with Connected Pieces
Authors : Eshwar Ram Arunachaleswaran , Siddharth Barman , Rachitesh Kumar and Nidhi Rathi
Algorithm #1 : ALG
Programmer: Ori Zitzer
Since: 2019-12
"""

from fairpy import Allocation
from fairpy.agents import *
import random

import logging
logger = logging.getLogger(__name__)



def agentNormalize(agents: List[Agent])->List[Agent]:
    """
    replace all the agents with PiecewiseConstantAgent1Segment that normalize to (0,1) segment
    :param agents: a list of agents that need to be normalized
    :return: a list of normalized agents
    """
    for agent,i in zip(agents,range(len(agents))):
        agents[i] = PiecewiseConstantAgent1Segment(agent.valuation.values, name=agent.name())
    return agents


def findRemainIntervals(pieces: List[Any])->List[tuple]:
    """
    Returns the remaining intervals from the allocation in (0,1)
    :param allocation: an Allocation
    :return: the remain intervals
    >>> pieces = 4*[[]]
    >>> print(findRemainIntervals(pieces))
    [(0, 1)]
    >>> pieces[1] = [(0.2,0.3)]
    >>> print(findRemainIntervals(pieces))
    [(0, 0.2), (0.3, 1)]
    >>> pieces[3] = [(0.4,0.73),(0.92,1)]
    >>> print(findRemainIntervals(pieces))
    [(0, 0.2), (0.3, 0.4), (0.73, 0.92)]
    """
    remain = []
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


def checkWhile(agents: List[Agent], pieces:List[Any], remain:List[tuple], epsilon:float)->tuple:
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
    >>> pieces = 4*[[]]
    >>> agents = [Alice,George,Abraham,Hanna]
    >>> agents = agentNormalize(agents)
    >>> pieces[1] = [(0.2,0.3)]
    >>> pieces[3] = [(0.4,0.73),(0.92,1)]
    >>> print(checkWhile(agents,pieces,findRemainIntervals(pieces),0))
    (0, 0.2)
    >>> pieces[0] = [(0,0.2)]
    >>> print(checkWhile(agents,pieces,findRemainIntervals(pieces),0))
    (0.3, 0.4)
    >>> pieces[2] = [(0.73, 0.92)]
    >>> print(checkWhile(agents,pieces,findRemainIntervals(pieces),0))
    (0.3, 0.4)
    >>> newPieces = 4*[[]]
    >>> newPieces[1] = [(0.1, 0.3)]
    >>> newPieces[3] = [(0.3, 0.73)]
    >>> print(checkWhile(agents, newPieces, findRemainIntervals(newPieces), 0.1))
    (0.73, 1)
    >>> newPieces[0] = [(0.73, 0.8)]
    >>> print(checkWhile(agents, newPieces, findRemainIntervals(newPieces), 0.1))
    (0, 0.1)
    >>> newPieces[2] = [(0.01, 0.05)]
    >>> print(checkWhile(agents, newPieces, findRemainIntervals(newPieces), 0.1))
    (0.05, 0.1)
    >>> newPieces = 4*[[]]
    >>> newPieces[1] = [(0.1, 0.3)]
    >>> newPieces[3] = [(0.3, 0.73)]
    >>> print(checkWhile(agents, newPieces, findRemainIntervals(newPieces), 0.3))
    (0.73, 1)
    >>> newPieces[0] = [(0.8,0.96)]
    >>> print(checkWhile(agents, newPieces, findRemainIntervals(newPieces), 0.3))
    None
    >>> newPieces[2] = [(0, 0.05)]
    >>> print(checkWhile(agents, newPieces, findRemainIntervals(newPieces), 0.3))
    None
    """
    nSquared = len(agents)*len(agents)
    piecesList = []
    # turn the pieces from list of lists of tuples into list of tuples
    for list in pieces:
        if list != None: piecesList += list
    if len(piecesList)==0:
        return (0,1)
    for interval in remain:
        for agent,i in zip(agents,range(len(agents))):
            if (pieces[i] == None or len(pieces[i])==0):
                continue
            if (agent.eval(pieces[i][0][0], pieces[i][0][1]) <
                    (agent.eval(interval[0],interval[1]) - (epsilon/nSquared))):
                return interval
    return None



#######################################




def getC(agents: List[Agent], pieces:List[Any], epsilon:float, interval:tuple)->List[Agent]:
    """
    Get the C group from the Algorithm
    :param agents: A list of agents
    :param allocation: An Allocation
    :param epsilon: A constant between 0 to 1/3
    :param interval: The chosen interval out of the remain intervals
    :return: All the agents that their current evaluation to their piece is smaller than
                the evaluation to the interval - (epsilon/n^2) when n is the number of agents

    >>> pieces = 4*[[]]
    >>> Alice = PiecewiseConstantAgent([33, 33], "Alice")
    >>> George = PiecewiseConstantAgent([5,5],"George")
    >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
    >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
    >>> agents = [Alice,George,Abraham,Hanna]
    >>> agents = agentNormalize(agents)
    >>> pieces[1] =[(0.2,0.3)]
    >>> pieces[3] = [(0.4,0.7)]
    >>> interval = checkWhile(agents, pieces, findRemainIntervals(pieces), 0.2)
    >>> print([agent[0].name() for agent in getC(agents,pieces,0.2,interval)])
    ['Alice', 'George', 'Abraham']
    >>> pieces[0] = [(0.75,1)]
    >>> interval = checkWhile(agents, pieces, findRemainIntervals(pieces), 0)
    >>> print([agent[0].name() for agent in getC(agents,pieces,0.2,interval)])
    ['George', 'Abraham']
    """
    nSquared = len(agents) * len(agents)
    newAgents = []
    for agent, i in zip(agents, range(len(agents))):
        if(pieces[i]==None or len(pieces[i])==0):
            newAgents.append((agent,i))
            continue
        if (agent.eval(pieces[i][0][0], pieces[i][0][1]) <
                agent.eval(interval[0], interval[1]) - (epsilon / nSquared)):
            newAgents.append((agent,i))
    return newAgents


def findRb(agent:Agent , pieces:List[Any], epsilon:float,index:int,interval:tuple,n:int)->float:
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
    >>> pieces = 4*[None]
    >>> print(round(findRb(Hanna,pieces,0.1,3,(0,1),4),6))
    0.002083
    """
    currentPieceEval = 0
    if pieces[index]!=None:
        currentPiece = pieces[index][0]
        currentPieceEval = agent.eval(currentPiece[0],currentPiece[1])
    return agent.mark(interval[0],currentPieceEval + epsilon/(n*n))


def findPiece(reamin:List[tuple], attr:float , leftOrRight:int)->tuple:
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


def setRemain(partialAlloc:List[List[tuple]], agents: List[Agent])->List[List[tuple]]:
    """
    Set the remain intervals to the agents
    :param allocation: A partial allocation of (0,1)
    :param agents: A list of agents
    :return: A complete allocation of (0,1)
    >>> Alice = PiecewiseConstantAgent([33, 33], "Alice")
    >>> George = PiecewiseConstantAgent([5, 5], "George")
    >>> agents = [Alice, George]
    >>> pieces = 2*[None]
    >>> pieces[0] = [(0.4, 0.73)]
    >>> pieces[1] = [(0.2, 0.3)]
    >>> pieces = setRemain(pieces,agents)
    >>> pieces
    [[(0.4, 0.73), (0.73, 1)], [(0.2, 0.3), (0.3, 0.4), (0, 0.2)]]
    >>> print(Allocation(agents,pieces))
    Alice gets {(0.4, 0.73),(0.73, 1)} with value 19.8.
    George gets {(0, 0.2),(0.2, 0.3),(0.3, 0.4)} with value 2.
    <BLANKLINE>
    """
    remain = findRemainIntervals(partialAlloc)
    for i,pieces in zip(range(len(partialAlloc)),partialAlloc):
        if(pieces==None):
            maxPiece , maxEval = 0,0
            for remainPiece in remain:
                if agents[i].eval(remainPiece[0],remainPiece[1])>=maxEval:
                    maxEval = agents[i].eval(remainPiece[0],remainPiece[1])
                    maxPiece = remainPiece
            remain.remove(maxPiece)
            partialAlloc[i] = [maxPiece]
        
    for pieces in partialAlloc:
        if(pieces==None):
            continue
        right = pieces[0][1]
        newPart = findPiece(remain, right,0)
        if newPart == None : continue
        pieces.append(newPart)
        remain.remove(newPart)

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
    """
    new_pieces = len(agents)*[None]
    for pieces,i in  zip(alloction,range(len(alloction))):
        if (pieces == None):
            continue
        new_pieces[i] = [intervalUnionFromList(pieces)]
    return Allocation(agents, new_pieces)


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
    >>> pieces = [ [(0,0.9)] , [(0.9,1)] ]
    >>> alloc = Allocation(all_agents, pieces)
    >>> print(efCheck(alloc, 0.1))
    The Allocation isn't (3 + 9ε/n)approximately envy-free allocation
    >>> pieces = [ [(0,0.5)] , [(0.5,1)] ]
    >>> alloc = Allocation(all_agents, pieces)
    >>> print(efCheck(alloc, epsilon) )
    The Allocation is (3 + 9ε/n)approximately envy-free allocation
    """
    agents = allocation.agents
    o = (1/(3+(9*epsilon)/len(agents)))
    for i,a in zip(range(len(agents)),agents):
        aPiece = allocation[i][0]
        for piece in allocation:
            if a.eval(aPiece[0],aPiece[1])<o*a.eval(piece[0][0],piece[0][1]):
                return "The Allocation isn't (3 + 9ε/n)approximately envy-free allocation"
    return "The Allocation is (3 + 9ε/n)approximately envy-free allocation"





if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures,tests))
