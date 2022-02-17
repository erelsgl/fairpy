#!python3
"""
Utilities related to partitioning sets of numbers.

Programmer: Erel Segal-Halevi
Since: 2019-07
"""

import itertools
from typing import *
from numbers import Number
import prtpy

Partition = List[List[Any]]



#### EXACT COMPUTATION OF THE MAXIMIN PARTITION ####


import cvxpy
from fairpy.solve import *

import logging
logger = logging.getLogger(__name__)




def smallest_sums(partition:list, num_of_sums:int=1)->float:
    """
    Given a partition, return the sum of the smallest k parts (k = num_of_sums)
    
    >>> smallest_sums([[1,2],[3,4],[5,6]])
    3
    >>> smallest_sums([[1,2],[3,4],[5,6]], num_of_sums=2)
    10
    """
    sorted_sums = sorted([sum(part) for part in partition])
    return sum(sorted_sums[:num_of_sums])

def maximin_share_partition__cvxpy(
    c:int, valuation:list, items:Collection[Any], 
    multiplicity=1, numerator:int=1, 
    fix_smallest_part_value:Number=None
) -> Tuple[Partition, List[Number], Number]:
    """
    Computes the 1-of-c maximin share by solving an integer linear program, using CVXPY.
    Credit: Rob Pratt, https://or.stackexchange.com/a/6115/2576

    :param c: number of parts in the partition.
    :param numerator: number of parts that the agent is allowed to take (default: 1).
    :param valuation: maps an item to its value.
    :param multiplicity: The multiplicity of all items (int), or a map from an item to its multiplicity (list). Default: 1.
    :param items: a set of items. Default: all items.

    :return (partition, part_values, maximin-share value)
    """
    parts = range(c)
    num_of_items = len(valuation)
    if isinstance(multiplicity, Number):
        multiplicity = [multiplicity]*num_of_items

    min_value = cvxpy.Variable(nonneg=True)
    vars:dict = {
        item:
        [cvxpy.Variable(integer=True) for part in parts]
        for item in items
    }	# vars[i][j] is 1 iff item i is in part j.
    constraints = []
    parts_values = [
        sum([vars[item][part]*valuation[item] for item in items])
        for part in parts]

    constraints = []
    # Each variable must be non-negative:
    constraints += [vars[item][part]  >= 0 for part in parts for item in items] 	
    # Each item must be in exactly one part:
    constraints += [sum([vars[item][part] for part in parts]) == multiplicity[item] for item in items] 	
    # Parts must be in ascending order of value (a symmetry-breaker):
    constraints += [parts_values[part+1] >= parts_values[part] for part in range(c-1)]
    # The sum of each part must be at least min_value (by definition of min_value):
    constraints += [sum(parts_values[0:numerator]) >= min_value] 
    if fix_smallest_part_value is not None:
        constraints += [parts_values[0] == fix_smallest_part_value]


    solvers = [(cvxpy.SCIP, {}),(cvxpy.GLPK_MI, {}),(cvxpy.XPRESS, {})] 
        # GLPK_MI is very slow; 
        # ECOS_BB gives wrong results even on simple problems - not recommended;
        # CBC is not installed; 
        # XPRESS works well, but it is not free.
    maximize(min_value, constraints, solvers=solvers)

    partition = [
        sum([int(vars[item][part].value)*[item] for item in items if vars[item][part].value>=1], [])
        for part in parts
    ]
    part_values = [parts_values[part].value for part in parts]
    return (partition, part_values, min_value.value)




def maximin_share_partition(c:int, valuation:list, items:Collection[Any]=None, numerator:int=1, **kwargs)->int:
    """	
    Compute the of 1-of-c MMS of the given items, by the given valuation.
    :return (partition, part_values, maximin-share value)

    >>> maximin_share_partition(c=1, valuation=[10,20,40,1])
    ([[0, 1, 2, 3]], [71.0], 71.0)
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1])
    ([[0, 1, 3], [2]], [31.0, 40.0], 31.0)
    >>> int(maximin_share_partition(c=3, valuation=[10,20,40,1])[2])
    11
    >>> int(maximin_share_partition(c=4, valuation=[10,20,40,1])[2])
    1
    >>> int(maximin_share_partition(c=5, valuation=[10,20,40,1])[2])
    0
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1], items=[1,2])
    ([[1], [2]], [20.0, 40.0], 20.0)
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1], copies=2)
    ([[0, 1, 2, 3], [0, 1, 2, 3]], [71.0, 71.0], 71.0)
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1], copies=[2,1,1,0])
    ([[0, 0, 1], [2]], [40.0, 40.0], 40.0)
    >>> maximin_share_partition(c=3, valuation=[10,20,40,1], numerator=2)
    ([[0, 3], [1], [2]], [11.0, 20.0, 40.0], 31.0)
    >>> #maximin_share_partition(c=3, valuation=[10,20,40,1], numerator=2, fix_smallest_part_value=0)
    """
    if len(valuation)==0:
        raise ValueError("Valuation is empty")
    num_of_items = len(valuation)
    if items is None:
        items = list(range(num_of_items))

    bins:prtpy = prtpy.partition(
        algorithm=prtpy.exact.integer_programming,
        numbins=c,
        items=items,
        map_item_to_value=lambda item: valuation[item],
        objective=prtpy.obj.MaximizeKSmallestSums(numerator),
        outputtype=prtpy.out.PartitionAndSums,
        **kwargs
    )

    return (bins.bins, list(bins.sums), sum(sorted(bins.sums)[:numerator]))







if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

    from fairpy import solve
    import sys
    solve.logger.addHandler(logging.StreamHandler(sys.stdout))
    solve.logger.setLevel(logging.INFO)	
