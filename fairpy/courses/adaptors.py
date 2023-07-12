"""
This module implements Adaptor functions for fair course allocation algorithms.

The functions accept a course allocation algorithm as an argument.

They allow you to call the allocation algorithm with convenient input types,
such as: a list of values, or a dict that maps an item to its value.

Author: Erel Segal-Halevi
Since: 2023-07
"""

import fairpy
from typing import Callable, List, Any
from fairpy.courses.instance import Instance

def divide(
    algorithm: Callable,
    valuations: Any,
    agent_capacities: Any = None,  # default is unbounded (= num of items)
    agent_priorities: Any = None,  # default is that all agents have same priority
    item_capacities:  Any = None,  # default is 1 per course
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

    >>> crs = fairpy.courses
    >>> valuations = {"Alice": {"c1":2, "c2": 3, "c3": 4}, "Bob": {"c1": 4, "c2": 5, "c3": 6}}
    >>> agent_capacities = {"Alice": 2, "Bob": 1}
    >>> item_capacities  = {"c1": 2, "c2": 1, "c3": 1}
    >>> divide(algorithm=crs.round_robin, agent_capacities=agent_capacities, item_capacities=item_capacities, valuations=valuations)
    {'Alice': ['c1', 'c3'], 'Bob': ['c2']}
    """
    instance = Instance(valuations=valuations, agent_capacities=agent_capacities, agent_priorities=agent_priorities, item_capacities=item_capacities)
    result = algorithm(instance, **kwargs)
    return result



if __name__ == "__main__":
    import doctest, sys
    print(doctest.testmod())
