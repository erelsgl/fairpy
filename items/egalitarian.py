#!python3

""" 
Find fractional egalitarian allocations for agents with additive valuations:
* maximin-optimal 
* leximin-optimal (future work).

Author: Erel Segal-Halevi
Since:  2021-05
"""

import numpy as np, cvxpy
from fairpy import valuations
from fairpy.items.allocations import AllocationMatrix
from fairpy.items.solvers import solve

def maximin_optimal_allocation(agents) -> AllocationMatrix:
	"""
	Find the maximin-optimal (aka Egalitarian) allocation.
	:param v: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix z of a similar shape in which z[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the leximin vector of utilities.
	>>> maximin_optimal_allocation([ [3] , [5] ]).round(3)   # single item
	[[0.625]
	 [0.375]]
	>>> maximin_optimal_allocation([ [3,3] , [1,1] ]).round(3)   # two identical items
	[[0.25 0.25]
	 [0.75 0.75]]
	>>> maximin_optimal_allocation([ [4,2] , [1,4] ]).round(3)   # two different items
	[[1. 0.]
	 [0. 1.]]
	>>> v = [ [4,2] , [1,3] ]   # two different items
	>>> a = maximin_optimal_allocation(v).round(3)
	>>> a
	[[0.8 0. ]
	 [0.2 1. ]]
	>>> print(a.utility_profile(v))
	[3.2 3.2]
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
	min_utility = cvxpy.Variable()
	order_constraints = [
		utilities[i] >= min_utility 
		for i in v.agents()
	]

	prob = cvxpy.Problem(
		cvxpy.Maximize(min_utility),
		feasibility_constraints + positivity_constraints + order_constraints)
	solve(prob, solvers=[cvxpy.XPRESS,cvxpy.OSQP,cvxpy.SCS])
	return AllocationMatrix(z.value)



def maximin_optimal_allocation_for_families(agents, families:list) -> AllocationMatrix:
	"""
	Find the maximin-optimal (aka Egalitarian) allocation among families.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
	:param families: a list of lists. Each list represents a family and contains the indices of the agents in the family.

	:return allocation_matrix:  a matrix z of a similar shape in which z[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the leximin vector of utilities.
	>>> families = [ [0], [1] ]  # two singleton families
	>>> maximin_optimal_allocation_for_families([ [3] , [5] ], families).round(3)   
	[[0.625]
	 [0.375]]
	>>> maximin_optimal_allocation_for_families([ [3,3] , [1,1] ], families).round(3)   # two identical items
	[[0.25 0.25]
	 [0.75 0.75]]
	>>> maximin_optimal_allocation_for_families([ [4,2] , [1,4] ], families).round(3)   # two different items
	[[1. 0.]
	 [0. 1.]]
	>>> v = [ [4,2] , [1,3] ]   # two different items
	>>> a = maximin_optimal_allocation_for_families(v, families).round(3)
	>>> a
	[[0.8 0. ]
	 [0.2 1. ]]
	>>> print(a.utility_profile(v))
	[3.2 3.2]
	>>> families = [ [0, 1] ]  # One couple
	>>> maximin_optimal_allocation_for_families([ [4,2] , [1,4] ], families).round(3)  
	[[1. 1.]]
	"""
	v = valuations.matrix_from(agents)

	num_of_families = len(families)
	map_agent_to_family = [None]*v.num_of_agents
	for f,family in enumerate(families):
		for agent in family:
			map_agent_to_family[agent] = f

	z = cvxpy.Variable((num_of_families, v.num_of_objects))
	feasibility_constraints = [
		sum([z[f][o] for f in range(num_of_families)])==1
		for o in v.objects()
	]
	positivity_constraints = [
		z[f][o] >= 0 for f in range(num_of_families)
		for o in v.objects()
	]

	utilities = [sum([z[map_agent_to_family[i]][o]*v[i][o] for o in v.objects()]) for i in v.agents()]
	min_utility = cvxpy.Variable()
	order_constraints = [
		utilities[i] >= min_utility 
		for i in v.agents()
	]
	prob = cvxpy.Problem(
		cvxpy.Maximize(min_utility),
		feasibility_constraints + positivity_constraints + order_constraints)
	solve(prob, solvers=[cvxpy.XPRESS,cvxpy.OSQP,cvxpy.SCS])
	return AllocationMatrix(z.value)




if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
