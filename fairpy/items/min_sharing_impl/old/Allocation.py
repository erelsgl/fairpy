#!python3

import numpy as np

class Allocation():
    """
    this class represent an allocation of objects to agents,
    represented by matrix - if graph[i][j] = x its mean that agent i
    gets x%  from object j
    0 <= graph[i][j] <= 1
    """
    def __init__(self,alloction_matrix):
        self.__alloction_matrix = alloction_matrix
        self.__is_prop = True
        self.__is_envy_free = True
    def __repr__(self):
        pass

    def num_of_sharing(self)-> int :
        """
        this function calculate the number of sharing in
        the allocation
        :return: the number of sharing
        """
        if self.__alloction_matrix is None:
            raise ValueError("No allocation!")
        num_of_edge = 0
        for i in range(len(self.__alloction_matrix)):
            for j in range(len(self.__alloction_matrix[0])):
                num_of_edge += np.ceil(self.__alloction_matrix[i][j])
        num_of_obj = len(self.__alloction_matrix[0])
        return num_of_edge - num_of_obj

    def round(self):
        """
        this function round the allocation_matrix for 3 digit after the decimal point
        """
        if self.__alloction_matrix is None:
            raise ValueError("No allocation!")
        for i in range(len(self.__alloction_matrix)):
            for j in range(len(self.__alloction_matrix[i])):
                fraction = np.round(self.__alloction_matrix[i][j], 3)
                if fraction==0:
                    fraction=0   # avoid "negative zero"
                self.__alloction_matrix[i][j] = fraction


    def get_allocation(self):
        return self.__alloction_matrix

    def is_prop(self,valuation_matrix) -> bool:
        """
        this function return if this graph is
        not proportional
        note - is this phase we can only know if from this graph
        you cant make a prop  allocation
        this function calculate like every agent gets all the objects he is connecting to.
        (and calculate it only one time)
        """
        flag = True
        i = 0
        while(i < len(self.__alloction_matrix))and(flag):
            if not (self.is_single_proportional(valuation_matrix, i)):
                flag = False
                self.__is_prop = False
            i += 1
        return self.__is_prop


    def is_single_proportional(self, matv, x):
        """
        this function check if the ConsumptionGraph is proportional
        according to single agent i
        for specific i and any j : ui(xi)>=1/n(xi)
        :param matv represent the value for the agents
        :param x the index of agent we check
        :return: bool value if the allocation is proportional
        """
        sum = 0
        part = 0
        for i in range(0, len(self.__alloction_matrix[0])):
            sum += matv[x][i]
            part += matv[x][i] * self.__alloction_matrix[x][i]
        sum = sum / len(self.__alloction_matrix)
        return part >= sum



    def is_envy_free(self,valuation_matrix) -> bool:
        """
        this function return if this graph is
        not proportional
        note - is this phase we can only know if from this graph
        you cant make a prop  allocation
        this function calculate like every agent gets all the objects he is connecting to.
        (and calculate it only one time)
        """
        flag = True
        i = 0
        while(i < len(self.__alloction_matrix))and(flag):
            if not (self.is_single_envy_free(valuation_matrix, i)):
                flag = False
                self.__is_envy_free = False
            i += 1
        return self.__is_envy_free


    def is_single_envy_free(self, matv, x):
        """
        this function check if the ConsumptionGraph is proportional
        according to single agent i
        for specific i and any j : ui(xi)>=1/n(xi)
        :param matv represent the value for the agents
        :param x the index of agent we check
        :return: bool value if the allocation is proportional
        """
        sum = 0
        part = 0
        other_part = 0
        for i in range(0, len(self.__alloction_matrix[0])):
            part += matv[x][i] * self.__alloction_matrix[x][i]
        for i in range(0, len(self.__alloction_matrix)):
            other_part = 0
            for j in range(0 , len(self.__alloction_matrix[0])):
                other_part += matv[x][j]*self.__alloction_matrix[i][j]
            if(part < other_part):
                self.__is_envy_free = False
                return False
        return True



if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
