#!python3

""" 
Find a fractionl allocation among n agents, with at most n-1 sharings.

Programmer: Erel Segal-Halevi.
Since:  2021-10
"""

from typing import *
import cvxpy, logging
from fairpy import adapt_matrix_algorithm, Allocation, ValuationMatrix
from fairpy.solve import solve

logger = logging.getLogger(__name__)


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
    def implementation_with_matrix_input(v:ValuationMatrix):
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
        solvers = [
            (cvxpy.MOSEK, {"bfs":True}),     # Always finds a 
            (cvxpy.OSQP, {})                 # I am not sure it returns a Basic Feasible Solution!
        ]
        solve(problem, solvers=solvers)
        if problem.status=="optimal":
            allocation_matrix = allocation_vars.value
            return allocation_matrix
        else:
            raise cvxpy.SolverError(f"No optimal solution found: status is {problem.status}")
    return adapt_matrix_algorithm(implementation_with_matrix_input, instance)







if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
