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

    >>> a = Allocation(agents=range(3), bundles=[[3,6],None,[2,5]], values=[9,0,6.999999])
    >>> Allocation.default_separator=","
    >>> a
    Agent #0 gets {3,6} with value 9.
    Agent #1 gets None with value 0.
    Agent #2 gets {2,5} with value 7.
    <BLANKLINE>
    >>> Allocation.default_precision=9
    >>> a
    Agent #0 gets {3,6} with value 9.
    Agent #1 gets None with value 0.
    Agent #2 gets {2,5} with value 6.999999.
    <BLANKLINE>
    """

    default_precision:int=3   # number of significant digits of values in printing
    default_separator:str=","

    agents:List[Any]
    bundles:List[List[Any]]
    values:List[float]

    num_of_agents:int

    def __init__(self, agents: List[Any], bundles: List[List[Any]], values:List[float]=None):
        """
        Initializes an allocation to the given agents, of the given bundles, with the given values.

        :param agents: Mandatory. Either a list of names (ints/strings), or a list of Agent objects. 
                       In case of Agent objects, the objects must have a name() and a value() methods.
        :param bundles: Mandatory. For each agent, there must be a bundle (a list of items), or None.
        :param values: Optional. For each agent, there should be the value of his bundle.
                       If it is not given, then it is filled in using the Agent object's value method.
        """
        num_of_agents = len(agents)
        if num_of_agents!=len(bundles) or (values is not None and num_of_agents!=len(values)):
            raise ValueError("Numbers of agents, bundles and values must be identical, but they are not: {len(agents)}, {len(bundles)}, {len(values)}")
        self.num_of_agents = num_of_agents
        self.agents = agents
        #
        self.bundles = bundles
        if values is None:
            values = [agent.value(bundles[i]) for i,agent in enumerate(agents)]
        self.values = values

    def get_bundle(self, agent_index: int):
        return self.bundles[agent_index]

    def get_bundles(self):
        return self.bundles

    def __getitem__(self, agent_index:int):
        return self.get_bundle(agent_index)

    @staticmethod
    def agent_name(agent):
        if hasattr(agent,'name'):
            return agent.name() 
        elif isinstance(agent,int):
            return (f"Agent #{agent}")
        else:
            return agent


    def __repr__(self):
        result = ""
        for i_agent, agent in enumerate(self.agents):
            agent_bundle = self.bundles[i_agent]
            agent_value = self.values[i_agent]
            agent_bundle_str = stringify_bundle(agent_bundle, separator=Allocation.default_separator)
            result += f"{self.agent_name(agent)} gets {agent_bundle_str} with value {agent_value:.{Allocation.default_precision}g}.\n"
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
