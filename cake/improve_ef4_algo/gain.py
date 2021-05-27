#!python3

import itertools
from typing import List

from fairpy.agents import Agent, PiecewiseConstantAgent
from fairpy.cake.improve_ef4_algo.allocation import CakeAllocation, CakeSlice
from fairpy.cake.improve_ef4_algo.domination import get_agent_satisfaction, value_for_slices
from fairpy.cake.improve_ef4_algo.util import exclude_from_list


def get_agent_gain(agent: Agent, other_agents: List[Agent], allocation: CakeAllocation) -> float:
    """
    Gets the gain of an agent in the scope of a given allocation, where gain(agent)
    is defined by how agent is satisfied with their allocation, in comparison to others in the allocation.
    More specifically, the gain for agent A, is the difference between their satisfaction
    (as described by `get_agent_satisfaction`)  with their allocated slices in contrast to how satisfied they
    would have being with all the slices other were allocated.
    :param agent: agent to check gain for
    :param other_agents: other agents which participated with the allocation
    :param allocation: allocation scope to check in
    :return: the result of gain(agent) in the scope of the given allocation

    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> get_agent_gain(a, [b], alloc) == a.total_value() / 2
    True
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> s2 = [CakeSlice(1, 1.5), CakeSlice(1.5, 2)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s + s2)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> ignore = [alloc.allocate_slice(b, sl) for sl in s2]
    >>> get_agent_gain(a, [b], alloc) == (a.total_value() / 2 - b.total_value() / 2)
    True
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> get_agent_gain(b, [a], alloc) == -a.total_value() / 2
    True
    """
    return get_agent_satisfaction(agent, allocation) - \
           sum([value_for_slices(agent, allocation.get_allocation_for_agent(oagent))
                for oagent in other_agents])


def is_allocation_gain_larger_then_others(agent: Agent, other_agents: List[Agent], allocation: CakeAllocation,
                                          other_allocations: List[CakeAllocation]) -> bool:
    """
    Gets whether or not an agent's gain, as defined by `get_agent_gain` in an allocation scope,
    is > to the sum of the same agent's gain throughout all other allocations.
    :param agent: agent whose gain to test
    :param other_agents: other agents participating in the allocations
    :param allocation: allocation scope to check gain(agent) against other allocations
    :param other_allocations: other allocations to check gain against
    :return true if gain(agent) in allocation > sum of gain(agent) for other allocations

    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> other_allocs = [CakeAllocation([]) for i in range(3)]
    >>> is_allocation_gain_larger_then_others(a, [b], alloc, other_allocs)
    True
    """
    gain_for_allocation = get_agent_gain(agent, other_agents, allocation)
    gain_for_other_allocations = sum([get_agent_gain(agent, other_agents, alloc)
                                      for alloc in other_allocations])

    return gain_for_allocation > gain_for_other_allocations


def allocation_with_lowest_gain(agents: List[Agent], allocations: List[CakeAllocation]) -> CakeAllocation:
    """
    Finds an allocation such that for all agents, gain(agent) (as defined by `get_agent_gain`) in that
    allocation scope is less than the sum of gain(agent) for all other allocation scopes.
    :param agents: agents to check gain for
    :param allocations: allocations to check
    :return: allocation such that for all agents, gain(agent) <= sum gain(agent) for other allocations.

    >>> a = PiecewiseConstantAgent([33, 1], "agent")
    >>> b = PiecewiseConstantAgent([1, 33], "agent2")
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1), CakeSlice(1, 1.5), CakeSlice(1.5, 2)]
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s[:2]]
    >>> ignore = [alloc.allocate_slice(b, sl) for sl in s[2:]]
    >>> alloc2 = CakeAllocation(s)
    >>> allocation_with_lowest_gain([a, b], [alloc, alloc2]) == alloc2
    True
    """
    low_gain_allocations = list(itertools.chain.from_iterable([
        [allocation for allocation in allocations
         if not is_allocation_gain_larger_then_others(agent, exclude_from_list(agents, [agent]), allocation,
                                                      exclude_from_list(allocations, [allocation]))]
        for agent in agents
    ]))

    repeat_allocations = [alloc for alloc in low_gain_allocations
                          if low_gain_allocations.count(alloc) == len(agents)]
    if len(repeat_allocations) == 0:
        raise ValueError("No repeat allocation found")

    return repeat_allocations[0]


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
