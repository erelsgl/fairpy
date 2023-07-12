"""
Given an instance and an allocation, calculate various measures of satisfaction.
"""

from fairpy.courses.instance import Instance
from typing import *

class AgentBundleValueMatrix:

    def __init__(self, instance:Instance, allocation:Dict[Any, List[Any]]):
        """
        :param instance: an input instance to the fair-course-allocation problem.
        :param allocation: a dict mapping each agent to its bundle (a list)

        >>> instance = Instance(
        ...   agent_capacities = {"Alice": 2, "Bob": 3}, 
        ...   item_capacities  = {"c1": 4, "c2": 5}, 
        ...   valuations       = {"Alice": {"c1": 11, "c2": 22}, "Bob": {"c1": 33, "c2": 44}})
        >>> allocation = {"Alice": ["c1"], "Bob": ["c2"]}
        >>> matrix = AgentBundleValueMatrix(instance, allocation)
        >>> matrix.matrix
        {'Alice': {'Alice': 11, 'Bob': 22}, 'Bob': {'Alice': 33, 'Bob': 44}}
        >>> matrix.utilitarian_value()
        55
        >>> matrix.egalitarian_value()
        11
        >>> matrix.make_envy_matrix()
        >>> matrix.envy_matrix
        {'Alice': {'Alice': 0, 'Bob': 11}, 'Bob': {'Alice': -11, 'Bob': 0}}
        >>> matrix.max_envy()
        11
        >>> matrix.mean_envy()
        5.5
        """
        self.agents = instance.agents
        self.allocation = allocation
        self.matrix = {
            agent1: {
                agent2: instance.agent_bundle_value(agent1, allocation[agent2])
                for agent2 in self.agents
            }
            for agent1 in self.agents
        }
        self.envy_matrix = None  # maps each agent-pair to the envy between them.
        self.envy_vector = None  # maps each agent to his maximum envy.

    def utilitarian_value(self)->float:
        return sum([self.matrix[agent][agent] for agent in self.agents])/len(self.agents)

    def egalitarian_value(self)->float:
        return min([self.matrix[agent][agent] for agent in self.agents])
    
    def make_envy_matrix(self):
        if self.envy_matrix is not None:
            return
        self.envy_matrix = {
            agent1: {
                agent2: self.matrix[agent1][agent2] - self.matrix[agent1][agent1]
                for agent2 in self.agents
            }
            for agent1 in self.agents
        }
        self.envy_vector = {
            agent1: max(self.envy_matrix[agent1].values())
            for agent1 in self.agents
        }

    def max_envy(self):
        self.make_envy_matrix()
        return max(self.envy_vector.values())

    def mean_envy(self):
        self.make_envy_matrix()
        return sum([max(envy,0) for envy in self.envy_vector.values()]) / len(self.agents)

    def egalitarian_value(self):
        return min([self.matrix[agent][agent] for agent in self.agents])


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
