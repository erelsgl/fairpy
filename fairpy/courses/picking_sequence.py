"""
Allocate course seats using a picking sequence.

Three interesting special cases of a picking-sequence are: round-robin, balanced round-robin, and serial dictatorship.

Programmer: Erel Segal-Halevi
Since: 2023-06
"""

from fairpy import AgentList
from itertools import cycle

import logging
logger = logging.getLogger(__name__)

from typing import List, Any, Dict


def picking_sequence(agents:AgentList, agent_capacities:List[int], course_capacities: Dict[Any,int], agent_order:List[int]) -> List[List[Any]]:
    """
    Allocate the given items to the given agents using the given picking sequence.
    :param agents a list of Agent objects, containing the agents' valuations.
    :param agent_capacities: maps an agent index to the number of courses he needs.
    :param course_capacities: maps a course index to the number of seats in the course.
    :param agent_order: a list of indices of agents, representing the picking sequence. The agents will pick items in this order.
    :return a list of bundles, one per student: each bundle is a list of courses.

    >>> s1 = {"c1": 10, "c2": 8, "c3": 6}
    >>> s2 = {"c1": 6, "c2": 8, "c3": 10}
    >>> agents = AgentList({"Alice": s1, "Bob": s1, "Chana": s2, "Dana": s2})
    >>> agent_capacities = [2,3,2,3]                     # 10 seats required
    >>> course_capacities = {"c1": 2, "c2": 3, "c3": 4}  # 9 seats available
    >>> picking_sequence(agents, agent_capacities, course_capacities, agent_order=[0,1,2,3,3,2,1,0])
    [['c1', 'c3'], ['c1', 'c2', 'c3'], ['c2', 'c3'], ['c2', 'c3']]
    """
    assert isinstance(agents, AgentList)
    agent_order = list(agent_order)
    remaining_agents = set(range(len(agents))) 
    remaining_courses = {c for c in course_capacities.keys() if course_capacities[c]>0}   # should be a set, to allow set-difference
    logger.info("\nPicking-sequence with agent-order %s and courses %s", agent_order, remaining_courses)
    bundles = [set() for _ in agents]    # Each bundle is a set, since each agent can get at most one seat in each course
    for agent_index in cycle(agent_order):
        if len(remaining_agents)==0 or len(remaining_courses)==0:
            break 
        if not agent_index in remaining_agents:
            continue
        agent = agents[agent_index]
        potential_courses_for_agent = remaining_courses.difference(bundles[agent_index])
        if len(potential_courses_for_agent)==0:
            logger.info("%s cannot pick any more courses: remaining=%s, bundle=%s", agent.name(), remaining_courses, bundles[agent_index])
            remaining_agents.remove(agent_index)
            continue
        best_item_for_agent = max(potential_courses_for_agent, key=agent.value)
        bundles[agent_index].add(best_item_for_agent)
        logger.info("%s takes %s (value %d)", agent.name(), best_item_for_agent, agent.value(best_item_for_agent))
        course_capacities[best_item_for_agent] -= 1
        if course_capacities[best_item_for_agent]==0:
            remaining_courses.remove(best_item_for_agent)
        if len(bundles[agent_index]) == agent_capacities[agent_index]:
            logger.info("%s has already picked %d courses: %s", agent.name(), len(bundles[agent_index]), bundles[agent_index])
            remaining_agents.remove(agent_index)
    return [sorted(bundle) for bundle in bundles]

def round_robin(agents:AgentList, agent_capacities:List[int], course_capacities: Dict[Any,int], agent_order:List[int]=None) -> List[List[Any]]:
    """
    Allocate the given items to the given agents using the round-robin protocol, in the given agent-order.
    :param agents a list of Agent objects.
    :param agent_order (optional): a list of indices of agents. The agents will pick items in this order.
    :param items (optional): a list of items to allocate. Default is allocate all items.
    :return a list of bundles; each bundle is a list of items.

    >>> s1 = {"c1": 10, "c2": 8, "c3": 6}
    >>> s2 = {"c1": 6, "c2": 8, "c3": 10}
    >>> agents = AgentList({"Alice": s1, "Bob": s1, "Chana": s2, "Dana": s2})
    >>> agent_capacities = [2,3,2,3]                     # 10 seats required
    >>> course_capacities = {"c1": 2, "c2": 3, "c3": 4}  # 9 seats available
    >>> round_robin(agents, agent_capacities, course_capacities)
    [['c1', 'c2'], ['c1', 'c2', 'c3'], ['c2', 'c3'], ['c3']]
    """
    assert isinstance(agents, AgentList)
    if agent_order is None: agent_order = range(len(agents))
    return picking_sequence(agents, agent_capacities, course_capacities, agent_order)


round_robin.logger = picking_sequence.logger = logger


### MAIN

if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print (f"{failures} failures, {tests} tests")
    # doctest.run_docstring_examples(picking_sequence, globals())
