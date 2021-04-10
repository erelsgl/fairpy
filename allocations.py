#!python3

"""
Represents an allocation of objects to agents ---  the output of an item-allocation algorithm.

An immutable object; used mainly for display purposes.

Programmer: Erel Segal-Halevi
Since: 2021-04
"""

from typing import List, Any


class Allocation:
    """
    Represents an allocation of objects to agents.
    An immutable object; used mainly for display purposes.

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
    >>> from valuations import ValuationMatrix
    >>> a = Allocation(agents=ValuationMatrix([[10,20,30,40,50],[999,999,999,999,999],[50,40,30,20,10]]), bundles=[[0,4],None,[1,2]])
    >>> a
    Agent #0 gets {0,4} with value 60.
    Agent #1 gets None with value 0.
    Agent #2 gets {1,2} with value 70.
    <BLANKLINE>
    """

    default_precision:int=3   # number of significant digits in printing
    default_separator:str=","

    agents:List[Any]
    bundles:List[List[Any]]
    map_agent_to_value:List[float]

    num_of_agents:int

    def __init__(self, agents: List[Any], bundles: List[List[Any]], map_agent_to_value:List[float]=None):
        """
        Initializes an allocation to the given agents, of the given bundles, with the given values.

        :param agents: Mandatory. Either a list of names (ints/strings), or a list of Agent objects. 
                       In case of Agent objects, the objects must have a name() and a value() methods.
        :param bundles: Mandatory. For each agent, there must be a bundle (a list of items), or None.
        :param map_agent_to_value: Optional. For each agent, there should be the value of his bundle.
                       If it is not given, then it is filled in using the Agent object's value method.
        """
        num_of_agents = agents.num_of_agents if hasattr(agents,'num_of_agents') else len(agents)
        if num_of_agents!=len(bundles):
            raise ValueError(f"Numbers of agents and bundles must be identical, but they are not: {num_of_agents}, {len(bundles)}")
        if map_agent_to_value is not None and num_of_agents!=len(map_agent_to_value):
            raise ValueError(f"Numbers of agents and values must be identical, but they are not: {num_of_agents}, {len(map_agent_to_value)}")
        self.num_of_agents = num_of_agents
        #
        self.bundles = bundles
        self.agents = agents
        #
        map_agent_to_name = agents

        if hasattr(agents, 'agent_value_for_bundle'):
           map_agent_to_value = [agents.agent_value_for_bundle(i,bundles[i]) for i,_ in enumerate(agents)]
           map_agent_to_name  = [f"Agent #{i}" for i in range(num_of_agents)]

        elif hasattr(agents[0], 'value'):
           map_agent_to_value = [agent.value(bundles[i]) for i,agent in enumerate(agents)]
           map_agent_to_name  = [agent.name() for agent in agents]

        elif isinstance(agents[0], int):
            map_agent_to_name = [f"Agent #{i}" for i in agents]

        else:
            map_agent_to_name = agents

        if map_agent_to_value is None:      
            raise ValueError("Cannot compute agents' valuations")          

        self.map_agent_to_value = map_agent_to_value
        self.map_agent_to_name  = map_agent_to_name

    def get_bundle(self, agent_index: int):
        return self.bundles[agent_index]

    def get_bundles(self):
        return self.bundles

    def __getitem__(self, agent_index:int):
        return self.get_bundle(agent_index)

    def __repr__(self):
        result = ""
        for i_agent, agent_name in enumerate(self.map_agent_to_name):
            agent_bundle = self.bundles[i_agent]
            agent_value = self.map_agent_to_value[i_agent]
            agent_bundle_str = stringify_bundle(agent_bundle, separator=Allocation.default_separator)
            result += f"{agent_name} gets {agent_bundle_str} with value {agent_value:.{Allocation.default_precision}g}.\n"
        return result


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
