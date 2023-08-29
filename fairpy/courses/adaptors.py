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
from fairpy.courses.allocation_utils import validate_allocation, allocation_is_fractional, AllocationBuilder
from fairpy.courses.explanations import ExplanationLogger

def divide(
    algorithm: callable,
    instance: Instance = None,
    valuations: any = None,
    agent_capacities: any = None,  # default is unbounded (= num of items)
    item_capacities:  any = None,  # default is 1 per course
    **kwargs
):
    """
    Apply the given algorithm to the given fair-course-allocation instance.

    :param algorithm: a specific algorithm for course-allocation. Should accept an AllocationBuilder object as a parameter.

    :param instance (optional): a fair-allocation instance. If instance is not given, then it is constructed using the following arguments (valuations, agent_capacities, item_capacities).
    :param valuations: any structure that maps an agent and an item to a value.
    :param agent_capacities: any structure that maps an agent to an integer capacity.
    :param item_capacities: any structure that maps an item to an integer capacity.
    :param kwargs: any other arguments expected by `algorithm`.

    :return: an allocation.

    >>> valuations = {"Alice": {"c1":2, "c2": 3, "c3": 4}, "Bob": {"c1": 4, "c2": 5, "c3": 6}}
    >>> agent_capacities = {"Alice": 2, "Bob": 1}
    >>> item_capacities  = {"c1": 2, "c2": 1, "c3": 1}
    >>> divide(algorithm=fairpy.courses.round_robin, agent_capacities=agent_capacities, item_capacities=item_capacities, valuations=valuations)
    {'Alice': ['c1', 'c3'], 'Bob': ['c2']}
    """
    if instance is None:
        instance = Instance(valuations=valuations, agent_capacities=agent_capacities, item_capacities=item_capacities)
    alloc = AllocationBuilder(instance)
    explanation_logger:ExplanationLogger = kwargs.get("explanation_logger", None)
    if explanation_logger:
        # instance.explain_valuations(explanation_logger)
        explanation_logger.explain_valuations(instance)
    algorithm(alloc, **kwargs)
    allocation = alloc.sorted()
    if explanation_logger:
        explanation_logger.info("")
        explanation_logger.explain_allocation(allocation, instance)
        # AgentBundleValueMatrix(instance, allocation, normalized=True).explain(explanation_logger)
    return allocation


def divide_with_priorities(
    algorithm: callable,
    agent_priority_classes = list[list[any]],
    instance: Instance = None,
    valuations: any = None,
    agent_capacities: any = None,  # default is unbounded (= num of items)
    item_capacities:  any = None,  # default is 1 per course
    **kwargs
):
    """
    Apply the given algorithm to the given fair-course-allocation instance, where agents are grouped into priority classes.
    Each priority class receives all its items first, before the next priority class starts getting items.

    :param algorithm: a specific algorithm for course-allocation. Should accept an AllocationBuilder object as a parameter.
    :param agent_priority_classes: a list of lists, describing a partition of the agents in the instance into priority classes.

    :param instance (optional): a fair-allocation instance. If instance is not given, then it is constructed using the following arguments (valuations, agent_capacities, item_capacities).
    :param valuations: any structure that maps an agent and an item to a value.
    :param agent_capacities: any structure that maps an agent to an integer capacity.
    :param item_capacities: any structure that maps an item to an integer capacity.
    :param kwargs: any other arguments expected by `algorithm`.

    :return: an allocation.

    >>> valuations = {"Alice": {"c1":2, "c2": 3, "c3": 4}, "Bob": {"c1": 4, "c2": 5, "c3": 6}}
    >>> agent_capacities = {"Alice": 2, "Bob": 1}
    >>> item_capacities  = {"c1": 2, "c2": 1, "c3": 1}
    >>> instance = Instance(agent_capacities=agent_capacities, item_capacities=item_capacities, valuations=valuations)
    >>> divide_with_priorities(fairpy.courses.round_robin, instance=instance, agent_priority_classes=[["Alice","Bob"]])
    {'Alice': ['c1', 'c3'], 'Bob': ['c2']}
    >>> divide_with_priorities(fairpy.courses.round_robin, instance=instance, agent_priority_classes=[["Alice"],["Bob"]]) # Alice has priority
    {'Alice': ['c2', 'c3'], 'Bob': ['c1']}
    >>> divide_with_priorities(fairpy.courses.round_robin, instance=instance, agent_priority_classes=[["Bob"],["Alice"]]) # Bob has priority
    {'Alice': ['c1', 'c2'], 'Bob': ['c3']}
    """
    if instance is None:
        instance = Instance(valuations=valuations, agent_capacities=agent_capacities, item_capacities=item_capacities)
    alloc = AllocationBuilder(instance)
    explanation_logger = kwargs.get("explanation_logger",None)
    if explanation_logger:
        # instance.explain_valuations(explanation_logger)
        explanation_logger.explain_valuations(instance)
    for priority_class in agent_priority_classes:
        alloc.remaining_agent_capacities = {agent:instance.agent_capacity(agent) for agent in priority_class}
        algorithm(alloc, **kwargs)
    allocation = alloc.sorted()
    if explanation_logger:
        explanation_logger.info("")
        explanation_logger.explain_allocation(allocation, instance)
    return allocation



def divide_random_instance(
        algorithm:callable, 
        num_of_agents:int, num_of_items:int, 
        agent_capacity_bounds:tuple, item_capacity_bounds:tuple, 
        item_base_value_bounds:tuple, item_subjective_ratio_bounds:tuple,
        normalized_sum_of_values:float, 
        random_seed:int=None, 
        **kwargs
):
    if random_seed is None:
        random_seed = np.random.randint(1, 2**31)
    np.random.seed(random_seed)
    print("Random seed: ", random_seed)

    random_instance = Instance.random(num_of_agents=num_of_agents, num_of_items=num_of_items, agent_capacity_bounds=agent_capacity_bounds, item_capacity_bounds=item_capacity_bounds, 
                                      item_base_value_bounds=item_base_value_bounds, item_subjective_ratio_bounds=item_subjective_ratio_bounds,
                                      normalized_sum_of_values=normalized_sum_of_values, random_seed=random_seed)
    allocation = divide(algorithm, instance=random_instance, **kwargs)
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

    # divide_random_instance(
    #     fairpy.courses.round_robin, num_of_agents=70, num_of_items=10, agent_capacity_bounds=[6,6], item_capacity_bounds=[40,40], 
    #     item_base_value_bounds=[0,200], item_subjective_ratio_bounds=[0.5,1.5],
    #     normalized_sum_of_values=1000
    # )

