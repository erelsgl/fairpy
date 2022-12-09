#!python3
"""
    Some tests for the min-sharing algorithm.

    Programmer: Eliyahu Sattat
    Since:  2020
"""

import doctest as doctest
from fairpy.items.min_sharing_impl.ConsumptionGraph import ConsumptionGraph



def is_prop(g ,valuation_matrix) -> bool:
    """
    this function return if this graph is
    not proportional
    note - is this phase we can only know if from this graph
    you cant make a prop  allocation
    this function calculate like every agent gets all the objects he is connecting to.
    (and calculate it only one time)
    >>> v = [[1,3,5,2],[4,3,2,4]]
    >>> g = [[0,0,1,1],[1,1,0,1]]
    >>> is_prop(g,v)
    True
    >>> v = [[11,3],[7,7]]
    >>> g = [[0,1],[1,0]]
    >>> is_prop(g,v)
    False
    >>> v = [[11,3],[7,7]]
    >>> g = [[1,0],[0,1]]
    >>> is_prop(g,v)
    True
    >>> v = [[11,3],[7,7],[3,6]]
    >>> g = [[0,0],[0,1],[1,1]]
    >>> is_prop(g,v)
    False
    >>> v =  [[150., 150. ,150. ,150., 150. ,250.],[150., 150. ,150. ,150., 150. ,250.],[150., 150. ,150. ,150., 150. ,250.]]
    >>> g = [[1. ,  1.  ,  0.222, 0.  ,  0. ,   0.   ], [0.,    0. ,   0.  ,  0.444 ,0.999 ,0.466], [0. ,   0. ,   0.777 ,0.555 ,0. ,   0.533]]
    >>> is_prop(g,v)
    False
    >>> v = [[300.0, 300.0, 400.0], [307.0, 308.0, 385.0], [312.0, 313.0, 375.0]]
    >>> g = [[0.  ,  0.  ,  0.837],[0.  ,  0.898 ,0.162],[0.999, 0.101 ,0.   ]]
    >>> is_prop(g,v)
    True
    """
    flag = True
    i = 0
    while(i < len(g) )and(flag):
        if not (is_single_proportional(g,valuation_matrix, i)):
            flag = False
        i += 1
    return flag


def is_single_proportional(g,matv, x):
    """
    this function check if the ConsumptionGraph is proportional
    according to single agent i
    for specific i and any j : ui(xi)>=1/n(xi)
    :param matv represent the value for the agents
    :param x the index of agent we check
    :return: bool value if the allocation is proportional
    >>> v =  [[150., 150. ,150. ,150., 150. ,250.],[150., 150. ,150. ,150., 150. ,250.],[150., 150. ,150. ,150., 150. ,250.]]
    >>> g = [[1. ,  1.  ,  0.222, 0.  ,  0. ,   0.   ], [0.,    0. ,   0.  ,  0.444 ,0.999 ,0.466], [0. ,   0. ,   0.777 ,0.555 ,0. ,   0.533]]
    >>> is_single_proportional(g,v,0)
    False
    >>> is_single_proportional(g,v,1)
    False
    >>> is_single_proportional(g,v,2)
    False
    >>> g = [[1,1,0,0],[1,1,0,1]]
    >>> v = [[1,3,5,2],[4,3,2,4]]
    >>> is_single_proportional(g,v,0)
    False
    >>> is_single_proportional(g,v,1)
    True
    >>> g = [[1, 0.0, 0.0], [0.0, 1, 1], [0.0, 0.0, 0.0]]
    >>> v = [[1,3,5],[4,3,2],[4,3,2]]
    >>> is_single_proportional(g,v,0)
    False
    >>> is_single_proportional(g,v,1)
    True
    >>> is_single_proportional(g,v,2)
    False
    >>> g = [[1, 1, 1], [0.0, 1, 1], [0.0, 0.0, 1]]
    >>> v = [[1,3,5],[4,3,2],[4,3,2]]
    >>> is_single_proportional(g,v,0)
    True
    >>> is_single_proportional(g,v,1)
    True
    >>> is_single_proportional(g,v,2)
    False
    >>> g = [[0.0, 0.0, 1], [0.0, 1, 0.0], [0.0, 0.0, 1]]
    >>> v = [[1,3,5],[4,1,2],[4,3,2]]
    >>> is_single_proportional(g,v,0)
    True
    >>> is_single_proportional(g,v,1)
    False
    >>> is_single_proportional(g,v,2)
    False
    """
    sum = 0
    part = 0
    for i in range(0, len(g[0])):
        sum += matv[x][i]
        part += matv[x][i] * g[x][i]
    sum = sum / len(g)
    #print("sum= {}".format(sum))
    #print("part= {}".format(part))
    return part >= sum



if __name__ == '__main__':
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

