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

import cvxpy
from fairpy import (
    Allocation,
    AllocationToFamilies,
    map_agent_to_family,
    ValuationMatrix,
    Agent,
    AdditiveValuation,
    convert_input_to_valuation_matrix,
)
from fairpy.solve import solve

from cvxpy_leximin import Problem, Leximin
from typing import Any

import logging

logger = logging.getLogger(__name__)


##### Utility functions for comparing leximin vectors


def is_leximin_better(x: list, y: list):
    """
    >>> is_leximin_better([6,2,4],[7,3,1])
    True
    >>> is_leximin_better([6,2,4],[3,3,3])
    False
    """
    return sorted(x) > sorted(y)


##### Find a leximin-optimal allocation for individual agents


@convert_input_to_valuation_matrix
def leximin_optimal_allocation(instance: Any, **solver_options) -> Allocation:
    """
    Find the leximin-optimal (aka Egalitarian) allocation.
    :param instance: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the leximin vector of utilities.
    >>> logger.setLevel(logging.WARNING)
    >>> a = leximin_optimal_allocation([[5,0],[3,3]]).round(2)
    >>> a
    Agent #0 gets { 75.0% of 0} with value 3.75.
    Agent #1 gets { 25.0% of 0, 100.0% of 1} with value 3.75.
    <BLANKLINE>
    >>> a.matrix
    [[0.75 0.  ]
     [0.25 1.  ]]
    >>> a.utility_profile()
    array([3.75, 3.75])
    >>> v = [[3,0],[5,5]]
    >>> print(leximin_optimal_allocation(v).round(3).utility_profile())
    [3. 5.]
    >>> v = [[5,5],[3,0]]
    >>> print(leximin_optimal_allocation(v).round(3).utility_profile())
    [5. 3.]
    >>> v = [[3,0,0],[0,4,0],[5,5,5]]
    >>> print(leximin_optimal_allocation(v).round(3).utility_profile())
    [3. 4. 5.]
    >>> v = [[4,0,0],[0,3,0],[5,5,10],[5,5,10]]
    >>> print(leximin_optimal_allocation(v).round(3).utility_profile())
    [4. 3. 5. 5.]
    >>> v = [[3,0,0],[0,3,0],[5,5,10],[5,5,10]]
    >>> a = leximin_optimal_allocation(v)
    >>> print(a.round(3).utility_profile())
    [3. 3. 5. 5.]
    >>> v = [[1/3, 0, 1/3, 1/3],[1, 1, 1, 0]]
    >>> a = leximin_optimal_allocation(v)
    >>> logger.setLevel(logging.WARNING)
    """
    v = ValuationMatrix(instance)
    allocation_vars = cvxpy.Variable((v.num_of_agents, v.num_of_objects))
    feasibility_constraints = [
        sum([allocation_vars[i][o] for i in v.agents()]) == 1
        for o in v.objects()
    ]
    positivity_constraints = [
        allocation_vars[i][o] >= 0 for i in v.agents() for o in v.objects()
    ]
    utilities = [
        sum([allocation_vars[i][o] * v[i][o] for o in v.objects()])
        for i in v.agents()
    ]
    problem = Problem(
        Leximin(utilities),
        constraints=feasibility_constraints + positivity_constraints,
        **solver_options
    )
    solve(problem)
    allocation_matrix = allocation_vars.value
    logger.debug("allocation_matrix:\n%s", allocation_matrix)
    return allocation_matrix


##### leximin for families


def leximin_optimal_allocation_for_families(
    instance: Any, families: list
) -> AllocationToFamilies:
    """
    Find the leximin-optimal (aka Egalitarian) allocation among families.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param families: a list of lists. Each list represents a family and contains the indices of the agents in the family.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the leximin vector of utilities.
    >>> families = [ [0], [1] ]  # two singleton families
    >>> v = [[5,0],[3,3]]
    >>> print(leximin_optimal_allocation_for_families(v,families).round(2).utility_profile())
    [3.75 3.75]
    >>> v = [[3,0],[5,5]]
    >>> print(leximin_optimal_allocation_for_families(v,families).round(2).utility_profile())
    [3. 5.]
    >>> families = [ [0], [1], [2] ]  # three singleton families
    >>> v = [[3,0,0],[0,4,0],[5,5,5]]
    >>> print(leximin_optimal_allocation_for_families(v,families).round(2).utility_profile())
    [3. 4. 5.]
    >>> families = [ [0, 1], [2] ]
    >>> print(leximin_optimal_allocation_for_families(v,families).round(2).utility_profile())
    [3. 4. 5.]
    >>> families = [ [0], [1,2] ]

    >>> print(leximin_optimal_allocation_for_families(v,families).round(2).utility_profile())
    [ 3.  4. 10.]
    """
    v = ValuationMatrix(instance)
    num_of_objects = v.num_of_objects
    num_of_agents = v.num_of_agents
    num_of_families = len(families)
    agent_to_family = map_agent_to_family(families, num_of_agents)
    logger.info("map_agent_to_family = %s", agent_to_family)
    allocation_vars = cvxpy.Variable((num_of_families, num_of_objects))
    feasibility_constraints = [
        sum([allocation_vars[f][o] for f in range(num_of_families)]) == 1
        for o in range(num_of_objects)
    ]
    positivity_constraints = [
        allocation_vars[f][o] >= 0
        for f in range(num_of_families)
        for o in range(num_of_objects)
    ]
    utilities = [
        sum(
            [
                allocation_vars[agent_to_family[i]][o] * v[i][o]
                for o in range(num_of_objects)
            ]
        )
        for i in range(num_of_agents)
    ]
    problem = Problem(
        Leximin(utilities),
        constraints=feasibility_constraints + positivity_constraints,
    )
    solve(problem)
    allocation_matrix = allocation_vars.value

    return AllocationToFamilies(v, allocation_matrix, families)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
