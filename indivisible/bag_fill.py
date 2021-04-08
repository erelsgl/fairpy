#!python3

"""
An implementation of bag-filling.
   Can be used in various algorithms for fair allocation of indivisible items.

Programmer: Erel Segal-Halevi
Since:  2021-04
"""

from fairpy.valuations import ValuationMatrix
from fairpy.allocations import Allocation
from typing import *
import numpy as np


##############################################################################


class Bag:
	"""
	represents a bag for objects. 
	Different agents may have different valuations for the objects.
	>>> valuations = ValuationMatrix([[11,33],[44,22]])
	>>> thresholds = [30,30]
	>>> bag = Bag(valuations, thresholds)
	>>> print(bag)
	Bag objects: [], values: [0. 0.]
	>>> print(bag.willing_agent([0,1]))
	None
	>>> bag.append(0)
	>>> print(bag)
	Bag objects: [0], values: [11. 44.]
	>>> print(bag.willing_agent([0,1]))
	1
	>>> bag.append(1)
	>>> print(bag)
	Bag objects: [0, 1], values: [44. 66.]
	>>> print(bag.willing_agent([0,1]))
	0
	"""
	objects: List[int]
	valuations: ValuationMatrix
	map_agent_to_bag_value: List[float]

	def __init__(self, v:ValuationMatrix, map_agent_to_value_threshold:List[float]):
		self.objects = []
		self.valuations = v
		self.map_agent_to_value_threshold = map_agent_to_value_threshold
		self.map_agent_to_bag_value = np.zeros(v.num_of_agents)

	def append(self, object:int):
		"""
		Append the given object to the bag, and update the agents' valuations accordingly.
		"""
		self.objects.append(object)
		for agent in self.valuations.agents():
			self.map_agent_to_bag_value[agent] += self.valuations[agent][object]

	def willing_agent(self, remaining_agents)->int:
		"""
		:return the index of an arbitrary agent, from the list of remaining agents, who is willing to accept the bag 
		 (i.e., the bag's value is above the agent's threshold).
		 If no remaining agent is willing to accept the bag, None is returned.
		"""
		for agent in remaining_agents:
			if self.map_agent_to_bag_value[agent] >= self.map_agent_to_value_threshold[agent]:
				return agent
		return None


	def __str__(self):
		return f"Bag objects: {self.objects}, values: {self.map_agent_to_bag_value}"


##############################################################################


def bag_fill(v:ValuationMatrix, map_agent_to_value_threshold:List[float]):
	"""
	:param v: a valuation matrix (a row for each agent, a column for each object).
	:param map_agent_to_value_threshold: determines, for each agent, the minimum value that should be in a bag before the agent accepts it.

	>>> valuations = ValuationMatrix([[11,33],[44,22]])
	>>> bag_fill(valuations, map_agent_to_value_threshold=[30,30])
	0's bundle: {1},  value: 33.
	1's bundle: {0},  value: 44.
	<BLANKLINE>
	>>> bag_fill(valuations, map_agent_to_value_threshold=[10,10])
	0's bundle: {0},  value: 11.
	1's bundle: {1},  value: 22.
	<BLANKLINE>
	>>> bag_fill(valuations, map_agent_to_value_threshold=[40,30])
	0's bundle: None,  value: 0.
	1's bundle: {0},  value: 44.
	<BLANKLINE>
	"""
	if len(map_agent_to_value_threshold) != v.num_of_agents:
		raise ValueError(f"Number of valuations {v.num_of_agents} differs from number of thresholds {len(map_agent_to_value_threshold)}")

	allocations = [None] * v.num_of_agents
	remaining_objects = list(v.objects())
	remaining_agents  = list(v.agents())
	v = ValuationMatrix(v)
	bag = Bag(v, map_agent_to_value_threshold)
	for object in remaining_objects:
		bag.append(object)
		if (willing_agent := bag.willing_agent(remaining_agents)) is not None:
			allocations[willing_agent] = bag.objects
			remaining_agents.remove(willing_agent)
			if len(remaining_agents)==0:
				break
			bag = Bag(v, map_agent_to_value_threshold)
	valuations = [v.agent_value_for_bundle(agent,allocations[agent]) for agent in v.agents()]
	return Allocation(v.agents(), allocations, valuations)


if __name__ == '__main__':
	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))

