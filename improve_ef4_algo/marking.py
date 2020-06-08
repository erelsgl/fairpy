from typing import *

from agents import Agent, PiecewiseConstantAgent
from improve_ef4_algo.allocation import CakeAllocation, Marking
from improve_ef4_algo.cake import CakeSlice, Mark
from improve_ef4_algo.preference import find_favorite_slice, Preferences, AgentPreference


def marked_slices_by_agents(marks: List[Mark]) -> Dict[Agent, List[CakeSlice]]:
    """
    Groups all slices by the agent which marked them, as defined by `mark.agent`.
    :param marks: marks to group
    :return: dictionary mapping agents to a lists of slices they marked.

    >>> s = CakeSlice(0, 1)
    >>> a = PiecewiseConstantAgent([33, 11, 1], "agent")
    >>> a2 = PiecewiseConstantAgent([33, 11, 66], "agent")
    >>> m = [Mark(a, s, 0.1), Mark(a2, s, 0.2)]
    >>> res = marked_slices_by_agents(m)
    >>> res[a][0] == s
    True
    >>> res[a2][0] == s
    True
    """
    agents_to_marks = {}
    for mark in marks:
        if mark.agent not in agents_to_marks:
            agents_to_marks[mark.agent] = []
        if mark.slice not in agents_to_marks[mark.agent]:
            agents_to_marks[mark.agent].append(mark.slice)
    return agents_to_marks


def mark_by_preferences(agent: Agent, preferences: Preferences, marking: Marking,
                        excluded_agents: List[Agent]) -> Mark:
    """
    Marks slices by the preference of agent and conflicts it has with other agents,
    as defined by the envy-free algorithm's core protocol lines 7-12 regarding 
    competitions and conflicts.
    :param agent: agent who marks by their preference
    :param preferences: preferences for all agents participating
    :param marking: marking context
    :param excluded_agents: agents whose preferences should be ignored
    :return: mark made

    >>> s = CakeSlice(0, 1)
    >>> s2 = CakeSlice(1, 1.5)
    >>> s3 = CakeSlice(1.7, 2)
    >>> a = PiecewiseConstantAgent([33, 11, 1], "agent")
    >>> a2 = PiecewiseConstantAgent([3, 11, 1], "agent2")
    >>> p = AgentPreference(a, s, s2, s3)
    >>> p2 = AgentPreference(a2, s, s2, s3)
    >>> prefs = Preferences({a: p, a2: p2})
    >>> marking = Marking()
    >>> mark = mark_by_preferences(a, prefs, marking, [])
    >>> mark.agent == a
    True
    >>> mark.slice == s
    True
    """
    excluded_agents_for_conflicts = [agent]
    excluded_agents_for_conflicts.extend(excluded_agents)

    preference = preferences.try_get_preference_for_agent(agent)
    favorite = preference.first
    conflicts_for_primary = preferences.find_agents_with_preference_for(favorite,
                                                                        exclude_agents=excluded_agents_for_conflicts)

    # line 8 if, not talking about lack of conflict for primary slice...
    # if conflicts_for_primary.primary_count == 0:
    #   return

    second_favorite = preference.second
    conflicts_for_secondary = preferences.find_agents_with_preference_for(second_favorite,
                                                                          exclude_agents=excluded_agents_for_conflicts)

    if conflicts_for_secondary.count == 0:
        # mark primary so it is equal to secondary in value
        return marking.mark_to_equalize_value(agent, favorite, second_favorite)

    if conflicts_for_secondary.primary_count == 0 and conflicts_for_secondary.secondary_count == 1:
        competitor_preference = conflicts_for_secondary.preferences[0]
        exclude = [competitor_preference.agent]
        exclude.extend(excluded_agents)
        competitor_primary_conflicts = preferences.find_agents_with_preference_for(competitor_preference.first,
                                                                                   exclude_agents=exclude)
        if conflicts_for_primary.primary_count == 1 and competitor_primary_conflicts.primary_count == 1:
            # mark primary so it is equal to secondary in value
            return marking.mark_to_equalize_value(agent, favorite, second_favorite)

    # mark secondary so it is equal to third preference in value
    third_favorite = preference.third
    return marking.mark_to_equalize_value(agent, second_favorite, third_favorite)


def allocate_by_rightmost_to_agent(agent: Agent, marked_slices: List[CakeSlice], allocation: CakeAllocation,
                                   marking: Marking) -> Tuple[Dict[Agent, CakeSlice], List[List[CakeSlice]]]:
    """
    Allocates slices by the rightmost rule, as described by envy-free algorithm's main
    protocol line 15: `agent` receives their preferred slice out of two slices
    where they made the rightmost mark, while the agent who made the second-rightmost
    mark on the preferred slice of `agent`, receives the second marked slice until
    its second-rightmost mark.

    Let's define `agent` who made the rightmost mark, on two slices (s1, s2).
    Each slice (of s1,s2) will have 2 marks at the least. The slices
    are split into to parts each at the location of the second-rightmost mark
    (s11 {second-rightmost mark} s12), (s21 {second-rightmost mark} s22).

    Define a as `agent`'s preferred slice out of s11 and s21, and b the other slice.
    `agent` is receives that slice. The agent who made the second-rightmost mark on slice
    a, receives slice b.
    :param agent: agent with 2 rightmost marks, one on each slice
    :param marked_slices: slices marked by agent
    :param allocation: the current allocation scope
    :param marking: the marking context
    :return: a tuple composed of a dict mapping agent to slice received, and a list of slices made

    >>> s = CakeSlice(0, 1)
    >>> s2 = CakeSlice(1, 1.5)
    >>> s3 = CakeSlice(1.7, 2)
    >>> a = PiecewiseConstantAgent([10, 10, 10], "agent")
    >>> a2 = PiecewiseConstantAgent([10, 10, 10], "agent2")
    >>> marking = Marking()
    >>> m = marking.mark(a, s, 10)
    >>> m = marking.mark(a, s2, 5)
    >>> m = marking.mark(a2, s, 5)
    >>> m = marking.mark(a2, s2, 2.5)
    >>> alloc = CakeAllocation([s, s2, s3])
    >>> allocated, sliced = allocate_by_rightmost_to_agent(a, [s, s2, s3], alloc, marking)
    >>> sliced
    [[(0,0.5), (0.5,1)], [(1,1.25), (1.25,1.5)]]
    >>> {agent.name(): slice for agent, slice in allocated.items()}
    {'agent': (0,0.5), 'agent2': (1,1.25)}
    """
    marks = marking.rightmost_marks()

    second_rightmost1 = marking.second_rightmost_mark(marks[0].slice)
    second_rightmost2 = marking.second_rightmost_mark(marks[1].slice)

    sliced1 = marked_slices[0].slice_at(second_rightmost1.mark_position)
    sliced2 = marked_slices[1].slice_at(second_rightmost2.mark_position)
    allocation.set_slice_split(marked_slices[0], list(sliced1))
    allocation.set_slice_split(marked_slices[1], list(sliced2))

    slice_option1 = sliced1[0]
    slice_option2 = sliced2[0]
    favorite = find_favorite_slice(agent, [slice_option1, slice_option2])
    mark_on_favorite = second_rightmost1 if favorite == slice_option1 else second_rightmost2
    other_slice = slice_option1 if favorite == slice_option2 else slice_option2

    allocation.allocate_slice(agent, favorite)
    allocation.allocate_slice(mark_on_favorite.agent, other_slice)

    return {agent: favorite, mark_on_favorite.agent: other_slice}, [sliced1, sliced2]


def allocate_all_partials_by_marks(rightmost_marks: List[Mark], allocation: CakeAllocation,
                                   marking: Marking) -> Tuple[Dict[Agent, CakeSlice], List[List[CakeSlice]]]:
    """
    Cuts all marked slices until the second-rightmost mark, and for each, the left slice
    (until that mark) is given to the agent who made the rightmost mark on the full slice.
    As defined in envy-free algorithm's main protocol line 18.

    :param rightmost_marks: rightmost marks on the slices
    :param allocation: allocation scope
    :param marking: marking context
    :return: a tuple composed of a map of agents to allocated slices, and the sliced parts

    >>> s = CakeSlice(0, 1)
    >>> s2 = CakeSlice(1, 1.5)
    >>> s3 = CakeSlice(1.7, 2)
    >>> a = PiecewiseConstantAgent([10, 10, 10], "agent")
    >>> a2 = PiecewiseConstantAgent([10, 10, 10], "agent2")
    >>> marking = Marking()
    >>> m1 = marking.mark(a, s, 5)
    >>> m2 = marking.mark(a, s2, 2.5)
    >>> m3 = marking.mark(a2, s, 2.5)
    >>> m4 = marking.mark(a2, s2, 5)
    >>> alloc = CakeAllocation([s, s2, s3])
    >>> allocated, sliced = allocate_all_partials_by_marks([m1, m4], alloc, marking)
    >>> sliced
    [[(0,0.25), (0.25,1)], [(1,1.25), (1.25,1.5)]]
    >>> {agent.name(): slice for agent, slice in allocated.items()}
    {'agent': (0,0.25), 'agent2': (1,1.25)}
    """
    allocated_slices = {}
    sliced_parts = []
    for mark in rightmost_marks:
        slice = mark.slice

        second_rightmost = marking.second_rightmost_mark(slice)

        sliced = slice.slice_at(second_rightmost.mark_position)
        allocation.set_slice_split(slice, sliced)
        sliced_parts.append(sliced)

        allocation.allocate_slice(mark.agent, sliced[0])
        allocated_slices[mark.agent] = sliced[0]

    return allocated_slices, sliced_parts


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
