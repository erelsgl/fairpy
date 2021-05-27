#!python3
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

from fairpy import Allocation
from fairpy.agents import Agent
import fairpy.cake.improve_ef4_algo.improve_ef4_impl as impl

from fairpy.cake.pieces import round_allocation

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

    >>> from fairpy.cake.pieces import round_allocation 
    >>> from fairpy.agents import PiecewiseConstantAgent 
    >>> agents = [PiecewiseConstantAgent([3, 6, 3], "agent1"), PiecewiseConstantAgent([0, 2, 4], "agent2"), PiecewiseConstantAgent([6, 4, 2], "agent3"), PiecewiseConstantAgent([3, 3, 3], "agent4")]
    >>> allocation = improve_ef4_protocol(agents)
    >>> round_allocation(allocation)
    agent1 gets {(0.667, 0.833),(1.5, 2.0)} with value 3.5.
    agent2 gets {(0.333, 0.5),(2.0, 3)} with value 4.
    agent3 gets {(0.833, 1.0),(1.0, 1.5)} with value 3.
    agent4 gets {(0, 0.333),(0.5, 0.667)} with value 1.5.
    <BLANKLINE>
    """
    if len(agents) != 4:
        raise ValueError("expected 4 agents")

    algorithm = impl.Algorithm(agents, logger)
    result = algorithm.main()

    pieces = len(agents)*[None]
    for i in range(len(agents)):
        agent = agents[i]
        allocated_slices = result.get_allocation_for_agent(agent)
        pieces[i] = [(s.start, s.end) for s in allocated_slices]

    return Allocation(agents, pieces)


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures,tests))
