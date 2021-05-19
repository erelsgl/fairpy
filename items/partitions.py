#!python3

"""
Utilities for generating partitions of a given subset.

Programmer: Erel Segal-Halevi
Since: 2019-07
"""

import itertools
from typing import List

def partitions(collection:set):
    """
    Generates all partitions of the given set.
    Based on code by alexis, https://stackoverflow.com/a/30134039/827927

    >>> list(partitions([1,2,3]))
    [[[1, 2, 3]], [[1], [2, 3]], [[1, 2], [3]], [[2], [1, 3]], [[1], [2], [3]]]
    """
    if len(collection) == 1:
        yield [ collection ]
        return
    first = collection[0]
    for smaller in partitions(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset
        yield [ [ first ] ] + smaller


def partitions_to_at_most_c(collection:list, c:int):
    """
    Generates all partitions of the given set whose size is at most c subsets.

    >>> list(partitions_to_at_most_c([1,2,3], 2))
    [[[1, 2, 3]], [[1], [2, 3]], [[1, 2], [3]], [[2], [1, 3]]]
    """
    if len(collection) == 1:
        yield [ collection ]
        return
    first = collection[0]
    for smaller in partitions(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset
        if len(smaller)<c:
            yield [ [ first ] ] + smaller


def partitions_to_exactly_c(collection: list, c: int):
    """
    Generates all partitions of the given set whose size is exactly c subsets.
    NOTE: This is very inefficient - better to use powerset.

    >>> list(partitions_to_exactly_c([1,2,3], 2))
    [[[1], [2, 3]], [[1, 2], [3]], [[2], [1, 3]]]
    >>> list(partitions_to_exactly_c([1,2], 3))
    []
    """
    for p in partitions_to_at_most_c(collection, c):
        if len(p)==c:
            yield p

def powerset(iterable):
    """
    Returns all subsets of the given iterable.
    Based on code from https://docs.python.org/3.7/library/itertools.html .

    >>> list(powerset([1,2,3]))
    [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    """
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


def bidirectional_balanced_partition(num_of_parts:int, item_sizes:List[int])->List[List[int]]:
    """
    Partition the numbers using "bidirectional balanced partition" (ABCCBA order)
    >>> bidirectional_balanced_partition(2, [1,2,3,4,5,6])
    [[6, 3, 2], [5, 4, 1]]
    >>> bidirectional_balanced_partition(3, [1,2,3,4,5,6])
    [[6, 1], [5, 2], [4, 3]]
    """
    values = sorted(item_sizes, reverse=True)
    parts = [ [] for i in range(num_of_parts) ]
    current_bundle = 0
    current_direction = +1
    for v in values:
        parts[current_bundle].append(v)
        current_bundle += current_direction
        if current_bundle > num_of_parts-1:
            current_bundle = num_of_parts-1
            current_direction = -1
        if current_bundle < 0:
            current_bundle = 0
            current_direction = +1
    return parts


def greedy_partition(num_of_parts:int, item_sizes:List[int])->List[List[int]]:
    """
    Partition the numbers using the greedy algorithm: https://en.wikipedia.org/wiki/Greedy_number_partitioning
    >>> greedy_partition(2, [1,2,3,4,5,6])
    [[6, 3, 2], [5, 4, 1]]
    >>> greedy_partition(3, [1,2,3,4,5,6])
    [[6, 1], [5, 2], [4, 3]]
    """
    values = sorted(item_sizes, reverse=True)
    parts = [ [] for i in range(num_of_parts) ]
    sums  = [ 0 for i in range(num_of_parts)  ]
    for v in values:
        index_of_part_with_smallest_sum = min(range(num_of_parts), key=lambda i:sums[i])
        parts[index_of_part_with_smallest_sum].append(v)
        sums [index_of_part_with_smallest_sum] += v
    return parts


def smallest_sums(parts:list, num_of_sums:int=1):
    """
    Given a partition, return the sum of the smallest k parts (k = num_of_sums)
    
    >>> smallest_sums([[1,2],[3,4],[5,6]])
    3
    >>> smallest_sums([[1,2],[3,4],[5,6]], num_of_sums=2)
    10
    """
    sorted_sums = sorted([sum(part) for part in parts])
    return sum(sorted_sums[:num_of_sums])




if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
