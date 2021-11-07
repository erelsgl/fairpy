#!python3

from typing import List

from fairpy.agents import Agent, PiecewiseConstantAgent
from fairpy.cake.improve_ef4_algo.allocation import CakeAllocation
from fairpy.cake.improve_ef4_algo.cake import CakeSlice


def value_for_slices(agent: Agent, slices: List[CakeSlice]) -> float:
    """
    Gets the sum value of all slices for the agent, as described by
    `CakeSlice.value_according_to`.
    :param agent: agent who evaluates the slices
    :param slices: slices to evaluate
    :return: value of all slices according to `agent`

    >>> s = [CakeSlice(0, 3)]
    >>> a = PiecewiseConstantAgent([33, 33, 11], "agent")
    >>> value_for_slices(a, s) == a.total_value()
    True
    >>> s = [CakeSlice(0, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> value_for_slices(a, s) == a.total_value() / 2
    True
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> value_for_slices(a, s) == a.total_value() / 2
    True
    """
    return sum([slice.value_according_to(agent) for slice in slices])


def get_agent_satisfaction(agent: Agent, allocation: CakeAllocation) -> float:
    """
    Gets how much an agent is satisfied from their allocation slices in allocation.
    The satisfaction is measured by how much the agent values those slices.
    :param agent: agent to check satisfaction of
    :param allocation: allocation to check allocation slices from
    :return: the satisfaction value of `agent` with slices allocated in `allocation`

    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> get_agent_satisfaction(a, alloc) == a.total_value() / 2
    True
    """
    return value_for_slices(agent, allocation.get_allocation_for_agent(agent))


def get_most_satisfied_agent(agents: List[Agent], allocation: CakeAllocation) -> Agent:
    """
    Gets the agent with the highest satisfaction, as described in `get_agent_satisfaction`, value
    among the given agents in the scope of an allocation.
    :param agents: agents to find most satisfied among
    :param allocation: allocation scope to check satisfaction in
    :return: agent in agents with the highest satisfaction

    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> get_most_satisfied_agent([a, b], alloc) == a
    True
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> get_most_satisfied_agent([a, b], alloc) == b
    False
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> alloc.allocate_slice(b, CakeSlice(1, 1.22))
    >>> get_most_satisfied_agent([a, b], alloc) == a
    True
    """
    return max([agent for agent in agents], key=lambda x: get_agent_satisfaction(x, allocation))


def get_least_satisfied_agent(agents: List[Agent], allocation: CakeAllocation) -> Agent:
    """
    Gets the agent with the lowest satisfaction, as described in `get_agent_satisfaction`, value
    among the given agents in the scope of an allocation.
    :param agents: agents to find least satisfied among
    :param allocation: allocation scope to check satisfaction in
    :return: agent in agents with the lowest satisfaction

    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> get_least_satisfied_agent([a, b], alloc) == b
    True
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> get_least_satisfied_agent([a, b], alloc) == a
    False
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> alloc.allocate_slice(b, CakeSlice(1, 1.22))
    >>> get_least_satisfied_agent([a, b], alloc) == b
    True
    """
    return min([agent for agent in agents], key=lambda x: get_agent_satisfaction(x, allocation))


def is_dominated_by(agent: Agent, dominator: Agent, allocation: CakeAllocation) -> bool:
    """
    Get whether or not agent is dominated by another in the scope of a given cake allocation.
    Domination is defined as being more satisfied (as described in `get_agent_satisfaction`)
    than another agent.
    :param agent: agent to check if dominated by
    :param dominator: agent to check if dominates
    :param allocation: allocation scope to check domination in
    :return: true if `agent` satisfaction is lower than `dominator` satisfaction in the scope of allocation.

    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> is_dominated_by(b, a, alloc)
    True
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> is_dominated_by(a, b, alloc)
    False
    """
    return get_agent_satisfaction(agent, allocation) < get_agent_satisfaction(dominator, allocation)


def is_dominated_by_all(agent: Agent, others: List[Agent], allocation: CakeAllocation) -> bool:
    """
    Get whether or not agent is dominated by other agents in the scope of a given cake allocation,
    where foreach agent in others, `is_dominated_by(agent, other, allocation)` follows as true
    :param agent: agent to check if dominated by
    :param others: agents to check if dominate
    :param allocation: allocation scope to check domination in
    :return: true if `agent` satisfaction is lower than `dominator` satisfaction in the scope of allocation.

    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> c = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> alloc.allocate_slice(a, s[0])
    >>> alloc.allocate_slice(b, s[1])
    >>> is_dominated_by_all(c, [a, b], alloc)
    True
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> is_dominated_by_all(b, [a], alloc)
    True
    >>> s = [CakeSlice(0, 0.5), CakeSlice(0.5, 1)]
    >>> a = PiecewiseConstantAgent([33, 33], "agent")
    >>> b = PiecewiseConstantAgent([33, 33], "agent2")
    >>> alloc = CakeAllocation(s)
    >>> ignore = [alloc.allocate_slice(a, sl) for sl in s]
    >>> is_dominated_by_all(a, [b], alloc)
    False
    """
    return all([is_dominated_by(agent, other, allocation) for other in others])


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
