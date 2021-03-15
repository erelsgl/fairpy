#!python3


import cvxpy

from fairpy.divisible.AllocationMatrix import AllocationMatrix
from fairpy.divisible.min_sharing_impl.ConsumptionGraph import ConsumptionGraph
from fairpy.divisible.min_sharing_impl.FairAllocationProblem import FairAllocationProblem

import logging
logger = logging.getLogger(__name__)


class FairEnvyFreeAllocationProblem(FairAllocationProblem):
    """
    This class solves an envy-free allocation Problem.
    It inherits FairAllocationProblem.

    Envy free definition:
    V = agents valuation
    X = envy free allocation
    For all i, j:
    Vi(Xi) ≥ Vi(Xj)
    """

    def __init__(self, valuation):
        super().__init__(valuation)


    def find_allocation_for_graph(self, consumption_graph: ConsumptionGraph)->AllocationMatrix:
        """
        Accepts a consumption graph and tries to find an envy free allocation.
        Uses cvxpy to solve a linear program.
        the condition for the convex problem is:
        1) each alloc[i][j] >=0 - an agent cant get minus pesent
        from some item
        2) if consumption_graph[i][j] == 0 so alloc[i][j]= 0 .
        if in the current consumption graph the agent i doesnt consume the item j
        so in the allocation he is get 0% from this item
        3) the envy free condition (by definition)
        4) the sum of every column in the allocation == 1
        each item divided exactly to 100 percent
        and after solving the problem - check if the result are better from the
        "min_sharing_allocation"  (meaning if the current allocation has fewer sharings from "min_sharing_allocation")
        and update it
        :param consumption_graph: some given consumption graph
        :return: update "min_sharing_allocation"
        # the test are according to the result of ver 1 in GraphCheck
        >>> v = [[5, 2, 1.5,1], [9, 1, 3,2.5], [10, 3, 2,4]]
        >>> fefap =FairEnvyFreeAllocationProblem(v)
        >>> g1 = [[1, 1, 0.0, 0.0], [1, 0.0, 1, 0.0], [1, 0.0, 0.0, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fefap.find_allocation_for_graph(g).round(2))
        [[0.33 1.   0.   0.  ]
         [0.33 0.   1.   0.  ]
         [0.33 0.   0.   1.  ]]
        >>> g1 = [[1, 1, 0.0, 0.0], [1, 0.0, 1, 0.0], [1, 0.0, 0.0, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fefap.find_allocation_for_graph(g).round(2))
        [[0.33 1.   0.   0.  ]
         [0.33 0.   1.   0.  ]
         [0.33 0.   0.   1.  ]]
        >>> g1 = [[1, 1, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [1, 0.0, 1, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fefap.find_allocation_for_graph(g))
        None
        >>> g1 = [[1, 1, 0.0, 0.0], [1, 0.0, 1, 1], [1, 0.0, 0.0, 0.0]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fefap.find_allocation_for_graph(g).round(2))
        [[0.3  1.   0.   0.  ]
         [0.05 0.   1.   1.  ]
         [0.65 0.   0.   0.  ]]
        >>> g1 = [[1, 1, 0.0, 0.0], [1, 0.0, 1, 1], [1, 0.0, 0.0, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fefap.find_allocation_for_graph(g).round(2))
        [[0.33 1.   0.   0.  ]
         [0.22 0.   1.   0.43]
         [0.45 0.   0.   0.57]]
        >>> g1 = [[1, 1, 0.0, 0.0], [1, 0.0, 1, 1], [0.0, 0.0, 0.0, 0.0]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fefap.find_allocation_for_graph(g))
        None
        >>> g1 = [[1, 1, 0.0, 0.0], [1, 0.0, 1, 0.0], [1, 0.0, 0.0, 1]]
        >>> g = ConsumptionGraph(g1)
        >>> print(fefap.find_allocation_for_graph(g).round(2))
        [[0.33 1.   0.   0.  ]
         [0.33 0.   1.   0.  ]
         [0.33 0.   0.   1.  ]]
        """
        mat = cvxpy.Variable((self.num_of_agents, self.num_of_items))
        constraints = []
        # every var >=0 and if there is no edge the var is zero
        # and envy_free condition
        for i in range(self.num_of_agents):
            agent_sum = 0
            for j in range(self.num_of_items):
                agent_sum += mat[i][j] * self.valuation[i][j]
                if (consumption_graph.get_graph()[i][j] == 0):
                    constraints.append(mat[i][j] == 0)
                else:
                    constraints.append(mat[i][j] >= 0)
            anther_agent_sum = 0
            for j in range(self.num_of_agents):
                anther_agent_sum = 0
                for k in range(self.num_of_items):
                    anther_agent_sum += mat[j][k] * self.valuation[i][k]
                constraints.append(agent_sum >= anther_agent_sum)
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
            logger.info("Found an envy-free allocation")
            return AllocationMatrix(mat.value)
        else:
            return None



if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))



