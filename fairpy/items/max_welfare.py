#!python3

"""
Find a fractionl allocation that maximizes a social welfare function (- a monotone function of the utilities),
     for agents with additive valuations.

Examples are: max-sum, max-product, max-min.
See also: [leximin.py](leximin.py)

Author: Erel Segal-Halevi
Since:  2021-05
"""

import cvxpy
from fairpy import ValuationMatrix, Allocation, AllocationToFamilies, convert_input_to_valuation_matrix
from fairpy.solve import maximize
from typing import Any

import logging
logger = logging.getLogger(__name__)

@convert_input_to_valuation_matrix
def max_welfare_allocation(instance:Any, welfare_function, welfare_constraint_function=None) -> Allocation:
    """
    Find an allocation maximizing a given social welfare function. (aka Max Nash Welfare) allocation.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param welfare_function:   a monotonically-increasing function w: R -> R representing the welfare function to maximize.
    :param welfare_constraint: a predicate w: R -> {true,false} representing an additional constraint on the utility of each agent.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.

    For usage examples, see the functions max_sum_allocation, max_product_allocation, max_minimum_allocation.
    """
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
    if welfare_constraint_function is not None:
        welfare_constraints = [welfare_constraint_function(utility) for utility in utilities]
    else:
        welfare_constraints = []
    max_welfare = maximize(welfare_function(utilities), feasibility_constraints+positivity_constraints+welfare_constraints)
    logger.info("Maximum welfare is %g",max_welfare)
    allocation_matrix = allocation_vars.value
    return allocation_matrix



from fairpy.families import AllocationToFamilies, map_agent_to_family

def max_welfare_allocation_for_families(instance, families:list, welfare_function, welfare_constraint_function=None) -> AllocationToFamilies:
    """
    Find an allocation maximizing a given social welfare function. (aka Max Nash Welfare) allocation.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param families: a list of lists. Each list represents a family and contains the indices of the agents in the family.
    :param welfare_function:   a monotonically-increasing function w: R -> R representing the welfare function to maximize.
    :param welfare_constraint: a predicate w: R -> {true,false} representing an additional constraint on the utility of each agent.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.

    For usage examples, see the function max_minimum_allocation_for_families.
    """
    v = ValuationMatrix(instance)
    num_of_families = len(families)
    agent_to_family = map_agent_to_family(families, v.num_of_agents)

    alloc = cvxpy.Variable((num_of_families, v.num_of_objects))
    feasibility_constraints = [
        sum([alloc[f][o] for f in range(num_of_families)])==1
        for o in v.objects()
    ]
    positivity_constraints = [
        alloc[f][o] >= 0 for f in range(num_of_families)
        for o in v.objects()
    ]
    utilities = [sum([alloc[agent_to_family[i]][o]*v[i][o] for o in v.objects()]) for i in v.agents()]

    if welfare_constraint_function is not None:
        welfare_constraints = [welfare_constraint_function(utility) for utility in utilities]
    else:
        welfare_constraints = []
    max_welfare = maximize(welfare_function(utilities), feasibility_constraints+positivity_constraints+welfare_constraints)
    logger.info("Maximum welfare is %g",max_welfare)
    return AllocationToFamilies(v, alloc.value, families)




def max_sum_allocation(instance) -> Allocation:
    """
    Find the max-sum (aka Utilitarian) allocation.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the product (= sum of logs) of utilities
    >>> max_sum_allocation([ [3] , [5] ]).round(3).matrix   # single item
    [[0.]
     [1.]]
    >>> max_sum_allocation([ [3,3] , [1,1] ]).round(3).matrix   # two identical items
    [[1. 1.]
     [0. 0.]]
    >>> max_sum_allocation([ [3,2] , [1,4] ]).round(3).matrix   # two different items
    [[1. 0.]
     [0. 1.]]
    """
    return max_welfare_allocation(instance,
        welfare_function=lambda utilities: sum(utilities),
        welfare_constraint_function=lambda utility: utility >= 0)


def max_power_sum_allocation(instance, power:float) -> Allocation:
    """
    Find the maximum of sum of utility to the given power.
    * When power=1, it is equivalent to max-sum;
    * When power -> 0, it converges to max-product;
    * When power -> -infinity, it converges to leximin.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the product (= sum of logs) of utilities
    >>> max_power_sum_allocation([ [3] , [5] ], 1).round(3).matrix
    [[0.]
     [1.]]
    >>> max_power_sum_allocation([ [3] , [5] ], 0.1).round(3).matrix
    [[0.486]
     [0.514]]
    >>> max_power_sum_allocation([ [3] , [5] ], 0).round(3).matrix
    [[0.5]
     [0.5]]
    >>> max_power_sum_allocation([ [3] , [5] ], -0.1).round(3).matrix
    [[0.512]
     [0.488]]
    >>> max_power_sum_allocation([ [3] , [5] ], -1).round(3).matrix
    [[0.564]
     [0.436]]
    """
    if power>0:
        welfare_function=lambda utilities: sum([utility**power for utility in utilities])
    elif power<0:
        welfare_function=lambda utilities: -sum([utility**power for utility in utilities])
    else:
        welfare_function=lambda utilities: sum([cvxpy.log(utility) for utility in utilities])
    return max_welfare_allocation(instance,
        welfare_function=welfare_function,
        welfare_constraint_function=lambda utility: utility >= 0)


def max_product_allocation(instance) -> Allocation:
    """
    Find the max-product (aka Max Nash Welfare) allocation.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the product (= sum of logs) of utilities
    >>> max_product_allocation([ [3] , [5] ]).round(3).matrix   # single item
    [[0.5]
     [0.5]]
    >>> max_product_allocation([ [3,3] , [1,1] ]).round(3).matrix   # two identical items
    [[0.5 0.5]
     [0.5 0.5]]
    >>> max_product_allocation([ [3,2] , [1,4] ]).round(3).matrix   # two different items
    [[1. 0.]
     [0. 1.]]
    """
    return max_welfare_allocation(instance,
        welfare_function=lambda utilities: sum([cvxpy.log(utility) for utility in utilities]),
        welfare_constraint_function=lambda utility: utility >= 0)


def max_minimum_allocation(instance) -> Allocation:
    """
    Find the max-minimum (aka Egalitarian) allocation.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the leximin vector of utilities.
    >>> a = max_minimum_allocation([ [3] , [5] ])   # single item
    >>> a
    Agent #0 gets { 62.5% of 0} with value 1.88.
    Agent #1 gets { 37.5% of 0} with value 1.88.
    <BLANKLINE>
    >>> a.matrix
    [[0.625]
     [0.375]]
    >>> max_minimum_allocation([ [4,2] , [1,4] ]).round(3).matrix   # two different items
    [[1. 0.]
     [0. 1.]]
    >>> alloc = max_minimum_allocation([ [3,3] , [1,1] ]).round(3).matrix   # two identical items
    >>> [sum(alloc[i]) for i in alloc.agents()]
    [0.5, 1.5]
    >>> v = [ [4,2] , [1,3] ]   # two different items
    >>> a = max_minimum_allocation(v).round(3)
    >>> a.matrix
    [[0.8 0. ]
     [0.2 1. ]]
    >>> print(a.utility_profile())
    [3.2 3.2]
    """
    return max_welfare_allocation(instance,
        welfare_function=lambda utilities: cvxpy.min(cvxpy.hstack(utilities)),
        welfare_constraint_function=lambda utility: utility >= 0)



def max_minimum_allocation_for_families(instance, families) -> AllocationToFamilies:
    """
    Find the max-minimum (aka Egalitarian) allocation.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param families: a list of lists. Each list represents a family and contains the indices of the agents in the family.

    :return allocation_matrix:  a matrix alloc of a similar shape in which alloc[i][j] is the fraction allocated to agent i from object j.
    The allocation should maximize the leximin vector of utilities.
    >>> families = [ [0], [1] ]  # two singleton families
    >>> max_minimum_allocation_for_families([ [3] , [5] ],families).round(3).matrix
    [[0.625]
     [0.375]]
    >>> max_minimum_allocation_for_families([ [4,2] , [1,4] ], families).round(3).matrix   # two different items
    [[1. 0.]
     [0. 1.]]
    >>> alloc = max_minimum_allocation_for_families([ [3,3] , [1,1] ], families).round(3).matrix   # two identical items
    >>> [sum(alloc[i]) for i in alloc.agents()]
    [0.5, 1.5]
    >>> v = [ [4,2] , [1,3] ]   # two different items
    >>> a = max_minimum_allocation_for_families(v, families).round(3)
    >>> a
    Family #0 with members [0] gets { 80.0% of 0} with values [3.2].
    Family #1 with members [1] gets { 20.0% of 0, 100.0% of 1} with values [3.2].
    <BLANKLINE>
    >>> a.matrix
    [[0.8 0. ]
     [0.2 1. ]]
    >>> print(a.utility_profile())
    [3.2 3.2]
    >>> families = [ [0, 1] ]  # One couple
    >>> max_minimum_allocation_for_families([ [4,2] , [1,4] ], families).round(3).matrix
    [[1. 1.]]
    >>> families = [ [0, 1], [2, 3] ]  # Two couples
    >>> a = max_minimum_allocation_for_families([ [4,2] , [1,4], [3,3], [5,5] ], families).round(3).matrix
    >>> a
    [[0.414 0.621]
     [0.586 0.379]]
    """
    return max_welfare_allocation_for_families(instance, families,
        welfare_function=lambda utilities: cvxpy.min(cvxpy.hstack(utilities)),
        welfare_constraint_function=lambda utility: utility >= 0)






if __name__ == '__main__':
    import sys
    logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    from fairpy import solve
    solve.logger.addHandler(logging.StreamHandler(sys.stdout))
    # solve.logger.setLevel(logging.INFO)

    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
