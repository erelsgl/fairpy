"""
Implement a fractional egalitarian course allocation using linear programming.
Can be used as a basis for an almost-egalitarian allocation, using rounding.

Programmer: Erel Segal-Halevi.
Since: 2023-07
"""

from fairpy.courses.instance import Instance
from fairpy.courses.allocation_utils import sorted_allocation, rounded_allocation
from fairpy.courses.linear_programming_utils import allocation_variables, allocation_constraints

import cvxpy, numpy as np, networkx
from cvxpy_leximin import Problem, Leximin
from fairpy.solve import solve
import matplotlib.pyplot as plt # for plotting the consumption graph (for debugging)


import logging
logger = logging.getLogger(__name__)

def fractional_leximin_optimal_allocation(instance: Instance, normalize_utilities=True, **solver_options):
    """
    Find the leximin-optimal (aka Egalitarian) allocation.
    :param instance: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param allocation_constraint_function: a predicate w: R -> {true,false} representing an additional constraint on the allocation variables.
    :param solver_options: kwargs sent to the cvxpy solver.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the leximin vector of utilities.
    >>> logger.setLevel(logging.WARNING)
    >>> np.set_printoptions(precision=3)

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
        **solver_options
    )
    solve(problem, solvers = [(cvxpy.SCIPY, {'method':'highs-ds'})])  # highs-ds is a variant of simplex (guaranteed to return a corner solution)
    allocation_matrix = {agent: {item: allocation_vars[agent][item].value+0 for item in instance.items} for agent in instance.agents}
    # logger.debug("\nAllocation_matrix:\n%s", allocation_matrix)
    # logger.debug("\nRaw utilities:\n%s", {agent: raw_utilities[agent].value+0 for agent in instance.agents})
    # logger.debug("\nMax utilities:\n%s", {agent: instance.agent_maximum_value(agent) for agent in instance.agents})
    # logger.debug("\nNormalized utilities:\n%s", {agent: normalized_utilities[agent].value+0 for agent in instance.agents})
    return allocation_matrix



if __name__ == "__main__":
    import doctest, sys
    print("\n",doctest.testmod(), "\n")

    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)

    from fairpy.courses.adaptors import divide_random_instance
    divide_random_instance(algorithm=fractional_leximin_optimal_allocation, 
                           num_of_agents=10, num_of_items=3, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1, normalize_utilities=True)
