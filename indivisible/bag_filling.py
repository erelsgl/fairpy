#!python3

"""
A utility class Bag for bag-filling, which is a subroutine in 
    various algorithms for fair allocation of indivisible items.

Programmer: Erel Segal-Halevi
Since:  2021-04
"""

from fairpy.valuations import ValuationMatrix
from typing import List
import numpy as np

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



if __name__ == '__main__':
	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))

