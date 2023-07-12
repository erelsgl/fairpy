"""
Allocate course seats using a picking sequence.

Three interesting special cases of a picking-sequence are: round-robin, balanced round-robin, and serial dictatorship.

Programmer: Erel Segal-Halevi
Since: 2023-06
"""

from fairpy import AgentList
from itertools import cycle
from instance import FairCourseAllocationInstance

import logging
logger = logging.getLogger(__name__)

from typing import List, Any, Dict


def picking_sequence(instance: FairCourseAllocationInstance, agent_order:list) -> List[List[Any]]:
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
    >>> instance = FairCourseAllocationInstance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    >>> picking_sequence(instance, agent_order=["Alice","Bob", "Chana", "Dana","Dana","Chana","Bob", "Alice"])
    {'Alice': ['c1', 'c3'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c2', 'c3']}
    """
    agent_order = list(agent_order) 
    remaining_agents = set(instance.agents) 
    remaining_course_capacities = {course: instance.item_capacity(course) for course in instance.items}
    remaining_courses = {c for c in instance.items if instance.item_capacity(c)>0}   # should be a set, to allow set-difference
    logger.info("\nPicking-sequence with agents %s, agent-order %s, and courses %s", remaining_agents, agent_order, remaining_courses)
    bundles = {agent: set() for agent in instance.agents}    # Each bundle is a set, since each agent can get at most one seat in each course
    for agent in agent_order:
        if agent not in instance.agents:
            raise ValueError(f"Agent {agent} in agent_order but not in instance.agents")
    for agent in cycle(agent_order):
        if len(remaining_agents)==0 or len(remaining_courses)==0:
            break 
        if not agent in remaining_agents:
            continue
        potential_courses_for_agent = remaining_courses.difference(bundles[agent])
        if len(potential_courses_for_agent)==0:
            logger.info("Agent %s cannot pick any more courses: remaining=%s, bundle=%s", agent, remaining_courses, bundles[agent])
            remaining_agents.remove(agent)
            continue
        best_item_for_agent = max(potential_courses_for_agent, key=lambda item: instance.agent_item_value(agent,item))
        bundles[agent].add(best_item_for_agent)
        logger.info("Agent %s takes %s (value %d)", agent, best_item_for_agent, instance.agent_item_value(agent, best_item_for_agent))
        remaining_course_capacities[best_item_for_agent] -= 1
        if remaining_course_capacities[best_item_for_agent]==0:
            remaining_courses.remove(best_item_for_agent)
        if len(bundles[agent]) == instance.agent_capacity(agent):
            logger.info("Agent %s has already picked %d courses: %s", agent, len(bundles[agent]), bundles[agent])
            remaining_agents.remove(agent)
    return {agent: sorted(bundle) for agent,bundle in bundles.items()}

def round_robin(instance: FairCourseAllocationInstance, agent_order:list=None) -> List[List[Any]]:
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
    >>> instance = FairCourseAllocationInstance(agent_capacities=agent_capacities, item_capacities=course_capacities, valuations=valuations)
    >>> round_robin(instance)
    {'Alice': ['c1', 'c2'], 'Bob': ['c1', 'c2', 'c3'], 'Chana': ['c2', 'c3'], 'Dana': ['c3']}
    """
    if agent_order is None: agent_order = instance.agents
    return picking_sequence(instance, agent_order)


round_robin.logger = picking_sequence.logger = logger


### MAIN

if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print (f"{failures} failures, {tests} tests")
    # doctest.run_docstring_examples(picking_sequence, globals())
        