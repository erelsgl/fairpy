#!python3

"""
Classes for representing a Bundle (a set of objects given to an agent) and an Allocation (a matching of bundles to agents).

An Allocation is the output of a fair allocation algorithm.

The objects are used mainly for display purposes.

Programmer: Erel Segal-Halevi
Since: 2021-04
"""

from typing import List, Any, Dict
import numpy as np
from collections import defaultdict
from collections.abc import Iterable
import fairpy
from fairpy import ValuationMatrix
from fairpy.bundles import *


DEFAULT_PRECISION = 3     # number of significant digits in printing
DEFAULT_SEPARATOR = ","   # separator between items in printing




class AllocationMatrix:
    """
    A matrix z in which each row represents an agent, each column represents an object, and z[i][j] is the fraction given to agent i from object j.

    >>> z = AllocationMatrix([[.2,.3,.5],[.8,.7,.5]])
    >>> z[0,1]
    0.3
    >>> z[0]
    array([0.2, 0.3, 0.5])
    >>> z
    [[0.2 0.3 0.5]
     [0.8 0.7 0.5]]
    """

    def __init__(self, allocation_matrix:np.ndarray):
        if isinstance(allocation_matrix,list):
            allocation_matrix = np.array(allocation_matrix)
        elif isinstance(allocation_matrix,AllocationMatrix):
            allocation_matrix = allocation_matrix._z
        self._z = allocation_matrix
        self.num_of_agents = len(allocation_matrix)
        self.num_of_objects = len(allocation_matrix[0])

    def agents(self):
        return range(self.num_of_agents)

    def objects(self):
        return range(self.num_of_objects)

    def num_of_sharings(self):
        """
        Return the number of sharings in this allocation.
        >>> AllocationMatrix([ [1, 1, 0, 0] , [0, 0, 1, 0] , [0, 0, 0, 1] ]).num_of_sharings()   # No sharing
        0
        >>> AllocationMatrix([ [1, 0.5, 0, 0] , [0, 0.5, 1, 0] , [0, 0, 0, 1] ]).num_of_sharings()   # One sharing
        1
        >>> AllocationMatrix([ [1, 0.4, 0, 0] , [0, 0.4, 1, 0] , [0, 0.2, 0, 1] ]).num_of_sharings()   # Two sharings in same object
        2
        >>> AllocationMatrix([ [1, 0.4, 0, 0] , [0, 0.6, 0.3, 0] , [0, 0, 0.7, 1] ]).num_of_sharings()   # Two sharings in different objects
        2
        """
        num_of_edges = 0
        for i in self.agents():
            for o in self.objects():
                num_of_edges += np.ceil(self._z[i][o])
        return int(num_of_edges - self.num_of_objects)

    def round(self, num_digits:int):
        """
        Rounds the allocation to the given number of digits.
        WARNING: The rounding might change the sum of rows and columns.
        See here http://people.mpi-inf.mpg.de/~doerr/papers/unbimatround.pdf 
        for an unbiased matrix rounding algorithm
        """
        for i in range(len(self._z)):
            for j in range(len(self._z[i])):
                fraction = np.round(self._z[i][j], num_digits)
                if fraction==0:
                    fraction=0   # avoid "negative zero"
                self._z[i][j] = fraction
        return self

    def __getitem__(self, key):
        if isinstance(key,tuple):
            return self._z[key[0]][key[1]]  # 'key' (agent index, item index); return this agent's valuation for that item.
        else:
            return self._z[key]  # 'key' is the index of an agent; return this agent's valuation.

    def __repr__(self):
        return np.array2string (self._z, max_line_width=100)		






class Allocation:
    """
    Represents an allocation of objects (divisible or indivisible) to agents. 
    This is the output of a fair allocation algorithm.
    It is an immutable object. It is used mainly to display the allocation in a nice way.

    >>> agent_dict = {"Alice":{"x":1,"y":2,"z":3},"George":{"x":4,"y":5,"z":6}}

    ### A dict of agents and a dict of bundles:
    >>> a = Allocation(agents=agent_dict, bundles =  {"Alice":{"x","z"}, "George":{"y"}})
    >>> a
    Alice gets {x,z} with value 4.
    George gets {y} with value 5.
    <BLANKLINE>
    >>> a.map_item_to_agents()
    {'x': ['Alice'], 'z': ['Alice'], 'y': ['George']}

    ### A dict of agents and a partial dict of bundles:
    >>> a = Allocation(agents=agent_dict, bundles =  {"Alice":{"x","z"}})
    >>> a
    Alice gets {x,z} with value 4.
    George gets {} with value 0.
    <BLANKLINE>
    >>> a.map_item_to_agents()
    {'x': ['Alice'], 'z': ['Alice']}

    ### A list of agents and a dict of bundles (Note there is no value information here):
    >>> a = Allocation(agents=["Alice","George"], bundles =  {"Alice":["x","z"], "George":["x", "y"]})
    >>> a
    Alice gets {x,z} with value nan.
    George gets {x,y} with value nan.
    <BLANKLINE>
    >>> a.map_item_to_agents()
    {'x': ['Alice', 'George'], 'z': ['Alice'], 'y': ['George']}
    >>> a.map_item_to_agents(sortkey=lambda name: -a.map_agent_index_to_name.index(name))
    {'x': ['George', 'Alice'], 'z': ['Alice'], 'y': ['George']}
    >>> a.map_agent_to_bundle()
    {'Alice': ['x', 'z'], 'George': ['x', 'y']}

    ### A valuation list-of-lists and a list of bundles:
    >>> a = Allocation(agents=[[10,20,30,40,50],[999,999,999,999,999],[50,40,30,20,10]], bundles=[[0,4],None,[1,2]])
    >>> a
    Agent #0 gets {0,4} with value 60.
    Agent #1 gets {} with value 0.
    Agent #2 gets {1,2} with value 70.
    <BLANKLINE>
    >>> for bundle in a: print(bundle.items)
    [0, 4]
    []
    [1, 2]

    ### A valuation matrix and an allocation matrix:
    >>> a = Allocation(agents=ValuationMatrix([[10,20,30,40,50],[999,999,999,999,999],[50,40,30,20,10]]), bundles=AllocationMatrix([[1,0,0,0,1],[0,0,0,0,0],[0,1,1,0,0]]))
    >>> a
    Agent #0 gets { 100% of 0, 100% of 4} with value 60.
    Agent #1 gets {} with value 0.
    Agent #2 gets { 100% of 1, 100% of 2} with value 70.
    <BLANKLINE>
    >>> for bundle in a: print(bundle)
    { 100% of 0, 100% of 4}
    {}
    { 100% of 1, 100% of 2}
    >>> a = Allocation(agents=ValuationMatrix([[10,20,30,40,50],[999,999,999,999,999],[50,40,30,20,10]]), bundles=AllocationMatrix([[1/3,0,0,0,1],[2/3,0,0,0,0],[0,1,1,0,0]]))
    >>> a
    Agent #0 gets { 33.333% of 0, 100.0% of 4} with value 53.3.
    Agent #1 gets { 66.667% of 0} with value 666.
    Agent #2 gets { 100.0% of 1, 100.0% of 2} with value 70.
    <BLANKLINE>
    >>> a.round(2)
    Agent #0 gets { 33.0% of 0, 100.0% of 4} with value 53.3.
    Agent #1 gets { 67.0% of 0} with value 669.
    Agent #2 gets { 100.0% of 1, 100.0% of 2} with value 70.
    <BLANKLINE>
    >>> a.matrix
    [[0.33 0.   0.   0.   1.  ]
     [0.67 0.   0.   0.   0.  ]
     [0.   1.   1.   0.   0.  ]]

    ### A valuation matrix and a numpy array as allocation matrix
    >>> Allocation(agents=ValuationMatrix([[10,20,30,40,50],[999,999,999,999,999],[50,40,30,20,10]]), bundles=np.array([[1/3,0,0,0,1],[2/3,0,0,0,0],[0,1,1,0,0]]))
    Agent #0 gets { 33.333% of 0, 100.0% of 4} with value 53.3.
    Agent #1 gets { 66.667% of 0} with value 666.
    Agent #2 gets { 100.0% of 1, 100.0% of 2} with value 70.
    <BLANKLINE>

    ### A dict of agents and a dict of bundles, but in non-alphabetic order.
    >>> agents = {"b": [1,2], "a": [11,22]}
    >>> bundles = {"b": [0], "a":[1]}
    >>> Allocation(agents, bundles)
    b gets {0} with value 1.
    a gets {1} with value 22.
    <BLANKLINE>
    """
    def __init__(self, agents: List[Any], bundles: List[List[Any]], matrix=None):
        """
        Initializes an allocation to the given agents, of the given bundles, with the given values.

        :param agents: Mandatory. Possible types:
          * A list of names (ints/strings).
          * A list of Agent objects, which must have a name() and a value() methods.
          * A dict from agent name to agent valuation (e.g. representing additive valuation).

        :param bundles: Mandatory. For each agent, there must be a bundle (a list of items), or None. Possible types:
          * A list of bundles.
          * A dict from agent names to bundles.
        `bundles` must be the same types as `agents`: either both are lists or both are dicts.
        """
        if isinstance(agents,dict) and not isinstance(bundles,dict):
            raise ValueError(f"Cannot match agents to bundles: agents is a dict but bundles is {type(bundles)}")

        if isinstance(agents,dict) or (isinstance(agents,list) and isinstance(agents[0],list)):       # If "agents" is a dict mapping an agent name to its valuation...
            agents = fairpy.agents_from(agents)  # ... convert it to a list mapping an agent index to its valuation.

        map_agent_index_to_name = self.map_agent_index_to_name = fairpy.agent_names_from(agents)

        if isinstance(bundles,dict):       # If "bundles" is a dict mapping an agent name to its bundle... 
            bundles = [bundles.get(name,None) for name in map_agent_index_to_name]  # ... convert it to a list mapping an agent index to its bundle.

        if isinstance(bundles, np.ndarray):
            bundles = AllocationMatrix(bundles)
        if isinstance(bundles, AllocationMatrix):
            self.matrix = bundles
            bundles = [FractionalBundle(bundles[i]) for i in bundles.agents()]
        else:
            bundles = [bundle_from(bundles[i]) for i in range(len(bundles))]
        if matrix is not None:
            self.matrix = AllocationMatrix(matrix)

        # Compute num_of_agents:
        num_of_agents = agents.num_of_agents if hasattr(agents,'num_of_agents') else len(agents)
        num_of_bundles = len(bundles)
        if num_of_agents!=num_of_bundles:
            raise ValueError(f"Numbers of agents and bundles must be identical, but they are not: {num_of_agents}, {num_of_bundles}")

        # Verify that all bundles are iterable:
        for i_bundle,bundle in enumerate(bundles):
            if bundle is not None and not isinstance(bundle, Iterable):
                raise ValueError(f"Bundle {i_bundle} should be iterable, but it is {type(bundle)}")

        # Initialize bundles and agents:
        self.num_of_agents = num_of_agents
        self.num_of_bundles = num_of_bundles
        self.agents = agents
        self.bundles = bundles
        self.agent_bundle_value_matrix = compute_agent_bundle_value_matrix(agents, bundles, num_of_agents, num_of_bundles)


    def get_bundles(self):
        """
        Return a mapping from each agent's name to the bundle he/she received.
        """
        return self.bundles


    def map_agent_to_bundle(self):
        """
        Return a mapping from each agent's name to the bundle he/she received.
        """
        return {
            self.map_agent_index_to_name[i_agent]: self.bundles[i_agent].items
            for i_agent in range(self.num_of_agents)
        }

    def map_item_to_agents(self, sortkey=None)->Dict[str,Any]:
        """
        Return a mapping from each item to the agent/s who receive this item (may be more than one if there are multiple copies)
        """
        result = defaultdict(list)
        for i_agent, bundle in enumerate(self.bundles):
            if bundle is None:
                continue
            for item in bundle:
                result[item].append(self.map_agent_index_to_name[i_agent])
        if sortkey is not None:
            for item,winners in result.items():
                winners.sort(key=sortkey)
        return dict(result)

    def round(self, num_digits:int):
        if hasattr(self,'matrix'):
            self.matrix.round(num_digits)
        if isinstance(self.bundles[0],FractionalBundle):
            for bundle in self.bundles:
                bundle.round(num_digits)
        self.agent_bundle_value_matrix = compute_agent_bundle_value_matrix(self.agents, self.bundles, self.num_of_agents, self.num_of_bundles)
        return self

    def num_of_sharings(self)->int:
        return self.matrix.num_of_sharings()

    def __getitem__(self, agent_index:int):
        return self.bundles[agent_index]

    def __iter__(self):
       return self.bundles.__iter__() 

    def utility_profile(self)->list:
        """
        Returns a vector that maps each agent index to its utility (=sum of values) under this allocation.
        >>> v = ValuationMatrix([[0.5,1,0],[0.5,0,1]])
        >>> z = AllocationMatrix([[.2,.3,.5],[.8,.7,.5]])
        >>> Allocation(v,z).utility_profile()
        array([0.4, 0.9])
        """
        return np.array([self.agent_bundle_value_matrix[i_agent,i_agent] for i_agent in range(self.num_of_agents)])

    def utility_profile_matrix(self)->list:
        """
        Returns a vector that maps each agent index to its utility (=sum of values) under this allocation.
        >>> v = ValuationMatrix([[0.5,1,0],[0.5,0,1]])
        >>> z = AllocationMatrix([[.2,.3,.5],[.8,.7,.5]])
        >>> Allocation(v,z).utility_profile_matrix()
        array([[0.4, 1.1],
               [0.6, 0.9]])
        """
        return self.agent_bundle_value_matrix


    def str_with_values(self, precision=None)->str:
        """
        Returns a representation of the current allocation, showing the value of each agent to his own bundle.
        
        >>> agents = {"Alice":{"x":1.000000001,"y":2,"z":3},"George":{"x":4,"y":5,"z":6}}
        >>> a = Allocation(agents=agents, bundles = {"Alice": {"x","z"}, "George": {"y"}})
        >>> print(a.str_with_values())
        Alice gets {x,z} with value 4.
        George gets {y} with value 5.
        <BLANKLINE>
        >>> print(a.str_with_values(precision=10))
        Alice gets {x,z} with value 4.000000001.
        George gets {y} with value 5.
        <BLANKLINE>
        """
        if precision is None: precision=DEFAULT_PRECISION
        result = ""
        for i_agent, agent_name in enumerate(self.map_agent_index_to_name):
            agent_bundle = self.bundles[i_agent]
            agent_value = self.agent_bundle_value_matrix[i_agent,i_agent]
            result += f"{agent_name} gets {agent_bundle} with value {agent_value:.{precision}g}.\n"
        return result

    def str_with_value_matrix(self, separator=None, precision=None)->str:
        """
        Returns a representation of the current allocation, showing the value of each agent to *all* bundles.

        >>> agents = {"Alice":{"x":1.000000001,"y":2,"z":3},"George":{"x":4,"y":5,"z":6}}
        >>> a = Allocation(agents=agents, bundles = {"Alice":{"x","z"}, "George": {"y"}})
        >>> print(a.str_with_value_matrix())
        Alice gets {x,z}. Values: [4] 2.
        George gets {y}. Values: 10 [5].
        <BLANKLINE>
        """
        if separator is None: separator=DEFAULT_SEPARATOR
        if precision is None: precision=DEFAULT_PRECISION
        result = ""
        for i_agent, agent_name in enumerate(self.map_agent_index_to_name):
            agent_bundle = self.bundles[i_agent]
            values_str = ""
            for i_bundle, bundle in enumerate(self.bundles):
                agent_value_to_bundle = self.agent_bundle_value_matrix[i_agent,i_bundle]
                agent_value_to_bundle_str = f"{agent_value_to_bundle:.{precision}g}"
                if i_bundle==i_agent:
                    agent_value_to_bundle_str = "["+agent_value_to_bundle_str+"]"
                values_str += " " + agent_value_to_bundle_str
            result += f"{agent_name} gets {agent_bundle}. Values:{values_str}.\n"
        return result

    def __repr__(self)->str:
        return self.str_with_values(precision=DEFAULT_PRECISION)




def compute_agent_bundle_value_matrix(agents, bundles, num_of_agents, num_of_bundles):
    """
    Compute a matrix U in which each row is an agent, each column is a bundle,
    and U[i,j] is the value of agent i to bundle j.

    >>> agents=ValuationMatrix([[1,2,3.5],[4,5,6]])
    >>> bundles = [[0,1],[2]]
    >>> compute_agent_bundle_value_matrix(agents, bundles, 2, 2)
    array([[3. , 3.5],
           [9. , 6. ]])

    >>> agents=fairpy.agents_from(agents)
    >>> compute_agent_bundle_value_matrix(agents, bundles, 2, 2)
    array([[3. , 3.5],
           [9. , 6. ]])
    """
    agent_bundle_value_matrix = np.zeros([num_of_agents,num_of_bundles])
    # print("bundles: ",bundles)
    if hasattr(agents, 'agent_value_for_bundle'):  # E.g. when agents is a ValuationMatrix.
        # print("agents 1: ",agents)
        for i_agent in range(num_of_agents):
            for i_bundle in range(num_of_bundles):
                agent_bundle_value_matrix[i_agent,i_bundle] = agents.agent_value_for_bundle(i_agent, bundles[i_bundle])
    elif hasattr(next(iter(agents)), 'value'):              # E.g. when agents is a list of Agent objects
        # print("agents 2: ",agents)
        for i_agent in range(num_of_agents):
            for i_bundle in range(num_of_bundles):
                agent = agents[i_agent]
                bundle = bundles[i_bundle]
                try:
                    value = agent.value(bundle)
                except TypeError as err:
                    raise TypeError(f"Cannot compute the value of agent {type(agent)} for bundle {bundle} of type {type(bundle)}") from err
                agent_bundle_value_matrix[i_agent,i_bundle] = value
                    
    else:
        # WARNING: Cannot compute agents' values at all
        for i_agent in range(num_of_agents):
            for i_bundle in range(num_of_bundles):
                agent_bundle_value_matrix[i_agent,i_bundle] = np.nan
    return agent_bundle_value_matrix


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
    # agents = {"b": [1,2], "a": [11,22]}
    # bundles = {"b": [0], "a":[1]}
    # allocation = Allocation(agents, bundles)
    # print(allocation)
