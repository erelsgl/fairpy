#!python3
"""
    A min-sharing proportional allocation algorithm.

    Programmer: Eliyahu Sattat
    Since:  2020
"""

from fairpy import ValuationMatrix

from fairpy.items.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy.items.min_sharing_impl.FairThresholdAllocationProblem import FairThresholdAllocationProblem

from cvxpy.constraints.constraint import Constraint

import logging
logger = logging.getLogger(__name__)


class FairProportionalAllocationProblem(FairThresholdAllocationProblem):
    """
    Finds a proportional allocation with minimum sharing.
    
    Proportional allocation definition:
    V = agents valuation
    C = all agents properties
    X = proportional allocation
    n = the number of the agents
    For all i: Vi(Xi) ≥ Vi(C) / n

    >>> v = [[1, 2, 3,4], [4, 5, 6,5], [7, 8, 9,6]]
    >>> fpap =FairProportionalAllocationProblem(v)
    >>> g1 = [[0.0, 0.0, 0.0, 1], [1, 1, 1, 1], [0.0, 0.0, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [1, 1, 1, 1], [1, 0.0, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 0.0, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 1, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g).round(2))
    [[0.   0.   0.   0.88]
     [0.   0.46 1.   0.05]
     [1.   0.54 0.   0.07]]
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 0.0, 1, 1], [1, 1, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> fpap.find_allocation_for_graph(g).round(2).num_of_sharings()
    2
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 0.0, 1, 1], [1, 1, 1, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g).round(2))
    [[0.   0.   0.   0.84]
     [0.   0.   0.99 0.15]
     [1.   1.   0.01 0.01]]
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 0.0, 0.0, 0.0]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 1, 0.0, 0.0]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g).round(2))
    [[0.   0.   0.   0.86]
     [0.   0.47 1.   0.14]
     [1.   0.53 0.   0.  ]]
    >>> v = [ [465,0,535] , [0,0,1000]  ]  # This example exposed a bug in OSQP solver!
    >>> fpap =FairProportionalAllocationProblem(v)
    >>> g1 = [[1,1,1],[0,0,1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g).round(3))
    [[1.    1.    0.391]
     [0.    0.    0.609]]
    """

    def __init__(self, valuation_matrix):
        valuation_matrix = ValuationMatrix(valuation_matrix)
        thresholds = [
            sum(valuation_matrix[i]) / valuation_matrix.num_of_agents 
            for i in valuation_matrix.agents()]
        logger.info("The proportionality thresholds are: %s",thresholds)
        super().__init__(valuation_matrix, thresholds)

    def fairness_adjective(self)->str:
        return "proportional"


if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
