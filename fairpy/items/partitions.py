#!python3
"""
Utilities related to partitioning sets of numbers.

Programmer: Erel Segal-Halevi
Since: 2019-07
"""

import itertools
from typing import *
from numbers import Number

Partition = List[List[Any]]




####  ENUMERATING ALL OR SOME OF THE PARTITIONS ####

def powerset(items: Collection[Any]) -> Generator[tuple,None,None]:
    """
    Generates all subsets of the given iterable.
    Based on code from https://docs.python.org/3.7/library/itertools.html.
    :param items: an iterable.
    >>> for s in powerset([1,2,3]): print(s)
    ()
    (1,)
    (2,)
    (3,)
    (1, 2)
    (1, 3)
    (2, 3)
    (1, 2, 3)
    """
    s = list(items)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


def all_partitions(items: Collection[Any]) -> Generator[Partition,None,None]:
    """
    Generates all partitions of the given set.
    Based on code by alexis, https://stackoverflow.com/a/30134039/827927

    >>> for p in all_partitions([1,2,3]): print(p)
    [[1, 2, 3]]
    [[1], [2, 3]]
    [[1, 2], [3]]
    [[2], [1, 3]]
    [[1], [2], [3]]
    """
    if len(items) == 1:
        yield [ items ]
        return
    first = items[0]
    for smaller in all_partitions(items[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset
        yield [ [ first ] ] + smaller


def partitions_to_at_most_c_subsets(c:int, items: Collection[Any]) -> Generator[Partition,None,None]:
    """
    Generates all partitions of the given set whose size is at most c subsets.

    >>> for p in partitions_to_at_most_c_subsets(2, [1,2,3]): print(p)
    [[1, 2, 3]]
    [[1], [2, 3]]
    [[1, 2], [3]]
    [[2], [1, 3]]
    """
    if len(items) == 1:
        yield [ items ]
        return
    first = items[0]
    for smaller in all_partitions(items[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset
        if len(smaller)<c:
            yield [ [ first ] ] + smaller


def partitions_to_exactly_c_subsets(c: int, items: Collection[Any]) -> Generator[Partition,None,None]:
    """
    Generates all partitions of the given set whose size is exactly c subsets.
    NOTE: This is very inefficient - better to use powerset.

    >>> for p in partitions_to_exactly_c_subsets(2, [1,2,3]): print(p)
    [[1], [2, 3]]
    [[1, 2], [3]]
    [[2], [1, 3]]
    >>> list(partitions_to_exactly_c_subsets(3, [1,2]))
    []
    """
    for p in partitions_to_at_most_c_subsets(c, items):
        if len(p)==c:
            yield p






#### COMPUTING A BALANCED PARTITION OF NUMBERS ####


def greedy_partition(c:int, items:Collection[Number]) -> Partition:
    """
    Partition the numbers using the greedy number partitioning algorithm:
       https://en.wikipedia.org/wiki/Greedy_number_partitioning
    >>> greedy_partition(2, [1,2,3,4,5,9])
    [[9, 3], [5, 4, 2, 1]]
    >>> greedy_partition(3, [1,2,3,4,5,9])
    [[9], [5, 2, 1], [4, 3]]
    """
    values = sorted(items, reverse=True)
    parts = [ [] for i in range(c) ]
    sums  = [ 0 for i in range(c)  ]
    for v in values:
        index_of_part_with_smallest_sum = min(range(c), key=lambda i:sums[i])
        parts[index_of_part_with_smallest_sum].append(v)
        sums [index_of_part_with_smallest_sum] += v
    return parts


def bidirectional_balanced_partition(c:int, items:Collection[Number]) -> Partition:
    """
    Partition the numbers using "bidirectional balanced partition" (ABCCBA order).

    >>> bidirectional_balanced_partition(2, [1,2,3,4,5,9])
    [[9, 3, 2], [5, 4, 1]]
    >>> bidirectional_balanced_partition(3, [1,2,3,4,5,9])
    [[9, 1], [5, 2], [4, 3]]
    """
    values = sorted(items, reverse=True)
    parts = [ [] for i in range(c) ]
    current_bundle = 0
    current_direction = +1
    for v in values:
        parts[current_bundle].append(v)
        current_bundle += current_direction
        if current_bundle > c-1:
            current_bundle = c-1
            current_direction = -1
        if current_bundle < 0:
            current_bundle = 0
            current_direction = +1
    return parts





#### EXACT COMPUTATION OF THE MAXIMIN PARTITION ####


import cvxpy
from fairpy.solve import *

import logging
logger = logging.getLogger(__name__)


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


    solvers = [(cvxpy.SCIP, {}),(cvxpy.GLPK_MI, {})] 
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



def value_of_bundle(valuation:list, bundle:list):
    return sum([valuation[item] for item in bundle])


def maximin_share_partition__bruteforce(c:int, valuation:list, items:Collection[Any])->int:
    """
    Computes the 1-of-c MMS by brute force - enumerating all partitions.
    """
    best_partition_value = -1
    best_partition = None
    for partition in partitions_to_exactly_c_subsets(c, items):
        partition_value = min([value_of_bundle(valuation,bundle) for bundle in partition])
        if best_partition_value < partition_value:
            best_partition_value = partition_value
            best_partition = partition
    part_values = [value_of_bundle(valuation, part) for part in best_partition]
    return (best_partition, part_values, best_partition_value)



def maximin_share_partition(c:int, valuation:list, items:Collection[Any]=None, engine="cvxpy", **kwargs)->int:
    """	
    Compute the of 1-of-c MMS of the given items, by the given valuation.
    :return (partition, part_values, maximin-share value)

    >>> maximin_share_partition(c=1, valuation=[10,20,40,1])
    ([[0, 1, 2, 3]], [71.0], 71.0)
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1])
    ([[0, 1, 3], [2]], [31.0, 40.0], 31.0)
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1], engine="bruteforce")
    ([[2], [0, 1, 3]], [40, 31], 31)
    >>> int(maximin_share_partition(c=3, valuation=[10,20,40,1])[2])
    11
    >>> int(maximin_share_partition(c=4, valuation=[10,20,40,1])[2])
    1
    >>> int(maximin_share_partition(c=5, valuation=[10,20,40,1])[2])
    0
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1], items=[1,2])
    ([[1], [2]], [20.0, 40.0], 20.0)
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1], multiplicity=2)
    ([[0, 1, 2, 3], [0, 1, 2, 3]], [71.0, 71.0], 71.0)
    >>> maximin_share_partition(c=2, valuation=[10,20,40,1], multiplicity=[2,1,1,0])
    ([[0, 0, 1], [2]], [40.0, 40.0], 40.0)
    >>> maximin_share_partition(c=3, valuation=[10,20,40,1], numerator=2)
    ([[0, 3], [1], [2]], [11.0, 20.0, 40.0], 31.0)
    >>> maximin_share_partition(c=3, valuation=[10,20,40,1], numerator=2, fix_smallest_part_value=0)
    ([[], [0, 1, 3], [2]], [0.0, 31.0, 40.0], 31.0)
    """
    if len(valuation)==0:
        raise ValueError("Valuation is empty")
    num_of_items = len(valuation)
    if items is None:
        items = list(range(num_of_items))

    if engine=="cvxpy":
        return maximin_share_partition__cvxpy(c, valuation, items, **kwargs)
    elif engine=="bruteforce":
        return maximin_share_partition__bruteforce(c, valuation, items, **kwargs)
    else:
        raise ValueError("Unknown engine "+engine)
    




#### OTHER UTILITIES ####

def smallest_sums(partition:Partition, num_of_sums:int=1)->Number:
    """
    Given a partition, return the sum of the smallest k parts (k = num_of_sums)
    
    >>> smallest_sums([[1,2],[3,4],[5,6]])
    3
    >>> smallest_sums([[1,2],[3,4],[5,6]], num_of_sums=2)
    10
    """
    sorted_sums = sorted([sum(part) for part in partition])
    return sum(sorted_sums[:num_of_sums])




if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))

    from fairpy import solve
    import sys
    solve.logger.addHandler(logging.StreamHandler(sys.stdout))
    solve.logger.setLevel(logging.INFO)	
