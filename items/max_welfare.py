#!python3

""" 
Find a fractionl allocation that maximizes a social welfare function (- a monotone function of the utilities),
     for agents with additive valuations.

Examples are: max-sum, max-product and max-min.

Author: Erel Segal-Halevi
Since:  2021-05
"""

import numpy as np, cvxpy
from fairpy import valuations
from fairpy.items.allocations import AllocationMatrix
from fairpy.items.solvers import solve


DEFAULT_SOLVERS=[cvxpy.XPRESS, cvxpy.OSQP, cvxpy.SCS]


def max_welfare_allocation(agents, welfare_function, welfare_constraint_function=None, solvers=DEFAULT_SOLVERS) -> AllocationMatrix:
	"""
	Find an allocation maximizing a given social welfare function. (aka Max Nash Welfare) allocation.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
	:param welfare_function:   a monotonically-increasing function w: R -> R representing the welfare function to maximize.
	:param welfare_constraint: a predicate w: R -> {true,false} representing an additional constraint on the utility of each agent.

	:return allocation_matrix:  a matrix z of a similar shape in which z[i][j] is the fraction allocated to agent i from object j.

	For usage examples, see the functions max_sum_allocation, max_product_allocation, max_minimum_allocation.

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
	if welfare_constraint_function is not None:
		welfare_constraints = [welfare_constraint_function(utility) for utility in utilities]
	else:
		welfare_constraints = []
	social_welfare = welfare_function(utilities)
	prob = cvxpy.Problem(
		cvxpy.Maximize(social_welfare),
		feasibility_constraints + positivity_constraints + welfare_constraints)
	solve(prob, solvers=solvers)
	return AllocationMatrix(z.value)



def max_sum_allocation(agents, solvers=DEFAULT_SOLVERS) -> AllocationMatrix:
	"""
	Find the max-sum (aka Utilitarian) allocation.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix z of a similar shape in which z[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the product (= sum of logs) of utilities
	>>> max_sum_allocation([ [3] , [5] ]).round(3)   # single item
	[[0.]
	 [1.]]
	>>> max_sum_allocation([ [3,3] , [1,1] ]).round(3)   # two identical items
	[[1. 1.]
	 [0. 0.]]
	>>> max_sum_allocation([ [3,2] , [1,4] ]).round(3)   # two different items
	[[1. 0.]
	 [0. 1.]]
	"""
	return max_welfare_allocation(agents,
		welfare_function=lambda utilities: sum(utilities),
		welfare_constraint_function=lambda utility: utility >= 0,
		solvers=solvers)


def max_power_sum_allocation(agents, power:float, solvers=DEFAULT_SOLVERS) -> AllocationMatrix:
	"""
	Find the maximum of sum of utility to the given power.
	* When power=1, it is equivalent to max-sum;
	* When power -> 0, it converges to max-product;
	* When power -> -infinity, it converges to leximin.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix z of a similar shape in which z[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the product (= sum of logs) of utilities
	>>> max_power_sum_allocation([ [3] , [5] ], 1).round(3)   
	[[0.]
	 [1.]]
	>>> max_power_sum_allocation([ [3] , [5] ], 0.1).round(3)   
	[[0.486]
	 [0.514]]
	>>> max_power_sum_allocation([ [3] , [5] ], 0).round(3)   
	[[0.5]
	 [0.5]]
	>>> max_power_sum_allocation([ [3] , [5] ], -0.1).round(3)   
	[[0.512]
	 [0.488]]
	>>> max_power_sum_allocation([ [3] , [5] ], -1).round(3)   
	[[0.564]
	 [0.436]]
	>>> max_power_sum_allocation([ [3] , [5] ], -100).round(3)   
	[[0.613]
	 [0.387]]
	"""
	if power>0:
		welfare_function=lambda utilities: sum([utility**power for utility in utilities])
	elif power<0:
		welfare_function=lambda utilities: -sum([utility**power for utility in utilities])
	else:
		welfare_function=lambda utilities: sum([cvxpy.log(utility) for utility in utilities])
	return max_welfare_allocation(agents,
		welfare_function=welfare_function,
		welfare_constraint_function=lambda utility: utility >= 0,
		solvers=solvers)


def max_product_allocation(agents, solvers=DEFAULT_SOLVERS) -> AllocationMatrix:
	"""
	Find the max-product (aka Max Nash Welfare) allocation.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

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
	return max_welfare_allocation(agents,
		welfare_function=lambda utilities: sum([cvxpy.log(utility) for utility in utilities]),
		welfare_constraint_function=lambda utility: utility >= 0,
		solvers=solvers)


def max_minimum_allocation(agents, solvers=DEFAULT_SOLVERS) -> AllocationMatrix:
	"""
	Find the max-minimum (aka Egalitarian) allocation.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix z of a similar shape in which z[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the leximin vector of utilities.
	>>> max_minimum_allocation([ [3] , [5] ]).round(3)   # single item
	[[0.625]
	 [0.375]]
	>>> max_minimum_allocation([ [3,3] , [1,1] ]).round(3)   # two identical items
	[[0.25 0.25]
	 [0.75 0.75]]
	>>> max_minimum_allocation([ [4,2] , [1,4] ]).round(3)   # two different items
	[[1. 0.]
	 [0. 1.]]
	>>> v = [ [4,2] , [1,3] ]   # two different items
	>>> a = max_minimum_allocation(v).round(3)
	>>> a
	[[0.8 0. ]
	 [0.2 1. ]]
	>>> print(a.utility_profile(v))
	[3.2 3.2]
	"""
	return max_welfare_allocation(agents,
		welfare_function=lambda utilities: cvxpy.min(cvxpy.hstack(utilities)),
		welfare_constraint_function=lambda utility: utility >= 0,
		solvers=solvers)




if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
