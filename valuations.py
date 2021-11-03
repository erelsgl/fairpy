#!python3

"""
A valuation matrix is a matrix v in which each row represents an agent, 
   each column represents an object, and v[i][j] is the value of agent i to object j.
It is used as an input to algorithms of fair division with additive valuations,
   both of divisible and of indivisible goods.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import numpy as np
from typing import *
from fairpy.bundles import *

class ValuationMatrix:
    """
    A valuation matrix is a matrix v in which each row represents an agent, 
        each column represents an object, and v[i][j] is the value of agent i to object j.
    
    It can be initialized by:

    * A 2-dimensional numpy array (np.ndarray);
    * A list of lists;
    * Another ValuationMatrix.

    >>> v = ValuationMatrix([[1,4,7],[6,3,0]])    # Initialize from a list of lists
    >>> v[0,1]   # value for agent 0 of item 1
    4
    >>> v[0][1]  # value for agent 0 of item 1
    4
    >>> v[0]     # values for agent 0
    array([1, 4, 7])
    >>> v
    [[1 4 7]
     [6 3 0]]
    >>> for agent in v.agents(): print(v[agent])
    [1 4 7]
    [6 3 0]
    >>> v.agent_value_for_bundle(0, [0,2])
    8
    >>> v.agent_value_for_bundle(0, FractionalBundle([1,0,1]))  # equivalent to the above
    8
    >>> v.agent_value_for_bundle(0, FractionalBundle([0.5,0,1.5]))
    11.0
    >>> v.agent_value_for_bundle(1, [1,0])
    9
    >>> v.agent_value_for_bundle(1, None)
    0
    >>> v.without_agent(0)
    [[6 3 0]]
    >>> v.without_object(1)
    [[1 7]
     [6 0]]
    >>> v = ValuationMatrix(np.ones([2,3]))        # Initialize from a numpy array.
    >>> v
    [[1. 1. 1.]
     [1. 1. 1.]]
    >>> int(v.agent_value_for_bundle(0,[1,2]))
    2
    >>> v2 = ValuationMatrix(v)
    >>> v2
    [[1. 1. 1.]
     [1. 1. 1.]]
    """

    def __init__(self, valuation_matrix: np.ndarray):
        if isinstance(valuation_matrix, list):
            valuation_matrix = np.array(valuation_matrix)
        elif isinstance(valuation_matrix, ValuationMatrix):
            valuation_matrix = valuation_matrix._v

        self._v = valuation_matrix
        self.num_of_agents = len(valuation_matrix)
        self.num_of_objects = 0 if self.num_of_agents == 0 else len(valuation_matrix[0])

    def agents(self):
        return range(self.num_of_agents)

    def objects(self):
        return range(self.num_of_objects)

    def __getitem__(self, key):
        if isinstance(key,tuple):
            return self._v[key[0]][key[1]]  # agent's value for a single object
        else:
            return self._v[key]             # agent's values for all objects

    def agent_value_for_bundle(self, agent:int, bundle:Bundle)->float:
        if bundle is None:
            return 0
        elif isinstance(bundle,FractionalBundle):
            return sum([self._v[agent][object] * fraction for object,fraction in enumerate(bundle.fractions)])
        else:
            return sum([self._v[agent][object] for object in bundle])


    def without_agent(self, agent:int)->'ValuationMatrix':
        """
        :return a copy of this valuation matrix, in which the given agent is removed.
        """
        if isinstance(agent,int):
            return ValuationMatrix(np.delete(self._v, agent, axis=0))
        else:
            raise IndexError(f"agent index should be an integer, but it is {agent}")
            

    def without_object(self, object:int)->'ValuationMatrix':
        """
        :return a copy of this valuation matrix, in which the given object is removed.
        """
        if isinstance(object,int):
            return ValuationMatrix(np.delete(self._v, object, axis=1))
        else:
            raise IndexError(f"object index should be an integer, but it is {object}")

    def submatrix(self, agents: List[int], objects: List[int]):
        """
        :return a submatrix of this valuation matrix, containing only specified agents and objects.
        """
        return ValuationMatrix(self._v[np.ix_(agents, objects)])

    def verify_ordered(self)->bool:
        """
        Verifies that the instance is ordered --- all valuations are ordered by descending value.

        >>> v = ValuationMatrix([[7,4,1],[6,3,0]])
        >>> v.verify_ordered()
        >>> v = ValuationMatrix([[7,4,1],[6,0,3]])
        >>> v.verify_ordered()
        Traceback (most recent call last):
        ...
        ValueError: Valuations of agent 1 are not ordered: [6 0 3]
        """
        for i in self.agents():
            v_i = self._v[i]
            if any(v_i[j] < v_i[j+1] for j in range(self.num_of_objects-1)):
                raise ValueError(f"Valuations of agent {i} are not ordered: {v_i}")

    def total_values(self) -> np.ndarray:
        """
        Return a 1-dimensional array in which elemenet i is the total value of agent i for all items.
        """
        return np.sum(self._v, axis=1, keepdims=True)

    def normalize(self) -> int:
        """
        Normalize valuation matrix so that each agent has equal total value of all items.
        In case of integer values they remain integer to avoid floating point mistakes.

        :return the common value after normalization.
        """
        total_values = self.total_values()

        if issubclass(self._v.dtype.type, np.integer):
            total_value = np.lcm.reduce(total_values)
            self._v *= total_value // total_values
            return total_value

        self._v /= total_values
        return 1

    def verify_normalized(self) -> int:
        """
        Check if total value of each agent is the same. Return total value.
        """
        total_values = np.sum(self._v, axis=1)
        if not np.all(total_values == total_values[0]):
            raise ValueError("Valuation matrix is not normalized")
        return total_values[0]

    def equals(self, other)->bool:
        return np.array_equal(self._v, other._v)

    def __repr__(self):
        return np.array2string (self._v, max_line_width=100)		




if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

