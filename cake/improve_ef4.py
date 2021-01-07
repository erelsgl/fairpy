"""
Implements an envy-free cake-cutting protocol for 4 agents.

Reference:

    Georgios Amanatidis,  George Christodoulou,  John Fearnley,  Evangelos Markakis,  Christos-Alexandros Psomas, Eftychia Vakaliou (2018).
    ["An improved envy-free cake cutting protocol for four agents"](https://arxiv.org/abs/1807.00317)
    Proceedings of SAGT 2018, 87--99.

Programmer: Shir Fishbain
Since: 2020-07
"""

import logging
from typing import List

import fairpy.cake.improve_ef4_algo.improve_ef4_impl as impl
from fairpy.cake.agents import Agent
from fairpy.cake.allocations import Allocation

logger = logging.getLogger(__name__)


def improve_ef4_protocol(agents: List[Agent]) -> Allocation:
    """
    Runs the "An Improved Envy-Free Cake Cutting Protocol for Four Agents" to allocate
    a cake to 4 agents.

    In actuality, this is a proxy function for `improve_ef4_algo.improve_ef4_impl.Algorithm`
    class and its `main` function, which provide the actual algorithm implementation.

    :param agents: list of agents to run the algorithm on
    :return: an 'Allocation' object, containing allocation of cake slices to the given agents
    :throws ValueError: if the agents list given does not contain 4 agents
    """
    if len(agents) != 4:
        raise ValueError("expected 4 agents")

    algorithm = impl.Algorithm(agents, logger)
    result = algorithm.main()

    allocation = Allocation(agents)
    for i in range(len(agents)):
        agent = agents[i]
        allocated_slices = result.get_allocation_for_agent(agent)
        allocation.set_piece(i, [(s.start, s.end) for s in allocated_slices])

    return allocation

