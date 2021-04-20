#!python3
"""
Calculate the maximin-share of an additive valuation function.

Author: Erel Segal-Halevi
Since : 2021-04
"""

from fairpy.indivisible import partitions 
import pulp

def value_1_of_c_MMS__pulp(valuation:list, items:list, c:int)->int:
	"""
	Computes the 1-of-c MMS by solving an integer linear program, using PULP.
	Credit: https://or.stackexchange.com/a/6115/2576
	"""
	parts = range(c)
	min_value = pulp.LpVariable("min_value", cat=pulp.LpContinuous)
	vars = [
		[pulp.LpVariable(f"x_{item}_{part}", lowBound=0, upBound=1, cat=pulp.LpInteger)
		for part in parts]
		for item in items
	]	# vars[i][j] is 1 iff item i is in part j.
	mms_problem = pulp.LpProblem("MMS_problem", pulp.LpMaximize)
	mms_problem += min_value    # Objective function
	for item in items:  # Add a feasiblity constraint for each item
		mms_problem += pulp.lpSum([vars[item][part] for part in parts]) == 1	
	for part in parts:  # Add a feasiblity constraint for each item
		mms_problem += min_value <= pulp.lpSum([vars[item][part]*valuation[item] for item in items])
	pulp.PULP_CBC_CMD(msg=False).solve(mms_problem)
	return min_value.value()


def value_of_bundle(valuation:list, bundle:list):
	return sum([valuation[item] for item in bundle])


def value_1_of_c_MMS__bruteforce(valuation:list, items:list, c:int)->int:
	"""
	Computes the 1-of-c MMS by brute force - enumerating all partitions.
	"""
	best_partition_value = -1
	for partition in partitions.partitions_to_exactly_c(items, c):
		partition_value = min([value_of_bundle(valuation,bundle) for bundle in partition])
		if best_partition_value < partition_value:
			best_partition_value = partition_value
	return best_partition_value



def value_1_of_c_MMS(valuation:list, items:list, c:int)->int:
	"""	
	Compute the of 1-of-c MMS of the given items, by the given valuation.
	>>> int(value_1_of_c_MMS([10,20,40,0], list(range(4)), c=1))
	70
	>>> int(value_1_of_c_MMS([10,20,40,0], list(range(4)), c=2))
	30
	>>> int(value_1_of_c_MMS([10,20,40,0], list(range(4)), c=3))
	10
	>>> int(value_1_of_c_MMS([10,20,40,0], list(range(4)), c=4))
	0
	"""
	# return value_1_of_c_MMS__bruteforce(valuation, items, c)
	return value_1_of_c_MMS__pulp(valuation, items, c)




if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
