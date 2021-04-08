#!python3

"""
Represents an allocation of a indivisible items among agents ---  the output of an item-allocation algorithm.
Used mainly for display purposes.

Programmer: Erel Segal-Halevi
Since: 2020-11
"""

from typing import *
from fairpy.indivisible.agents import Agent, AdditiveAgent, Item, Bundle


class Allocation:
    """
    >>> Alice = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="Alice")
    >>> George = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="George")
    >>> A = Allocation([Alice, George], ["xy","z"])
    >>> print(A)
    Alice's bundle: {x,y},  value: 3,  all values: [3, 3]
    George's bundle: {z},  value: 1,  all values: [5, 1]
    <BLANKLINE>
    >>> B = Allocation([George, Alice])
    >>> B.set_bundles(["xy","z"])
    >>> print(B)
    George's bundle: {x,y},  value: 5,  all values: [5, 1]
    Alice's bundle: {z},  value: 3,  all values: [3, 3]
    <BLANKLINE>
    """

    def __init__(self, agents: List[Agent], bundles: List[Bundle] = None):
        self.agents = agents
        if bundles is None:
            bundles = [None] * len(agents)
        self.bundles = bundles

    def get_bundle(self, agent_index: int):
        return self.bundles[agent_index]

    def get_bundles(self):
        return self.bundles

    def set_bundle(self, agent_index: int, bundle: Bundle):
        """
        Sets the bundle of the given index.

        :param agent_index: index of the agent.
        :param bundle: a list of intervals.
        """
        self.bundles[agent_index] = bundle

    def set_bundles(self, bundles: List[Bundle]):
        """
        Sets the bundle of the given index.

        :param agent_index: index of the agent.
        :param bundle: a list of intervals.
        """
        self.bundles = bundles

    def __repr__(self):
        result = ""
        for i_agent, agent in enumerate(self.agents):
            agent_bundle = self.bundles[i_agent]
            agent_value = agent.value(agent_bundle)
            all_values = [agent.value(bundle) for bundle in self.bundles]
            # all_differences = [agent_value - agent.value(bundle) for bundle in self.bundles]
            result += f"{agent.name()}'s bundle: {stringify_bundle(agent_bundle)},  value: {agent_value},  all values: {all_values}\n"
        return result


def stringify_bundle(bundle: Bundle):
    """
    Convert a bundle where each item is a character to a compact string representation.
    For testing purposes only.

    >>> stringify_bundle({'x','y'})
    '{x,y}'
    >>> stringify_bundle({'y','x'})
    '{x,y}'
    """
    return "{" + ",".join(sorted(bundle)) + "}"
    # return ",".join(["".join(item) for item in bundle])



if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))







