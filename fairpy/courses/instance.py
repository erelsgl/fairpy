"""
class fairpy.courses.Instance:  an instance of the fair course allocation problem.

Author: Erel Segal-Halevi
Since: 2023-07
"""

from typing import Callable, List, Any, Tuple
import numpy as np


class Instance:
    """
    Represents an instance of the fair course-allocation problem.
    Exposes the following functions:
     * agent_capacity:       maps an agent name/index to its capacity (num of seats required).
     * item_capacity:        maps an item  name/index to its capacity (num of seats allocated).
     * agent_item_value:      maps an agent,item pair to the agent's value for the item.
     * agents: an enumeration of the agents (derived from agent_capacity).
     * items: an enumeration of the items (derived from item_capacity).

    ### dict of dicts:
    >>> instance = Instance(
    ...   agent_capacities = {"Alice": 2, "Bob": 3}, 
    ...   item_capacities  = {"c1": 4, "c2": 5}, 
    ...   valuations       = {"Alice": {"c1": 11, "c2": 22}, "Bob": {"c1": 33, "c2": 44}})
    >>> instance.agent_capacity("Alice")
    2
    >>> instance.item_capacity("c2")
    5
    >>> instance.agent_item_value("Bob", "c1")
    33
    >>> instance.agent_bundle_value("Bob", ["c1","c2"])
    77

    ### dict of lists:
    >>> instance = Instance(
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
        self.agent_priority = agent_priority_func or default_agent_priority_func(1)
        self.item_capacity  = item_capacity_func  or default_item_capacity_func(1)
        self.agent_item_value = agent_item_value_func

        # Keep the input parameters, for debug
        self._agent_capacities = agent_capacities
        self._item_capacities  = item_capacities
        self._valuations       = valuations


    def agent_bundle_value(self, agent:Any, bundle:List[Any]):
        return sum([self.agent_item_value(agent,item) for item in bundle])
    

    @staticmethod
    def random(num_of_agents, num_of_items, 
               agent_capacity_bounds,
               item_capacity_bounds,
               item_value_bounds,
               normalized_sum_of_values):
        """
        Generate a random instance.
        """
        agents  = [f"s{i+1}" for i in range(num_of_agents)]
        items   = [f"c{i+1}" for i in range(num_of_items)]
        agent_capacities  = {agent: np.random.randint(agent_capacity_bounds[0], agent_capacity_bounds[1]+1) for agent in agents}
        item_capacities   = {item: np.random.randint(item_capacity_bounds[0], item_capacity_bounds[1]+1) for item in items}
        valuations = {
            agent: random_valuation(items, item_value_bounds, normalized_sum_of_values)
            for agent in agents
        }
        return Instance(valuations=valuations, agent_capacities=agent_capacities, item_capacities=item_capacities)
        


def random_valuation(items, item_value_bounds, normalized_sum_of_values):
    valuations = {
        item: np.random.randint(item_value_bounds[0],item_value_bounds[1]+1)
        for item in items
    }
    raw_sum_of_values = sum(valuations.values())
    return  { 
        item: int(np.round(value*normalized_sum_of_values/raw_sum_of_values))
        for item,value in valuations.items()
    }



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


def default_agent_priority_func(default_priority:int):
    return lambda agent:default_priority


def default_item_capacity_func(default_capacity:int=1):
    return lambda item:default_capacity


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())

    random_instance = Instance.random(num_of_agents=4, num_of_items=2, agent_capacity_bounds=[6,6], item_capacity_bounds=[40,40], item_value_bounds=[1,200], normalized_sum_of_values=1000)
    print(random_instance.agents)
    print(random_instance.items)
    print(random_instance._valuations)

    random_instance = Instance.random(num_of_agents=70, num_of_items=10, agent_capacity_bounds=[6,6], item_capacity_bounds=[40,40], item_value_bounds=[1,200], normalized_sum_of_values=1000)
    print(random_instance.agents)
    print(random_instance.items)
    print(random_instance._valuations)
