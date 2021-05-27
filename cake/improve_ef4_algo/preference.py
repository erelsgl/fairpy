#!python3

from typing import *

from fairpy.agents import Agent, PiecewiseConstantAgent
from fairpy.cake.improve_ef4_algo.cake import CakeSlice


class Preferences(object):
    """
    Represents preferences of agents for a specific cake state.

    A preference is defined as 3 favorite slices, as defined by `find_favorite_slice`, ordered by most
    preferred slice to least preferred slice.

    Allows searching for preferences by agent or by slices.

    To create, use `get_preferences_for_agents`.
    """

    def __init__(self, agent_to_preference):
        self._agents_to_preferences = agent_to_preference

    def get_preference_for_agent(self, agent: Agent) -> Tuple[CakeSlice, CakeSlice, CakeSlice]:
        """
        Get the preference of the given agent.

        :param agent: agent to find preference for
        :return: the preference if found, in a format of a tuple of favorite slices in order of preferences
        :throws KeyError: if not preference was found
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = CakeSlice(0, 1), CakeSlice(1, 1.5), CakeSlice(1.5, 1.6)
        >>> prefs = Preferences({a: p})
        >>> prefs.get_preference_for_agent(a) == p
        True
        """
        if agent not in self._agents_to_preferences:
            raise KeyError('No preference for agent')
        return self._agents_to_preferences[agent]

    def find_agents_with_preference_for(self, slice: CakeSlice, exclude_agents: List[Agent] = None) \
            -> Tuple[List[Agent], List[Agent]]:
        """
        Searches amongst all the agent preferences for preferences for `slice` is either a first or second
        preference.
        :param slice: slice to search for in preferences
        :param exclude_agents: agents whose preference should be ignored
        :return a tuple containing a list of agents where the slice is the first preference, and a list
            where the slice is the second preference

        >>> pslice = CakeSlice(1, 1.5)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6)
        >>> prefs = Preferences({a: p})
        >>> result_first, result_second = prefs.find_agents_with_preference_for(pslice)
        >>> result_second[0] == a
        True
        >>> pslice = CakeSlice(1, 1.5)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6)
        >>> a2 = PiecewiseConstantAgent([1, 1], "agent2")
        >>> p2 = CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6)
        >>> prefs = Preferences({a: p, a2: p2})
        >>> result_first, result_second = prefs.find_agents_with_preference_for(pslice)
        >>> all([pref in [a, a2] for pref in result_second])
        True
        >>> pslice = CakeSlice(1, 1.5)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6)
        >>> a2 = PiecewiseConstantAgent([1, 1], "agent2")
        >>> p2 = CakeSlice(0, 1), CakeSlice(1.5, 1.6), pslice
        >>> prefs = Preferences({a: p, a2: p2})
        >>> result_first, result_second = prefs.find_agents_with_preference_for(pslice)
        >>> len(result_first) == 0 and len(result_second) == 1 and result_second[0] == a
        True
        >>> pslice = CakeSlice(1, 1.5)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6)
        >>> a2 = PiecewiseConstantAgent([1, 1], "agent2")
        >>> p2 = CakeSlice(0, 1), CakeSlice(1.5, 1.6), CakeSlice(1, 2)
        >>> prefs = Preferences({a: p, a2: p2})
        >>> result_first, result_second = prefs.find_agents_with_preference_for(pslice)
        >>> len(result_first) == 0 and len(result_second) == 1 and result_second[0] == a
        True
        >>> pslice = CakeSlice(1, 1.5)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6)
        >>> a2 = PiecewiseConstantAgent([1, 1], "agent2")
        >>> p2 = pslice, CakeSlice(0, 1), CakeSlice(1.5, 1.6)
        >>> prefs = Preferences({a: p, a2: p2})
        >>> result_first, result_second = prefs.find_agents_with_preference_for(pslice, exclude_agents=[a2])
        >>> len(result_first) == 0 and len(result_second) == 1 and result_second[0] == a
        True
        """
        if exclude_agents is None:
            exclude_agents = []

        preferences_first = [agent for agent, preference in self._agents_to_preferences.items()
                             if agent not in exclude_agents and preference[0] == slice]
        preferences_second = [agent for agent, preference in self._agents_to_preferences.items()
                              if agent not in exclude_agents and preference[1] == slice]
        return preferences_first, preferences_second


def find_favorite_slice(agent: Agent, slices: List[CakeSlice], exclude_slices: List[CakeSlice] = None) -> CakeSlice:
    """
    Get the agent's favorite, defined by the one which will bring the highest satisfaction,
    slice from a list of different slices.
    :param agent: agent whose favorite to find
    :param slices: slices from which to search
    :param exclude_slices: slices to ignore while searching
    :return: the slice which gives `agent` the highest satisfaction out of all `slices`.

    >>> s = [CakeSlice(0, 1), CakeSlice(1, 2), CakeSlice(2, 3)]
    >>> a = PiecewiseConstantAgent([33, 11, 1], "agent")
    >>> find_favorite_slice(a, s)
    (0,1)
    >>> s = [CakeSlice(0, 1), CakeSlice(1, 2), CakeSlice(2, 3)]
    >>> a = PiecewiseConstantAgent([33, 11, 66], "agent")
    >>> find_favorite_slice(a, s)
    (2,3)
    """
    if exclude_slices is None:
        exclude_slices = []

    dict = {cake_slice: cake_slice.value_according_to(agent) for cake_slice in slices
            if cake_slice not in exclude_slices}
    if len(dict) == 0:
        raise ValueError("Favorite not found")
    maximum = max(dict, key=dict.get)
    return maximum


def get_agent_preference(agent: Agent, slices: List[CakeSlice]) -> Tuple[CakeSlice, CakeSlice, CakeSlice]:
    """
    Gets the preference of agent, from the given slices.
    :param agent: agent whose preference to find.
    :param slices: slices out of to search.
    :return `AgentPreference` representing the preference of `agent` out of `slices`.

    >>> s = [CakeSlice(0, 1), CakeSlice(1, 2), CakeSlice(2, 3)]
    >>> a = PiecewiseConstantAgent([33, 11, 1], "agent")
    >>> get_agent_preference(a, s)
    ((0,1), (1,2), (2,3))
    >>> s = [CakeSlice(0, 1), CakeSlice(1, 2), CakeSlice(2, 3)]
    >>> a = PiecewiseConstantAgent([33, 11, 66], "agent")
    >>> get_agent_preference(a, s)
    ((2,3), (0,1), (1,2))
    """
    first = find_favorite_slice(agent, slices)
    second = find_favorite_slice(agent, slices, exclude_slices=[first])
    third = find_favorite_slice(agent, slices, exclude_slices=[first, second])

    return first, second, third


def get_preferences_for_agents(agents: List[Agent], slices: List[CakeSlice]) -> Preferences:
    """
    Gets the preferences of all agents out of given slices.
    :param agents: agents whose preference to find
    :param slices: slices to find preferences among
    :return: `Preferences` object holding preferences for each agent, as described by
        `get_agent_preference`.

    >>> s = [CakeSlice(0, 1), CakeSlice(1, 2), CakeSlice(2, 3)]
    >>> a = PiecewiseConstantAgent([33, 11, 1], "agent")
    >>> prefs = get_preferences_for_agents([a], s)
    >>> prefs.get_preference_for_agent(a)
    ((0,1), (1,2), (2,3))
    >>> s = [CakeSlice(0, 1), CakeSlice(1, 2), CakeSlice(2, 3)]
    >>> a = PiecewiseConstantAgent([33, 11, 1], "agent")
    >>> a2 = PiecewiseConstantAgent([33, 11, 66], "agent")
    >>> prefs = get_preferences_for_agents([a,a2], s)
    >>> prefs.get_preference_for_agent(a)
    ((0,1), (1,2), (2,3))
    >>> prefs.get_preference_for_agent(a2)
    ((2,3), (0,1), (1,2))
    """
    agents_to_preferences = {agent: get_agent_preference(agent, slices) for agent in agents}
    return Preferences(agents_to_preferences)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
