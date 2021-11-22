#!python3
"""
An algorithm for 1-out-of-(3n/2) MMS allocation of indivisible objects.

Programmer: Erel Segal-Halevi
Since:  2021-04
"""

from fairpy import convert_input_to_valuation_matrix, Allocation
from fairpy.items.bag_filling import Bag, SequentialAllocation

from typing import List

import logging
logger = logging.getLogger(__name__)

@convert_input_to_valuation_matrix
def bidirectional_bag_filling(instance, thresholds:List[float]) -> Allocation:
	"""
	Runs a bi-directional bag-filling algorithm.
	Assumes that the instance is ordered: item 0 is the highest-valued for all agents, then item 1, etc.

	>>> identical_valuations = [97,96,90,12,3,2,1,1,1]
	>>> valuation_matrix = [identical_valuations for _ in range(3)]
	>>> bidirectional_bag_filling(valuation_matrix, thresholds=[100,100,100])
	Agent #0 gets {0,6,7,8} with value 100.
	Agent #1 gets {1,4,5} with value 101.
	Agent #2 gets {2,3} with value 102.
	<BLANKLINE>
	>>> bidirectional_bag_filling(valuation_matrix, thresholds=[101,101,101])
	Agent #0 gets {0,5,6,7,8} with value 102.
	Agent #1 gets {1,3,4} with value 111.
	Agent #2 gets {} with value 0.
	<BLANKLINE>
	"""
	valuation_matrix = instance
	valuation_matrix.verify_ordered()
	if len(thresholds) != valuation_matrix.num_of_agents:
		raise ValueError(f"Number of valuations {valuation_matrix.num_of_agents} differs from number of thresholds {len(thresholds)}")
	allocation = SequentialAllocation(valuation_matrix.agents(), valuation_matrix.objects(), logger)
	bag = Bag(valuation_matrix, thresholds)
	while True:
		if len(allocation.remaining_objects)==0:  break

		# Initialize a bag with the highest-valued object:
		highest_valued_object = allocation.remaining_objects[0]
		bag.append(highest_valued_object)

		# Fill the bag with the lowest-valued objects:
		lowest_valued_objects = reversed(allocation.remaining_objects[1:])
		(willing_agent, allocated_objects) = bag.fill(lowest_valued_objects, allocation.remaining_agents)
		if willing_agent is None: break
		allocation.let_agent_get_objects(willing_agent, allocated_objects)
		bag.reset()
	return allocation.bundles
	



if __name__ == "__main__":
	# import sys
	# logger.addHandler(logging.StreamHandler(sys.stdout))
	# logger.setLevel(logging.INFO)

	# import fairpy.items.bag_filling as bag_filling
	# bag_filling.logger.addHandler(logging.StreamHandler(sys.stdout))
	# bag_filling.logger.setLevel(logging.INFO)
	
	import doctest
	(failures,tests) = doctest.testmod(report=True)
	print ("{} failures, {} tests".format(failures,tests))
