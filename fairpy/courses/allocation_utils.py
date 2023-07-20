"""
Utils for post-processing allocations
"""

import numpy as np

from fairpy.courses.instance import Instance
from typing import *
from collections import defaultdict


def validate_allocation(instance:Instance, allocation:dict, title:str=""):
    """
    Validate that the given allocation is feasible for the given input-instance.
    Checks agent capacities, item capacities, and uniqueness of items.

    >>> instance = Instance(
    ...   agent_capacities = {"Alice": 2, "Bob": 3}, 
    ...   item_capacities  = {"c1": 1, "c2": 2, "c3": 3}, 
    ...   valuations       = {"Alice": {"c1": 11, "c2": 22, "c3": 33}, "Bob": {"c1": 33, "c2": 44, "c3": 55}})
    >>> validate_allocation(instance, allocation = {"Alice": ["c1", "c2"]})
    >>> validate_allocation(instance, allocation = {"Alice": ["c1", "c2", "c3"]})
    Traceback (most recent call last):
    ...
    ValueError: : Agent Alice has capacity 2, but received more items: ['c1', 'c2', 'c3'].
    >>> validate_allocation(instance, allocation = {"Alice": ["c1", "c1"]})
    Traceback (most recent call last):
    ...
    ValueError: : Agent Alice received two or more copies of the same item. Bundle: ['c1', 'c1'].
    >>> validate_allocation(instance, allocation = {"Alice": ["c1", "c2"], "Bob": ["c2","c3"]})
    >>> validate_allocation(instance, allocation = {"Alice": ["c1", "c2"], "Bob": ["c2","c1"]})
    Traceback (most recent call last):
    ...
    ValueError: : Item c1 has capacity 1, but is given to more agents: ['Alice', 'Bob'].
    >>> validate_allocation(instance, allocation = {"Alice": ["c1"], "Bob": ["c2","c3"]})
    Traceback (most recent call last):
    ...
    ValueError: : Wasteful allocation:
    Item c2 has remaining capacity: 2>['Bob'].
    Agent Alice has remaining capacity: 2>['c1'].    
    """

    ### validate agent capacity and uniqueness:
    agents_below_their_capacity = []
    for agent,bundle in allocation.items():
        agent_capacity = instance.agent_capacity(agent)
        if len(bundle) > agent_capacity:
            raise ValueError(f"{title}: Agent {agent} has capacity {agent_capacity}, but received more items: {bundle}.")
        if len(set(bundle))!=len(bundle):
            raise ValueError(f"{title}: Agent {agent} received two or more copies of the same item. Bundle: {bundle}.")
        if len(bundle) < agent_capacity:
            agents_below_their_capacity.append(agent)

    ### validate item capacity:
    map_item_to_list_of_owners = defaultdict(list)
    items_below_their_capacity = []
    for agent,bundle in allocation.items():
        for item in bundle:
            map_item_to_list_of_owners[item].append(agent)
    for item,list_of_owners in map_item_to_list_of_owners.items():
        item_capacity = instance.item_capacity(item)
        if len(list_of_owners) > item_capacity:
            raise ValueError(f"{title}: Item {item} has capacity {item_capacity}, but is given to more agents: {list_of_owners}.")
        if len(list_of_owners) < item_capacity:
            items_below_their_capacity.append(item)

    ### validate no waste:
    for agent in agents_below_their_capacity:
        for item in items_below_their_capacity:
            bundle = allocation[agent]
            if item not in bundle and instance.agent_item_value(agent,item)>0:
                item_message = f"Item {item} has remaining capacity: {instance.item_capacity(item)}>{map_item_to_list_of_owners[item]}."
                agent_message = f"Agent {agent} has remaining capacity: {instance.agent_capacity(agent)}>{bundle}."
                raise ValueError(f"{title}: Wasteful allocation:\n{item_message}\n{agent_message}")



def sorted_allocation(map_agent_name_to_bundle:dict):
    for agent,bundle in map_agent_name_to_bundle.items():
        if isinstance(bundle,list):
            bundle.sort()
        else: 
            map_agent_name_to_bundle[agent] = sorted(bundle)
    return map_agent_name_to_bundle

def rounded_allocation(allocation_matrix:dict, digits:int):
    return {agent:{item:np.round(allocation_matrix[agent][item],digits) for item in allocation_matrix[agent].keys()} for agent in allocation_matrix.keys()}


if __name__ == "__main__":
    import doctest
    print(doctest.testmod(optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE))
