#!python3

""" 
Find a fractionl allocation that maximizes a social welfare function (- a monotone function of the utilities),
     for agents with additive valuations.

Examples are: max-sum, max-product, max-min, and leximin.

Author: Erel Segal-Halevi
Since:  2021-05
"""

import numpy as np, cvxpy
from fairpy import valuations
from fairpy.items.allocations import AllocationMatrix
from fairpy.solve import maximize

import logging
logger = logging.getLogger(__name__)


def max_welfare_allocation(agents, welfare_function, welfare_constraint_function=None) -> AllocationMatrix:
	"""
	Find an allocation maximizing a given social welfare function. (aka Max Nash Welfare) allocation.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
	:param welfare_function:   a monotonically-increasing function w: R -> R representing the welfare function to maximize.
	:param welfare_constraint: a predicate w: R -> {true,false} representing an additional constraint on the utility of each agent.

	:return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.

	For usage examples, see the functions max_sum_allocation, max_product_allocation, max_minimum_allocation.
	"""
	v = valuations.matrix_from(agents)
	alloc = cvxpy.Variable((v.num_of_agents, v.num_of_objects))
	feasibility_constraints = [
		sum([alloc[i][o] for i in v.agents()])==1
		for o in v.objects()
	]
	positivity_constraints = [
		alloc[i][o] >= 0 for i in v.agents()
		for o in v.objects()
	]
	utilities = [sum([alloc[i][o]*v[i][o] for o in v.objects()]) for i in v.agents()]
	if welfare_constraint_function is not None:
		welfare_constraints = [welfare_constraint_function(utility) for utility in utilities]
	else:
		welfare_constraints = []
	max_welfare = maximize(welfare_function(utilities), feasibility_constraints+positivity_constraints+welfare_constraints)
	logger.info("Maximum welfare is %g",max_welfare)
	return AllocationMatrix(alloc.value)


def max_welfare_allocation_for_families(agents, families:list, welfare_function, welfare_constraint_function=None) -> AllocationMatrix:
	"""
	Find an allocation maximizing a given social welfare function. (aka Max Nash Welfare) allocation.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
	:param families: a list of lists. Each list represents a family and contains the indices of the agents in the family.
	:param welfare_function:   a monotonically-increasing function w: R -> R representing the welfare function to maximize.
	:param welfare_constraint: a predicate w: R -> {true,false} representing an additional constraint on the utility of each agent.

	:return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.

	For usage examples, see the function max_minimum_allocation_for_families.
	"""
	v = valuations.matrix_from(agents)
	num_of_families = len(families)
	map_agent_to_family = [None]*v.num_of_agents
	for f,family in enumerate(families):
		for agent in family:
			map_agent_to_family[agent] = f

	alloc = cvxpy.Variable((num_of_families, v.num_of_objects))
	feasibility_constraints = [
		sum([alloc[f][o] for f in range(num_of_families)])==1
		for o in v.objects()
	]
	positivity_constraints = [
		alloc[f][o] >= 0 for f in range(num_of_families)
		for o in v.objects()
	]
	utilities = [sum([alloc[map_agent_to_family[i]][o]*v[i][o] for o in v.objects()]) for i in v.agents()]

	if welfare_constraint_function is not None:
		welfare_constraints = [welfare_constraint_function(utility) for utility in utilities]
	else:
		welfare_constraints = []
	max_welfare = maximize(welfare_function(utilities), feasibility_constraints+positivity_constraints+welfare_constraints)
	logger.info("Maximum welfare is %g",max_welfare)
	return AllocationMatrix(alloc.value)




def max_sum_allocation(agents) -> AllocationMatrix:
	"""
	Find the max-sum (aka Utilitarian) allocation.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
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
		welfare_constraint_function=lambda utility: utility >= 0)


def max_power_sum_allocation(agents, power:float) -> AllocationMatrix:
	"""
	Find the maximum of sum of utility to the given power.
	* When power=1, it is equivalent to max-sum;
	* When power -> 0, it converges to max-product;
	* When power -> -infinity, it converges to leximin.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
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
	"""
	if power>0:
		welfare_function=lambda utilities: sum([utility**power for utility in utilities])
	elif power<0:
		welfare_function=lambda utilities: -sum([utility**power for utility in utilities])
	else:
		welfare_function=lambda utilities: sum([cvxpy.log(utility) for utility in utilities])
	return max_welfare_allocation(agents,
		welfare_function=welfare_function,
		welfare_constraint_function=lambda utility: utility >= 0)


def max_product_allocation(agents) -> AllocationMatrix:
	"""
	Find the max-product (aka Max Nash Welfare) allocation.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
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
		welfare_constraint_function=lambda utility: utility >= 0)


def max_minimum_allocation(agents) -> AllocationMatrix:
	"""
	Find the max-minimum (aka Egalitarian) allocation.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the leximin vector of utilities.
	>>> max_minimum_allocation([ [3] , [5] ]).round(3)   # single item
	[[0.625]
	 [0.375]]
	>>> max_minimum_allocation([ [4,2] , [1,4] ]).round(3)   # two different items
	[[1. 0.]
	 [0. 1.]]
	>>> alloc = max_minimum_allocation([ [3,3] , [1,1] ]).round(3)   # two identical items
	>>> [sum(alloc[i]) for i in alloc.agents()]
	[0.5, 1.5]
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
		welfare_constraint_function=lambda utility: utility >= 0)



def max_minimum_allocation_for_families(agents, families) -> AllocationMatrix:
	"""
	Find the max-minimum (aka Egalitarian) allocation.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
	:param families: a list of lists. Each list represents a family and contains the indices of the agents in the family.

	:return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the leximin vector of utilities.
	>>> families = [ [0], [1] ]  # two singleton families
	>>> max_minimum_allocation_for_families([ [3] , [5] ],families).round(3)
	[[0.625]
	 [0.375]]
	>>> max_minimum_allocation_for_families([ [4,2] , [1,4] ], families).round(3)   # two different items
	[[1. 0.]
	 [0. 1.]]
	>>> alloc = max_minimum_allocation_for_families([ [3,3] , [1,1] ], families).round(3)   # two identical items
	>>> [sum(alloc[i]) for i in alloc.agents()]
	[0.5, 1.5]
	>>> v = [ [4,2] , [1,3] ]   # two different items
	>>> a = max_minimum_allocation_for_families(v, families).round(3)
	>>> a
	[[0.8 0. ]
	 [0.2 1. ]]
	>>> print(a.utility_profile(v))
	[3.2 3.2]
	>>> families = [ [0, 1] ]  # One couple
	>>> max_minimum_allocation_for_families([ [4,2] , [1,4] ], families).round(3)  
	[[1. 1.]]
	"""
	return max_welfare_allocation_for_families(agents, families,
		welfare_function=lambda utilities: cvxpy.min(cvxpy.hstack(utilities)),
		welfare_constraint_function=lambda utility: utility >= 0)





###### LEXIMIN RULES


def leximin_optimal_allocation(agents) -> AllocationMatrix:
	"""
	Find the leximin-optimal (aka Egalitarian) allocation.
	--- DRAFT ---
	:param v: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the leximin vector of utilities.
	>>> v = [[5,0],[3,3]]
	>>> print(leximin_optimal_allocation(v).round(3).utility_profile(v))
	[3.75 3.75]
	>>> v = [[3,0],[5,5]]
	>>> print(leximin_optimal_allocation(v).round(3).utility_profile(v))
	[3. 5.]
	>>> v = [[3,0,0],[0,4,0],[5,5,5]]
	>>> print(leximin_optimal_allocation(v).round(3).utility_profile(v))
	[3. 4. 5.]
	"""
	v = valuations.matrix_from(agents)
	alloc = cvxpy.Variable((v.num_of_agents, v.num_of_objects))
	feasibility_constraints = [
		sum([alloc[i][o] for i in v.agents()])==1
		for o in v.objects()
	]
	positivity_constraints = [
		alloc[i][o] >= 0 for i in v.agents()
		for o in v.objects()
	]
	utilities = [sum([alloc[i][o]*v[i][o] for o in v.objects()]) for i in v.agents()]

	def max_minimum_with_fixed_agents(map_fixed_agent_to_fixed_utility:dict):
		fixed_agents = map_fixed_agent_to_fixed_utility.keys()
		non_fixed_agents = [i for i in v.agents() if i not in fixed_agents]
		min_utility_for_non_fixed_agens = cvxpy.Variable()
		order_constraints_for_fixed_agents = [
			utilities[i] >= map_fixed_agent_to_fixed_utility[i]
			for i in fixed_agents
		]
		order_constraints_for_non_fixed_agents = [
			utilities[i] >= min_utility_for_non_fixed_agens
			for i in non_fixed_agents
		]
		order_constraints = order_constraints_for_fixed_agents + order_constraints_for_non_fixed_agents
		return maximize(min_utility_for_non_fixed_agens, feasibility_constraints + positivity_constraints + order_constraints)

	active_agents = list(v.agents())
	map_fixed_agent_to_fixed_utility = {}
	min_utility_for_active_agents = max_minimum_with_fixed_agents({})
	active_allocation = alloc.value
	logger.info(f"Min utility for all agents {active_agents}: {min_utility_for_active_agents}")
	if len(active_agents)<=1:
		return AllocationMatrix(alloc.value)

	while True:
		map_scapegoat_to_minvalue_without_scapegoat = {}
		map_scapegoat_to_allocation_without_scapegoat = {}
		for scapegoat in active_agents:
			min_utility_without_scapegoat = max_minimum_with_fixed_agents({**map_fixed_agent_to_fixed_utility, scapegoat:min_utility_for_active_agents})
			logger.info(f"Min utility without {scapegoat}: {min_utility_without_scapegoat}")
			map_scapegoat_to_minvalue_without_scapegoat[scapegoat] = min_utility_without_scapegoat
			map_scapegoat_to_allocation_without_scapegoat[scapegoat] = alloc.value
		best_scapegoat = max(active_agents, key=lambda i: map_scapegoat_to_minvalue_without_scapegoat[i])
		best_utility_without_scapegoat = map_scapegoat_to_minvalue_without_scapegoat[best_scapegoat]
		best_allocation_without_scapegoat = map_scapegoat_to_allocation_without_scapegoat[best_scapegoat]
		if best_utility_without_scapegoat > min_utility_for_active_agents:
			logger.info(f"Best scapegoat is {best_scapegoat}: fixing its utility to {min_utility_for_active_agents}, and increasing the others' min utility to {best_utility_without_scapegoat}.")
			map_fixed_agent_to_fixed_utility[best_scapegoat] = min_utility_for_active_agents
			min_utility_for_active_agents = best_utility_without_scapegoat
			active_allocation = best_allocation_without_scapegoat
			active_agents = [i for i in active_agents if i!=best_scapegoat]
			if len(active_agents)<=1: 
				map_fixed_agent_to_fixed_utility[active_agents[0]] = best_utility_without_scapegoat
				logger.info(f"Only one agent remains - keeping the utility profile {map_fixed_agent_to_fixed_utility}.\n")
				break
		else:
			for i in active_agents:
				map_fixed_agent_to_fixed_utility[i] = min_utility_for_active_agents
			logger.info(f"No scapegoat improves the current utility - keeping the utility profile {map_fixed_agent_to_fixed_utility}.\n")
			break

	return AllocationMatrix(active_allocation)


def leximin_optimal_allocation_for_families(agents, families:list) -> AllocationMatrix:
	"""
	Find the leximin-optimal (aka Egalitarian) allocation among families.
	:param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
	:param families: a list of lists. Each list represents a family and contains the indices of the agents in the family.

	:return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the leximin vector of utilities.
	>>> families = [ [0], [1] ]  # two singleton families
	>>> v = [[5,0],[3,3]]
	>>> print(leximin_optimal_allocation_for_families(v,families).round(3).utility_profile_for_families(v,families))
	[3.75 3.75]
	>>> v = [[3,0],[5,5]]
	>>> print(leximin_optimal_allocation_for_families(v,families).round(3).utility_profile_for_families(v,families))
	[3. 5.]
	>>> families = [ [0], [1], [2] ]  # three singleton families
	>>> v = [[3,0,0],[0,4,0],[5,5,5]]
	>>> print(leximin_optimal_allocation_for_families(v,families).round(3).utility_profile_for_families(v,families))
	[3. 4. 5.]
	>>> families = [ [0, 1], [2] ]  
	>>> print(leximin_optimal_allocation_for_families(v,families).round(3).utility_profile_for_families(v,families))
	[3. 4. 5.]
	>>> families = [ [0], [1,2] ]  
	>>> print(leximin_optimal_allocation_for_families(v,families).round(3).utility_profile_for_families(v,families))
	[ 3.  4. 10.]
	>>> families = [ [1], [0,2] ]  
	>>> print(leximin_optimal_allocation_for_families(v,families).round(3).utility_profile_for_families(v,families))
	[ 3.  4. 10.]
	"""
	v = valuations.matrix_from(agents)
	num_of_families = len(families)
	map_agent_to_family = [None]*v.num_of_agents
	for f,family in enumerate(families):
		for agent in family:
			map_agent_to_family[agent] = f

	logger.info("map_agent_to_family = %s",map_agent_to_family)
	alloc = cvxpy.Variable((num_of_families, v.num_of_objects))
	feasibility_constraints = [
		sum([alloc[f][o] for f in range(num_of_families)])==1
		for o in v.objects()
	]
	positivity_constraints = [
		alloc[f][o] >= 0 for f in range(num_of_families)
		for o in v.objects()
	]
	utilities = [sum([alloc[map_agent_to_family[i]][o]*v[i][o] for o in v.objects()]) for i in v.agents()]

	def max_minimum_with_fixed_agents(map_fixed_agent_to_fixed_utility:dict):
		fixed_agents = map_fixed_agent_to_fixed_utility.keys()
		non_fixed_agents = [i for i in v.agents() if i not in fixed_agents]
		min_utility_for_non_fixed_agens = cvxpy.Variable()
		order_constraints_for_fixed_agents = [
			utilities[i] >= map_fixed_agent_to_fixed_utility[i]
			for i in fixed_agents
		]
		order_constraints_for_non_fixed_agents = [
			utilities[i] >= min_utility_for_non_fixed_agens
			for i in non_fixed_agents
		]
		order_constraints = order_constraints_for_fixed_agents + order_constraints_for_non_fixed_agents
		return maximize(min_utility_for_non_fixed_agens, feasibility_constraints + positivity_constraints + order_constraints)

	active_agents = list(v.agents())
	map_fixed_agent_to_fixed_utility = {}
	min_utility_for_active_agents = max_minimum_with_fixed_agents({})
	active_allocation = alloc.value
	logger.info(f"Min utility for all agents {active_agents}: {min_utility_for_active_agents}")
	if len(active_agents)<=1:
		return AllocationMatrix(alloc.value)

	while True:
		map_scapegoat_to_minvalue_without_scapegoat = {}
		map_scapegoat_to_allocation_without_scapegoat = {}
		for scapegoat in active_agents:
			min_utility_without_scapegoat = max_minimum_with_fixed_agents({**map_fixed_agent_to_fixed_utility, scapegoat:min_utility_for_active_agents})
			logger.info(f"Min utility without {scapegoat}: {min_utility_without_scapegoat}")
			map_scapegoat_to_minvalue_without_scapegoat[scapegoat] = min_utility_without_scapegoat
			map_scapegoat_to_allocation_without_scapegoat[scapegoat] = alloc.value
		best_scapegoat = max(active_agents, key=lambda i: map_scapegoat_to_minvalue_without_scapegoat[i])
		best_utility_without_scapegoat = map_scapegoat_to_minvalue_without_scapegoat[best_scapegoat]
		best_allocation_without_scapegoat = map_scapegoat_to_allocation_without_scapegoat[best_scapegoat]
		if best_utility_without_scapegoat > min_utility_for_active_agents:
			logger.info(f"Best scapegoat is {best_scapegoat}: fixing its utility to {min_utility_for_active_agents}, and increasing the others' min utility to {best_utility_without_scapegoat}.")
			map_fixed_agent_to_fixed_utility[best_scapegoat] = min_utility_for_active_agents
			min_utility_for_active_agents = best_utility_without_scapegoat
			active_allocation = best_allocation_without_scapegoat
			active_agents = [i for i in active_agents if i!=best_scapegoat]
			if len(active_agents)<=1: 
				map_fixed_agent_to_fixed_utility[active_agents[0]] = best_utility_without_scapegoat
				logger.info(f"Only one agent remains - keeping the utility profile {map_fixed_agent_to_fixed_utility}.\n")
				break
		else:
			for i in active_agents:
				map_fixed_agent_to_fixed_utility[i] = min_utility_for_active_agents
			logger.info(f"No scapegoat improves the current utility - keeping the utility profile {map_fixed_agent_to_fixed_utility}.\n")
			break

	return AllocationMatrix(active_allocation)






if __name__ == '__main__':
	import sys
	logger.addHandler(logging.StreamHandler(sys.stdout))
	# logger.setLevel(logging.INFO)

	from fairpy import solve
	solve.logger.addHandler(logging.StreamHandler(sys.stdout))
	# solve.logger.setLevel(logging.INFO)

	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))
