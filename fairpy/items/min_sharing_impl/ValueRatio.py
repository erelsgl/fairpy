#!python3
"""
    A class for computing and caching the value-ratios of different agents.

    Programmer: Eliyahu Sattat
    Since:  2020
"""

import numpy as np
from fairpy.items.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy import ValuationMatrix



class ValueRatio():
    """
    this class represent all the ratio between the agents
    """


    def __init__(self, valuation_matrix):
        valuation_matrix = ValuationMatrix(valuation_matrix)
        self.valuation_matrix = valuation_matrix
        self.all_ratios = compute_all_ratios(valuation_matrix)

    def create_the_value_ratio_for_2(self, consumption_graph:ConsumptionGraph, x:int, y:int):
        """
        Build the array for value ratio between two agents:  x and y.
        according to the given graph and the properties of agent x in this graph
        and sort it.
        :param consumption_graph: the current graph we are working on.
        :param x: the index of the first agent.
        :param y: the index of the second agent.
        :return: the sorted array of tuples (index of location in v, the ratio)

        >>> a = [[20,30,40,10],[10,60,10,20]]
        >>> v = ValueRatio(a)
        >>> g1 = [[1,1,1,1]]
        >>> g = ConsumptionGraph(g1)
        >>> v.create_the_value_ratio_for_2(g,0,1)
        [(2, 4.0), (0, 2.0), (1, 0.5), (3, 0.5)]
        >>> a = [[20,30,40,20],[10,60,10,20]]
        >>> v = ValueRatio(a)
        >>> g1 = [[0.0,1,0.0,1]]
        >>> g = ConsumptionGraph(g1)
        >>> v.create_the_value_ratio_for_2(g,0,1)
        [(3, 1.0), (1, 0.5)]
        >>> a = [[40,30,20],[40,30,20],[10,10,10]]
        >>> v = ValueRatio(a)
        >>> g1 = [[1,1,0],[0,1,1]]
        >>> g = ConsumptionGraph(g1)
        >>> v.create_the_value_ratio_for_2(g,1,2)
        [(1, 3.0), (2, 2.0)]
        >>> a = [[40,30,20],[40,10,20],[10,10,10]]
        >>> v = ValueRatio(a)
        >>> g1 = [[1,1,0],[0,1,1]]
        >>> g = ConsumptionGraph(g1)
        >>> v.create_the_value_ratio_for_2(g,1,2)
        [(2, 2.0), (1, 1.0)]
        >>> a = [[40,30,20],[40,30,20],[10,10,10],[5,2,1]]
        >>> v = ValueRatio(a)
        >>> g1 = [[1,0,1],[0,1,1]]
        >>> g = ConsumptionGraph(g1)
        >>> v.create_the_value_ratio_for_2(g,0,3)
        [(2, 20.0), (0, 8.0)]
        >>> a = [[40,30,20],[40,30,20],[10,10,10],[0,2,1]]
        >>> v = ValueRatio(a)
        >>> g1 = [[1,0,1],[0,1,1]]
        >>> g = ConsumptionGraph(g1)
        >>> v.create_the_value_ratio_for_2(g,0,3)
        [(0, inf), (2, 20.0)]
        >>> a = [[40,30,20],[40,30,20],[10,10,10],[0,2,1]]
        >>> v = ValueRatio(a)
        >>> g1 = [[1,0,1],[0,1,1]]
        >>> g = ConsumptionGraph(g1)
        >>> v.create_the_value_ratio_for_2(g,0,1)
        [(0, 1.0), (2, 1.0)]
        """
        graph = consumption_graph.get_graph()
        ratios_for_x_and_y = self.all_ratios[x][y]
        ans = []
        for o in self.valuation_matrix.objects():
            if(graph[x][o]==1):
                ans.append(ratios_for_x_and_y[o])
        ans.sort(key=second, reverse=True)  # sort from large to small ratio
        return ans

def second(pair):
    return pair[1]



def compute_all_ratios(valuation_matrix)->list:
    """
    Creates a list of matrices.
    Each matrix is the ratio between agent i and all the other agents.
    For example:   
       ans[3] = matrix of the ratio between agent #3 and all ether agents.
       So ans[3][4] = the ratio array between agent 3 to agent 4.
    :param valuation_matrix: the valuation of the agents.
    :return: ans - list of all the matrices.
    >>> v = [[1,2],[3,4]]
    >>> compute_all_ratios(v)
    [[[(0, 1.0), (1, 1.0)], [(0, 0.3333333333333333), (1, 0.5)]], [[(0, 3.0), (1, 2.0)], [(0, 1.0), (1, 1.0)]]]
    >>> v = [[1,0],[3,7]]
    >>> compute_all_ratios(v)
    [[[(0, 1.0), (1, 1.0)], [(0, 0.3333333333333333), (1, 0.0)]], [[(0, 3.0), (1, inf)], [(0, 1.0), (1, 1.0)]]]
    >>> v = [[1,0,2],[3,7,2.5],[4,2,0]]
    >>> compute_all_ratios(v)
    [[[(0, 1.0), (1, 1.0), (2, 1.0)], [(0, 0.3333333333333333), (1, 0.0), (2, 0.8)], [(0, 0.25), (1, 0.0), (2, inf)]], [[(0, 3.0), (1, inf), (2, 1.25)], [(0, 1.0), (1, 1.0), (2, 1.0)], [(0, 0.75), (1, 3.5), (2, inf)]], [[(0, 4.0), (1, inf), (2, 0.0)], [(0, 1.3333333333333333), (1, 0.2857142857142857), (2, 0.0)], [(0, 1.0), (1, 1.0), (2, 1.0)]]]
    """
    valuation_matrix = ValuationMatrix(valuation_matrix)
    ans = []
    for i in valuation_matrix.agents():
        mat = np.zeros((valuation_matrix.num_of_agents, valuation_matrix.num_of_objects)).tolist()
        for j in valuation_matrix.agents():
            for k in valuation_matrix.objects():
                if (valuation_matrix[i][k]==0) and (valuation_matrix[j][k]==0):
                    temp = 1.0
                else:
                    if(valuation_matrix[j][k]==0):
                        temp = np.inf
                    else:
                        temp = valuation_matrix[i][k] / valuation_matrix[j][k]
                mat[j][k] = (k,temp)
        ans.append(mat)
    return ans


if __name__ == '__main__':
    import doctest as doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
