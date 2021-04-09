#!python3

"""
A utility function to round a piece, for presentation purposes.
"""

from fairpy.allocations import Allocation


def round_piece(piece:list, digits:int=3):
    """
    Round the numbers in the given piece. For presentation purposes.
    :param piece:   A list of intervals.
    :param digits:  How many digits after the decimal point.

    >>> round_piece([(0.1999999, 0.300001), (0.40000001, 0.599999)], 3)
    [(0.2, 0.3), (0.4, 0.6)]
    """
    return [(round(interval[0],digits),round(interval[1],digits)) for interval in piece]

def round_allocation(allocation:Allocation, digits:int=3)->Allocation:
    """
    Rounds all the pieces in the given allocaton. 
    For presentation purposes.
    """
    allocation.bundles = [round_piece(piece,digits) for piece in allocation.bundles]
    return allocation


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures,tests))
