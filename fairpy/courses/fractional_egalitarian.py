"""
Implement a fractional egalitarian course allocation using linear programming.
Can be used as a basis for an almost-egalitarian allocation, using rounding.

Programmer: Erel Segal-Halevi.
Since: 2023-07
"""

from fairpy.courses.instance import Instance
from fairpy.courses.linear_programming_utils import allocation_variables, allocation_constraints

import cvxpy
from cvxpy_leximin import Problem, Leximin
from fairpy.solve import solve


import logging
logger = logging.getLogger(__name__)


def fractional_egalitarian_allocation(instance: Instance, normalize_utilities=True, **solver_options):
    """
    Find an egalitarian allocation - an allocation that maximizes the minimum utility.

    :param instance: a fair-course-allocation instance.
    :param normalize_utilities: True to use utilities normalized by the max possible agent value; False to use raw utilities.
    :param solver_options: kwargs sent to the cvxpy solver.

    :param instance: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param allocation_constraint_function: a predicate w: R -> {true,false} representing an additional constraint on the allocation variables.
    :param solver_options: kwargs sent to the cvxpy solver.

    :return a fractional allocation --- a dict of dicts, in which alloc[i][j] is the fraction allocated to agent i from object j.
    
    >>> logger.setLevel(logging.WARNING)
    >>> from fairpy.courses.allocation_utils import rounded_allocation

    >>> instance = Instance(valuations=[[5,0],[3,3]])
    >>> a = fractional_egalitarian_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 0.75, 1: 0.0}, 1: {0: 0.25, 1: 1.0}}
    """

    allocation_vars, raw_utilities, normalized_utilities = allocation_variables(instance)
    utilities = normalized_utilities if normalize_utilities else raw_utilities
    basic_constraints = allocation_constraints(instance, allocation_vars)

    # 1. Find the egalitarian value:
    min_utility = cvxpy.Variable()
    problem = Problem(
        cvxpy.Maximize(min_utility),
        constraints=basic_constraints + [min_utility <= utilities[agent] for agent in instance.agents],
        **solver_options
    )
    solve(problem, solvers = [(cvxpy.SCIPY, {'method':'highs-ds'})])  # highs-ds is a variant of simplex (guaranteed to return a corner solution)

    allocation_matrix = {agent: {item: allocation_vars[agent][item].value+0 for item in instance.items} for agent in instance.agents}
    logger.debug("\nAllocation_matrix:\n%s", allocation_matrix)
    logger.debug("\nUtilities:\n%s", {agent: utilities[agent].value+0 for agent in instance.agents})
    # logger.debug("\nRaw utilities:\n%s", {agent: raw_utilities[agent].value+0 for agent in instance.agents})
    # logger.debug("\nMax utilities:\n%s", {agent: instance.agent_maximum_value(agent) for agent in instance.agents})
    # logger.debug("\nNormalized utilities:\n%s", {agent: normalized_utilities[agent].value+0 for agent in instance.agents})
    return allocation_matrix

def fractional_egalitarian_utilitarian_allocation(instance: Instance, normalize_utilities=True, tolerance_factor=0.01, **solver_options):
    """
    Find an egalitarian allocation - an allocation that maximizes the minimum utility.
    Among all egalitarian allocations, find one that also maximizes the sum of utilities (so that it is Pareto-optimal).

    :param instance: a fair-course-allocation instance.
    :param normalize_utilities: True to use utilities normalized by the max possible agent value; False to use raw utilities.
    :param solver_options: kwargs sent to the cvxpy solver.

    :param instance: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param allocation_constraint_function: a predicate w: R -> {true,false} representing an additional constraint on the allocation variables.
    :param solver_options: kwargs sent to the cvxpy solver.

    :return a fractional allocation --- a dict of dicts, in which alloc[i][j] is the fraction allocated to agent i from object j.

    >>> logger.setLevel(logging.WARNING)
    >>> from fairpy.courses.allocation_utils import rounded_allocation

    >>> instance = Instance(valuations=[[5,0],[3,3]])
    >>> a = fractional_egalitarian_utilitarian_allocation(instance, normalize_utilities=False, tolerance_factor=0)
    >>> rounded_allocation(a,3)
    {0: {0: 0.75, 1: 0.0}, 1: {0: 0.25, 1: 1.0}}

    >>> instance = Instance(valuations=[[3,0],[5,5]])
    >>> a = fractional_egalitarian_utilitarian_allocation(instance, normalize_utilities=False, tolerance_factor=0)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0}, 1: {0: 0.0, 1: 1.0}}

    >>> instance = Instance(valuations=[[5,5],[3,0]])
    >>> a = fractional_egalitarian_utilitarian_allocation(instance, normalize_utilities=False, tolerance_factor=0)
    >>> rounded_allocation(a,3)
    {0: {0: 0.0, 1: 1.0}, 1: {0: 1.0, 1: 0.0}}

    >>> instance = Instance(valuations=[[3,0,0],[0,4,0],[5,5,5]])
    >>> a = fractional_egalitarian_utilitarian_allocation(instance, normalize_utilities=False, tolerance_factor=0)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 0.0}, 1: {0: 0.0, 1: 0.75, 2: 0.0}, 2: {0: 0.0, 1: 0.25, 2: 1.0}}

    >>> instance = Instance(valuations=[[4,0,0],[0,3,0],[5,5,10],[5,5,10]])
    >>> a = fractional_egalitarian_utilitarian_allocation(instance, normalize_utilities=False, tolerance_factor=0)
    >>> rounded_allocation(a,3)
    {0: {0: 0.75, 1: 0.0, 2: 0.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0}, 2: {0: 0.0, 1: 0.0, 2: 0.825}, 3: {0: 0.25, 1: 0.0, 2: 0.175}}

    >>> instance = Instance(valuations=[[3,0,0],[0,3,0],[5,5,10],[5,5,10]])
    >>> a = fractional_egalitarian_utilitarian_allocation(instance, normalize_utilities=False, tolerance_factor=0)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 0.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0}, 2: {0: 0.0, 1: 0.0, 2: 0.7}, 3: {0: 0.0, 1: 0.0, 2: 0.3}}

    >>> instance = Instance(valuations=[[1/3, 0, 1/3, 1/3],[1, 1, 1, 0]])
    >>> a = fractional_egalitarian_utilitarian_allocation(instance, normalize_utilities=False, tolerance_factor=0)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 1.0, 3: 1.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0, 3: 0.0}}
    """

    allocation_vars, raw_utilities, normalized_utilities = allocation_variables(instance)
    utilities = normalized_utilities if normalize_utilities else raw_utilities
    basic_constraints = allocation_constraints(instance, allocation_vars)

    # 1. Find the egalitarian value:
    min_utility = cvxpy.Variable()
    problem = Problem(
        cvxpy.Maximize(min_utility),
        constraints=basic_constraints + [min_utility <= utilities[agent] for agent in instance.agents],
        **solver_options
    )
    solve(problem, solvers = [(cvxpy.SCIPY, {'method':'highs-ds'})])  # highs-ds is a variant of simplex (guaranteed to return a corner solution)

    # 2. Find the utilitarian-subject-to-egalitarian value:
    min_utility_value = min_utility.value
    logger.debug("\nEgalitarian utility:\n%s", min_utility_value)
    threshold_utility = (1-tolerance_factor)*min_utility_value
    logger.debug("\nThreshold for utilitarian allocation:\n%s", threshold_utility)

    problem = cvxpy.Problem(
        cvxpy.Maximize(sum(utilities.values())),
        constraints=basic_constraints + [utilities[agent] >= threshold_utility for agent in instance.agents],
        **solver_options
    )
    solve(problem, solvers = [(cvxpy.SCIPY, {'method':'highs-ds'})])

    allocation_matrix = {agent: {item: allocation_vars[agent][item].value+0 for item in instance.items} for agent in instance.agents}
    logger.debug("\nAllocation_matrix:\n%s", allocation_matrix)
    logger.debug("\nUtilities:\n%s", {agent: utilities[agent].value+0 for agent in instance.agents})
    # logger.debug("\nRaw utilities:\n%s", {agent: raw_utilities[agent].value+0 for agent in instance.agents})
    # logger.debug("\nMax utilities:\n%s", {agent: instance.agent_maximum_value(agent) for agent in instance.agents})
    # logger.debug("\nNormalized utilities:\n%s", {agent: normalized_utilities[agent].value+0 for agent in instance.agents})
    return allocation_matrix



def fractional_leximin_optimal_allocation(instance: Instance, normalize_utilities=True, **solver_options):
    """
    Find a leximin-optimal allocation.
    :param instance: a fair-course-allocation instance.
    :param normalize_utilities: True to use utilities normalized by the max possible agent value; False to use raw utilities.
    :param solver_options: kwargs sent to the cvxpy solver.

    :return a fractional allocation --- a dict of dicts, in which alloc[i][j] is the fraction allocated to agent i from object j.
    
    >>> logger.setLevel(logging.WARNING)
    >>> from fairpy.courses.allocation_utils import rounded_allocation

    >>> instance = Instance(valuations=[[5,0],[3,3]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 0.75, 1: 0.0}, 1: {0: 0.25, 1: 1.0}}

    >>> instance = Instance(valuations=[[3,0],[5,5]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0}, 1: {0: 0.0, 1: 1.0}}

    >>> instance = Instance(valuations=[[5,5],[3,0]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 0.0, 1: 1.0}, 1: {0: 1.0, 1: 0.0}}

    >>> instance = Instance(valuations=[[3,0,0],[0,4,0],[5,5,5]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 0.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0}, 2: {0: 0.0, 1: 0.0, 2: 1.0}}

    >>> instance = Instance(valuations=[[4,0,0],[0,3,0],[5,5,10],[5,5,10]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 0.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0}, 2: {0: 0.0, 1: 0.0, 2: 0.5}, 3: {0: 0.0, 1: 0.0, 2: 0.5}}

    >>> instance = Instance(valuations=[[3,0,0],[0,3,0],[5,5,10],[5,5,10]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 0.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0}, 2: {0: 0.0, 1: 0.0, 2: 0.5}, 3: {0: 0.0, 1: 0.0, 2: 0.5}}

    >>> instance = Instance(valuations=[[1/3, 0, 1/3, 1/3],[1, 1, 1, 0]])
    >>> a = fractional_leximin_optimal_allocation(instance, normalize_utilities=False)
    >>> rounded_allocation(a,3)
    {0: {0: 1.0, 1: 0.0, 2: 1.0, 3: 1.0}, 1: {0: 0.0, 1: 1.0, 2: 0.0, 3: 0.0}}
    """

    allocation_vars, raw_utilities, normalized_utilities = allocation_variables(instance)
    utilities = normalized_utilities if normalize_utilities else raw_utilities
    problem = Problem(
        Leximin(utilities.values()),
        constraints=allocation_constraints(instance, allocation_vars),
        upper_tolerance=1.01,
        lower_tolerance=0.99,
        **solver_options
    )
    solve(problem, solvers = [(cvxpy.SCIPY, {'method':'highs-ds'})])  # highs-ds is a variant of simplex (guaranteed to return a corner solution)
    allocation_matrix = {agent: {item: allocation_vars[agent][item].value+0 for item in instance.items} for agent in instance.agents}
    # logger.debug("\nAllocation_matrix:\n%s", allocation_matrix)
    # logger.debug("\nRaw utilities:\n%s", {agent: raw_utilities[agent].value+0 for agent in instance.agents})
    # logger.debug("\nMax utilities:\n%s", {agent: instance.agent_maximum_value(agent) for agent in instance.agents})
    # logger.debug("\nNormalized utilities:\n%s", {agent: normalized_utilities[agent].value+0 for agent in instance.agents})
    return allocation_matrix


fractional_egalitarian_allocation.logger = fractional_egalitarian_utilitarian_allocation.logger = fractional_leximin_optimal_allocation.logger = logger

if __name__ == "__main__":
    import doctest, sys
    logger.addHandler(logging.StreamHandler(sys.stdout))
    print("\n",doctest.testmod(), "\n")

    # logger.setLevel(logging.DEBUG)
    # from fairpy.courses.adaptors import divide_random_instance
    # divide_random_instance(algorithm=fractional_egalitarian_utilitarian_allocation, 
    #                        num_of_agents=10, num_of_items=3, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
    #                        item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
    #                        random_seed=1, normalize_utilities=True)

    # divide_random_instance(algorithm=fractional_leximin_optimal_allocation, 
    #                        num_of_agents=10, num_of_items=3, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
    #                        item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
    #                        random_seed=1, normalize_utilities=True)
