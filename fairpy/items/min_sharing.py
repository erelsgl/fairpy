#!python3

"""
An implementation of the min-sharing algorithm. Reference:

Fedor Sandomirskiy and Erel Segal-Halevi (2020).
["Efficient Fair Division with Minimal Sharing"](https://arxiv.org/abs/1908.01669).

Programmer: Eliyahu Sattat
Since:  2020
"""

from fairpy import ValuationMatrix, AllocationMatrix

from fairpy.items.min_sharing_impl.FairProportionalAllocationProblem import FairProportionalAllocationProblem
from fairpy.items.min_sharing_impl.FairEnvyFreeAllocationProblem import FairEnvyFreeAllocationProblem
from fairpy.items.min_sharing_impl.FairMaxProductAllocationProblem import FairMaxProductAllocationProblem

def proportional_allocation_with_min_sharing(instance:ValuationMatrix, num_of_decimal_digits=3)->AllocationMatrix:
    """
    Finds a proportional allocation with a minimum number of sharings.

    >>> print(proportional_allocation_with_min_sharing(ValuationMatrix([ [3] , [5] ])).round(2))   # single item
    [[0.5]
     [0.5]]
    >>> print(proportional_allocation_with_min_sharing(ValuationMatrix([ [3,2] , [1,4] ])).round(2))   # two items
    [[1. 0.]
     [0. 1.]]
    >>> print(proportional_allocation_with_min_sharing(ValuationMatrix([ [10,18,1,1] , [10,18,1,1] , [10,10,5,5] ])))   # three items
    [[1. 0. 0. 0.]
     [0. 1. 0. 0.]
     [0. 0. 1. 1.]]
    """
    return FairProportionalAllocationProblem(instance).find_allocation_with_min_sharing(num_of_decimal_digits)


def envyfree_allocation_with_min_sharing(instance:ValuationMatrix, num_of_decimal_digits=3)->AllocationMatrix:
    """
    Finds an envy-free allocation with a minimum number of sharings.

    >>> print(envyfree_allocation_with_min_sharing(ValuationMatrix([ [3] , [5] ])).round(2))   # single item
    [[0.5]
     [0.5]]
    >>> print(envyfree_allocation_with_min_sharing(ValuationMatrix([ [3,2] , [1,4] ])).round(2))   # two items
    [[1. 0.]
     [0. 1.]]
    >>> print(envyfree_allocation_with_min_sharing(ValuationMatrix([ [10,18,1,1] , [10,18,1,1] , [10,10,5,5] ])))   # three items
    [[1.    0.    0.    0.   ]
     [0.    0.556 0.    0.   ]
     [0.    0.444 1.    1.   ]]
    """
    return FairEnvyFreeAllocationProblem(instance).find_allocation_with_min_sharing(num_of_decimal_digits)


def maxproduct_allocation_with_min_sharing(instance:ValuationMatrix, tolerance:float=0.01, num_of_decimal_digits=3)->AllocationMatrix:
    """
    Finds an approximate max-product (aka max Nash welfare) allocation with a minimum number of sharings.
    The utility of each agent will be at least (1-tolerance) of his utility in the max Nash welfare allocation.

    >>> print(maxproduct_allocation_with_min_sharing(ValuationMatrix([ [3] , [5] ])).round(2))  # single item
    [[0.5]
     [0.5]]
    >>> print(maxproduct_allocation_with_min_sharing(ValuationMatrix([ [3,2] , [1,4] ])).round(2))   # two items
    [[1. 0.]
     [0. 1.]]
    >>> print(maxproduct_allocation_with_min_sharing(ValuationMatrix([ [10,18,1,1] , [10,18,1,1] , [10,10,5,5] ])))   # three items
    [[0.73  0.295 0.    0.   ]
     [0.    0.705 0.    0.   ]
     [0.27  0.    1.    1.   ]]
    """
    return FairMaxProductAllocationProblem(instance,tolerance).find_allocation_with_min_sharing(num_of_decimal_digits)




if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
