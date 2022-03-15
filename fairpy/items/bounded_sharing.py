#!python3

""" 
Find a fractionl allocation among n agents, with at most n-1 sharings.

Programmer: Erel Segal-Halevi.
Since:  2021-10
"""

from typing import *
import cvxpy, logging, numpy as np
from fairpy import convert_input_to_valuation_matrix, Allocation, ValuationMatrix
from fairpy.solve import solve
from fairpy.items.max_welfare import max_product_allocation

logger = logging.getLogger(__name__)

@convert_input_to_valuation_matrix
def dominating_allocation_with_bounded_sharing(instance:Any, thresholds:List) -> Allocation:
    """
    Finds an allocation in which each agent i gets value at least thresholds[i],
    and has at most n-1 sharings, where n is the number of agents.

    IDEA: find a Basic Feasible Solution (BFS) of a linear program.
    NOTE: some solvers return a BFS by default (particularly, those running Simplex).

    >>> logger.setLevel(logging.WARNING)
    >>> instance = [[8,2],[5,5]]
    >>> dominating_allocation_with_bounded_sharing(instance, thresholds=[0,0]).round(3)
    Agent #0 gets {} with value 0.
    Agent #1 gets { 100.0% of 0, 100.0% of 1} with value 10.
    <BLANKLINE>
    >>> dominating_allocation_with_bounded_sharing(instance, thresholds=[1,1]).round(3)
    Agent #0 gets { 12.5% of 0} with value 1.
    Agent #1 gets { 87.5% of 0, 100.0% of 1} with value 9.38.
    <BLANKLINE>
    >>> dominating_allocation_with_bounded_sharing(instance, thresholds=[2,2]).round(3)
    Agent #0 gets { 25.0% of 0} with value 2.
    Agent #1 gets { 75.0% of 0, 100.0% of 1} with value 8.75.
    <BLANKLINE>
    >>> dominating_allocation_with_bounded_sharing(instance, thresholds=[5,5]).round(3)
    Agent #0 gets { 62.5% of 0} with value 5.
    Agent #1 gets { 37.5% of 0, 100.0% of 1} with value 6.88.
    <BLANKLINE>
    """
    # logger.info("Finding an allocation with thresholds %s", thresholds)
    v = ValuationMatrix(instance)
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
    utility_constraints = [
        utilities[i] >= thresholds[i] for i in range(v.num_of_agents-1)
    ]
    constraints = feasibility_constraints+positivity_constraints+utility_constraints
    problem = cvxpy.Problem(cvxpy.Maximize(utilities[v.num_of_agents-1]), constraints)
    logger.info("constraints: %s", constraints)
    solvers = [
        (cvxpy.SCIPY, {'method': 'highs-ds'}),        # Always finds a BFS
        (cvxpy.MOSEK, {"bfs":True}),                  # Always finds a BFS
        (cvxpy.OSQP, {}),                             # Default - not sure it returns a BFS
        (cvxpy.SCIPY, {}),                            # Default - not sure it returns a BFS
    ]
    solve(problem, solvers=solvers)
    if problem.status=="optimal":
        allocation_matrix = allocation_vars.value
        return allocation_matrix
    else:
        raise cvxpy.SolverError(f"No optimal solution found: status is {problem.status}")



@convert_input_to_valuation_matrix
def proportional_allocation_with_bounded_sharing(instance:Any, entitlements:List=None) -> Allocation:
    """
    Finds a Pareto-optimal and proportional allocation
          with at most n-1 sharings, where n is the number of agents.

    :param instance: a valuation profile in any supported format.
    :param entitlements: the entitlement of each agent. Optional, default is (1,...,1) which means equal entitlements.

    IDEA: find a Basic Feasible Solution (BFS) of a linear program.
    NOTE: some solvers return a BFS by default (particularly, those running Simplex).

    >>> logger.setLevel(logging.WARNING)
    >>> instance = [[8,2],[5,5]]
    >>> proportional_allocation_with_bounded_sharing(instance).round(3)
    Agent #0 gets { 62.5% of 0} with value 5.
    Agent #1 gets { 37.5% of 0, 100.0% of 1} with value 6.88.
    <BLANKLINE>
    >>> proportional_allocation_with_bounded_sharing(instance, entitlements=[4,1]).round(3)
    Agent #0 gets { 100.0% of 0} with value 8.
    Agent #1 gets { 100.0% of 1} with value 5.
    <BLANKLINE>
    >>> proportional_allocation_with_bounded_sharing(instance, entitlements=[3,2]).round(3)
    Agent #0 gets { 75.0% of 0} with value 6.
    Agent #1 gets { 25.0% of 0, 100.0% of 1} with value 6.25.
    <BLANKLINE>
    """
    v = ValuationMatrix(instance)
    if entitlements is None:
        entitlements = np.ones(v.num_of_agents)
    else:
        entitlements = np.array(entitlements)
    entitlements = entitlements/sum(entitlements)  # normalize
    logger.info("Normalized entitlements: %s", entitlements)
    logger.info("Total values: %s", v.total_values())
    thresholds = v.total_values() * entitlements
    logger.info("Value thresholds: %s", thresholds)
    return dominating_allocation_with_bounded_sharing(v, thresholds)



def efficient_envyfree_allocation_with_bounded_sharing(instance:Any) -> Allocation:
    """
    Finds a max-product allocation, which is known to be envy-free and Pareto-optimal.
          and has at most n-1 sharings, where n is the number of agents.

    :param instance: a valuation profile in any supported format.

    >>> logger.setLevel(logging.WARNING)
    >>> instance = [[8,2],[5,5]]
    >>> efficient_envyfree_allocation_with_bounded_sharing(instance).round(3)
    Agent #0 gets { 100.0% of 0} with value 8.
    Agent #1 gets { 100.0% of 1} with value 5.
    <BLANKLINE>
    """
    max_prod_allocation = max_product_allocation(instance)
    thresholds = max_prod_allocation.utility_profile()
    return dominating_allocation_with_bounded_sharing(instance, thresholds)


if __name__ == '__main__':
    import sys
    solve.logger.addHandler(logging.StreamHandler(sys.stdout))
    solve.logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
