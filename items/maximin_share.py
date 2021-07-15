#!python3
"""
Calculate the maximin-share of an additive valuation function.

Author: Erel Segal-Halevi
Since : 2021-04
"""

import cvxpy
from fairpy.items import partitions 
from fairpy.solve import *
import numbers

import logging
logger = logging.getLogger(__name__)


def value_1_of_c_MMS__cvxpy(c:int, valuation:list, capacity=1, items:set=None, numerator:int=1, show_solver_log=False)->int:
	"""
	Computes the 1-of-c MMS by solving an integer linear program, using CVXPY.
	Credit: Rob Pratt, https://or.stackexchange.com/a/6115/2576

	:param c: number of parts in the partition.
	:param numerator: number of parts that the agent is allowed to take (default: 1).
	:param valuation: maps an item to its value.
	:param capacity: The capacity of all items (int), or a map from an item to its capacity (list). Default: 1.
	:param items: a set of items. Default: all items.
	:return the value off the 1-out-of-c MMS of the given items.
	"""
	parts = range(c)
	num_of_items = len(valuation)
	if items is None:
		items = range(num_of_items)
	if isinstance(capacity,numbers.Number):
		capacity = [capacity]*num_of_items

	min_value = cvxpy.Variable(nonneg=True)
	vars:dict = {
		item:
		[cvxpy.Variable(integer=True) for part in parts]
		for item in items
	}	# vars[i][j] is 1 iff item i is in part j.
	constraints = []
	parts_values = [
		sum([vars[item][part]*valuation[item] for item in items])
		for part in parts]

	constraints = []
	# Each variable must be non-negative
	constraints += [vars[item][part]  >= 0 for part in parts for item in items] 	
	# Each item must be in exactly one part:
	constraints += [sum([vars[item][part] for part in parts]) == capacity[item] for item in items] 	
	# Parts must be in descending order of value (a symmetry-breaker):
	constraints += [parts_values[part+1] >= parts_values[part] for part in range(c-1)]
	# The sum of each part must be at least min_value (by definition of min_value):
	constraints += [sum(parts_values[0:numerator]) >= min_value] 

	maximize(min_value, constraints)  # Solvers info: GLPK_MI is too slow; ECOS_BB gives wrong results even on simple problems; CBC is not installed; XPRESS gives an error

	parts_contents = [
		sum([int(vars[item][part].value)*[item] for item in items if vars[item][part].value>=1], [])
		for part in parts
	]
	logger.info("parts_contents: %s", parts_contents)
	logger.info("parts_values: %s", [parts_values[part].value for part in parts])
	return min_value.value



def value_of_bundle(valuation:list, bundle:list):
	return sum([valuation[item] for item in bundle])

def value_1_of_c_MMS__bruteforce(c:int, valuation:list, items:set=None)->int:
	"""
	Computes the 1-of-c MMS by brute force - enumerating all partitions.
	"""
	best_partition_value = -1
	for partition in partitions.partitions_to_exactly_c(items, c):
		partition_value = min([value_of_bundle(valuation,bundle) for bundle in partition])
		if best_partition_value < partition_value:
			best_partition_value = partition_value
	return best_partition_value



def value_1_of_c_MMS(c:int, valuation:list, **kwargs)->int:
	"""	
	Compute the of 1-of-c MMS of the given items, by the given valuation.
	>>> int(value_1_of_c_MMS(c=1, valuation=[10,20,40,0]))
	70
	>>> int(value_1_of_c_MMS(c=2, valuation=[10,20,40,0]))
	30
	>>> int(value_1_of_c_MMS(c=3, valuation=[10,20,40,0]))
	10
	>>> int(value_1_of_c_MMS(c=4, valuation=[10,20,40,0]))
	0
	>>> int(value_1_of_c_MMS(c=5, valuation=[10,20,40,0]))
	0
	>>> int(value_1_of_c_MMS(c=2, valuation=[10,20,40,0], items=[1,2]))
	20
	>>> int(value_1_of_c_MMS(c=2, valuation=[10,20,40,0], capacity=2))
	70
	>>> int(value_1_of_c_MMS(c=2, valuation=[10,20,40,0], capacity=[2,1,1,0]))
	40
	>>> int(value_1_of_c_MMS(c=3, valuation=[10,20,40,0], numerator=2))
	30
	"""
	if len(valuation)==0:
		raise ValueError("Valuation is empty")
	# return value_1_of_c_MMS__bruteforce(c, valuation, items=items)
	return value_1_of_c_MMS__cvxpy(c, valuation, **kwargs)




if __name__ == "__main__":
	import sys
	logger.addHandler(logging.StreamHandler(sys.stdout))
	# logger.setLevel(logging.INFO)

	from fairpy import solve
	solve.logger.addHandler(logging.StreamHandler(sys.stdout))
	# solve.logger.setLevel(logging.INFO)			

	import doctest
	(failures,tests) = doctest.testmod(report=True,optionflags=doctest.FAIL_FAST + doctest.NORMALIZE_WHITESPACE)
	print ("{} failures, {} tests".format(failures,tests))

	valuation = [5, 5, 5, 7, 7, 7, 11, 17, 23, 23, 23, 31, 31, 31, 65]  # The APS example of Babaioff, Ezra and Feige (2021), Lemma C.3.
	c = 3
	print(value_1_of_c_MMS__cvxpy(c, valuation, show_solver_log=True))


