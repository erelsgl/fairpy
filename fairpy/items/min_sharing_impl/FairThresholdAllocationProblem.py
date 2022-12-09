#!python3
"""
    A min-sharing fair allocation algorithm, where fairness is determined by general thresholds.

    Programmer: Eliyahu Sattat
    Since:  2020
"""

import cvxpy

from fairpy import ValuationMatrix, AllocationMatrix

from fairpy.items.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy.items.min_sharing_impl.FairAllocationProblem import FairAllocationProblem

from cvxpy.constraints.constraint import Constraint

import logging
logger = logging.getLogger(__name__)


class FairThresholdAllocationProblem(FairAllocationProblem):
    """
    Finds a min-sharing allocation
      under the constraint that each agent's value is above some threshold.
    Proportionality is a special case.

    Definition:
    V = agents valuation
    X = proportional allocation
    T = the thresholds
    For all i: Vi(Xi) ≥ Ti
    """

    def __init__(self, valuation_matrix:ValuationMatrix, thresholds:list):
        """
        :param valuations: the agents' valuations, V[i][o] for each agent i and object o
        :param thresholds: the agents' value-thresholds, T[i] for each agent i.
        """
        assert isinstance(valuation_matrix, ValuationMatrix)
        super().__init__(valuation_matrix)
        self.thresholds = thresholds


    def find_allocation_for_graph(self, consumption_graph: ConsumptionGraph)->AllocationMatrix:
        """
        Accepts a consumption graph and tries to find a proportional allocation.
        Uses cvxpy to solve a linear program.
        The condition for the program is:
        1) each alloc[i][j] >=0 - an agent cannot get a negative amount of some item.
        2) if consumption_graph[i][j] == 0 then alloc[i][j]= 0 .
           If in the current consumption graph the agent i doesnt consume the item j,
           then in the allocation he gets 0% from this item.
        3) The proportional condition (by definition).
        4) The sum of every column in the allocation == 1:
           Exactly 100 percent of each item are allocated.
        After solving the problem, check if the results are better than the
        "min_sharing_allocation"  (meaning if the current allocation has lass sharing than "min_sharing_allocation")
        and update it if needed.
        :param consumption_graph: some given consumption graph.
        :return: update "min_sharing_allocation"

        # the test are according to the result of ver 1 in GraphCheck
        >>> v = ValuationMatrix([[1, 2, 3,4], [4, 5, 6,5], [7, 8, 9,6]])
        >>> thresholds = [10/3, 20/3, 30/3]  # equivalent to proportional
        >>> fpap = FairThresholdAllocationProblem(v,thresholds)
        >>> g1 = [[0.0, 0.0, 0.0, 1], [1, 1, 1, 1], [0.0, 0.0, 0.0, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g))
        None
        >>> g1 = [[0.0, 0.0, 0.0, 1], [1, 1, 1, 1], [1, 0.0, 0.0, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g))
        None
        >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 0.0, 0.0, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g))
        None
        >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 1, 0.0, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g).round(2))
        [[0.   0.   0.   0.88]
         [0.   0.46 1.   0.05]
         [1.   0.54 0.   0.07]]
        >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 0.0, 1, 1], [1, 1, 0.0, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> fpap.find_allocation_for_graph(g).round(2).num_of_sharings()
        2
        >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 0.0, 1, 1], [1, 1, 1, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g).round(2))
        [[0.   0.   0.   0.84]
         [0.   0.   0.99 0.15]
         [1.   1.   0.01 0.01]]
        >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 0.0, 0.0, 0.0]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g))
        None
        >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 1, 0.0, 0.0]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g).round(2))
        [[0.   0.   0.   0.86]
         [0.   0.47 1.   0.14]
         [1.   0.53 0.   0.  ]]

        # This example exposed a bug in OSQP solver!
        >>> v = ValuationMatrix([ [465,0,535] , [0,0,1000]  ]) 
        >>> fpap =FairThresholdAllocationProblem(v,thresholds)
        >>> g1 = [[1,1,1],[0,0,1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g).round(3))
        [[1.    1.    0.389]
         [0.    0.    0.611]]
        """
        mat = cvxpy.Variable((self.valuation.num_of_agents, self.valuation.num_of_objects))
        constraints = []
        # every var >=0 and if there is no edge the var is zero
        # and proportional condition
        for i in self.valuation.agents():
            total_value_of_agent_i = 0
            for j in self.valuation.objects():
                if (consumption_graph.get_graph()[i][j] == 0):
                    logger.info("graph[%d][%d]==0",i,j)
                    constraints.append(mat[i][j] == 0)
                else:
                    logger.info("graph[%d][%d]>0",i,j)
                    constraints.append(mat[i][j] >= 0)
                total_value_of_agent_i += mat[i][j] * self.valuation[i][j]
            constraints.append(total_value_of_agent_i >= self.thresholds[i])
        # the sum of each column is 1 (the property on each object is 100%)
        for i in self.valuation.objects():
            constraints.append(sum(mat[:, i]) == 1)
        objective = cvxpy.Maximize(1)
        prob = cvxpy.Problem(objective, constraints)
        solver1 = "ECOS"
        solver2 = "SCS"
        # See here https://www.cvxpy.org/tutorial/advanced/index.html for a list of supported solvers
        # CBC, GLPK, GLPK_MI, CPLEX, NAG all fail. 
        # OSQP violates ==0 constraints.
        try:
            prob.solve(solver=solver1) 
        except cvxpy.SolverError:
            logger.info("%s solver raised SolverError -- trying %s solver", solver1, solver2)
            prob.solve(solver="SCS")
        if prob.status == 'optimal':
            if mat.value is None:
                raise ValueError("mat.value is None! prob.status="+prob.status)
            for constraint in constraints:
                logger.info("Constraint: %s, violation: %f", constraint, constraint.violation())
            return AllocationMatrix(mat.value)
        else:
            return None



if __name__ == '__main__':
    # import logging, sys
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    # v = [ [465,0,535] , [0,0,1000]  ]
    # fpap =FairThresholdAllocationProblem(v)
    # g1 = [[1,1,1],[0,0,1]]
    # g = ConsumptionGraph(g1)
    # print(fpap.find_allocation_for_graph(g).round(3))

    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
