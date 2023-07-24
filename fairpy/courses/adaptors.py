"""
This module implements Adaptor functions for fair course allocation algorithms.

The functions accept a course allocation algorithm as an argument.

They allow you to call the allocation algorithm with convenient input types,
such as: a list of values, or a dict that maps an item to its value.

Author: Erel Segal-Halevi
Since: 2023-07
"""

import fairpy, numpy as np
from fairpy.courses.instance import Instance
from fairpy.courses.satisfaction import AgentBundleValueMatrix
from fairpy.courses.allocation_utils import validate_allocation, allocation_is_fractional

def divide(
    algorithm: callable,
    valuations: any,
    agent_capacities: any = None,  # default is unbounded (= num of items)
    agent_priorities: any = None,  # default is that all agents have same priority
    item_capacities:  any = None,  # default is 1 per course
    **kwargs
):
    """
    An adaptor partition function.

    :param algorithm: a specific algorithm for course-allocation. Should accept (at least) the following parameters: 
        agent_capacity:       callable; maps an agent name/index to its capacity (num of seats required).
        item_capacity:        callable; maps an item name/index to its capacity  (num of seats allocated).
        agent_item_value:     callable; maps an agent,item pair to the agent's value for the item.

    :param kwargs: any other arguments expected by `algorithm`.

    :return: an allocation.

    >>> valuations = {"Alice": {"c1":2, "c2": 3, "c3": 4}, "Bob": {"c1": 4, "c2": 5, "c3": 6}}
    >>> agent_capacities = {"Alice": 2, "Bob": 1}
    >>> item_capacities  = {"c1": 2, "c2": 1, "c3": 1}
    >>> divide(algorithm=fairpy.courses.round_robin, agent_capacities=agent_capacities, item_capacities=item_capacities, valuations=valuations)
    {'Alice': ['c1', 'c3'], 'Bob': ['c2']}
    """
    instance = Instance(valuations=valuations, agent_capacities=agent_capacities, agent_priorities=agent_priorities, item_capacities=item_capacities)
    result = algorithm(instance, **kwargs)
    return result


def divide_random_instance(algorithm, num_of_agents, num_of_items, 
                           agent_capacity_bounds, item_capacity_bounds, 
                           item_base_value_bounds, item_subjective_ratio_bounds,
                           normalized_sum_of_values, random_seed=None, **kwargs):
    if random_seed is None:
        random_seed = np.random.randint(1, 2**31)
    np.random.seed(random_seed)
    print("Random seed: ", random_seed)

    random_instance = Instance.random(num_of_agents=num_of_agents, num_of_items=num_of_items, agent_capacity_bounds=agent_capacity_bounds, item_capacity_bounds=item_capacity_bounds, 
                                      item_base_value_bounds=item_base_value_bounds, item_subjective_ratio_bounds=item_subjective_ratio_bounds,
                                      normalized_sum_of_values=normalized_sum_of_values, random_seed=random_seed)
    allocation = algorithm(random_instance, **kwargs)
    print("\nAllocation: ", allocation)

    if not allocation_is_fractional(allocation):
        validate_allocation(random_instance, allocation)
        matrix = AgentBundleValueMatrix(random_instance, allocation)
        matrix.use_normalized_values()

        print(f"   utilitarian value: {int(matrix.utilitarian_value())}%")
        print(f"   egalitarian value: {int(matrix.egalitarian_value())}%")
        print(f"   max envy: {int(matrix.max_envy())}%")
        print(f"   mean envy: {int(matrix.mean_envy())}%")
    else:
        pass # TODO: compute statistics of fractional allocations

    return allocation




if __name__ == "__main__":
    import doctest, sys
    print(doctest.testmod())

    divide_random_instance(
        fairpy.courses.round_robin, num_of_agents=70, num_of_items=10, agent_capacity_bounds=[6,6], item_capacity_bounds=[40,40], 
        item_base_value_bounds=[0,200], item_subjective_ratio_bounds=[0.5,1.5],
        normalized_sum_of_values=1000
    )
