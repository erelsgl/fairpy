"""
Defines a list of agents.
This is the input to many fair allocation algorithms.

Programmer: Erel Segal-Halevi
Since: 2022-11
"""

from typing import Any, List

from fairpy.items.valuations import *
from fairpy.cake.valuations  import *
from fairpy.agents import Agent, AdditiveAgent, BinaryAgent

class AgentList:
    def __init__(self, input:Any):
        """
        Attempts to construct a list of agents from various input formats.
        The returned value is a list of Agent objects.

        From dict of dicts:
        >>> myagents = AgentList({"Alice":{"x":1,"y":2}, "George":{"x":3,"y":4}})
        >>> myagents[0]
        Alice is an agent with a Additive valuation: x=1 y=2.
        >>> myagents[1]
        George is an agent with a Additive valuation: x=3 y=4.
        >>> myagents[1].name()
        'George'
        >>> myagents[0].value({'x','y'})
        3
        >>> AgentList({"Alice":[1,2], "George":[3,4]})[1]
        George is an agent with a Additive valuation: v0=3 v1=4.
        
        From list of dicts:
        >>> AgentList([{"x":1,"y":2}, {"x":3,"y":4}])[0]
        Agent #0 is an agent with a Additive valuation: x=1 y=2.
        
        From list of lists:
        >>> AgentList([[1,2],[3,4]])[1]
        Agent #1 is an agent with a Additive valuation: v0=3 v1=4.
        
        From numpy array:
        >>> AgentList(np.ones([2,4]))[1]
        Agent #1 is an agent with a Additive valuation: v0=1.0 v1=1.0 v2=1.0 v3=1.0.

        From list of valuations:
        >>> l = AgentList([AdditiveValuation([1,2]), BinaryValuation("xy")])
        >>> l[0]
        Agent #0 is an agent with a Additive valuation: v0=1 v1=2.
        
        From list of agents:
        >>> AgentList([AdditiveAgent([1,2]), BinaryAgent("xy")])[0]
        Anonymous is an agent with a Additive valuation: v0=1 v1=2.
        
        From an existing AgentList object:
        >>> AgentList(myagents)
        [Alice is an agent with a Additive valuation: x=1 y=2., George is an agent with a Additive valuation: x=3 y=4.]
        """
        if isinstance(input, AgentList):
            self.agents = input.agents
        else:
            self.agents = agents_from(input)

    def all_items(self):
        return self.agents[0].all_items()

    def __getitem__(self, i:int):
        return self.agents[i]

    def __repr__(self):
        return repr(self.agents)

    def __str__(self):
        return str(self.agents)

    def __len__(self):
        return len(self.agents)





def agents_from(input:Any)->List[Agent]:
    """
    Attempts to construct a list of agents from various input formats.
    The returned value is a list of Agent objects.

    >>> ### From dict of dicts:
    >>> agents_from({"Alice":{"x":1,"y":2}, "George":{"x":3,"y":4}})[0]
    Alice is an agent with a Additive valuation: x=1 y=2.
    >>> agents_from({"Alice":[1,2], "George":[3,4]})[1]
    George is an agent with a Additive valuation: v0=3 v1=4.
    >>> ### From list of dicts:
    >>> agents_from([{"x":1,"y":2}, {"x":3,"y":4}])[0]
    Agent #0 is an agent with a Additive valuation: x=1 y=2.
    >>> ### From list of lists:
    >>> agents_from([[1,2],[3,4]])[1]
    Agent #1 is an agent with a Additive valuation: v0=3 v1=4.
    >>> ### From numpy array:
    >>> agents_from(np.ones([2,4]))[1]
    Agent #1 is an agent with a Additive valuation: v0=1.0 v1=1.0 v2=1.0 v3=1.0.

    >>> ### From list of valuations:
    >>> l = agents_from([AdditiveValuation([1,2]), BinaryValuation("xy")])
    >>> l[0]
    Agent #0 is an agent with a Additive valuation: v0=1 v1=2.
    >>> ### From list of agents:
    >>> agents_from([AdditiveAgent([1,2]), BinaryAgent("xy")])[0]
    Anonymous is an agent with a Additive valuation: v0=1 v1=2.
    """
    if isinstance(input,np.ndarray):
        input = ValuationMatrix(input)
    if isinstance(input,ValuationMatrix):
        return [
            Agent(AdditiveValuation(input[index]), name=f"Agent #{index}")
            for index in input.agents()
        ]
    input_0 = _representative_item(input)
    if input_0 is None:
        return []
    elif isinstance(input_0, Agent):  # The input is already a list of Agent objects - nothing more to do.
        return input
    elif hasattr(input_0, "value"):   # The input is a list of Valuation objects - we just need to add names.
        return [
            Agent(valuation, name=f"Agent #{index}")
            for index,valuation in enumerate(input)
        ]
    else:
        return AdditiveAgent.list_from(input)




def agent_names_from(input:Any)->List[str]:
    """
    Attempts to extract a list of agent names from various input formats.
    The returned value is a list of strings.

    >>> ### From dict:
    >>> agent_names_from({"Alice":{"x":1,"y":2}, "George":{"x":3,"y":4}})
    ['Alice', 'George']
    >>> ### From list of dicts:
    >>> agent_names_from([{"x":1,"y":2}, {"x":3,"y":4}])
    ['Agent #0', 'Agent #1']
    >>> ### From list of lists:
    >>> agent_names_from([[1,2],[3,4]])
    ['Agent #0', 'Agent #1']
    >>> ### From list of valuations:
    >>> agent_names_from([AdditiveValuation([1,2]), BinaryValuation("xy")])
    ['Agent #0', 'Agent #1']
    >>> ### From list of agents:
    >>> agent_names_from([AdditiveAgent([1,2], name="Alice"), BinaryAgent("xy", name="George")])
    ['Alice', 'George']
    >>> d = {"Alice": 123, "George": 456}
    >>> agent_names_from(d.keys())
    ['Alice', 'George']
    """
    if hasattr(input, "keys"):
        return sorted(input.keys())
    elif hasattr(input, 'num_of_agents'):
        num_of_agents = input.num_of_agents
        return [f"Agent #{i}" for i in range(num_of_agents)]
    elif isinstance(input, AgentList):
        return agent_names_from(input.agents)

    if len(input)==0:
        return []

    input_0 = next(iter(input))
    if hasattr(input_0, "name"):  
        return [agent.name() for agent in input]
    elif isinstance(input_0, int):
        return [f"Agent #{index}" for index in input]
    elif isinstance(input_0, str):
        return list(input)  # convert to a list; keep the original order
    else:
        return [f"Agent #{i}" for i in range(len(input))]





######## UTILITY FUNCTIONS #######


def _representative_item(input:Any):
    if isinstance(input, list):
        if len(input)==0:
            return None
        else:
            return input[0]
    elif isinstance(input, dict):
        if len(input)==0:
            return None
        else:
            return next(iter(input.values()))
    else:
        raise ValueError(f"input should be a list or a dict, but it is {type(input)}")



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print (f"{failures} failures, {tests} tests")
