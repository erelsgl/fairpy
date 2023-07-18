"""
Given an instance and an allocation, validate that the allocation is feasible.
"""

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
    ...   valuations       = {"Alice": {"c1": 11, "c2": 22}, "Bob": {"c1": 33, "c2": 44}})
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
    """

    ### validate agent capacity and uniqueness:
    for agent,bundle in allocation.items():
        agent_capacity = instance.agent_capacity(agent)
        if len(bundle) > agent_capacity:
            raise ValueError(f"{title}: Agent {agent} has capacity {agent_capacity}, but received more items: {bundle}.")
        if len(set(bundle))!=len(bundle):
            raise ValueError(f"{title}: Agent {agent} received two or more copies of the same item. Bundle: {bundle}.")

    ### validate item capacity:
    map_item_to_list_of_owners = defaultdict(list)
    for agent,bundle in allocation.items():
        for item in bundle:
            map_item_to_list_of_owners[item].append(agent)
    for item,list_of_owners in map_item_to_list_of_owners.items():
        item_capacity = instance.item_capacity(item)
        if len(list_of_owners) > item_capacity:
            raise ValueError(f"{title}: Item {item} has capacity {item_capacity}, but is given to more agents: {list_of_owners}.")




if __name__ == "__main__":
    import doctest
    print(doctest.testmod(optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE))
