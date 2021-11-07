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
from fairpy.cake.fe_cake_division_connected_pieces_utils import *
import numpy as np
import logging
logger = logging.getLogger(__name__)




def ALG(agents: List[Agent], epsilon:float)->Allocation:
    """
    ALG: Algorithm that find Fair and Efficient Cake Division with Connected Pieces

    :param agents: a list that must contain at least 2 Agent objects.
            epsilon: constant between 0 to 1/3
    :return: a Fair and Efficient allocation.

    >>> Alice = PiecewiseConstantAgent([33,33], "Alice")
    >>> print(ALG([Alice],0.2))
    Alice gets {(0, 1)} with value 1.
    <BLANKLINE>
    >>> Alice = PiecewiseConstantAgent([3, 6, 3], name="Alice")
    >>> Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
    >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
    >>> all_agents = [Alice,  Abraham, Hanna]
    >>> round_allocation(ALG(all_agents,0.2))
    Alice gets {(0.429, 0.777)} with value 0.439.
    Abraham gets {(0, 0.429)} with value 0.739.
    Hanna gets {(0.777, 1)} with value 0.223.
    <BLANKLINE>
    >>> Alice = PiecewiseConstantAgent([3, 6, 3], name="Alice")
    >>> Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")
    >>> epsilon  =0.1
    >>> all_agents = [Alice, Hanna]
    >>> alloc = ALG(all_agents, epsilon)
    >>> print(efCheck(alloc, epsilon) )
    The Allocation is (3 + 9ε/n)approximately envy-free allocation

    """
    logger.info(" Initialize partial allocation P = {P1, . . . , Pn} with empty interval")
    agents = agentNormalize(agents)
    pieces = len(agents)*[None]
    interval = (checkWhile(agents,pieces,findRemainIntervals(pieces),epsilon))
    N = len(agents)
    while interval !=None:
        logger.info("\nThere exists an agent a∈[n] and an unassigned interval (%f,%f) from the remain intervals"
                    " such that Va(Pa) < Va(%f,%f) − epsilon/n^2",interval[0],interval[1],interval[0],interval[1])
        Rb = []
        C = getC(agents,pieces,epsilon,interval)
        names =[]
        for b in C:
            agent = b[0]
            names.append(agent.name())
            index = b[1]
            findRb(agent, pieces, epsilon, index, interval, N)
            Rb.append(findRb(agent,pieces,epsilon,index,interval,N))
        str =""
        for name in names:
            if name == names[0]:
                str+= name
            else:
                str+= " ,"+name
        logger.info("C = all agents satisfying the above condition = {%s}",str)
        a = C[np.argmin(np.asarray(Rb))]
        logger.info("%s is the chosen one with the minimum Rb = %s",a[0].name(), Rb[np.argmin(Rb)])
        pieces[a[1]] = [(interval[0],Rb[np.argmin(Rb)])]
        logger.info("Update partial allocation , Now the partial Allocation is:")
        logger.info(pieces)
        interval = (checkWhile(agents, pieces, findRemainIntervals(pieces), epsilon))
    logger.info("Associate unassigned intervals")
    return allocationToOnePiece(setRemain(pieces,agents),agents)



from fairpy.cake.pieces import round_allocation
if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures,tests))
