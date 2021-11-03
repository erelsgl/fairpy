#!python3
"""
    ConsumptionGraph class - a bipartite graph representing what agent consumes which object.

    Programmer: Eliyahu Sattat
    Since:  2020
"""


import itertools
from fairpy import ValuationMatrix

class ConsumptionGraph():
    """
    Represents a graph of consumption of the agents.
    Represented by a binary matrix:
      graph[i][0] = 1 it means that agent i consumes a positive fraction of object o.
    """

    def __init__(self, graph):
        self.__graph = graph
        self.num_of_agents = len(graph)
        self.num_of_objects = len(graph[0])
        self.__is_prop = True
        self.__calculate_prop = False
        self.__num_of_sharing = -1

    def get_graph(self):
        return self.__graph

    def get_num_of_sharing(self) -> int:
        """
        this function return the number of
        sharing in the ConsumptionGraph
        and calculate it only one time
        >>> g = ConsumptionGraph([[1, 1, 0.0], [0.0, 1, 1], [0.0, 0.0, 0.0]])
        >>> g.get_num_of_sharing()
        1.0
        >>> g.get_num_of_sharing()
        1.0
        >>> g = ConsumptionGraph([[1, 1, 1], [0.0, 1, 1], [1, 0.0, 0.0]])
        >>> g.get_num_of_sharing()
        3.0
        >>> g = ConsumptionGraph([[0.0, 0.0, 1], [0.0, 1, 0.0], [1, 0.0, 0.0]])
        >>> g.get_num_of_sharing()
        0.0
        >>> g = ConsumptionGraph([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
        >>> g.get_num_of_sharing()
        0.0
        >>> g = ConsumptionGraph([[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]])
        >>> g.get_num_of_sharing()
        4.0
        """
        if self.__num_of_sharing == -1:
             num_of_edges = 0
             for i in range(self.num_of_agents):
                 num_of_edges += sum(self.__graph[i])
             if(num_of_edges - self.num_of_objects < 0):
                    self.__num_of_sharing =  0.0
             else:
                self.__num_of_sharing = num_of_edges - self.num_of_objects
        return self.__num_of_sharing

    def can_be_proportional(self, valuation_matrix) -> bool:
        """
        Checks if this graph can possibly correspond to a proportional allocation.
        Note: from the graph we can only know a necessary condition:
          if every agent gets all the objects he is connected to, his value should be at least 1/n.
        >>> v = [[1,3,5,2],[4,3,2,4]]
        >>> g = ConsumptionGraph([[0,0,1,1],[1,1,0,1]])
        >>> g.can_be_proportional(v)
        True
        >>> v = [[11,3],[7,7]]
        >>> g = ConsumptionGraph([[0,1],[1,0]])
        >>> g.can_be_proportional(v)
        False
        >>> v = [[11,3],[7,7]]
        >>> g = ConsumptionGraph([[1,0],[0,1]])
        >>> g.can_be_proportional(v)
        True
        >>> v = [[11,3],[7,7],[3,6]]
        >>> g = ConsumptionGraph([[0,0],[0,1],[1,1]])
        >>> g.can_be_proportional(v)
        False
        """
        if self.__calculate_prop == False:
            self.__calculate_prop == True
            flag = True
            i = 0
            while(i < self.num_of_agents) and(flag):
                if not (self.is_single_proportional(valuation_matrix, i)):
                    flag = False
                    self.__is_prop = False
                i += 1
        return self.__is_prop


    def is_single_proportional(self, valuation_matrix, x:int)->bool:
        """
        Checks if this graph can possibly correspond to a proportional allocation for a single agent x.
        for specific i and any j : ui(xi)>=1/n(xi)
        :param valuation_matrix represents the agents' valuations.
        :param x the index of agent we check
        :return: bool value if the allocation is proportional
        >>> g = ConsumptionGraph([[1,1,0,0],[1,1,0,1]])
        >>> v = [[1,3,5,2],[4,3,2,4]]
        >>> g.is_single_proportional(v,0)
        False
        >>> g.is_single_proportional(v,1)
        True
        >>> g = ConsumptionGraph([[1, 0.0, 0.0], [0.0, 1, 1], [0.0, 0.0, 0.0]])
        >>> v = [[1,3,5],[4,3,2],[4,3,2]]
        >>> g.is_single_proportional(v,0)
        False
        >>> g.is_single_proportional(v,1)
        True
        >>> g.is_single_proportional(v,2)
        False
        >>> g = ConsumptionGraph([[1, 1, 1], [0.0, 1, 1], [0.0, 0.0, 1]])
        >>> v = [[1,3,5],[4,3,2],[4,3,2]]
        >>> g.is_single_proportional(v,0)
        True
        >>> g.is_single_proportional(v,1)
        True
        >>> g.is_single_proportional(v,2)
        False
        >>> g = ConsumptionGraph([[0.0, 0.0, 1], [0.0, 1, 0.0], [0.0, 0.0, 1]])
        >>> v = [[1,3,5],[4,1,2],[4,3,2]]
        >>> g.is_single_proportional(v,0)
        True
        >>> g.is_single_proportional(v,1)
        False
        >>> g.is_single_proportional(v,2)
        False
        """
        valuation_matrix = ValuationMatrix(valuation_matrix)
        sum = 0
        part = 0
        for i in range(0, self.num_of_objects):
            sum += valuation_matrix[x][i]
            part += valuation_matrix[x][i] * self.__graph[x][i]
        sum = sum / valuation_matrix.num_of_agents
        return part >= sum

    def generate_all_codes(self):
        """
        this function generate all the codes for that graph
        (the code represent the new graph that can built from this graph and adding new agent)
        :return: generator for all the codes
        >>> a =[[1,0,1]]
        >>> g = ConsumptionGraph(a)
        >>> for x in g.generate_all_codes():
        ...     print(x)
        (0,)
        (1,)
        (2,)
        (3,)
        (4,)
    """
        agent_prop_counter = self.sum_of_agent_properties()
        for element in itertools.product(*(range(x) for x in agent_prop_counter)):
            yield element


    def sum_of_agent_properties(self):
        """
        this function return array that each arr[i] = the number
        of properties of agent i in graph multiple by 2 plus 1
        :return:  the number of properties of each agent in array
        >>> a =[[1,0,0],[1,1,1],[1,1,0]]
        >>> g = ConsumptionGraph(a)
        >>> g.sum_of_agent_properties()
        [3, 7, 5]
        >>> a =[[1,1,0],[1,1,1]]
        >>> g = ConsumptionGraph(a)
        >>> g.sum_of_agent_properties()
        [5, 7]
        >>> a =[[1,0,0],[1,1,1],[1,1,0]]
        >>> g = ConsumptionGraph(a)
        >>> g.sum_of_agent_properties()
        [3, 7, 5]
        >>> a =[[1,0,0],[0,0,1],[0,0,0]]
        >>> g = ConsumptionGraph(a)
        >>> g.sum_of_agent_properties()
        [3, 3, 1]
        >>> a =[[1,1]]
        >>> g = ConsumptionGraph(a)
        >>> g.sum_of_agent_properties()
        [5]
        """
        agent_prop_counter = [0] * self.num_of_agents
        for i in range(self.num_of_agents):
            # agent_prop_counter[i] = f(sum(graph[i]))
            for j in range(self.num_of_objects):
                if (self.__graph[i][j] == 1):
                    agent_prop_counter[i] += 1
        agent_prop_counter = [i * 2 + 1 for i in agent_prop_counter]
        return agent_prop_counter

    def __repr__(self):
        return self.__graph.__repr__()

    def __str__(self):
        return self.__graph.__str__()


if __name__ == '__main__':
    import doctest 
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

