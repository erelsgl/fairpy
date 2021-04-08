#!python3

"""
A simple one-directional bag-filling algorithm.
   Demonstrates using the Bag class.

Programmer: Erel Segal-Halevi
Since:  2021-04
"""

from fairpy.valuations import ValuationMatrix
from fairpy.allocations import Allocation
from fairpy.indivisible.bag_filling import Bag
from typing import List
import numpy as np


def one_directional_bag_filling(v:ValuationMatrix, map_agent_to_value_threshold:List[float]):
	"""
	A very simple bag-filling procedure: fills a bag in one direction.
	
	:param v: a valuation matrix (a row for each agent, a column for each object).
	:param map_agent_to_value_threshold: determines, for each agent, the minimum value that should be in a bag before the agent accepts it.

	>>> valuations = ValuationMatrix([[11,33],[44,22]])
	>>> one_directional_bag_filling(valuations, map_agent_to_value_threshold=[30,30])
	Agent #0 gets {1} with value 33.
	Agent #1 gets {0} with value 44.
	<BLANKLINE>
	>>> one_directional_bag_filling(valuations, map_agent_to_value_threshold=[10,10])
	Agent #0 gets {0} with value 11.
	Agent #1 gets {1} with value 22.
	<BLANKLINE>
	>>> one_directional_bag_filling(valuations, map_agent_to_value_threshold=[40,30])
	Agent #0 gets None with value 0.
	Agent #1 gets {0} with value 44.
	<BLANKLINE>
	"""
	v = ValuationMatrix(v)
	if len(map_agent_to_value_threshold) != v.num_of_agents:
		raise ValueError(f"Number of valuations {v.num_of_agents} differs from number of thresholds {len(map_agent_to_value_threshold)}")

	allocations = [None] * v.num_of_agents
	remaining_objects = list(v.objects())
	remaining_agents  = list(v.agents())
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
