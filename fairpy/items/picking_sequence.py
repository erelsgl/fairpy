"""
The Round Robin algorithm for item allocation. See https://en.wikipedia.org/wiki/Round-robin_item_allocation

The same function can be used for any picking sequence. See https://en.wikipedia.org/wiki/Picking_sequence.

Programmer: Erel Segal-Halevi
Since:  2020-07 - 2023-06
"""

from fairpy import AgentList

import logging
logger = logging.getLogger(__name__)

from typing import List, Any


def picking_sequence(agents:AgentList, agent_order:List[int], items:List[Any]=None) -> List[List[Any]]:
    """
    Allocate the given items to the given agents using the given picking sequence.
    :param agents a list of Agent objects.
    :param agent_order: a list of indices of agents, representing the picking sequence. The agents will pick items in this order.
    :param items (optional): a list of items to allocate. Default is allocate all items.
    :return a list of bundles; each bundle is a list of items.

    >>> from fairpy import AdditiveAgent
    >>> Alice = AdditiveAgent({"x": 11, "y": 22, "z": 44, "w":0}, name="Alice")
    >>> George = AdditiveAgent({"x": 22, "y": 11, "z": 66, "w":33}, name="George")
    >>> picking_sequence(AgentList([Alice,George]), agent_order=[0,1,1,0])    # Alice gets {z,y} and George gets {w,x}
    [['z', 'y'], ['w', 'x']]
    >>> picking_sequence(AgentList([Alice,George]), agent_order=[0,0,0,0])    # Alice gets everything and George gets nothing
    [['z', 'y', 'x', 'w'], []]
    >>> picking_sequence(AgentList([Alice,George]), agent_order=[0,0,0,1])    # Alice gets {z,y,x} and George gets {w}
    [['z', 'y', 'x'], ['w']]
    """
    assert isinstance(agents, AgentList)
    agent_order = list(agent_order)
    if items is None: items = agents.all_items()

    remaining_items = list(items)
    logger.info("\nPicking-sequence with agent-order %s and items %s", agent_order, remaining_items)
    bundles = [[] for _ in agents]
    while True:
        for agent_index in agent_order:
            if len(remaining_items)==0:
                return bundles
            agent = agents[agent_index]
            best_item_for_agent = max(remaining_items, key=agent.value)
            best_item_value = agent.value(best_item_for_agent)
            bundles[agent_index].append(best_item_for_agent)
            logger.info("%s takes %s (value %d)", agent.name(), best_item_for_agent, best_item_value)
            remaining_items.remove(best_item_for_agent)


def round_robin(agents:AgentList, agent_order:List[int]=None, items:List[Any]=None) -> List[List[Any]]:
    """
    Allocate the given items to the given agents using the round-robin protocol, in the given agent-order.
    :param agents a list of Agent objects.
    :param agent_order (optional): a list of indices of agents. The agents will pick items in this order.
    :param items (optional): a list of items to allocate. Default is allocate all items.
    :return a list of bundles; each bundle is a list of items.

    ### Dividing all items:
    >>> from fairpy import AdditiveAgent
    >>> Alice = AdditiveAgent({"x": 11, "y": 22, "z": 44, "w":0}, name="Alice")
    >>> George = AdditiveAgent({"x": 22, "y": 11, "z": 66, "w":33}, name="George")
    >>> allocation = round_robin(AgentList([Alice,George]), agent_order=[0,1])    # Alice gets {z,y} and George gets {w,x}
    >>> allocation
    [['z', 'y'], ['w', 'x']]
    >>> Alice.is_EF1(allocation[0], allocation)
    True
    >>> George.is_EF1(allocation[1], allocation)
    True
    >>> Alice.is_EF(allocation[0], allocation)
    True
    >>> George.is_EF(allocation[1], allocation)
    False

    ### Dividing only some of the items:
    >>> round_robin(AgentList([Alice,George]), agent_order=[0,1], items={"x","y","z"})
    [['z', 'y'], ['x']]

    ### Different input formats:
    >>> round_robin(AgentList([[11,22,44,0],[22,11,66,33]]), agent_order=[0,1], items={0,1,2,3})
    [[2, 1], [3, 0]]

    >>> round_robin(AgentList([[11,22,44,0],[22,11,66,33]]), agent_order=[0,1], items={0,1,2,3})
    [[2, 1], [3, 0]]
    """
    assert isinstance(agents, AgentList)
    if agent_order is None: agent_order = range(len(agents))
    return picking_sequence(agents, agent_order, items)


round_robin.logger = picking_sequence.logger = logger


### MAIN

if __name__ == "__main__":
    # logger.addHandler(logging.StreamHandler())
    # logger.setLevel(logging.INFO)
    #
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
