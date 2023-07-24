"""
Allocate course seats using a picking sequence.

Three interesting special cases of a picking-sequence are: round-robin, balanced round-robin, and serial dictatorship.

Programmer: Erel Segal-Halevi
Since: 2023-06
"""

from fairpy.courses.instance import Instance
from itertools import cycle
from fairpy.courses.allocation_utils import AllocationBuilder

import logging
logger = logging.getLogger(__name__)




def picking_sequence(instance: Instance, agent_order:list) -> list[list[any]]:
    """
    Allocate the given items to the given agents using the given picking sequence.
    :param instance: an instance of the fair course allocation problem. 
                     Contains functions defining the agent capacities, course capacities, and agent-item valuations.
    :param agent_order: a list of indices of agents, representing the picking sequence. The agents will pick items in this order.
    :return a list of bundles, one per student: each bundle is a list of courses.

    >>> s1 = {"c1": 10, "c2": 8, "c3": 6}
    >>> s2 = {"c1": 6, "c2": 8, "c3": 10}
    >>> agent_capacities = {"Alice": 2, "Bob": 3, "Chana": 2, "Dana": 3}      # 10 seats required
    >>> course_capacities = {"c1": 2, "c2": 3, "c3": 4}                       # 9 seats available
    >>> valuations = {"Alice": s1, "Bob": s1, "Chana": s2, "Dana": s2}
    >>> instance = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    >>> picking_sequence(instance, agent_order=["Alice","Bob", "Chana", "Dana","Dana","Chana","Bob", "Alice"])
    {'Alice': ['c1', 'c3'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c2', 'c3']}
    """
    agent_order = list(agent_order) 
    for agent in agent_order:
        if agent not in instance.agents:
            raise ValueError(f"Agent {agent} in agent_order but not in instance.agents")
    alloc = AllocationBuilder(instance)
    complete_allocation_using_picking_sequence(alloc, agent_order)
    return alloc.sorted()


def serial_dictatorship(instance: Instance, agent_order:list=None) -> list[list[any]]:
    """
    Allocate the given items to the given agents using the serial_dictatorship protocol, in the given agent-order.
    :param agents a list of Agent objects.
    :param agent_order (optional): a list of indices of agents. The agents will pick items in this order.
    :param items (optional): a list of items to allocate. Default is allocate all items.
    :return a list of bundles; each bundle is a list of items.

    >>> s1 = {"c1": 10, "c2": 8, "c3": 6}
    >>> s2 = {"c1": 6, "c2": 8, "c3": 10}
    >>> agent_capacities = {"Alice": 2, "Bob": 3, "Chana": 2, "Dana": 3}      # 10 seats required
    >>> course_capacities = {"c1": 2, "c2": 3, "c3": 4}                       # 9 seats available
    >>> valuations = {"Alice": s1, "Bob": s1, "Chana": s2, "Dana": s2}
    >>> instance = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    >>> serial_dictatorship(instance)
    {'Alice': ['c1', 'c2'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c3']}
    """
    if agent_order is None: agent_order = instance.agents
    agent_order = sum([instance.agent_capacity(agent) * [agent] for agent in agent_order], [])
    # print("agent_order=",agent_order)
    return picking_sequence(instance, agent_order)


def round_robin(instance: Instance, agent_order:list=None) -> list[list[any]]:
    """
    Allocate the given items to the given agents using the round-robin protocol, in the given agent-order.
    :param agents a list of Agent objects.
    :param agent_order (optional): a list of indices of agents. The agents will pick items in this order.
    :param items (optional): a list of items to allocate. Default is allocate all items.
    :return a list of bundles; each bundle is a list of items.

    >>> s1 = {"c1": 10, "c2": 8, "c3": 6}
    >>> s2 = {"c1": 6, "c2": 8, "c3": 10}
    >>> agent_capacities = {"Alice": 2, "Bob": 3, "Chana": 2, "Dana": 3}      # 10 seats required
    >>> course_capacities = {"c1": 2, "c2": 3, "c3": 4}                       # 9 seats available
    >>> valuations = {"Alice": s1, "Bob": s1, "Chana": s2, "Dana": s2}
    >>> instance = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    >>> round_robin(instance)
    {'Alice': ['c1', 'c2'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c3']}
    """
    if agent_order is None: agent_order = instance.agents
    return picking_sequence(instance, agent_order)

def bidirectional_round_robin(instance: Instance, agent_order:list=None) -> list[list[any]]:
    """
    Allocate the given items to the given agents using the bidirectional-round-robin protocol (ABCCBA), in the given agent-order.
    :param agents a list of Agent objects.
    :param agent_order (optional): a list of indices of agents. The agents will pick items in this order.
    :param items (optional): a list of items to allocate. Default is allocate all items.
    :return a list of bundles; each bundle is a list of items.

    >>> s1 = {"c1": 10, "c2": 8, "c3": 6}
    >>> s2 = {"c1": 6, "c2": 8, "c3": 10}
    >>> agent_capacities = {"Alice": 2, "Bob": 3, "Chana": 2, "Dana": 3}      # 10 seats required
    >>> course_capacities = {"c1": 2, "c2": 3, "c3": 4}                       # 9 seats available
    >>> valuations = {"Alice": s1, "Bob": s1, "Chana": s2, "Dana": s2}
    >>> instance = Instance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    >>> bidirectional_round_robin(instance)
    {'Alice': ['c1', 'c3'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c2', 'c3']}
    """
    if agent_order is None: agent_order = instance.agents
    return picking_sequence(instance, list(agent_order) + list(reversed(agent_order)))



def complete_allocation_using_picking_sequence(alloc: AllocationBuilder, agent_order: list):
    """
    A subroutine for picking sequence algorithms: receives an instance and a partial allocation, 
    and completes the partial allocation using the given picking sequence.    

    :param instance: an instance of the fair course allocation problem. 
    :param alloc: a partial allocation (in an AllocationBuilder object).
    :param agent_order: a list of indices of agents, representing the picking sequence. The agents will pick items in this order.
    """
    logger.info("\nPicking-sequence with items %s , agents %s, and agent-order %s", alloc.remaining_item_capacities, alloc.remaining_agent_capacities, agent_order)
    for agent in cycle(agent_order):
        if len(alloc.remaining_agent_capacities)==0 or len(alloc.remaining_item_capacities)==0:
            break 
        if not agent in alloc.remaining_agent_capacities:
            continue
        potential_items_for_agent = set(alloc.remaining_item_capacities.keys()).difference(alloc.bundles[agent])
        if len(potential_items_for_agent)==0:
            logger.info("Agent %s cannot pick any more items: remaining=%s, bundle=%s", agent, alloc.remaining_item_capacities, alloc.bundles[agent])
            alloc.remove_agent(agent)
            continue
        best_item_for_agent = max(potential_items_for_agent, key=lambda item: alloc.remaining_agent_item_value[agent][item])
        alloc.give(agent, best_item_for_agent, logger)



round_robin.logger = picking_sequence.logger = serial_dictatorship.logger = complete_allocation_using_picking_sequence.logger = logger


### MAIN

if __name__ == "__main__":
    import doctest, sys
    print("\n",doctest.testmod(), "\n")

    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    from fairpy.courses.adaptors import divide_random_instance
    divide_random_instance(algorithm=round_robin, 
                           num_of_agents=10, num_of_items=4, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1)
    divide_random_instance(algorithm=bidirectional_round_robin, 
                           num_of_agents=10, num_of_items=4, agent_capacity_bounds=[2,5], item_capacity_bounds=[3,12], 
                           item_base_value_bounds=[1,100], item_subjective_ratio_bounds=[0.5,1.5], normalized_sum_of_values=100,
                           random_seed=1)
