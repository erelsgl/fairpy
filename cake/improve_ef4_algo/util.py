#!python3

from typing import List


def exclude_from_list(list: List, excluded: List) -> List:
    """
    Creates a new list, excluding specified elements from it.

    :param list: list to copy and exclude from
    :param excluded: list of elements to exclude
    :return a new list, with all elements in `list` excluding `excluded`.

    >>> l = [1, 2, 3, 4]
    >>> exclude_from_list(l, [1, 3])
    [2, 4]
    """
    return [item for item in list if item not in excluded]


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
