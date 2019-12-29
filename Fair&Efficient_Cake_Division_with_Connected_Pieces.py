"""
Article name : Fair and Efficient Cake Division with Connected Pieces
Authors : Eshwar Ram Arunachaleswaran , Siddharth Barman , Rachitesh Kumar and Nidhi Rathi
Algorithm #1 : ALG
NAME : Ori Zitzer
Date : 27/12/19
"""
from agents import *
from allocations import *

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
    while():



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))