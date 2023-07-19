"""
Implement an "almost-egalitarian" course allocation,
by rounding a linear program.

Programmer: Erel Segal-Halevi.
Since: 2023-07
"""

from fairpy.items.leximin import leximin_optimal_allocation
from fairpy.courses.instance import Instance

from fairpy.courses.allocation import sorted_allocation

import cvxpy
from cvxpy_leximin import Problem, Leximin
from fairpy.solve import solve


import logging
logger = logging.getLogger(__name__)

def almost_egalitarian_allocation(instance: Instance, allocation_constraint_function=None, **solver_options):
    """
    Finds an almost-egalitarian allocation.

    # >>> from dicttools import stringify

    # >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=1, item_capacities=1)
    # >>> stringify(almost_egalitarian_allocation(instance))
    # "{avi:['x'], beni:['w']}"

    # >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=2, item_capacities=1)
    # >>> stringify(almost_egalitarian_allocation(instance))
    # "{avi:['x', 'y'], beni:['w', 'z']}"

    # >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=3, item_capacities=2)
    # >>> stringify(almost_egalitarian_allocation(instance))
    # "{avi:['x', 'y', 'z'], beni:['w', 'y', 'z']}"

    # >>> instance = Instance(valuations={"avi": {"x":5, "y":4, "z":3, "w":2}, "beni": {"x":2, "y":3, "z":4, "w":5}}, agent_capacities=4, item_capacities=2)
    # >>> stringify(almost_egalitarian_allocation(instance))
    # "{avi:['w', 'x', 'y', 'z'], beni:['w', 'x', 'y', 'z']}"
    """
    allocation_vars = {agent: {item: cvxpy.Variable() for item in instance.items} for agent in instance.agents}
    item_capacity_constraints = [
        sum([allocation_vars[agent][item] for agent in instance.agents]) <= instance.item_capacity(item)
        for item in instance.items
    ]
    agent_capacity_constraints = [
        sum([allocation_vars[agent][item] for item in instance.items]) <= instance.agent_capacity(agent)
        for agent in instance.agents
    ]
    positivity_constraints = [
        0 <= allocation_vars[agent][item] for agent in instance.agents for item in instance.items
    ]
    uniqueness_constraints = [
        allocation_vars[agent][item] <= 1 for agent in instance.agents for item in instance.items
    ]
    utilities = {
        agent:
        sum([allocation_vars[agent][item] * instance.agent_item_value(agent,item) for item in instance.items])
        for agent in instance.agents
    }
    if allocation_constraint_function is not None:
        allocation_constraints = [allocation_constraint_function(allocation_vars[agent]) for agent in instance.agents]
    else:
        allocation_constraints = []
    problem = Problem(
        Leximin(utilities.values()),
        constraints=item_capacity_constraints + agent_capacity_constraints + positivity_constraints + uniqueness_constraints + allocation_constraints,
        **solver_options
    )
    solve(problem)  # Adding 0 to remove negative zeros
    allocation_matrix = {agent: {item: allocation_vars[agent][item].value+0 for item in instance.items} for agent in instance.agents}
    logger.debug("allocation_matrix:\n%s", allocation_matrix)

    utility_vector = {agent: utilities[agent].value+0 for agent in instance.agents}
    logger.debug("utility_vector:\n%s", utility_vector)

    return allocation_matrix
    return sorted_allocation(bundles)



if __name__ == "__main__":
    import doctest, sys
    # print("\n",doctest.testmod(), "\n")

    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.DEBUG)

    from fairpy.courses.adaptors import divide_random_instance
    divide_random_instance(algorithm=almost_egalitarian_allocation, 
                           num_of_agents=10, num_of_items=4, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1)
