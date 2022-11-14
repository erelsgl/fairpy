#!python3
"""
    A min-sharing max-product allocation algorithm.

    Programmer: Eliyahu Sattat
    Since:  2020
"""

from fairpy import ValuationMatrix, AllocationMatrix
from fairpy.items.max_welfare import max_product_allocation
from fairpy.items.min_sharing_impl.FairThresholdAllocationProblem import FairThresholdAllocationProblem

import logging

logger = logging.getLogger(__name__)


class FairMaxProductAllocationProblem(FairThresholdAllocationProblem):
    """
    Finds a Nash-optimal (aka max-product) allocation with minimum sharing.

    >>> from fairpy.items.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
    >>> v = ValuationMatrix([[1, 2, 3,4], [4, 5, 6,5], [7, 8, 9,6]])
    >>> fpap =FairMaxProductAllocationProblem(v)
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
    [[0.   0.   0.   0.99]
     [0.   0.34 1.   0.  ]
     [1.   0.66 0.   0.  ]]


     
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 0.0, 1, 1], [1, 1, 0.0, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 0.0, 1, 1], [1, 1, 1, 1]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 0.0, 0.0, 0.0]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g))
    None


    
    >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 1, 0.0, 0.0]]
    >>> g = ConsumptionGraph(g1)
    >>> print(fpap.find_allocation_for_graph(g).round(2))
    [[0.   0.   0.   0.99]
     [0.   0.34 1.   0.01]
     [1.   0.66 0.   0.  ]]
    >>> # v = [ [465,0,535] , [0,0,1000]  ]  # This example exposed a bug in OSQP solver!
    >>> # fpap =FairMaxProductAllocationProblem(v)
    >>> # g1 = [[1,1,1],[0,0,1]]
    >>> # g = ConsumptionGraph(g1)
    >>> # print(fpap.find_allocation_for_graph(g).round(3))
    """

    def __init__(self, valuation_matrix:ValuationMatrix, tolerance=0.01):
        mpa = max_product_allocation(valuation_matrix)
        mpa_utilities = AllocationMatrix(mpa).utility_profile(valuation_matrix)
        logger.info("The max-product allocation is:\n%s,\nwith utility profile: %s",mpa,mpa_utilities)
        thresholds = mpa_utilities * (1-tolerance)
        logger.info("The thresholds are: %s",thresholds)
        logger.info("The proportionality thresholds are: %s", [
            sum(valuation_matrix[i]) / valuation_matrix.num_of_agents 
            for i in valuation_matrix.agents()])
        self.tolerance = tolerance
        super().__init__(valuation_matrix, thresholds)


    def fairness_adjective(self)->str:
        return "{}-max-product".format((1-self.tolerance))

if __name__ == '__main__':
    # import logging, sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
