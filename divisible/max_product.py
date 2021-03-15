#!python3

""" 
Find the fractional max-product (aka Max Nash Welfare) allocation.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import numpy as np, cvxpy
from fairpy.divisible.ValuationMatrix import ValuationMatrix
from fairpy.divisible.AllocationMatrix import AllocationMatrix

def max_product_allocation(v: ValuationMatrix, num_of_decimal_digits=3) -> AllocationMatrix:
	"""
	Find the max-product (aka Max Nash Welfare) allocation.
	:param v: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix z of a similar shape in which z[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the product (= sum of logs) of utilities
	>>> max_product_allocation([ [3] , [5] ]).round(3)   # single item
	[[0.5]
	 [0.5]]
	>>> max_product_allocation([ [3,3] , [1,1] ]).round(3)   # two identical items
	[[0.5 0.5]
	 [0.5 0.5]]
	>>> max_product_allocation([ [3,2] , [1,4] ]).round(3)   # two different items
	[[1. 0.]
	 [0. 1.]]
	"""
	v = ValuationMatrix(v)
	z = cvxpy.Variable((v.num_of_agents, v.num_of_objects))
	feasibility_constraints = [
		sum([z[i][o] for i in v.agents()])==1
		for o in v.objects()
	]
	positivity_constraints = [
		z[i][o] >= 0 for i in v.agents()
		for o in v.objects()
	]
	sum_of_logs = sum([
		cvxpy.log( sum([z[i][o]*v[i][o] for o in v.objects()]) )
		for i in v.agents()
	])
	prob = cvxpy.Problem(
		cvxpy.Maximize(sum_of_logs),
		feasibility_constraints + positivity_constraints)
	prob.solve()
	if prob.status == "infeasible":
		raise ValueError("Problem is infeasible")
	elif prob.status == "unbounded":
		raise ValueError("Problem is unbounded")
	else:
		return AllocationMatrix(z.value).round(num_of_decimal_digits)



def product_of_utilities(z:AllocationMatrix, v:ValuationMatrix)->float:
	"""
	Calculate the product of utilities of the given allocation, w.r.t. the given valuations.

	>>> alloc1 = AllocationMatrix([[1,0],[0,1]])
	>>> val1   = ValuationMatrix([[2,3],[4,5]])
	>>> np.round(product_of_utilities(alloc1, val1),2)
	10.0
	>>> val2   = ValuationMatrix([[3,2],[5,4]])
	>>> np.round(product_of_utilities(alloc1, val2),2)
	12.0
	"""
	sum_of_logs = sum([
		np.log(sum([v[i][o]*z[i][o] for o in v.objects()]))
		for i in v.agents()
	])
	return np.exp(sum_of_logs)

if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
