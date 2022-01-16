#!python3

""" 
Solving a multi-objective optimization problem using the leximin criterion:
maximize the smallest objective, then the next-smallest, and so on.

Based on:

Stephen J. Willson
["Fair Division Using Linear Programming"](https://swillson.public.iastate.edu/FairDivisionUsingLPUnpublished6.pdf)
* Part 6, pages 20--27.

Programmer: Erel Segal-Halevi.

Acknowledgments: I am grateful to Sylvain Bouveret for his help with the algorithm. All errors and bugs are my own.

Since:  2021-05
"""

import cvxpy, logging
logger = logging.getLogger(__name__)

from typing import *
from fairpy.solve import maximize

UPPER_TOLERANCE=1.01  # for comparing floating-point numbers
LOWER_TOLERANCE=0.9999

def leximin_solve(objectives:list, constraints:list, **kwargs):
    """
    Find a leximin-optimal vector of utilities, subject to the given constraints.

    :param objectives: A list of cvxpy expressions, representing the various objectives. The order in the list is irrelevant.
    :param constraints: A list of cvxpy constraints. The constraints must specify a convex domain.
    :param kwargs: keyword arguments passed on to cvxpy.Problem.solve().
    :return None. When the function completes, you can access the values of the variables and objectives in the leximin solution using the Variable.value field.

    EXAMPLE: resource allocation. There are three resources to allocate among two people.
    Alice values the resources at 5, 3, 0.
    Bob values the resources at 2, 4, 9.
    The variables a[0], a[1], a[2], a[3] denote the fraction of each resource given to Alice.
    >>> a = cvxpy.Variable(4)
    >>> feasible_allocation = [x>=0 for x in a] + [x<=1 for x in a]

    >>> utility_Alice = a[0]*5 + a[1]*3 + a[2]*0
    >>> utility_Bob   = (1-a[0])*2 + (1-a[1])*4 + (1-a[2])*9
    >>> leximin_solve(objectives=[utility_Alice, utility_Bob],  constraints=feasible_allocation)
    >>> round(utility_Alice.value), round(utility_Bob.value)
    (8, 9)
    >>> [round(x.value) for x in a]  # Alice gets all of resources 0 and 1; Bob gets all of resource 2.
    [1, 1, 0, 0]

    >>> utility_Alice = -5*a[0]  -3*a[1] -0*a[2]
    >>> utility_Bob   = -2*(1-a[0])  -4*(1-a[1])  -9*(1-a[2])
    >>> leximin_solve(objectives=[utility_Alice, utility_Bob],  constraints=feasible_allocation)
    >>> round(utility_Alice.value,2), round(utility_Bob.value,2)
    (-2.57, -2.57)
    >>> [round(x.value,3) for x in a]
    [-0.0, 0.857, 1.0, -0.0]

    >>> utility_Alice = (1/3)*a[0]  + 0*a[1] + (1/3)*a[2] + (1/3)*a[3]
    >>> utility_Bob   = 1*(1-a[0]) + 1*(1-a[1]) + 1*(1-a[2]) + 0*(1-a[3])
    >>> leximin_solve(objectives=[utility_Alice, utility_Bob],  constraints=feasible_allocation)
    >>> round(utility_Alice.value,3), round(utility_Bob.value,3)
    (1.0, 1.0)
    >>> [round(x.value,3) for x in a]
    [1.0, -0.0, 1.0, 1.0]
    """
    num_of_objectives = len(objectives)

    # During the algorithm, the objectives are partitioned into "free" and "saturated".
    # * "free" objectives are those that can potentially be made higher, without harming the smaller objectives.
    # * "saturated" objectives are those that have already attained their highest possible value in the leximin solution.
    # Initially, all objectives are free, and no objective is saturated:
    free_objectives = list(range(num_of_objectives))
    map_saturated_objective_to_saturated_value = num_of_objectives * [None]

    while True:
        logger.info("Saturated values: %s.", map_saturated_objective_to_saturated_value)
        minimum_value_for_free_objectives = cvxpy.Variable()
        inequalities_for_free_objectives = [
            objectives[i] >= minimum_value_for_free_objectives
            for i in free_objectives
        ]
        inequalities_for_saturated_objectives = [(objectives[i] >= value) for i,value in enumerate(map_saturated_objective_to_saturated_value) if value is not None]
        max_min_value_for_free_objectives = maximize(minimum_value_for_free_objectives, constraints + inequalities_for_saturated_objectives + inequalities_for_free_objectives, **kwargs)

        values_in_max_min_allocation = [objective.value for objective in objectives]
        logger.info("  max min value: %g, value-profile: %s", max_min_value_for_free_objectives, values_in_max_min_allocation)
        max_min_value_upper_threshold = UPPER_TOLERANCE*max_min_value_for_free_objectives if max_min_value_for_free_objectives>0 else (2-UPPER_TOLERANCE)*max_min_value_for_free_objectives
        max_min_value_lower_threshold = LOWER_TOLERANCE*max_min_value_for_free_objectives if max_min_value_for_free_objectives>0 else (2-LOWER_TOLERANCE)*max_min_value_for_free_objectives

        for ifree in free_objectives:  # Find whether i's value can be improved
            if values_in_max_min_allocation[ifree] > max_min_value_upper_threshold:
                logger.info("  Max value of objective #%d is %g, which is above %g, so objective remains free.", ifree, values_in_max_min_allocation[ifree], max_min_value_upper_threshold)
                continue
            inequalities_for_other_free_objectives = [
                objectives[i] >= max_min_value_lower_threshold
                for i in free_objectives if i!=ifree
            ]
            max_value_for_ifree = maximize(objectives[ifree], constraints + inequalities_for_saturated_objectives + inequalities_for_other_free_objectives, **kwargs)
            if max_value_for_ifree > max_min_value_upper_threshold:
                logger.info("  Max value of objective #%d is %g, which is above %g, so objective remains free.", ifree, max_value_for_ifree, max_min_value_upper_threshold)
                continue
            else:
                logger.info("  Max value of objective #%d is %g, which is below %g, so objective becomes saturated.", ifree, max_value_for_ifree, max_min_value_upper_threshold)
                map_saturated_objective_to_saturated_value[ifree] = max_min_value_for_free_objectives

        new_free_agents = [i for i in free_objectives if map_saturated_objective_to_saturated_value[i] is None]
        if len(new_free_agents)==len(free_objectives):
            raise ValueError("No new saturated objectives - this contradicts Willson's theorem! Are you sure the domain is convex?")
        elif len(new_free_agents)==0:
            logger.info("All objectives are saturated -- values are %s.", map_saturated_objective_to_saturated_value)
            return
        else:
            free_objectives = new_free_agents
            continue

leximin_solve.logger = logger





if __name__ == '__main__':
    import sys
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
