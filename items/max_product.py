#!python3

""" 
Find the fractional max-product (aka Max Nash Welfare) allocation
     for agents with additive valuations.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import numpy as np, cvxpy
from fairpy import valuations
from fairpy.items.allocations import AllocationMatrix
from fairpy.items.solvers import solve

def max_product_allocation(agents) -> AllocationMatrix:
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
	v = valuations.matrix_from(agents)
	z = cvxpy.Variable((v.num_of_agents, v.num_of_objects))
	feasibility_constraints = [
		sum([z[i][o] for i in v.agents()])==1
		for o in v.objects()
	]
	positivity_constraints = [
		z[i][o] >= 0 for i in v.agents()
		for o in v.objects()
	]
	utilities = [sum([z[i][o]*v[i][o] for o in v.objects()]) for i in v.agents()]
	sum_of_logs = sum([cvxpy.log(utility) for utility in utilities])
	prob = cvxpy.Problem(
		cvxpy.Maximize(sum_of_logs),
		feasibility_constraints + positivity_constraints)
	solve(prob, solvers=[cvxpy.XPRESS,cvxpy.OSQP,cvxpy.SCS])
	return AllocationMatrix(z.value)



def product_of_utilities(z:AllocationMatrix, v)->float:
	"""
	Calculate the product of utilities of the given allocation, w.r.t. the given valuations.

	>>> alloc1 = AllocationMatrix([[1,0],[0,1]])
	>>> val1   = valuations.matrix_from([[2,3],[4,5]])
	>>> np.round(product_of_utilities(alloc1, val1),2)
	10.0
	>>> val2   = valuations.matrix_from([[3,2],[5,4]])
	>>> np.round(product_of_utilities(alloc1, val2),2)
	12.0
	>>> alloc2 = AllocationMatrix([[0,0],[0,0]])
	>>> np.round(product_of_utilities(alloc2, val2),2)
	0.0
	"""
	utility_profile = z.utility_profile(v)
	with np.errstate(divide='ignore'): # ignore errors caused by log(0):
		sum_of_logs = sum([np.log(u) for u in utility_profile])
	return np.exp(sum_of_logs)


if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
