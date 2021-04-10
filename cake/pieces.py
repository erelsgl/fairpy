#!python3

"""
A utility function to round a piece, for presentation purposes.
"""

from fairpy import Allocation


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


def merge_allocations(self:Allocation, other:Allocation):
    """
    Merges this allocation with another allocation in place.

    Programmer: Guy Wolf.

    :param self: this allocation.
    :param other: the other allocation to merge with.

    >>> from fairpy.cake.agents import PiecewiseUniformAgent
    >>> Allocation.default_separator=", "
    >>> Alice = PiecewiseUniformAgent([(2,3)], "Alice")
    >>> George = PiecewiseUniformAgent([(0,10)], "George")
    >>> A = Allocation([Alice, George], [[(1,2)],[(4,5)]])
    >>> B = Allocation([George, Alice], [[(0,1)],[(2,3)]])
    >>> merge_allocations(A, B)
    >>> print(A)
    Alice gets {(1, 2), (2, 3)} with value 1.
    George gets {(0, 1), (4, 5)} with value 2.
    <BLANKLINE>
    """
    for i in range(len(self.bundles)):
        if(self.bundles[i] == None):
            self.bundles[i] = []
        for j in range(len(other.bundles)):
            #merge the same agents.
            if(other.agents[j].name() == self.agents[i].name()):
                if(other.bundles[j] == None):
                    other.bundles[j] = []
                self.bundles[i].extend(other.bundles[j])
                self.values[i] = self.agents[i].value(self.bundles[i])



if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures,tests))
