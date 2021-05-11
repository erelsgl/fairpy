#!python3

"""
Represents an allocation of objects to agents ---  the output of a fair allocation algorithm.

An immutable object; used mainly for display purposes.

Programmer: Erel Segal-Halevi
Since: 2021-04
"""

from fairpy.items.agents import AdditiveAgent
from typing import List, Any
import numpy as np


class Allocation:
    """
    Represents an allocation of objects (divisible or indivisible) to agents. 
    This is the output of a fair allocation algorithm.
    It is an immutable object. It is used mainly to display the allocation in a nice way.

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
    >>> a = Allocation(agents=["Alice","George","Dina"], bundles=[[3,6],None,[2,5]], map_agent_to_value=[9,0,6.999999])
    >>> a
    Alice gets {3,6} with value 9.
    George gets None with value 0.
    Dina gets {2,5} with value 7.
    <BLANKLINE>
    >>> agents = agents={"Alice":{"x":1,"y":2,"z":3},"George":{"x":4,"y":5,"z":6}}
    >>> a = Allocation(agents=agents, bundles = [{"x","z"},{"y"}])
    >>> a
    Alice gets {x,z} with value 4.
    George gets {y} with value 5.
    <BLANKLINE>
    >>> from fairpy.valuations import ValuationMatrix
    >>> a = Allocation(agents=ValuationMatrix([[10,20,30,40,50],[999,999,999,999,999],[50,40,30,20,10]]), bundles=[[0,4],None,[1,2]])
    >>> a
    Agent #0 gets {0,4} with value 60.
    Agent #1 gets None with value 0.
    Agent #2 gets {1,2} with value 70.
    <BLANKLINE>
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
          * A dict from agent name to agent valuation (representing additive valuation).

        :param bundles: Mandatory. For each agent, there must be a bundle (a list of items), or None. Possible types:
          * A list of bundles.
          * A map from agent names to bundles.

        :param map_agent_to_value: Optional. For each agent, there should be the value of his bundle.
                       If it is not given, then it is filled in using the Agent object's value method.
        """

        # Compute num_of_agents:
        num_of_agents = agents.num_of_agents if hasattr(agents,'num_of_agents') else len(agents)
        if num_of_agents!=len(bundles):
            raise ValueError(f"Numbers of agents and bundles must be identical, but they are not: {num_of_agents}, {len(bundles)}")
        if map_agent_to_value is not None and num_of_agents!=len(map_agent_to_value):
            raise ValueError(f"Numbers of agents and values must be identical, but they are not: {num_of_agents}, {len(map_agent_to_value)}")
        self.num_of_agents = num_of_agents

        # Initialize bundles and agents:
        self.bundles = bundles
        self.agents = agents

        # # Compute a mapping from agent id to the agent's valuation of his bundle:
        if isinstance(agents, dict):   
            agents = AdditiveAgent.list_from(agents)  
        # if hasattr(agents, 'agent_value_for_bundle'):  # E.g. when agents is a ValuationMatrix.
        #    map_agent_to_value = [agents.agent_value_for_bundle(i,bundles[i]) for i,_ in enumerate(agents)]
        # elif hasattr(agents[0], 'value'):              # E.g. when agents is a list of Agent.
        #    map_agent_to_value = [agent.value(bundles[i]) for i,agent in enumerate(agents)]
        # if map_agent_to_value is None:      
        #     raise ValueError("Cannot compute agents' valuations")          
        # self.map_agent_to_value = map_agent_to_value

        # Compute a matrix with each agent's values for all bundles:
        agent_bundle_value_matrix = np.zeros([num_of_agents,num_of_agents])
        if hasattr(agents, 'agent_value_for_bundle'):  # E.g. when agents is a ValuationMatrix.
            for i_agent in range(num_of_agents):
                for i_bundle in range(num_of_agents):
                    agent_bundle_value_matrix[i_agent,i_bundle] = agents.agent_value_for_bundle(i_agent,bundles[i_bundle])
        elif hasattr(agents[0], 'value'):              # E.g. when agents is a list of Agent.
            for i_agent in range(num_of_agents):
                for i_bundle in range(num_of_agents):
                    agent_bundle_value_matrix[i_agent,i_bundle] = agents[i_agent].value(bundles[i_bundle])
        elif map_agent_to_value is not None:
            # WARNING: In this case, only the value of each agent to his own bundle is computed.
            for i_agent in range(num_of_agents):
                agent_bundle_value_matrix[i_agent,i_agent] = map_agent_to_value[i_agent]
        else:
            raise ValueError("Cannot compute agents' valuations to their bundles")          
        self.agent_bundle_value_matrix = agent_bundle_value_matrix

        # Compute a mapping from agent id to agent name:
        map_agent_to_name = None
        if hasattr(agents[0], 'name'):
           map_agent_to_name  = [agent.name() for agent in agents]
        elif isinstance(agents[0], int):
            map_agent_to_name = [f"Agent #{i}" for i in agents]
        elif isinstance(agents[0], str):
            map_agent_to_name = agents
        else:
           map_agent_to_name  = [f"Agent #{i}" for i in range(num_of_agents)]
        self.map_agent_to_name  = map_agent_to_name


    def get_bundle(self, agent_index: int):
        return self.bundles[agent_index]

    def get_bundles(self):
        return self.bundles

    def __getitem__(self, agent_index:int):
        return self.get_bundle(agent_index)
       
    def str_with_values(self, separator=None, precision=None)->str:
        """
        Returns a representation of the current allocation, showing the value of each agent to his own bundle.
        
        >>> agents = {"Alice":{"x":1.000000001,"y":2,"z":3},"George":{"x":4,"y":5,"z":6}}
        >>> a = Allocation(agents=agents, bundles = [{"x","z"},{"y"}])
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
        >>> a = Allocation(agents=agents, bundles = [{"x","z"},{"y"}])
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
