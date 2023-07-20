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

def rounded_allocation(allocation_matrix:dict, digits:int):
    return {agent:{item:np.round(allocation_matrix[agent][item],digits) for item in allocation_matrix[agent].keys()} for agent in allocation_matrix.keys()}

def allocation_is_fractional(allocation:dict)->bool:
    """
    Weak check if the given allocation is fractional.
    The check is made only on one arbitrary bundle.

    >>> allocation_is_fractional({"agent1": {"item1": 0.3, "item2": 0.4}})
    True
    >>> allocation_is_fractional({"agent1": ["item1", "item2"]})
    False
    """
    arbitrary_bundle = next(iter(allocation.values()))
    if isinstance(arbitrary_bundle,list):
        return False
    elif isinstance(arbitrary_bundle,dict):
        arbitrary_value = next(iter(arbitrary_bundle.values()))
        if isinstance(arbitrary_value,float):
            return True
    raise ValueError(f"Bundle format is unknown: {arbitrary_bundle}")


class AllocationBuilder:
    """
    A class for incrementally constructing an allocation.
    """
    def __init__(self, instance:Instance):
        self.instance = instance
        self.remaining_agent_capacities = {agent: instance.agent_capacity(agent) for agent in instance.agents}
        self.remaining_item_capacities = {item: instance.item_capacity(item) for item in instance.items}
        self.bundles = {agent: set() for agent in instance.agents}    # Each bundle is a set, since each agent can get at most one seat in each course

    def remove_item(self, item:Any):
        del self.remaining_item_capacities[item]

    def remove_agent(self, agent:Any):
        del self.remaining_agent_capacities[agent]

    def give(self, agent:Any, item:Any, logger=None):
        if agent not in self.remaining_agent_capacities:
            raise ValueError(f"Agent {agent} has no remaining capacity")
        if item not in self.remaining_item_capacities:
            raise ValueError(f"Item {item} has no remaining capacity")
        self.bundles[agent].add(item)
        if logger is not None:
            logger.info("Agent %s takes item %s with value %s", agent, item, self.instance.agent_item_value(agent, item))
        self.remaining_agent_capacities[agent] -= 1
        if self.remaining_agent_capacities[agent] <= 0:
            self.remove_agent(agent)
        self.remaining_item_capacities[item] -= 1
        if self.remaining_item_capacities[item] <= 0:
            self.remove_item(item)


    def sorted(self):
        # Each bundle is a set:
        return {agent: sorted(bundle) for agent,bundle in self.bundles.items()}
    
        # Old version - each bundle is a list:
        for agent,bundle in self.bundles.items():
            bundle.sort()
        return self.bundles


if __name__ == "__main__":
    import doctest
    print(doctest.testmod(optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE))
