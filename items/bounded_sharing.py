#!python3

""" 
Find a fractionl allocation among n agents, with at most n-1 sharings.

Programmer: Erel Segal-Halevi.
Since:  2021-10
"""

import numpy as np, cvxpy
from fairpy import adaptors, valuations, Allocation, AllocationToFamilies

import logging
logger = logging.getLogger(__name__)


def dominating_allocation_with_bounded_sharing(instance, thresholds) -> Allocation:
    """
    Finds an allocation in which each agent i gets value at least thresholds[i],
    and has at most n-1 sharings, where n is the number of agents.

    Uses the Simplex algorithm.

    >>> logger.setLevel(logging.WARNING)
    >>> a = dominating_allocation_with_bounded_sharing([[5,0],[3,3]], [1,1])
    >>> a
    Agent #0 gets { 75.0% of 0} with value 3.75.
    Agent #1 gets { 25.0% of 0, 100.0% of 1} with value 3.75.
    <BLANKLINE>
    """
    def implementation_with_matrix_input(v):
        allocation_vars = cvxpy.Variable((v.num_of_agents, v.num_of_objects))
        feasibility_constraints = [
            sum([allocation_vars[i][o] for i in v.agents()])==1
            for o in v.objects()
        ]
        positivity_constraints = [
            allocation_vars[i][o] >= 0 for i in v.agents()
            for o in v.objects()
        ]
        utilities = [sum([allocation_vars[i][o]*v[i][o] for o in v.objects()]) for i in v.agents()]
        leximin_solve(objectives=utilities, constraints=feasibility_constraints+positivity_constraints, solver=solve.DEFAULT_SOLVERS[0])
        allocation_matrix = allocation_vars.value
        # return Allocation(v, allocation_matrix)
        return AllocationMatrix(allocation_matrix)
    return adaptors.adapt_matrix_algorithm(implementation_with_matrix_input, instance)





if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
