#!python3

"""
A utility function to round a piece, for presentation purposes.
"""

from fairpy import Allocation, Bundle


def round_bundle(bundle:list, digits:int=3):
    """
    Round the numbers in the given piece. For presentation purposes.
    :param piece:   A list of intervals.
    :param digits:  How many digits after the decimal point.

    >>> round_bundle([(0.1999999, 0.300001), (0.40000001, 0.599999)], 3)
    [(0.2, 0.3), (0.4, 0.6)]
    """
    return [(round(interval[0],digits),round(interval[1],digits)) for interval in bundle]

def round_allocation(allocation:Allocation, digits:int=3)->Allocation:
    """
    Rounds all the pieces in the given allocaton. 
    For presentation purposes.
    """
    rounded_bundles = [round_bundle(bundle,digits) for bundle in allocation.bundles]
    return Allocation(allocation.agents, rounded_bundles)



if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures,tests))
