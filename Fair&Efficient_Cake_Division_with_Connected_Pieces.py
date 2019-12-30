"""
Article name : Fair and Efficient Cake Division with Connected Pieces
Authors : Eshwar Ram Arunachaleswaran , Siddharth Barman , Rachitesh Kumar and Nidhi Rathi
Algorithm #1 : ALG
NAME : Ori Zitzer
Date : 27/12/19
"""
from agents import *
from allocations import *
import numpy as np
import random


def findRemainIntervals(allocation :Allocation):
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
        remain.append((piecesList[-1][1],1))

    return remain
def checkWhile(agents: List[Agent],allocation :Allocation,remain,epsilon):
    nSquared = len(agents)*len(agents)
    for agent,i in zip(agents,range(len(agents))):
        for interval in remain:
            if (agent.eval(allocation[i][0][0],allocation[i][0][1]) <
                    agent.eval(interval[0],interval[1]) - (epsilon/nSquared)):
                return interval
    return None
def getC(agents: List[Agent],allocation :Allocation,epsilon,interval):
    nSquared = len(agents) * len(agents)
    newAgents = []
    for agent, i in zip(agents, range(len(agents))):
        if (agent.eval(allocation[i][0][0], allocation[i][0][1]) <
                agent.eval(interval[0], interval[1]) - (epsilon / nSquared)):
            newAgents.append((agent,i))
    return newAgents
"""finish it"""
def findRb(agent:Agent , allocation:Allocation,epsilon,index,interval,n):
    currentPiece = allocation[index][0]
    currentPieceEval = agent.eval(currentPiece[0],currentPiece[1])
    Rb = (interval[1] + interval[0])/2
    equation = currentPieceEval - epsilon/(n*n)
    theta = Rb
    while agent.eval(interval[0],Rb) != equation:
        if(agent.eval(interval[0],Rb) > equation):
            Rb = (Rb+interval[0])/2
def findPiece(reamin:List[tuple],attr , leftOrRight):
    for piece in reamin:
        if piece[leftOrRight]==attr:
            return piece
    return None

def setRemain(allocation:Allocation):
    remain = findRemainIntervals(allocation)
    choice = random.choice(('Left', 'Right'))
    partialAlloc = allocation.get_pieces()
    for pieces in partialAlloc:
        right = pieces[0][1]
        newPart = findPiece(remain, right,0)
        if newPart == None : continue
        pieces.append(newPart)
        remain.remove(newPart)
    if len(remain) == 1:
        for pieces in partialAlloc:
            if remain[0][1] == pieces[0][0]:
                pieces.append(remain[0])
                break
    return partialAlloc
def intervalUnionFromList(intervals:List[tuple]):
    minimum = 1
    maximum = 0
    for interval in intervals:
        if interval[0] < minimum: minimum = interval[0]
        elif interval[1] > maximum: maximum = interval[1]
    return (minimum,maximum)
def allocationToOnePiece(alloction:List[List[tuple]],agents:List[Agent]):
    I = Allocation(agents)
    for pieces,i in  zip(alloction,range(len(alloction))):
        I.set_piece(i,intervalUnionFromList(pieces))
    return I


def ALG(agents: List[Agent],epsilon)->Allocation:
    """
        ALG: Algorithm that find Fair and Efficient Cake Division with Connected Pieces

        :param agents: a list that must contain at least 2 Agent objects.
                epsilon: constant between 0 to 1/3
        :return: a Fair and Efficient allocation.
        >>> Alice = PiecewiseConstantAgent([33,33], "Alice")
        >>> ALG([Alice])
        > Alice gets [(0, 1)] with value 66.00
        <BLANKLINE>
    """
    allocation = Allocation(agents)
    interval = (checkWhile(agents,allocation,findRemainIntervals(allocation),epsilon))
    N = len(agents)
    while interval !=None:
        Rb =np.array()
        C = getC(agents,allocation,epsilon,interval)
        for b in C:
            agent = b[0]
            index = b[1]
            r = findRb(agent,allocation,epsilon,index,interval,N)
            np.append(Rb,r)
        a = C[np.argmin(Rb)]
        allocation.set_piece(a[1] ,[(interval[0],Rb[np.argmin(Rb)])])
        interval = (checkWhile(agents, allocation, findRemainIntervals(allocation), epsilon))
    return allocationToOnePiece(setRemain(allocation),agents)


if __name__ == "__main__":
    Alice = PiecewiseConstantAgent([3, 6, 3], name="Alice")
    George = PiecewiseConstantAgent([0, 2, 4, 6], name="George")
    Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
    Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
    all_agents = [Alice, George, Abraham, Hanna]
    alloc = Allocation(all_agents)
    alloc.set_piece(0,[(0,0.1)])
    alloc.set_piece(1,[(0.2,0.3)])
    alloc.set_piece(2,[(0.4,0.7)])
    alloc.set_piece(3,[(0.8,1)])

    print(findRemainIntervals(alloc))
    """import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))"""