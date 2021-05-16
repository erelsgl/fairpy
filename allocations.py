#!python3

"""
Represents an allocation of objects to agents ---  the output of a fair allocation algorithm.

An immutable object; used mainly for display purposes.

Programmer: Erel Segal-Halevi
Since: 2021-04
"""

import fairpy
from typing import List, Any, Dict
import numpy as np
from collections import defaultdict, Iterable
from dicttools import stringify


class Allocation:
    """
    Represents an allocation of objects (divisible or indivisible) to agents. 
    This is the output of a fair allocation algorithm.
    It is an immutable object. It is used mainly to display the allocation in a nice way.

    >>> ### Initialize from list of indices:
    >>> a = Allocation(agents=range(3), bundles=[[3,6],None,[2,5]], map_agent_to_value=[9,0,6.999999])
    >>> Allocation.default_separator=","
    >>> Allocation.default_precision=3
    >>> a
    Agent #0 gets {3,6} with value 9.
    Agent #1 gets None with value 0.
    Agent #2 gets {2,5} with value 7.
    <BLANKLINE>
    >>> Allocation.default_separator=", "
    >>> Allocation.default_precision=9
    >>> a
    Agent #0 gets {3, 6} with value 9.
    Agent #1 gets None with value 0.
    Agent #2 gets {2, 5} with value 6.999999.
    <BLANKLINE>
    >>> Allocation.default_separator=","
    >>> Allocation.default_precision=3
    >>> ### Initialize from list of agent names:
    >>> a = Allocation(agents=["Alice","George","Dina"], bundles=[[3,6],None,[2,5]], map_agent_to_value=[9,0,6.999999])
    >>> a
    Alice gets {3,6} with value 9.
    George gets None with value 0.
    Dina gets {2,5} with value 7.
    <BLANKLINE>
    >>> agents = {"Alice":{"x":1,"y":2,"z":3},"George":{"x":4,"y":5,"z":6}}
    >>> ### Initialize from dict of agents and a dict of bundles:
    >>> a = Allocation(agents=agents, bundles =  {"Alice":{"x","z"}, "George":{"y"}})
    >>> a
    Alice gets {x,z} with value 4.
    George gets {y} with value 5.
    <BLANKLINE>
    >>> stringify(a.map_item_to_agents())
    "{x:['Alice'], y:['George'], z:['Alice']}"
    >>> ### Initialize from dict of agents and a partial dict of bundles:
    >>> a = Allocation(agents=agents, bundles =  {"Alice":{"x","z"}})
    >>> a
    Alice gets {x,z} with value 4.
    George gets None with value 0.
    <BLANKLINE>
    >>> stringify(a.map_item_to_agents())
    "{x:['Alice'], z:['Alice']}"
    >>> ### Initialize from list of agents and a dict of bundles:
    >>> a = Allocation(agents=["Alice","George"], bundles =  {"Alice":["x","z"], "George":["x", "y"]})
    >>> a
    Alice gets {x,z} with value nan.
    George gets {x,y} with value nan.
    <BLANKLINE>
    >>> stringify(a.map_item_to_agents())
    "{x:['Alice', 'George'], y:['George'], z:['Alice']}"
    >>> stringify(a.map_item_to_agents(sortkey=lambda name: -a.map_agent_to_name.index(name)))
    "{x:['George', 'Alice'], y:['George'], z:['Alice']}"
    >>> stringify(a.map_agent_to_bundle())
    "{Alice:['x', 'z'], George:['x', 'y']}"
    >>> from fairpy.valuations import ValuationMatrix
    >>> ### Initialize from valuation matrix and list of bundles:
    >>> a = Allocation(agents=ValuationMatrix([[10,20,30,40,50],[999,999,999,999,999],[50,40,30,20,10]]), bundles=[[0,4],None,[1,2]])
    >>> a
    Agent #0 gets {0,4} with value 60.
    Agent #1 gets None with value 0.
    Agent #2 gets {1,2} with value 70.
    <BLANKLINE>
    >>> for bundle in a: print(bundle)
    [0, 4]
    None
    [1, 2]
    """

    # static variables:
    default_precision:int=3     # number of significant digits in printing
    default_separator:str=","   # separator between items in printing


    def __init__(self, agents: List[Any], bundles: List[List[Any]], map_agent_to_value:List[float]=None):
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


        :param map_agent_to_value: Optional. For each agent, there should be the value of his bundle.
                       If it is not given, then it is filled in using the Agent object's value method.
        """

        if isinstance(agents,dict) and not isinstance(bundles,dict):
            raise ValueError(f"Cannot match agents to bundles: agents is a dict but bundles is {type(bundles)}")

        map_agent_to_name = self.map_agent_to_name = fairpy.agent_names_from(agents)

        if isinstance(bundles,dict):       # If "bundles" is a dict mapping an agent name to its bundle... 
            bundles = [bundles.get(name,None) for name in map_agent_to_name]  # ... convert it to a list mapping an agent index to its bundle.
            
        if isinstance(agents,dict):       # If "agents" is a dict mapping an agent name to its valuation...
            agents = fairpy.agents_from(agents)
            # agents = [agents[name] for name in map_agent_to_name]  # ... convert it to a list mapping an agent index to its valuation.

        # Compute num_of_agents:
        num_of_agents = agents.num_of_agents if hasattr(agents,'num_of_agents') else len(agents)
        if num_of_agents!=len(bundles):
            raise ValueError(f"Numbers of agents and bundles must be identical, but they are not: {num_of_agents}, {len(bundles)}")
        if map_agent_to_value is not None and num_of_agents!=len(map_agent_to_value):
            raise ValueError(f"Numbers of agents and values must be identical, but they are not: {num_of_agents}, {len(map_agent_to_value)}")
        self.num_of_agents = num_of_agents

        # Verify that all bundles are iterable:
        for i_bundle,bundle in enumerate(bundles):
            if bundle is not None and not isinstance(bundle, Iterable):
                raise ValueError(f"Bundle {i_bundle} should be iterable, but it is {type(bundle)}")
        # Initialize bundles and agents:
        self.agents = agents
        self.bundles = bundles

        # Compute a matrix with each agent's values for all bundles:
        agent_bundle_value_matrix = np.zeros([num_of_agents,num_of_agents])
        if hasattr(agents, 'agent_value_for_bundle'):  # E.g. when agents is a ValuationMatrix.
            for i_agent in range(num_of_agents):
                for i_bundle in range(num_of_agents):
                    agent_bundle_value_matrix[i_agent,i_bundle] = agents.agent_value_for_bundle(i_agent,bundles[i_bundle])
        elif hasattr(next(iter(agents)), 'value'):              # E.g. when agents is a list of Agent objects
            for i_agent in range(num_of_agents):
                for i_bundle in range(num_of_agents):
                    agent_bundle_value_matrix[i_agent,i_bundle] = agents[i_agent].value(bundles[i_bundle])
        elif map_agent_to_value is not None:
            # WARNING: In this case, only the value of each agent to his own bundle is computed.
            for i_agent in range(num_of_agents):
                agent_bundle_value_matrix[i_agent,i_agent] = map_agent_to_value[i_agent]
        else:
            # WARNING: Cannot compute agents' values at all
            for i_agent in range(num_of_agents):
                agent_bundle_value_matrix[i_agent,i_agent] = np.nan 
        self.agent_bundle_value_matrix = agent_bundle_value_matrix


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
            self.map_agent_to_name[i_agent]:self.bundles[i_agent]
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
                result[item].append(self.map_agent_to_name[i_agent])
        if sortkey is not None:
            for item,winners in result.items():
                winners.sort(key=sortkey)
        return result


    def __getitem__(self, agent_index:int):
        return self.bundles[agent_index]

    def __iter__(self):
       return self.bundles.__iter__() 
       
    def str_with_values(self, separator=None, precision=None)->str:
        """
        Returns a representation of the current allocation, showing the value of each agent to his own bundle.
        
        >>> agents = {"Alice":{"x":1.000000001,"y":2,"z":3},"George":{"x":4,"y":5,"z":6}}
        >>> a = Allocation(agents=agents, bundles = {"Alice": {"x","z"}, "George": {"y"}})
        >>> print(a.str_with_values())
        Alice gets {x,z} with value 4.
        George gets {y} with value 5.
        <BLANKLINE>
        >>> print(a.str_with_values(separator=";"))
        Alice gets {x;z} with value 4.
        George gets {y} with value 5.
        <BLANKLINE>
        >>> print(a.str_with_values(precision=10))
        Alice gets {x,z} with value 4.000000001.
        George gets {y} with value 5.
        <BLANKLINE>
        """
        if separator is None: separator=Allocation.default_separator
        if precision is None: precision=Allocation.default_precision
        result = ""
        for i_agent, agent_name in enumerate(self.map_agent_to_name):
            agent_bundle = self.bundles[i_agent]
            agent_value = self.agent_bundle_value_matrix[i_agent,i_agent]
            agent_bundle_str = stringify_bundle(agent_bundle, separator=separator)
            result += f"{agent_name} gets {agent_bundle_str} with value {agent_value:.{precision}g}.\n"
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
        if separator is None: separator=Allocation.default_separator
        if precision is None: precision=Allocation.default_precision
        result = ""
        for i_agent, agent_name in enumerate(self.map_agent_to_name):
            agent_bundle = self.bundles[i_agent]
            agent_bundle_str = stringify_bundle(agent_bundle, separator=Allocation.default_separator)
            values_str = ""
            for i_bundle, bundle in enumerate(self.bundles):
                agent_value_to_bundle = self.agent_bundle_value_matrix[i_agent,i_bundle]
                agent_value_to_bundle_str = f"{agent_value_to_bundle:.{precision}g}"
                if i_bundle==i_agent:
                    agent_value_to_bundle_str = "["+agent_value_to_bundle_str+"]"
                values_str += " " + agent_value_to_bundle_str
            result += f"{agent_name} gets {agent_bundle_str}. Values:{values_str}.\n"
        return result

    def __repr__(self)->str:
        return self.str_with_values(separator=Allocation.default_separator, precision=Allocation.default_precision)


def stringify_bundle(bundle: List[Any], separator=","):
    """
    Convert a bundle where each item is a character to a compact string representation.
    For testing purposes only.

    >>> stringify_bundle({'x','y'})
    '{x,y}'
    >>> stringify_bundle({'y','x'})
    '{x,y}'
    >>> stringify_bundle([2,1])
    '{1,2}'
    >>> stringify_bundle(None)
    'None'
    """
    if bundle is None:
        return "None"
    else:
        return "{" + separator.join(map(str,sorted(bundle))) + "}"
    # return ",".join(["".join(item) for item in bundle])



if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
