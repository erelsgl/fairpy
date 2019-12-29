"""
Article name : Fair and Efficient Cake Division with Connected Pieces
Authors : Eshwar Ram Arunachaleswaran , Siddharth Barman , Rachitesh Kumar and Nidhi Rathi
Algorithm #1 : ALG
NAME : Ori Zitzer
Date : 27/12/19
"""
from agents import *
from allocations import *
def findRemainIntervals(allocation :Allocation):
    remain = []
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
            newAgents.append(agent)
    return newAgents

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
    while interval !=None:
        for b in getC(agents,allocation,epsilon,interval):





if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))