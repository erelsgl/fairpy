#!python3

""" 
Find a fractionl allocation that maximizes the leximin vector.
Based on:

Stephen J. Willson
["Fair Division Using Linear Programming"](https://swillson.public.iastate.edu/FairDivisionUsingLPUnpublished6.pdf)
* Part 6, pages 20--27.

Programmer: Erel Segal-Halevi.
  I am grateful to Sylvain Bouveret for his help with the algorithm. All errors and bugs are my own.

See also: [max_welfare.py](max_welfare.py).

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


TOLERANCE_FACTOR=1.001  # for comparing floating-point numbers


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

	# Initially all agents are free - no agent is saturated:
	free_agents = list(v.agents())
	map_saturated_agent_to_saturated_utility = v.num_of_agents * [None]
	order_constraints_for_saturated_agents = []

	while True:
		logger.info("Saturated utilities: %s.", map_saturated_agent_to_saturated_utility)
		min_utility_for_free_agents = cvxpy.Variable()
		order_constraints_for_free_agents = [
			utilities[i] >= min_utility_for_free_agents
			for i in free_agents
		]
		max_min_utility_for_free_agents = maximize(min_utility_for_free_agents, feasibility_constraints + positivity_constraints + order_constraints_for_saturated_agents + order_constraints_for_free_agents)
		utilities_in_max_min_allocation = [utilities[i].value for i in v.agents()]
		leximin_optimal_allocation.num_of_calls_to_solver += 1
		logger.info("  max min value: %g, utility-profile: %s", max_min_utility_for_free_agents, utilities_in_max_min_allocation)

		for ifree in free_agents:  # Find whether i's utility can be improved
			if utilities_in_max_min_allocation[ifree] > TOLERANCE_FACTOR*max_min_utility_for_free_agents:
				logger.info("  Max utility of agent #%d is at least %g: agent remains free.", ifree, utilities_in_max_min_allocation[ifree])
				continue
			new_order_constraints_for_free_agents = [
				utilities[i] >= max_min_utility_for_free_agents
				for i in free_agents if i!=ifree
			]
			max_utility_for_ifree = maximize(utilities[ifree], feasibility_constraints + positivity_constraints + order_constraints_for_saturated_agents + new_order_constraints_for_free_agents)
			leximin_optimal_allocation.num_of_calls_to_solver += 1
			if max_utility_for_ifree > TOLERANCE_FACTOR*max_min_utility_for_free_agents:
				logger.info("  Max utility of agent #%d is %g: agent remains free.", ifree, max_utility_for_ifree)
				continue
			logger.info("  Max utility of agent #%d is %g: agent becomes saturated.", ifree, max_utility_for_ifree)
			map_saturated_agent_to_saturated_utility[ifree] = max_min_utility_for_free_agents
			order_constraints_for_saturated_agents.append(utilities[ifree] >= max_min_utility_for_free_agents)

		free_agents = [i for i in v.agents() if map_saturated_agent_to_saturated_utility[i] is None]
		if len(free_agents)==0:
			logger.info("All agents are saturated -- utility profile is %s.",map_saturated_agent_to_saturated_utility)
			logger.info("%d calls to solver.",leximin_optimal_allocation.num_of_calls_to_solver)
			return  AllocationMatrix(alloc.value)




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

	def max_minimum_with_saturated_agents(map_saturated_agent_to_saturated_utility:dict):
		saturated_agents = map_saturated_agent_to_saturated_utility.keys()
		non_saturated_agents = [i for i in v.agents() if i not in saturated_agents]
		min_utility_for_non_saturated_agents = cvxpy.Variable()
		order_constraints_for_saturated_agents = [
			utilities[i] >= map_saturated_agent_to_saturated_utility[i]
			for i in saturated_agents
		]
		order_constraints_for_non_saturated_agents = [
			utilities[i] >= min_utility_for_non_saturated_agents
			for i in non_saturated_agents
		]
		order_constraints = order_constraints_for_saturated_agents + order_constraints_for_non_saturated_agents
		return maximize(min_utility_for_non_saturated_agents, feasibility_constraints + positivity_constraints + order_constraints)

	free_agents = list(v.agents())
	map_saturated_agent_to_saturated_utility = {}
	min_utility_for_free_agents = max_minimum_with_saturated_agents({})
	active_allocation = alloc.value
	logger.info(f"Min utility for all agents {free_agents}: {min_utility_for_free_agents}")
	if len(free_agents)<=1:
		return AllocationMatrix(alloc.value)

	while True:
		map_scapegoat_to_minvalue_without_scapegoat = {}
		map_scapegoat_to_allocation_without_scapegoat = {}
		for scapegoat in free_agents:
			min_utility_without_scapegoat = max_minimum_with_saturated_agents({**map_saturated_agent_to_saturated_utility, scapegoat:min_utility_for_free_agents})
			logger.info(f"Min utility without {scapegoat}: {min_utility_without_scapegoat}")
			map_scapegoat_to_minvalue_without_scapegoat[scapegoat] = min_utility_without_scapegoat
			map_scapegoat_to_allocation_without_scapegoat[scapegoat] = alloc.value
		best_scapegoat = max(free_agents, key=lambda i: map_scapegoat_to_minvalue_without_scapegoat[i])
		best_utility_without_scapegoat = map_scapegoat_to_minvalue_without_scapegoat[best_scapegoat]
		best_allocation_without_scapegoat = map_scapegoat_to_allocation_without_scapegoat[best_scapegoat]
		if best_utility_without_scapegoat > min_utility_for_free_agents:
			logger.info(f"Best scapegoat is {best_scapegoat}: fixing its utility to {min_utility_for_free_agents}, and increasing the others' min utility to {best_utility_without_scapegoat}.")
			map_saturated_agent_to_saturated_utility[best_scapegoat] = min_utility_for_free_agents
			min_utility_for_free_agents = best_utility_without_scapegoat
			active_allocation = best_allocation_without_scapegoat
			free_agents = [i for i in free_agents if i!=best_scapegoat]
			if len(free_agents)<=1: 
				map_saturated_agent_to_saturated_utility[free_agents[0]] = best_utility_without_scapegoat
				logger.info(f"Only one agent remains - keeping the utility profile {map_saturated_agent_to_saturated_utility}.\n")
				break
		else:
			for i in free_agents:
				map_saturated_agent_to_saturated_utility[i] = min_utility_for_free_agents
			logger.info(f"No scapegoat improves the current utility - keeping the utility profile {map_saturated_agent_to_saturated_utility}.\n")
			break

	return AllocationMatrix(active_allocation)



if __name__ == '__main__':
	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))
