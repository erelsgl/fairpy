#!python3
"""
Calculate the maximin-share of an additive valuation function.

Author: Erel Segal-Halevi
Since : 2021-04
"""

from fairpy.indivisible import partitions 
import pulp
import numbers

def value_1_of_c_MMS__pulp(c:int, valuation:list, capacity=1, items:set=None)->int:
	"""
	Computes the 1-of-c MMS by solving an integer linear program, using PULP.
	Credit: https://or.stackexchange.com/a/6115/2576

	:param c: number of parts.
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
	min_value = pulp.LpVariable("min_value", cat=pulp.LpContinuous)
	vars:dict = {
		item:
		[pulp.LpVariable(f"x_{item}_{part}", lowBound=0, cat=pulp.LpInteger) for part in parts]
		for item in items
	}	# vars[i][j] is 1 iff item i is in part j.
	mms_problem = pulp.LpProblem("MMS_problem", pulp.LpMaximize)
	mms_problem += min_value    # Objective function: maximize min_value
	parts_values = [
		pulp.lpSum([vars[item][part]*valuation[item] for item in items])
		for part in parts]
	for item in items:  # Constraints: each item must be in exactly one part.
		mms_problem += (pulp.lpSum([vars[item][part] for part in parts]) == capacity[item])
	for part in parts:  # Constraint: the sum of each part must be at least min_value (by definition of min_value).
		mms_problem += (min_value <= parts_values[part])
	for part in range(c-1):  # Symmetry-breaking constraint: force value of parts to be in descending order
		mms_problem += (parts_values[part] >= parts_values[part+1])
	pulp.PULP_CBC_CMD(msg=False).solve(mms_problem)
	return min_value.value()


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



def value_1_of_c_MMS(c:int, valuation:list, capacity=1, items:set=None)->int:
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
	>>> int(value_1_of_c_MMS(c=5, valuation=[10,20,40,30]))
	0
	>>> int(value_1_of_c_MMS(c=2, valuation=[10,20,40,0], items=[1,2]))
	20
	>>> int(value_1_of_c_MMS(c=2, valuation=[10,20,40,0], capacity=2))
	70
	>>> int(value_1_of_c_MMS(c=2, valuation=[10,20,40,0], capacity=[2,1,1,0]))
	40
	"""
	# return value_1_of_c_MMS__bruteforce(c, valuation, items=items)
	return value_1_of_c_MMS__pulp(c, valuation, capacity=capacity, items=items)




if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
