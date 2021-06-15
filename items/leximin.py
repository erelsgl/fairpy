#!python3

""" 
Find a fractionl allocation that maximizes the leximin vector.

See also: [max_welfare.py](max_welfare.py).

Author: Erel Segal-Halevi
  I am grateful to Sylvain Bouveret for his help with the algorithm. All errors and bugs are my own.

Since:  2021-05
"""

import numpy as np, cvxpy
from fairpy import valuations
from fairpy.items.allocations import AllocationMatrix
from fairpy.solve import maximize
from typing import List

import logging
logger = logging.getLogger(__name__)


##### Utility functions for comparing leximin vectors

def is_leximin_better(x:list, y:list):
	"""
	>>> is_leximin_better([6,2,4],[7,3,1])
	True
	>>> is_leximin_better([6,2,4],[3,3,3])
	False
	"""
	return sorted(x) > sorted(y)



##### Find a leximin-optimal allocation for individual agents


def leximin_optimal_allocation(agents) -> AllocationMatrix:
	"""
	Find the leximin-optimal (aka Egalitarian) allocation.
	--- DRAFT ---
	:param v: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

	:return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
	The allocation should maximize the leximin vector of utilities.
	>>> logger.setLevel(logging.WARNING)
	>>> v = [[5,0],[3,3]]
	>>> print(leximin_optimal_allocation(v).round(3).utility_profile(v))
	[3.75 3.75]
	>>> v = [[3,0],[5,5]]
	>>> print(leximin_optimal_allocation(v).round(3).utility_profile(v))
	[3. 5.]
	>>> v = [[5,5],[3,0]]
	>>> print(leximin_optimal_allocation(v).round(3).utility_profile(v))
	[5. 3.]
	>>> v = [[3,0,0],[0,4,0],[5,5,5]]
	>>> print(leximin_optimal_allocation(v).round(3).utility_profile(v))
	[3. 4. 5.]
	>>> v = [[4,0,0],[0,3,0],[5,5,10],[5,5,10]]
	>>> print(leximin_optimal_allocation(v).round(3).utility_profile(v))
	[4. 3. 5. 5.]
	>>> v = [[3,0,0],[0,3,0],[5,5,10],[5,5,10]]
	>>> print(leximin_optimal_allocation(v).round(3).utility_profile(v))
	[3. 3. 5. 5.]
	>>> logger.setLevel(logging.WARNING)
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
	leximin_optimal_allocation.num_of_calls_to_solver = 0  # for performance analysis

	def leximin_optimal_with_fixed_agents(map_fixed_agent_to_fixed_utility:dict, lower_bound_on_max_min_utility_for_free_agents:float)->AllocationMatrix:
		"""
		A subroutine that assumes that, for some subset of the agents, the utility is held fixed,
		  and subject to this, computes the leximin-optimal allocation for the other ("free") agents.
		:param map_fixed_agent_to_fixed_utility
		:param lower_bound_on_max_min_utility_for_free_agents: if the max-min-utility we find is smaller than this, we will stop and not proceed with the recursion.
		:return an AllocationMatrix.
		"""
		num_of_fixed_agents = len(map_fixed_agent_to_fixed_utility)
		spaces = "."*(2*num_of_fixed_agents) # for nice display in logs
		logger.info("%sComputing leximin-optimal allocation with fixed agents %s and lower-bound %g", spaces, map_fixed_agent_to_fixed_utility, lower_bound_on_max_min_utility_for_free_agents)
		order_constraints_for_fixed_agents = [
			utilities[i] == fixed_utility
			for i,fixed_utility in map_fixed_agent_to_fixed_utility.items()
		]
		free_agents = [i for i in v.agents() if i not in map_fixed_agent_to_fixed_utility]
		min_utility_for_free_agents = cvxpy.Variable()
		order_constraints_for_free_agents = [
			utilities[i] >= min_utility_for_free_agents
			for i in free_agents
		]
		order_constraints = order_constraints_for_fixed_agents + order_constraints_for_free_agents
		max_min_utility_for_free_agents = maximize(min_utility_for_free_agents, feasibility_constraints + positivity_constraints + order_constraints)
		leximin_optimal_allocation.num_of_calls_to_solver += 1
		logger.info("%sMax min value is %g.", spaces, max_min_utility_for_free_agents)
		if max_min_utility_for_free_agents <= lower_bound_on_max_min_utility_for_free_agents:
			logger.info("%s  It is smaller than the lower bound -- skipping.",spaces)
			return None, max_min_utility_for_free_agents
		if len(free_agents) <= 1: 
			map_fixed_agent_to_fixed_utility[free_agents[0]] = max_min_utility_for_free_agents
			logger.info("%sAll agents are fixed -- utility profile %s.",spaces,map_fixed_agent_to_fixed_utility)
			return AllocationMatrix(alloc.value), max_min_utility_for_free_agents

		# Else, find a "scapegoat" - an agent whose utility is kept fixed at the minimum,
		#       such that the other agents can get higher utilities.
		map_scapegoat_to_leximin_vector_without_scapegoat = {}
		map_scapegoat_to_allocation_without_scapegoat     = {}
		new_lower_bound_on_max_min_utility_for_free_agents = lower_bound_on_max_min_utility_for_free_agents
		for scapegoat in free_agents:
			new_map_fixed_agent_to_fixed_utility = {**map_fixed_agent_to_fixed_utility, scapegoat:max_min_utility_for_free_agents}
			logger.info("%sRecursively computing Leximin-optimal vector when agent #%d is fixed at utility %g:", spaces, scapegoat, max_min_utility_for_free_agents)
			leximin_allocation_without_scapegoat, max_min_utility_without_scapegoat = leximin_optimal_with_fixed_agents(new_map_fixed_agent_to_fixed_utility, new_lower_bound_on_max_min_utility_for_free_agents)
			if leximin_allocation_without_scapegoat is not None:
				new_lower_bound_on_max_min_utility_for_free_agents = max_min_utility_without_scapegoat
				leximin_vector_without_scapegoat = sorted(leximin_allocation_without_scapegoat.utility_profile(v))
				logger.info("%sLeximin-optimal vector when agent #%d is fixed at utility %g = %s", spaces, scapegoat, max_min_utility_for_free_agents ,leximin_vector_without_scapegoat)
				map_scapegoat_to_leximin_vector_without_scapegoat[scapegoat] = leximin_vector_without_scapegoat
				map_scapegoat_to_allocation_without_scapegoat[scapegoat] = leximin_allocation_without_scapegoat
		best_scapegoat = max(map_scapegoat_to_leximin_vector_without_scapegoat.keys(), key=lambda i: map_scapegoat_to_leximin_vector_without_scapegoat[i])
		best_allocation_without_scapegoat = map_scapegoat_to_allocation_without_scapegoat[best_scapegoat]
		logger.info("%sBest scapegoat is %d, with leximin vector %s",spaces, best_scapegoat, map_scapegoat_to_leximin_vector_without_scapegoat[best_scapegoat])
		return best_allocation_without_scapegoat, max_min_utility_for_free_agents


	# Call the recursive function with no fixed agents and lower bound = 0:
	allocation, _ = leximin_optimal_with_fixed_agents({}, 0)  
	logger.info("%d calls to solver.",leximin_optimal_allocation.num_of_calls_to_solver)
	return allocation



##### leximin for families - DRAFT - does not work in all cases

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
		min_utility_for_non_fixed_agents = cvxpy.Variable()
		order_constraints_for_fixed_agents = [
			utilities[i] >= map_fixed_agent_to_fixed_utility[i]
			for i in fixed_agents
		]
		order_constraints_for_non_fixed_agents = [
			utilities[i] >= min_utility_for_non_fixed_agents
			for i in non_fixed_agents
		]
		order_constraints = order_constraints_for_fixed_agents + order_constraints_for_non_fixed_agents
		return maximize(min_utility_for_non_fixed_agents, feasibility_constraints + positivity_constraints + order_constraints)

	free_agents = list(v.agents())
	map_fixed_agent_to_fixed_utility = {}
	min_utility_for_free_agents = max_minimum_with_fixed_agents({})
	active_allocation = alloc.value
	logger.info(f"Min utility for all agents {free_agents}: {min_utility_for_free_agents}")
	if len(free_agents)<=1:
		return AllocationMatrix(alloc.value)

	while True:
		map_scapegoat_to_minvalue_without_scapegoat = {}
		map_scapegoat_to_allocation_without_scapegoat = {}
		for scapegoat in free_agents:
			min_utility_without_scapegoat = max_minimum_with_fixed_agents({**map_fixed_agent_to_fixed_utility, scapegoat:min_utility_for_free_agents})
			logger.info(f"Min utility without {scapegoat}: {min_utility_without_scapegoat}")
			map_scapegoat_to_minvalue_without_scapegoat[scapegoat] = min_utility_without_scapegoat
			map_scapegoat_to_allocation_without_scapegoat[scapegoat] = alloc.value
		best_scapegoat = max(free_agents, key=lambda i: map_scapegoat_to_minvalue_without_scapegoat[i])
		best_utility_without_scapegoat = map_scapegoat_to_minvalue_without_scapegoat[best_scapegoat]
		best_allocation_without_scapegoat = map_scapegoat_to_allocation_without_scapegoat[best_scapegoat]
		if best_utility_without_scapegoat > min_utility_for_free_agents:
			logger.info(f"Best scapegoat is {best_scapegoat}: fixing its utility to {min_utility_for_free_agents}, and increasing the others' min utility to {best_utility_without_scapegoat}.")
			map_fixed_agent_to_fixed_utility[best_scapegoat] = min_utility_for_free_agents
			min_utility_for_free_agents = best_utility_without_scapegoat
			active_allocation = best_allocation_without_scapegoat
			free_agents = [i for i in free_agents if i!=best_scapegoat]
			if len(free_agents)<=1: 
				map_fixed_agent_to_fixed_utility[free_agents[0]] = best_utility_without_scapegoat
				logger.info(f"Only one agent remains - keeping the utility profile {map_fixed_agent_to_fixed_utility}.\n")
				break
		else:
			for i in free_agents:
				map_fixed_agent_to_fixed_utility[i] = min_utility_for_free_agents
			logger.info(f"No scapegoat improves the current utility - keeping the utility profile {map_fixed_agent_to_fixed_utility}.\n")
			break

	return AllocationMatrix(active_allocation)



if __name__ == '__main__':
	import sys
	logger.addHandler(logging.StreamHandler(sys.stdout))
	logger.setLevel(logging.INFO)

	from fairpy import solve
	solve.logger.addHandler(logging.StreamHandler(sys.stdout))
	# solve.logger.setLevel(logging.INFO)

	# v = [[3,0,0],[0,4,0],[5,5,10],[5,5,10],[5,5,10]]
	# v = [[3,0],[5,5]]
	# v = [[3,0,0],[0,4,0],[5,5,5]]
	# v = [[3,0,0],[0,4,0],[5,5,10],[5,5,10]]
	# v = [[4,0,0],[0,3,0],[5,5,10],[5,5,10]]
	# print(leximin_optimal_allocation(v).round(3).utility_profile(v))

	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))
