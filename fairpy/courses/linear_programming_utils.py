"""
Define variables and constraints for linear programming

Programmer: Erel Segal-Halevi.
Since: 2023-07
"""

from fairpy.courses.instance import Instance
import cvxpy

def allocation_variables(instance: Instance)->tuple:
    """
    Construct cvxpy variables representing a fractional allocation, and construct expressions representing the utilities.

    :return allocation_vars, raw_utilities, normalized_utilities
    """
    allocation_vars = {agent: {item: cvxpy.Variable() for item in instance.items} for agent in instance.agents}
    raw_utilities = {
        agent:
        sum([allocation_vars[agent][item] * instance.agent_item_value(agent,item) for item in instance.items])
        for agent in instance.agents
    }
    normalized_utilities = {
        agent:
        sum([allocation_vars[agent][item] * instance.agent_normalized_item_value(agent,item) for item in instance.items])
        for agent in instance.agents
    }
    return allocation_vars, raw_utilities, normalized_utilities

def allocation_constraints(instance: Instance, allocation_vars:list):
    """
    Construct cvxpy constraints for a feasible fractional allocation:
    item_capacity_constraints, agent_capacity_constraints, positivity_constraints, uniqueness_constraints.

    :return a list of all constraints
    """
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
    return item_capacity_constraints + agent_capacity_constraints + positivity_constraints + uniqueness_constraints



if __name__ == "__main__":
    import doctest, sys
    print("\n",doctest.testmod(), "\n")
