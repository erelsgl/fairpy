"""
class fairpy.courses.Instance:  an instance of the fair course allocation problem.

Author: Erel Segal-Halevi
Since: 2023-07
"""

from numbers import Number
import numpy as np
from functools import cache
# from fairpy.courses.explanations import ExplanationLogger
from collections import defaultdict

import logging
logger = logging.getLogger(__name__)


class Instance:
    """
    Represents an instance of the fair course-allocation problem.
    Exposes the following functions:
     * agent_capacity:       maps an agent name/index to its capacity (num of seats required).
     * item_capacity:        maps an item  name/index to its capacity (num of seats allocated).
     * agent_conflicts:      maps an agent  name/index to a set of items that conflict with it (- cannot be allocated to this agent).
     * item_conflicts:       maps an item  name/index to a set of items that conflict with it (- cannot be allocated together).
     * agent_item_value:     maps an agent,item pair to the agent's value for the item.
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
    >>> instance.agent_fractionalbundle_value("Bob", {"c1":1, "c2":0.5})
    55.0
    >>> instance.agent_maximum_value("Alice")
    33
    >>> instance.agent_maximum_value("Bob")
    77
    >>> instance.agent_ranking("Alice", [])
    {'c2': 1, 'c1': 2}
    >>> instance.agent_ranking("Alice", ["c1"])
    {'c2': 1, 'c1': 2}
    >>> instance.agent_ranking("Alice", ["c2"])
    {'c2': 1, 'c1': 2}

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
    >>> instance.agent_maximum_value("Alice")
    99
    >>> instance.agent_maximum_value("Bob")
    264


    ### default values:
    >>> instance = Instance(valuations={"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}})
    >>> instance.agent_capacity("avi")
    2
    >>> instance.item_capacity("x")
    1
    >>> instance.agent_item_value("beni", "y")
    3
    >>> instance.agent_entitlement("Alice")
    1
    >>> instance.agent_conflicts("Alice")
    set()
    >>> instance.item_conflicts("c1")
    set()

    ### agent rankings
    >>> instance = Instance(valuations={"avi": {"x":5, "y": 5}, "beni": {"x":3, "y":3}}, agent_capacities=1)
    >>> instance.agent_capacity("avi")
    1
    >>> instance.agent_ranking("avi", ["x"])
    {'x': 1, 'y': 2}
    >>> instance.agent_ranking("avi", ["y"])
    {'y': 1, 'x': 2}

    ### conflicts:
    >>> instance = Instance(
    ...   agent_conflicts = {"Alice": {0,1,2}, "Bob": {2,3,4}}, 
    ...   item_conflicts  = [{"Alice", "Bob"}, set(), {"Alice"}, {"Bob"}, set()], 
    ...   valuations       = {"Alice": [22,33,44,55,66], "Bob": [66,77,88,99,100]})
    >>> instance.agent_conflicts("Bob")
    {2, 3, 4}
    >>> instance.item_conflicts(2)
    {'Alice'}
    """

    def __init__(self, valuations:any, agent_capacities:any=None, agent_entitlements:any=None, item_capacities:any=None, agent_conflicts:any=None, item_conflicts:any=None, agents:list=None, items:list=None):
        """
        Initialize an instance from the given 
        """
        agent_value_keys, item_value_keys, agent_item_value_func = get_keys_and_mapping_2d(valuations)

        agent_capacity_keys, agent_capacity_func = get_keys_and_mapping(agent_capacities)
        agent_entitlement_keys, agent_entitlement_func = get_keys_and_mapping(agent_entitlements)
        item_capacity_keys , item_capacity_func  = get_keys_and_mapping(item_capacities)

        self.agents = agents or agent_value_keys or agent_capacity_keys or agent_entitlement_keys 
        assert (self.agents is not None)
        self.num_of_agents = len(self.agents)
        self.items  = items  or item_capacity_keys or item_value_keys
        assert (self.items is not None)
        self.num_of_items = len(self.items)

        self.agent_capacity = agent_capacity_func or constant_function(len(self.items))
        self.agent_entitlement = agent_entitlement_func or constant_function(1)
        self.item_capacity  = item_capacity_func  or constant_function(1)
        self.agent_item_value = agent_item_value_func

        self.agent_conflicts = get_conflicts(agent_conflicts) or constant_function(set())
        self.item_conflicts = get_conflicts(item_conflicts) or constant_function(set())

        # Keep the input parameters, for debug
        self._agent_capacities = agent_capacities
        self._item_capacities  = item_capacities
        self._valuations       = valuations


    def agent_bundle_value(self, agent:any, bundle:list[any]):
        """
        Return the agent's value for a bundle (a list of items).
        """
        return sum([self.agent_item_value(agent,item) for item in bundle])

    def agent_fractionalbundle_value(self, agent:any, bundle:list[any]):
        """
        Return the agent's value for a fractional bundle (a dict mapping items to fractions).
        """
        return sum([self.agent_item_value(agent,item)*fraction for item,fraction in bundle.items()])
    
    def agent_ranking(self, agent:any, prioritized_items:list=[])->dict:
        """
        Compute a map in which each item is mapped to its ranking: the best item is mapped to 1, the second-best to 2, etc.

        :prioritized_items: a list of items that are "prioritized". 
             This list is used for tie-breaking, in cases the agent assigns the same value to different items.
        """
        other_items = [item for item in self.items if item not in prioritized_items]
        valuation = lambda item: self.agent_item_value(agent,item)
        sorted_items = sorted(prioritized_items + other_items, key=valuation, reverse=True)
        result = {}
        for i,item in enumerate(sorted_items):
            result[item] = i+1
        return result
    
    def map_agent_to_ranking(self, map_agent_to_prioritized_items={})->dict:
        """
        Compute a map in which each agent is mapped to a dict mapping each item to its ranking.
        For example, if item 'x' is the best item of Alice, then result["Alice"]["x"]==1.

        :map_agent_to_prioritized_items: maps each agent to a list of items that are "prioritized". 
             This list is used for tie-breaking, in cases the agent assigns the same value to different items.
        """
        return {agent: self.agent_ranking(agent, map_agent_to_prioritized_items[agent]) for agent in self.agents}

    
    @cache
    def agent_maximum_value(self, agent:any):
        """
        Return the maximum possible value of an agent: the sum of the top x items, where x is the agent's capacity.
        """
        return sum(sorted([self.agent_item_value(agent,item) for item in self.items],reverse=True)[0:self.agent_capacity(agent)])

    def agent_normalized_item_value(self, agent:any, item:any):
        return self.agent_item_value(agent,item) / self.agent_maximum_value(agent) * 100

    @staticmethod
    def random_uniform(num_of_agents:int, num_of_items:int, 
               agent_capacity_bounds:tuple[int,int],
               item_capacity_bounds:tuple[int,int],
               item_base_value_bounds:tuple[int,int],
               item_subjective_ratio_bounds:tuple[float,float],
               normalized_sum_of_values:int,
               agent_name_template="s{index}", item_name_template="c{index}",
               random_seed:int=None,
               ):
        """
        Generate a random instance by drawing values from uniform distributions.
        """
        if random_seed is None:
            random_seed = np.random.randint(1, 2**31)
        np.random.seed(random_seed)
        logger.info("Random seed: %d", random_seed)
        agents  = [agent_name_template.format(index=i+1) for i in range(num_of_agents)]
        items   = [item_name_template.format(index=i+1) for i in range(num_of_items)]
        agent_capacities  = {agent: np.random.randint(agent_capacity_bounds[0], agent_capacity_bounds[1]+1) for agent in agents}
        item_capacities   = {item: np.random.randint(item_capacity_bounds[0], item_capacity_bounds[1]+1) for item in items}
        base_values = normalized_valuation(random_valuation(num_of_items, item_base_value_bounds), normalized_sum_of_values)
        valuations = {
            agent: dict(zip(items, normalized_valuation(
                base_values *  random_valuation(num_of_items, item_subjective_ratio_bounds),
                normalized_sum_of_values
            )))
            for agent in agents
        }
        return Instance(valuations=valuations, agent_capacities=agent_capacities, item_capacities=item_capacities)
    

    @staticmethod
    def random_szws(num_of_agents:int, num_of_items:int, 
               agent_capacity:int,
               supply_ratio:float,         # The ratio: total number of items / total demand. The item capacity is determined by this number; all items have the same capacity.
               num_of_popular_items:int,   # Items 1,...,num_of_popular_items will be considered "popular", and have a high value for many students.
               num_of_favorite_items:int,  # For each student, a subset of num_of_favorite_items items out of the popular ones will be selected as "favorite".
               favorite_item_value_bounds:tuple[int,int],    # The value of a favorite course will be selected uniformly at random from this range.
               nonfavorite_item_value_bounds:tuple[int,int], # The value of a non-favorite course will be selected uniformly at random from this range.
               normalized_sum_of_values:int,
               agent_name_template="s{index}", item_name_template="c{index}",
               random_seed:int=None,
               ):
        """
        Generate a random instance with additive utilities, using the process described at:
            Soumalias, Zamanlooy, Weissteiner, Seuken: "Machine Learning-powered Course Allocation", arXiv 2210.00954, subsection 5.1
        NOTE: currently, we do not generate complementarities and substitutabilities. We also do not model reporting mistakes.
        """
        if random_seed is None:
            random_seed = np.random.randint(1, 2**31)
        np.random.seed(random_seed)
        logger.info("Random seed: %d", random_seed)

        item_capacity = np.round((supply_ratio * agent_capacity * num_of_agents) / num_of_items)

        agents  = [agent_name_template.format(index=i+1) for i in range(num_of_agents)]
        items   = [item_name_template.format(index=i+1) for i in range(num_of_items)]

        valuations = {}
        for agent in agents:
            favorite_items = np.random.choice(num_of_popular_items, num_of_favorite_items, replace=False)
            print(f"favorite_items for {agent}: ",favorite_items)
            valuation = np.zeros(num_of_items)
            for item_index in range(num_of_items):
                value_bounds = favorite_item_value_bounds if item_index in favorite_items else nonfavorite_item_value_bounds
                valuation[item_index] = np.random.uniform(low=value_bounds[0], high=value_bounds[1]+1)
            valuations[agent] = dict(zip(items, normalized_valuation(valuation, normalized_sum_of_values)))

        return Instance(valuations=valuations, agent_capacities=agent_capacity, item_capacities=item_capacity)


    @staticmethod
    def random_sample(max_num_of_agents:int, max_total_agent_capacity:int,
        prototype_valuations:dict, prototype_agent_capacities:dict, prototype_agent_conflicts:dict,
        item_capacities:dict, item_conflicts:dict, 
        random_seed:int=None,
        ):
        """
        Generate a random instance by sampling values of existing agents.

        :param max_num_of_agents: creates at most this number of agents.
        :param max_total_agent_capacity: the total capacity of all agents will be at most this number plus one agent.


        """
        if random_seed is None:
            random_seed = np.random.randint(1, 2**31)
        np.random.seed(random_seed)
        logger.info("Random seed: %d", random_seed)
        prototype_agents = list(prototype_valuations.keys())

        agent_capacities = dict()
        agent_conflicts = dict()
        valuations = dict()

        def add_agent(new_agent, prototype_agent):
            nonlocal max_total_agent_capacity, max_num_of_agents, agent_capacities, valuations, agent_conflicts
            new_agent_capacity = prototype_agent_capacities[prototype_agent]
            agent_capacities[new_agent] = new_agent_capacity
            if prototype_agent in prototype_agent_conflicts:
                agent_conflicts[new_agent]  = prototype_agent_conflicts[prototype_agent]
            valuations[new_agent] = prototype_valuations[prototype_agent]
            max_total_agent_capacity -= new_agent_capacity
            max_num_of_agents -= 1

        # First, add one copy of each prototype agent:
        for agent in prototype_agents:
            add_agent(f"{agent}", agent)

        # Next, add random copies until one of the max_ values is hit:
        i = 1
        while True:
            prototype_agent = np.random.choice(prototype_agents)
            new_agent = f"random{i}.{prototype_agent}"
            add_agent(new_agent, prototype_agent)
            if max_total_agent_capacity<=0:
                break
            if max_num_of_agents<=0:
                break
            i += 1

        return Instance(valuations=valuations, agent_capacities=agent_capacities, agent_conflicts=agent_conflicts,
                        item_capacities=item_capacities, item_conflicts=item_conflicts)


        

def random_valuation(numitems:int, item_value_bounds: tuple[float,float])->np.ndarray:
    """
    >>> r = random_valuation(10, [30, 40])
    >>> len(r)
    10
    >>> all(r>=30)
    True
    """
    return np.random.uniform(low=item_value_bounds[0], high=item_value_bounds[1]+1, size=numitems)

def normalized_valuation(raw_valuations:np.ndarray, normalized_sum_of_values:float):
    raw_sum_of_values = sum(raw_valuations)
    return  np.round(raw_valuations * normalized_sum_of_values / raw_sum_of_values).astype(int)


def get_keys_and_mapping(container: any) -> tuple[list,callable]:
    """
    Given a container of any supported type, returns:
    * an iterable of the container's keys;
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

    ### constant value
    >>> k,f = get_keys_and_mapping(1)
    >>> k   # None
    >>> f(2)
    1
    """
    if container is None:
        func = keys = None
    elif isinstance(container, dict):
        keys = container.keys()
        func = container.__getitem__
    elif isinstance(container, list):
        keys = range(len(container))
        func = container.__getitem__
    elif isinstance(container, np.ndarray):
        keys = range(len(container))
        func = container.__getitem__
    elif isinstance(container,Number):
        keys = None    # keys are unknown
        func = constant_function(container)
    elif callable(container):
        keys = None   # keys are unknown
        func = container 
    else:
        raise TypeError(f"container {container} of unknown type: {type(container)}")
    return keys,func
    

def get_keys_and_mapping_2d(container: any) -> tuple[list,callable]:
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
    >>> k1,k2,f = get_keys_and_mapping_2d([[11,22,33],[33,44,55]])
    >>> sorted(k1)
    [0, 1]
    >>> sorted(k2)
    [0, 1, 2]
    >>> f(0,1)
    22
    >>> f(1,0)
    33

    ### ndarray
    >>> k1,k2,f = get_keys_and_mapping_2d(np.array([[11,22,33],[33,44,55]]))
    >>> sorted(k1)
    [0, 1]
    >>> sorted(k2)
    [0, 1, 2]
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
        # f = lambda agent,item: container.get(agent,dict()).get(item,0)
        # f = lambda agent,item: container[agent].get(item,0)
        # f = lambda agent,item: container[agent][item]
        f = lambda agent,item: \
            container[agent].get(item,0) if isinstance(container[agent],dict) else container[agent][item]
        k1 = container.keys()
        k2, _ = get_keys_and_mapping(container[next(iter(container))])
    elif isinstance(container,list):
        f = lambda agent,item: container[agent][item]
        k1 = range(len(container))
        k2, _ = get_keys_and_mapping(container[0])
    elif isinstance(container, np.ndarray):
        f = lambda agent,item: container[agent][item]
        k1 = range(container.shape[0])
        k2 = range(container.shape[1])
    elif callable(container):
        f = container
        k1 = k2 = None
    else:
        raise TypeError(f"agent_item_value {container} of unknown type: {type(container)}")
    return k1,k2,f


def get_conflicts(container:any):
    """
    Given a container of any supported type, returns a callable function 
    that maps each key to a list of conflicting items.

    ### dict of lists
    >>> f = get_conflicts({"a":[1,2,3], "b":[3,4,5]})
    >>> f("a")
    [1, 2, 3]
    """
    if container is None:
        func = None
    elif isinstance(container, dict):   # dict of lists
        func = lambda x: container.get(x, set())
    elif isinstance(container, list):   # list of lists
        func = container.__getitem__
    elif callable(container):
        func = container 
    else:
        raise TypeError(f"container {container} of unknown type: {type(container)}")
    return func
    

Instance.logger = logger

def constant_function(constant_value)->callable:
    return lambda key:constant_value


if __name__ == "__main__":
    import doctest, sys
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)

    print(doctest.testmod())

    random_instance = Instance.random_uniform(
        num_of_agents=5, num_of_items=3, 
        agent_capacity_bounds=[2,6], item_capacity_bounds=[30,50], 
        item_base_value_bounds=[1,200], item_subjective_ratio_bounds=[0.5,1.5],
        # agent_name_template="agent{index}", item_name_template="item{index}",
        normalized_sum_of_values=1000)
    print("agents: ", random_instance.agents)
    print("items: ", random_instance.items)
    print("valuations: ", random_instance._valuations, "\n")

    random_instance = Instance.random_szws(  # SZWS experiment:
        num_of_agents=10, num_of_items=10, 
        agent_capacity=5, 
        supply_ratio = 1.25,      # 1.25, 1.5
        num_of_popular_items=6,   # 6, 9
        num_of_favorite_items=4,  # ?
        favorite_item_value_bounds=[100,200],
        nonfavorite_item_value_bounds=[1,100],
        normalized_sum_of_values=1000)
    print("agents: ", random_instance.agents)
    print("items: ", random_instance.items)
    print("item_capacities: ", random_instance._item_capacities)
    print("valuations: ", random_instance._valuations, "\n")

    random_instance = Instance.random_sample(
        max_num_of_agents=8, max_total_agent_capacity=1000,
        prototype_agent_capacities={"Alice": 5, "Bob": 6, "Chana": 7}, prototype_valuations={"Alice": {"c1": 55, "c2": 66, "c3": 77}, "Bob": {"c1": 77, "c2": 66, "c3": 55}, "Chana": {"c1": 66, "c2": 77, "c3": 55}},
        prototype_agent_conflicts={"Alice": ["c1"]},
        item_capacities={"c1": 5, "c2": 6, "c3": 7}, item_conflicts={})
    print("agents: ", random_instance.agents)
    print("items: ", random_instance.items)
    print("valuations: ", dict(random_instance._valuations), "\n")


    # Test the cache    
    # print(random_instance.agent_maximum_value("s1"))
    # print(random_instance.agent_maximum_value("s2"))
    # print(random_instance.agent_maximum_value("s1"))

