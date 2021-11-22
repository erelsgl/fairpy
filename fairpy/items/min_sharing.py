#!python3

"""
An implementation of the min-sharing algorithm. Reference:

Fedor Sandomirskiy and Erel Segal-Halevi (2020).
["Efficient Fair Division with Minimal Sharing"](https://arxiv.org/abs/1908.01669).

Programmer: Eliyahu Sattat
Since:  2020
"""

from fairpy import ValuationMatrix, Allocation, convert_input_to_valuation_matrix
from typing import Any

from fairpy.items.min_sharing_impl.FairProportionalAllocationProblem import FairProportionalAllocationProblem
from fairpy.items.min_sharing_impl.FairEnvyFreeAllocationProblem import FairEnvyFreeAllocationProblem
from fairpy.items.min_sharing_impl.FairMaxProductAllocationProblem import FairMaxProductAllocationProblem

@convert_input_to_valuation_matrix
def proportional_allocation_with_min_sharing(instance:Any, num_of_decimal_digits=3)->Allocation:
    """
    Finds a proportional allocation with a minimum number of sharings.

    >>> proportional_allocation_with_min_sharing([ [3] , [5] ]).round(2).matrix   # single item
    [[0.5]
     [0.5]]
    >>> proportional_allocation_with_min_sharing([ [3,2] , [1,4] ]).round(2).matrix   # two items
    [[1. 0.]
     [0. 1.]]
    >>> proportional_allocation_with_min_sharing([ [10,18,1,1] , [10,18,1,1] , [10,10,5,5] ]).num_of_sharings()   # three items
    0
    """
    return FairProportionalAllocationProblem(instance).find_allocation_with_min_sharing(num_of_decimal_digits)


@convert_input_to_valuation_matrix
def envyfree_allocation_with_min_sharing(instance:Any, num_of_decimal_digits=3)->Allocation:
    """
    Finds an envy-free allocation with a minimum number of sharings.

    >>> envyfree_allocation_with_min_sharing([ [3] , [5] ]).round(2).matrix   # single item
    [[0.5]
     [0.5]]
    >>> envyfree_allocation_with_min_sharing([ [3,2] , [1,4] ]).round(2).matrix   # two items
    [[1. 0.]
     [0. 1.]]
    >>> envyfree_allocation_with_min_sharing([ [10,18,1,1] , [10,18,1,1] , [10,10,5,5] ]).num_of_sharings()   # three items
    1
    """
    return FairEnvyFreeAllocationProblem(instance).find_allocation_with_min_sharing(num_of_decimal_digits)


@convert_input_to_valuation_matrix
def maxproduct_allocation_with_min_sharing(instance, tolerance:float=0.01, num_of_decimal_digits=3)->Allocation:
    """
    Finds an approximate max-product (aka max Nash welfare) allocation with a minimum number of sharings.
    The utility of each agent will be at least (1-tolerance) of his utility in the max Nash welfare allocation.

    >>> maxproduct_allocation_with_min_sharing([ [3] , [5] ]).round(2).matrix   # single item
    [[0.5]
     [0.5]]
    >>> maxproduct_allocation_with_min_sharing([ [3,2] , [1,4] ]).round(2).matrix   # two items
    [[1. 0.]
     [0. 1.]]
    >>> maxproduct_allocation_with_min_sharing([ [10,18,1,1] , [10,18,1,1] , [10,10,5,5] ]).num_of_sharings()   # three items
    2
    """
    return FairMaxProductAllocationProblem(instance,tolerance).find_allocation_with_min_sharing(num_of_decimal_digits)




if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
