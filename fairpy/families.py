#!python3

"""
Classes for handling fair allocation among families (pre-determined groups of agents).

Programmer: Erel Segal-Halevi
Since: 2021-07
"""

from fairpy import ValuationMatrix
from fairpy.allocations import *
from typing import List, Any
import numpy as np

def map_agent_to_family(families:List[List[int]], num_of_agents:int)->List[int]:
    """
    Converts a list of families, to a map from agent-index to its family/

    :param families a list of families; each family is a list of agent indices.
    :return a list of size num_of_agents, mapping each agent to the index of its family.

    >>> map_agent_to_family([[0,3],[1,2,4]], 5)
    [0, 1, 1, 0, 1]
    """
    the_map = [None]*num_of_agents
    for f,family in enumerate(families):
        for agent in family:
            the_map[agent] = f
    return the_map



class AllocationToFamilies:
    """
    Represents an allocation of objects (divisible or indivisible) to families (groups of agents).
    This is the output of an algorithm for fair allocation among families.
    It is an immutable object. It is used mainly to display the allocation in a nice way.

    >>> ### A valuation matrix and an allocation matrix:
    >>> agents = ValuationMatrix([[10,20,30,40,50],[999,999,999,999,999],[50,40,30,20,10]])
    >>> bundles = AllocationMatrix([[1,0,0,1,0],[0,1,1,0,0]])
    >>> families = [[0,2],[1]]  # agents 0,2 are a couple; agent 1 is a singleton.
    >>> a = AllocationToFamilies(agents=agents, bundles=bundles, families=families)
    >>> a
    Family #0 with members [0, 2] gets { 100% of 0, 100% of 3} with values [50.0, 70.0].
    Family #1 with members [1] gets { 100% of 1, 100% of 2} with values [1998.0].
    <BLANKLINE>
    >>> for bundle in a: print(bundle)
    { 100% of 0, 100% of 3}
    { 100% of 1, 100% of 2}
    >>> a.utility_profile()
    array([  50., 1998.,   70.])

    >>> ### A valuation matrix and a numpy array
    >>> AllocationToFamilies(agents=ValuationMatrix([[10,20,30,40,50],[999,999,999,999,999],[50,40,30,20,10]]), bundles=np.array([[1/3,0,0,0,1],[2/3,1,1,0,0]]), families=families)
    Family #0 with members [0, 2] gets { 33.333% of 0, 100.0% of 4} with values [53.333, 26.667].
    Family #1 with members [1] gets { 66.667% of 0, 100.0% of 1, 100.0% of 2} with values [2664.0].
    <BLANKLINE>
    """
    def __init__(self, agents: List[Any], bundles: List[List[Any]], families:List[int]):
        """
        Initializes an allocation to the given families, of the given bundles, with the given values.

        :param agents: Mandatory. Possible types:
          * A list of names (ints/strings).
          * A list of Agent objects, which must have a name() and a value() methods.
          * A dict from agent name to agent valuation (e.g. representing additive valuation).

        :param bundles: Mandatory. For each agent, there must be a bundle (a list of items), or None. Possible types:
          * A list of bundles.
          * A dict from agent names to bundles.
        `bundles` must be the same types as `agents`: either both are lists or both are dicts.

        :param families: Mandatory. For each family, holds the indices of agents in the family.
        """
        if isinstance(agents,dict) and not isinstance(bundles,dict):
            raise ValueError(f"Cannot match agents to bundles: agents is a dict but bundles is {type(bundles)}")

        map_agent_index_to_name = self.map_agent_index_to_name = fairpy.agent_names_from(agents)

        if isinstance(bundles,dict):       # If "bundles" is a dict mapping an agent name to its bundle... 
            bundles = [bundles.get(name,None) for name in map_agent_index_to_name]  # ... convert it to a list mapping an agent index to its bundle.

        if isinstance(bundles, np.ndarray):
            bundles = AllocationMatrix(bundles)
        if isinstance(bundles, AllocationMatrix):
            self.matrix = bundles
            bundles = [FractionalBundle(bundles[i]) for i in bundles.agents()]
        else:
            bundles = [ListBundle(bundles[i]) for i in range(len(bundles))]

        if isinstance(agents,dict):       # If "agents" is a dict mapping an agent name to its valuation...
            agents = fairpy.agents_from(agents)  # ... convert it to a list mapping an agent index to its valuation.

        # Compute num_of_agents:
        num_of_agents = agents.num_of_agents if hasattr(agents,'num_of_agents') else len(agents)
        num_of_bundles = len(bundles)
        num_of_families = len(families)
        if num_of_bundles!=num_of_families:
            raise ValueError(f"Numbers of families and bundles must be identical, but they are not: {num_of_families}, {num_of_bundles}")

        # Map each agent to its family:
        map_agent_to_family = [None]*num_of_agents
        for f,family in enumerate(families):
            for agent in family:
                map_agent_to_family[agent] = f
        self.map_agent_to_family = map_agent_to_family

        # Verify that all bundles are iterable:
        for i_bundle,bundle in enumerate(bundles):
            if bundle is not None and not isinstance(bundle, Iterable):
                raise ValueError(f"Bundle {i_bundle} should be iterable, but it is {type(bundle)}")

        # Initialize bundles and agents:
        self.num_of_agents = num_of_agents
        self.num_of_families = num_of_families
        self.num_of_bundles = num_of_bundles
        self.agents = agents
        self.families = families
        self.bundles = bundles
        self.agent_bundle_value_matrix = compute_agent_bundle_value_matrix(agents, bundles, num_of_agents, num_of_bundles)


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

    def num_of_shared_objects(self)->int:
        return self.matrix.num_of_shared_objects()

    def __getitem__(self, agent_index:int):
        return self.bundles[agent_index]

    def __iter__(self):
       return self.bundles.__iter__() 


    def utility_profile(self)->np.ndarray:
        """
        Returns a vector that maps each agent to its utility (=sum of values) under this allocation,
        which is considered an allocation for families.

        >>> v = ValuationMatrix([[0.5,1,0],[0.5,0,1]])
        >>> z = AllocationToFamilies(v, np.array([[.2,.3,.5],[.8,.7,.5]]), families=[[0],[1]])
        >>> z.utility_profile()
        array([0.4, 0.9])
        >>> z = AllocationToFamilies(v, np.array([[.2,.3,.5],[.8,.7,.5]]), families=[[1],[0]])
        >>> z.utility_profile()
        array([1.1, 0.6])
        >>> z = AllocationToFamilies(v, np.array([[1.,1.,1.]]), families=[[0,1]])
        >>> z.utility_profile()
        array([1.5, 1.5])
        """
        return np.array([self.agent_bundle_value_matrix[i_agent,self.map_agent_to_family[i_agent]] for i_agent in range(self.num_of_agents)])


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
        for i_family, family in enumerate(self.families):
            family_bundle = self.bundles[i_family]
            members_values = [
                np.round(self.agent_bundle_value_matrix[i_agent,i_family], precision)
                for i_agent in family
            ]
            result += f"Family #{i_family} with members {family} gets {family_bundle} with values {members_values}.\n"
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
            for i_bundle, _ in enumerate(self.bundles):
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
    """
    agent_bundle_value_matrix = np.zeros([num_of_agents,num_of_bundles])
    if hasattr(agents, 'agent_value_for_bundle'):  # E.g. when agents is a ValuationMatrix.
        for i_agent in range(num_of_agents):
            for i_bundle in range(num_of_bundles):
                agent_bundle_value_matrix[i_agent,i_bundle] = agents.agent_value_for_bundle(i_agent, bundles[i_bundle])
    elif hasattr(next(iter(agents)), 'value'):              # E.g. when agents is a list of Agent objects
        for i_agent in range(num_of_agents):
            for i_bundle in range(num_of_bundles):
                agent_bundle_value_matrix[i_agent,i_bundle] = agents[i_agent].value(bundles[i_bundle])
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
