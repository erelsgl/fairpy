#!python3

from typing import *

from fairpy.agents import Agent, PiecewiseConstantAgent
from fairpy.cake.improve_ef4_algo.allocation import CakeAllocation, Marking
from fairpy.cake.improve_ef4_algo.cake import CakeSlice
from fairpy.cake.improve_ef4_algo.preference import find_favorite_slice, Preferences


def mark_by_preferences(agent: Agent, preferences: Preferences, marking: Marking,
                        excluded_agents: List[Agent]) -> Tuple[CakeSlice, float]:
    """
    Marks slices by the preference of agent and conflicts it has with other agents,
    as defined by the envy-free algorithm's core protocol lines 7-12 regarding 
    competitions and conflicts.
    :param agent: agent who marks by their preference
    :param preferences: preferences for all agents participating
    :param marking: marking context
    :param excluded_agents: agents whose preferences should be ignored
    :return: mark made, as tuple of slice marked and marking position

    >>> s = CakeSlice(0, 1)
    >>> s2 = CakeSlice(1, 1.5)
    >>> s3 = CakeSlice(1.7, 2)
    >>> a = PiecewiseConstantAgent([33, 11, 1], "agent")
    >>> a2 = PiecewiseConstantAgent([3, 11, 1], "agent2")
    >>> p = s, s2, s3
    >>> p2 = s, s2, s3
    >>> prefs = Preferences({a: p, a2: p2})
    >>> marking = Marking()
    >>> marked_slice, mark = mark_by_preferences(a, prefs, marking, [])
    >>> marked_slice == s
    True
    """
    excluded_agents_for_conflicts = [agent]
    excluded_agents_for_conflicts.extend(excluded_agents)

    preference = preferences.get_preference_for_agent(agent)
    favorite = preference[0]
    conflicts_for_primary_first, _ = preferences\
        .find_agents_with_preference_for(favorite, exclude_agents=excluded_agents_for_conflicts)

    # line 8 if, not talking about lack of conflict for primary slice...
    # if conflicts_for_primary.primary_count == 0:
    #   return

    second_favorite = preference[1]
    second_favorite_conflicts_first, second_favorite_conflicts_second = preferences \
        .find_agents_with_preference_for(second_favorite, exclude_agents=excluded_agents_for_conflicts)

    if len(second_favorite_conflicts_first) == 0 and len(second_favorite_conflicts_second) == 0:
        # mark primary so it is equal to secondary in value
        return favorite, marking.mark_to_equalize_value(agent, favorite, second_favorite)

    if len(second_favorite_conflicts_first) == 0 and len(second_favorite_conflicts_second) == 1:
        competitor = second_favorite_conflicts_second[0]
        competitor_preference = preferences.get_preference_for_agent(competitor)
        exclude = [competitor]
        exclude.extend(excluded_agents)
        competitor_primary_conflicts_first, _ = preferences.find_agents_with_preference_for(competitor_preference[0],
                                                                                            exclude_agents=exclude)
        if len(conflicts_for_primary_first) == 1 and len(competitor_primary_conflicts_first) == 1:
            # mark primary so it is equal to secondary in value
            return favorite, marking.mark_to_equalize_value(agent, favorite, second_favorite)

    # mark secondary so it is equal to third preference in value
    third_favorite = preference[2]
    return second_favorite, marking.mark_to_equalize_value(agent, second_favorite, third_favorite)


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
    second_rightmost1_agent, second_rightmost1_pos = marking.second_rightmost_mark(marked_slices[0])
    second_rightmost2_agent, second_rightmost2_pos = marking.second_rightmost_mark(marked_slices[1])

    sliced1 = marked_slices[0].slice_at(second_rightmost1_pos)
    sliced2 = marked_slices[1].slice_at(second_rightmost2_pos)
    allocation.set_slice_split(marked_slices[0], list(sliced1))
    allocation.set_slice_split(marked_slices[1], list(sliced2))

    slice_option1 = sliced1[0]
    slice_option2 = sliced2[0]
    favorite = find_favorite_slice(agent, [slice_option1, slice_option2])
    marking_agent_on_fav = second_rightmost1_agent if favorite == slice_option1 else second_rightmost2_agent
    other_slice = slice_option1 if favorite == slice_option2 else slice_option2

    allocation.allocate_slice(agent, favorite)
    allocation.allocate_slice(marking_agent_on_fav, other_slice)

    return {agent: favorite, marking_agent_on_fav: other_slice}, [sliced1, sliced2]


def allocate_all_partials_by_marks(allocation: CakeAllocation,
                                   marking: Marking) -> Tuple[Dict[Agent, CakeSlice], List[List[CakeSlice]]]:
    """
    Cuts all marked slices until the second-rightmost mark, and for each, the left slice
    (until that mark) is given to the agent who made the rightmost mark on the full slice.
    As defined in envy-free algorithm's main protocol line 18.

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
    >>> allocated, sliced = allocate_all_partials_by_marks(alloc, marking)
    >>> sliced
    [[(0,0.25), (0.25,1)], [(1,1.25), (1.25,1.5)]]
    >>> {agent.name(): slice for agent, slice in allocated.items()}
    {'agent': (0,0.25), 'agent2': (1,1.25)}
    """
    allocated_slices = {}
    sliced_parts = []
    for agent, slices in marking.rightmost_marks_by_agents().items():
        for slice in slices:
            _, second_rightmost_pos = marking.second_rightmost_mark(slice)

            sliced = slice.slice_at(second_rightmost_pos)
            allocation.set_slice_split(slice, sliced)
            sliced_parts.append(sliced)

            allocation.allocate_slice(agent, sliced[0])
            allocated_slices[agent] = sliced[0]

    return allocated_slices, sliced_parts


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
