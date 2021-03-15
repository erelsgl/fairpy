#!python3

import cvxpy

from fairpy.divisible.AllocationMatrix import AllocationMatrix
from fairpy.divisible.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy.divisible.min_sharing_impl.FairAllocationProblem import FairAllocationProblem

import logging
logger = logging.getLogger(__name__)


class FairProportionalAllocationProblem(FairAllocationProblem):
    """
    This class solves a proportional allocation problem.
    she is inherited from FairAllocationProblem
    proportional definition:
    V = agents valuation
    C = all agents properties
    X = proportional allocation
    n = the number of the agents
    For all i: Vi(Xi) ≥ Vi(C) / n
    """

    def __init__(self, valuation):
        super().__init__(valuation)


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
        >>> v = [[1, 2, 3,4], [4, 5, 6,5], [7, 8, 9,6]]
        >>> fpap =FairProportionalAllocationProblem(v)
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
        [[0.   0.   0.   0.92]
         [0.   0.39 1.   0.04]
         [1.   0.61 0.   0.04]]
        >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 0.0, 1, 1], [1, 1, 0.0, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g).round(2))
        [[0.   0.   0.   0.84]
         [0.   0.   1.   0.14]
         [1.   1.   0.   0.01]]
        >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 0.0, 1, 1], [1, 1, 1, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g).round(2))
        [[0.   0.   0.   0.84]
         [0.   0.   1.   0.15]
         [1.   1.   0.   0.01]]
        >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 0.0, 0.0, 0.0]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g))
        None
        >>> g1 = [[0.0, 0.0, 0.0, 1], [0.0, 1, 1, 1], [1, 1, 0.0, 0.0]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fpap.find_allocation_for_graph(g).round(2))
        [[0.   0.   0.   0.91]
         [0.   0.37 1.   0.09]
         [1.   0.63 0.   0.  ]]
        """
        mat = cvxpy.Variable((self.num_of_agents, self.num_of_items))
        constraints = []
        # every var >=0 and if there is no edge the var is zero
        # and proportional condition
        for i in range(self.num_of_agents):
            count = 0
            for j in range(self.num_of_items):
                if (consumption_graph.get_graph()[i][j] == 0):
                    constraints.append(mat[i][j] == 0)
                else:
                    constraints.append(mat[i][j] >= 0)
                count += mat[i][j] * self.valuation[i][j]
            constraints.append(count >= sum(self.valuation[i]) / self.valuation.num_of_agents)
        # the sum of each column is 1 (the property on each object is 100%)
        for i in range(self.num_of_items):
            constraints.append(sum(mat[:, i]) == 1)
        objective = cvxpy.Maximize(1)
        prob = cvxpy.Problem(objective, constraints)
        try:
            prob.solve(solver="OSQP")
        except cvxpy.SolverError:
            prob.solve(solver="SCS")
        if prob.status == 'optimal':
            if mat.value is None:
                raise ValueError("mat.value is None! prob.status="+prob.status)
            logger.info("Found a proportional allocation")
            return AllocationMatrix(mat.value)
        else:
            return None



if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
