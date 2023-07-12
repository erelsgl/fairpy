"""
class FairCourseAllocationInstance:  an instance of the fair course allocation problem.

Author: Erel Segal-Halevi
Since: 2023-07
"""

from typing import Callable, List, Any, Tuple


class FairCourseAllocationInstance:
    """
    Represents an instance of the fair course-allocation problem.
    Exposes the following functions:
     * agent_capacity:       maps an agent name/index to its capacity (num of seats required).
     * item_capacity:        maps an item  name/index to its capacity (num of seats allocated).
     * agent_item_value:      maps an agent,item pair to the agent's value for the item.
     * agents: an enumeration of the agents (derived from agent_capacity).
     * items: an enumeration of the items (derived from item_capacity).

    ### dict of dicts:
    >>> instance = FairCourseAllocationInstance(
    ...   agent_capacities = {"Alice": 2, "Bob": 3}, 
    ...   item_capacities  = {"c1": 4, "c2": 5}, 
    ...   valuations       = {"Alice": {"c1": 11, "c2": 22}, "Bob": {"c1": 33, "c2": 44}})
    >>> instance.agent_capacity("Alice")
    2
    >>> instance.item_capacity("c2")
    5
    >>> instance.agent_item_value("Bob", "c1")
    33

    ### dict of lists:
    >>> instance = FairCourseAllocationInstance(
    ...   agent_capacities = {"Alice": 2, "Bob": 3}, 
    ...   item_capacities  = [1,2,3,4], 
    ...   valuations       = {"Alice": [22,33,44,55], "Bob": [66,77,88,99]})
    >>> instance.agent_capacity("Alice")
    2
    >>> instance.item_capacity(2)
    3
    >>> instance.agent_item_value("Alice", 3)
    55
    """

    def __init__(self, valuations:Any, agent_capacities:Any=None, agent_priorities:Any=None, item_capacities:Any=None, agents:list=None, items:list=None):
        """
        Initialize an instance from the given 
        """
        agent_value_keys, item_value_keys, agent_item_value_func = get_keys_and_mapping_2d(valuations)

        agent_capacity_keys, agent_capacity_func = get_keys_and_mapping(agent_capacities)
        agent_priority_keys, agent_priority_func = get_keys_and_mapping(agent_priorities)
        item_capacity_keys , item_capacity_func  = get_keys_and_mapping(item_capacities)

        self.agents = agents or agent_capacity_keys or agent_priority_keys or agent_value_keys
        self.items  = items  or item_capacity_keys or item_value_keys

        self.agent_capacity = agent_capacity_func or default_agent_capacity_func(len(self.items))
        self.item_capacity  = item_capacity_func  or default_item_capacity_func(1)
        self.agent_item_value = agent_item_value_func



def get_keys_and_mapping(container: Any) -> Tuple[List,Callable]:
    """
    Given a container of any supported type, returns:
    * a list of the container's keys;
    * a callable function that maps each key to its value.

    ### dict
    >>> k,f = get_keys_and_mapping({"a":1, "b":2})
    >>> sorted(k)
    ['a', 'b']
    >>> f("a")
    1

    ### list
    >>> k,f = get_keys_and_mapping([11, 12])
    >>> sorted(k)
    [0, 1]
    >>> f(1)
    12

    ### callable
    >>> k,f = get_keys_and_mapping(lambda item:item+5)
    >>> k   # None
    >>> f(2)
    7
    """
    if container is None:
        f = k = None
    elif isinstance(container, dict):
        k = container.keys()
        f = container.__getitem__
    elif isinstance(container, list):
        k = range(len(container))
        f = container.__getitem__
    elif callable(container):
        k = None   # keys are unknown
        f = container 
    else:
        raise TypeError(f"container {container} of unknown type: {type(container)}")
    return k,f
    

def get_keys_and_mapping_2d(container: Any) -> Tuple[List,Callable]:
    """
    Given a 2-dimensional container of any supported type, returns:
    * a list of the container's keys at first level;
    * a list of the container's keys at second level;
    * a callable function that maps each key-pair to a value.

    ### dict
    >>> k1,k2,f = get_keys_and_mapping_2d({"a": {"x":11, "y":22, "z": 33}, "b": {"x": 55, "y":33, "z":44}})
    >>> sorted(k1)
    ['a', 'b']
    >>> sorted(k2)
    ['x', 'y', 'z']
    >>> f('a','x')
    11
    >>> f('b','z')
    44

    ### list
    >>> k1,k2,f = get_keys_and_mapping_2d([[11,22],[33,44]])
    >>> sorted(k1)
    [0, 1]
    >>> sorted(k2)
    [0, 1]
    >>> f(0,1)
    22
    >>> f(1,0)
    33

    ### callable
    >>> k1,k2,f = get_keys_and_mapping_2d(lambda agent,item: agent+item)
    >>> k1   # None
    >>> k2   # None
    >>> f(1,2)
    3
    """
    if container is None:
        f = k1 = k2 = None
    elif isinstance(container,dict):
        f = lambda agent,item: container[agent][item]
        k1 = container.keys()
        k2, _ = get_keys_and_mapping(container[next(iter(container))])
    elif isinstance(container,list):
        f = lambda agent,item: container[agent][item]
        k1 = range(len(container))
        k2, _ = get_keys_and_mapping(container[0])
    elif callable(container):
        f = container
        k1 = k2 = None
    else:
        raise TypeError(f"agent_item_value {container} of unknown type: {type(container)}")
    return k1,k2,f

    


def default_agent_capacity_func(default_capacity:int):
    return lambda agent:default_capacity


def default_item_capacity_func(default_capacity:int=1):
    return lambda item:default_capacity


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
