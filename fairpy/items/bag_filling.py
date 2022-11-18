#!python3

"""
A utility class Bag for bag-filling --- a subroutine in 
    various algorithms for fair allocation of indivisible items.

Programmer: Erel Segal-Halevi
Since:  2021-04
"""

from fairpy import ValuationMatrix
from typing import List
import numpy as np

import logging
logger = logging.getLogger(__name__)


#####################


class Bag:
	"""
	represents a bag for objects. 
	Different agents may have different valuations for the objects.
	>>> values = [[11,33],[44,22]]
	>>> thresholds = [30,30]
	>>> bag = Bag(values, thresholds)
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
	>>> bag.reset()
	>>> print(bag)
	Bag objects: [], values: [0. 0.]
	>>> bag.append([0,1])
	>>> print(bag)
	Bag objects: [0, 1], values: [44. 66.]
	"""

	def __init__(self, values:ValuationMatrix, thresholds:List[float]):
		"""
		Initialize an empty bag.
		:param values: a matrix representing additive valuations (a row for each agent, a column for each object).
		:param thresholds: determines, for each agent, the minimum value that should be in a bag before the agent accepts it.
		"""
		self.values = ValuationMatrix(values)
		self.thresholds = thresholds
		self.reset()

	def reset(self): 
		"""
		Empty the bag.
		"""
		self.objects = []
		self.map_agent_to_bag_value = np.zeros(self.values.num_of_agents)
		logger.info("Starting an empty bag. %d agents and %d objects.", self.values.num_of_agents, self.values.num_of_objects)

	def append(self, object:int):
		"""
		Append the given object or objects to the bag, and update the agents' valuations accordingly.
		"""
		if isinstance(object,list):
			for o in object:
				self.append(o)
			return
		logger.info("   Appending object %s.", object)
		self.objects.append(object)
		for agent in self.values.agents():
			self.map_agent_to_bag_value[agent] += self.values[agent][object]
		logger.debug("      Bag values: %s.", self.map_agent_to_bag_value)

	def willing_agent(self, remaining_agents)->int:
		"""
		:return the index of an arbitrary agent, from the list of remaining agents, who is willing to accept the bag 
		 (i.e., the bag's value is above the agent's threshold).
		 If no remaining agent is willing to accept the bag, None is returned.
		"""
		for agent in remaining_agents:
			logger.debug("      Checking if agent %d is willing to take the bag", agent)
			if self.map_agent_to_bag_value[agent] >= self.thresholds[agent]:
				return agent
		return None


	def fill(self, remaining_objects, remaining_agents)->(int, list):
		"""
		Fill the bag with objects until at least one agent is willing to accept it.
		:return the willing agent, or None if the objects are insufficient.
		>>> bag = Bag(values=[[1,2,3,4,5,6],[6,5,4,3,2,1]], thresholds=[10,10])
		>>> remaining_objects = list(range(6))
		>>> remaining_agents = [0,1]
		>>> (willing_agent, allocated_objects) = bag.fill(remaining_objects, remaining_agents)
		>>> willing_agent
		1
		>>> allocated_objects
		[0, 1]
		>>> remaining_objects = list(set(remaining_objects) - set(allocated_objects))
		>>> bag = Bag(values=[[1,2,3,4,5,6],[6,5,4,3,2,1]], thresholds=[10,10])
		>>> bag.fill(remaining_objects, remaining_agents)
		(0, [2, 3, 4])
		>>> bag = Bag(values=[[20]], thresholds=[10])  # Edge case: single object
		>>> bag.fill(remaining_objects=[0], remaining_agents=[0])
		(0, [0])
		>>> bag = Bag(values=[[20,5]], thresholds=[10])  # Edge case: bag with an existing large object
		>>> bag.append(0)
		>>> bag.fill(remaining_objects=[1], remaining_agents=[0])
		(0, [0])
		"""
		if len(remaining_agents)==0:
			return (None, None)
		willing_agent = self.willing_agent(remaining_agents)
		if willing_agent is not None:
			return (willing_agent, self.objects)
		for object in remaining_objects:
			self.append(object)
			willing_agent = self.willing_agent(remaining_agents)
			if willing_agent is not None:
				return (willing_agent, self.objects)
		return (None, None)

	def __str__(self):
		return f"Bag objects: {self.objects}, values: {self.map_agent_to_bag_value}"



#####################



class SequentialAllocation:
	"""
	A class that handles the process of sequentially allocating bundles to agents, e.g., 
	  in a bag-filling procedure.
	"""

	def __init__(self, agents:list, objects:list, logger):
		self.remaining_agents = list(agents)
		self.remaining_objects = list(objects)
		self.bundles = len(agents)*[None]
		self.logger = logger

	def let_agent_get_objects(self, i_agent, allocated_objects):
		self.bundles[i_agent] = allocated_objects
		self.remaining_agents.remove(i_agent)
		for o in allocated_objects: 
			self.remaining_objects.remove(o)
		self.logger.info("Agent %d takes the bag with objects %s. Remaining agents: %s. Remaining objects: %s.", 
			i_agent, allocated_objects, self.remaining_agents, self.remaining_objects)



#####################


def one_directional_bag_filling(values: ValuationMatrix, thresholds:List[float]):
	"""
	The simplest bag-filling procedure: fills a bag in the given order of objects.
	
	:param valuations: a valuation matrix (a row for each agent, a column for each object).
	:param thresholds: determines, for each agent, the minimum value that should be in a bag before the agent accepts it.

	>>> one_directional_bag_filling(values=ValuationMatrix([[11,33],[44,22]]), thresholds=[30,30])
	[[1], [0]]
	>>> one_directional_bag_filling(values=ValuationMatrix([[11,33],[44,22]]), thresholds=[10,10])
	[[0], [1]]
	>>> one_directional_bag_filling(values=ValuationMatrix([[11,33],[44,22]]), thresholds=[40,30])
	[None, [0]]
	"""
	if len(thresholds) != values.num_of_agents:
		raise ValueError(f"Number of valuations {values.num_of_agents} differs from number of thresholds {len(thresholds)}")

	allocation = SequentialAllocation(values.agents(), values.objects(), logger)
	bag = Bag(values, thresholds)
	while True:
		(willing_agent, allocated_objects) = bag.fill(allocation.remaining_objects, allocation.remaining_agents)
		if willing_agent is None:  break
		allocation.let_agent_get_objects(willing_agent, allocated_objects)
		bag.reset()
	return allocation.bundles



if __name__ == '__main__':
	import sys
	logger.addHandler(logging.StreamHandler(sys.stdout))
	# logger.setLevel(logging.DEBUG)

	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))

