from typing import *

from improve_ef4.cake import CakeSlice
from agents import Agent, PiecewiseConstantAgent


class AgentPreference(object):
    """
    Represents the slices an agent prefers by order of satisfaction.
    """

    def __init__(self, agent: Agent, first: CakeSlice, second: CakeSlice,
                 third: CakeSlice):
        self._agent = agent
        self._first = first
        self._second = second
        self._third = third

    def __repr__(self):
        return "{}: {},{},{}".format(self.agent.name(),
                                     self.first, self.second, self.third)

    @property
    def agent(self) -> Agent:
        """
        Gets the agent who made this preference
        :return: agent who made this preference

        >>> pslice = CakeSlice(0, 1)
        >>> sslice = CakeSlice(1, 1.2)
        >>> tslice = CakeSlice(1.2, 1.3)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = AgentPreference(a, pslice, sslice, tslice)
        >>> p.agent == a
        True
        """
        return self._agent

    @property
    def first(self) -> CakeSlice:
        """
        Gets the first preference listed in this preference
        :return: first prefered slice

        >>> pslice = CakeSlice(0, 1)
        >>> sslice = CakeSlice(1, 1.2)
        >>> tslice = CakeSlice(1.2, 1.3)
        >>> p = AgentPreference(None, pslice, sslice, tslice)
        >>> p.first
        (0,1)
        """
        return self._first

    @property
    def second(self) -> CakeSlice:
        """
        Gets the second preference listed in this preference
        :return: second prefered slice

        >>> pslice = CakeSlice(0, 1)
        >>> sslice = CakeSlice(1, 1.2)
        >>> tslice = CakeSlice(1.2, 1.3)
        >>> p = AgentPreference(None, pslice, sslice, tslice)
        >>> p.second
        (1,1.2)
        """
        return self._second

    @property
    def third(self) -> CakeSlice:
        """
        Gets the third preference listed in this preference
        :return: third prefered slice

        >>> pslice = CakeSlice(0, 1)
        >>> sslice = CakeSlice(1, 1.2)
        >>> tslice = CakeSlice(1.2, 1.3)
        >>> p = AgentPreference(None, pslice, sslice, tslice)
        >>> p.third
        (1.2,1.3)
        """
        return self._third

    def has(self, slice: CakeSlice) -> bool:
        """
        Returns whether or not this preference contains the given slice
        as the primary or secondary preference.
        :param slice: slice to check
        :return: true if this preference contains the given slice as a primary
        or secondary preference.

        >>> pslice = CakeSlice(0, 1)
        >>> sslice = CakeSlice(1, 1.2)
        >>> p = AgentPreference(None, pslice, sslice, None)
        >>> p.has(pslice)
        True
        >>> pslice = CakeSlice(0, 1)
        >>> sslice = CakeSlice(1, 1.2)
        >>> p = AgentPreference(None, pslice, sslice, None)
        >>> p.has(sslice)
        True
        >>> pslice = CakeSlice(0, 1)
        >>> sslice = CakeSlice(1, 1.2)
        >>> p = AgentPreference(None, pslice, sslice, None)
        >>> p.has(CakeSlice(1.3, 3))
        False
        >>> pslice = CakeSlice(0, 1)
        >>> sslice = CakeSlice(1, 1.2)
        >>> tslice = CakeSlice(1.2, 1.3)
        >>> p = AgentPreference(None, pslice, sslice, tslice)
        >>> p.has(tslice)
        False
        """
        # no need to check third
        return self.first == slice or self.second == slice


class PreferenceSearch(object):
    """
    Represents a result of searching for agents which have a preference for
    some slice.
    """

    def __init__(self, slice: CakeSlice, agent_preferences: List[AgentPreference]):
        self._slice = slice
        self._preferences = agent_preferences

    @property
    def preferences(self) -> List[AgentPreference]:
        """
        Gets all the `AgentPreferences` in this search result.
        :return: list of preferences found.

        >>> pslice = CakeSlice(0.1, 1)
        >>> p = AgentPreference(None, CakeSlice(0,0.1), CakeSlice(0.1,1), CakeSlice(1,1.5))
        >>> p2 = AgentPreference(None, CakeSlice(0.1,1), CakeSlice(0,0.1), CakeSlice(1,1.5))
        >>> search = PreferenceSearch(pslice, [p, p2])
        >>> preferences_found = [pref in [p,p2] for pref in search.preferences]
        >>> all(preferences_found)
        True
        """
        return list(self._preferences)

    @property
    def count(self) -> int:
        """
        Gets the amount of preferences found in this search.
        :return: amount of preferences found.

        >>> pslice = CakeSlice(0.1, 1)
        >>> p = AgentPreference(None, CakeSlice(0,0.1), CakeSlice(0.1,1), CakeSlice(1,1.5))
        >>> p2 = AgentPreference(None, CakeSlice(0.1,1), CakeSlice(0,0.1), CakeSlice(1,1.5))
        >>> search = PreferenceSearch(pslice, [p, p2])
        >>> search.count
        2
        """
        return len(self._preferences)

    @property
    def primary_count(self) -> int:
        """
        Gets the amount of preferences found where the slice was the first
        preference.
        :return: amount of preferences found with the slice as the first preference.

        >>> pslice = CakeSlice(0.1, 1)
        >>> p = AgentPreference(None, CakeSlice(0,0.1), pslice, CakeSlice(1,1.5))
        >>> p2 = AgentPreference(None, pslice, CakeSlice(0,0.1), CakeSlice(1,1.5))
        >>> search = PreferenceSearch(pslice, [p, p2])
        >>> search.primary_count
        1
        """
        return len([preference for preference in self._preferences if preference.first == self._slice])

    @property
    def secondary_count(self) -> int:
        """
        Gets the amount of preferences found where the slice was the second
        preference.
        :return: amount of preferences found with the slice as the second preference.

        >>> pslice = CakeSlice(0.1, 1)
        >>> p = AgentPreference(None, CakeSlice(0,0.1), pslice, CakeSlice(1,1.5))
        >>> p2 = AgentPreference(None, pslice, CakeSlice(0,0.1), CakeSlice(1,1.5))
        >>> search = PreferenceSearch(pslice, [p, p2])
        >>> search.secondary_count
        1
        """
        return len([preference for preference in self._preferences if preference.second == self._slice])


class Preferences(object):
    """
    Represents preferences of agents for a specific cake state.
    """

    def __init__(self, agent_to_preference):
        self._agents_to_preferences = agent_to_preference

    def try_get_preference_for_agent(self, agent: Agent) -> Optional[AgentPreference]:
        """
        Tries to get the preference of the given agent.
        :param agent: agent to find preference for
        :return: the preference if found, None otherwise.

        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = AgentPreference(a, CakeSlice(0, 1), CakeSlice(1, 1.5), CakeSlice(1.5, 1.6))
        >>> prefs = Preferences({a: p})
        >>> prefs.try_get_preference_for_agent(a) == p
        True
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> prefs = Preferences({})
        >>> prefs.try_get_preference_for_agent(a) is None
        True
        """
        if agent not in self._agents_to_preferences:
            return None
        return self._agents_to_preferences[agent]

    def find_agents_with_preference_for(self, slice: CakeSlice, exclude_agents: List[Agent] = None) -> PreferenceSearch:
        """
        Searches amongst all the agent preferences for preferences for `slice` is either a first or second
        preference.
        :param slice: slice to search for in preferences
        :param exclude_agents: agents whose preference should be ignored
        :return `PreferenceSearch` result with all the preferences found.

        >>> pslice = CakeSlice(1, 1.5)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = AgentPreference(a, CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6))
        >>> prefs = Preferences({a: p})
        >>> result = prefs.find_agents_with_preference_for(pslice)
        >>> result.preferences[0] == p
        True
        >>> pslice = CakeSlice(1, 1.5)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = AgentPreference(a, CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6))
        >>> a2 = PiecewiseConstantAgent([1, 1], "agent2")
        >>> p2 = AgentPreference(a, CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6))
        >>> prefs = Preferences({a: p, a2: p2})
        >>> result = prefs.find_agents_with_preference_for(pslice)
        >>> all([pref in [p, p2] for pref in result.preferences])
        True
        >>> pslice = CakeSlice(1, 1.5)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = AgentPreference(a, CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6))
        >>> a2 = PiecewiseConstantAgent([1, 1], "agent2")
        >>> p2 = AgentPreference(a, CakeSlice(0, 1), CakeSlice(1.5, 1.6), pslice)
        >>> prefs = Preferences({a: p, a2: p2})
        >>> result = prefs.find_agents_with_preference_for(pslice)
        >>> result.count == 1 and result.preferences[0] == p
        True
        >>> pslice = CakeSlice(1, 1.5)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = AgentPreference(a, CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6))
        >>> a2 = PiecewiseConstantAgent([1, 1], "agent2")
        >>> p2 = AgentPreference(a, CakeSlice(0, 1), CakeSlice(1.5, 1.6), CakeSlice(1, 2))
        >>> prefs = Preferences({a: p, a2: p2})
        >>> result = prefs.find_agents_with_preference_for(pslice)
        >>> result.count == 1 and result.preferences[0] == p
        True
        >>> pslice = CakeSlice(1, 1.5)
        >>> a = PiecewiseConstantAgent([1, 1], "agent")
        >>> p = AgentPreference(a, CakeSlice(0, 1), pslice, CakeSlice(1.5, 1.6))
        >>> a2 = PiecewiseConstantAgent([1, 1], "agent2")
        >>> p2 = AgentPreference(a, pslice, CakeSlice(0, 1), CakeSlice(1.5, 1.6))
        >>> prefs = Preferences({a: p, a2: p2})
        >>> result = prefs.find_agents_with_preference_for(pslice, exclude_agents=[a2])
        >>> result.count == 1 and result.preferences[0] == p
        True
        """
        if exclude_agents is None:
            exclude_agents = []

        preferences = [preference for agent, preference in self._agents_to_preferences.items()
                       if agent not in exclude_agents and preference.has(slice)]
        return PreferenceSearch(slice, preferences)


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


def get_agent_preference(agent: Agent, slices: List[CakeSlice]) -> AgentPreference:
    """
    Gets the preference of agent, from the given slices.
    :param agent: agent whose preference to find.
    :param slices: slices out of to search.
    :return `AgentPreference` representing the preference of `agent` out of `slices`.

    >>> s = [CakeSlice(0, 1), CakeSlice(1, 2), CakeSlice(2, 3)]
    >>> a = PiecewiseConstantAgent([33, 11, 1], "agent")
    >>> get_agent_preference(a, s)
    agent: (0,1),(1,2),(2,3)
    >>> s = [CakeSlice(0, 1), CakeSlice(1, 2), CakeSlice(2, 3)]
    >>> a = PiecewiseConstantAgent([33, 11, 66], "agent")
    >>> get_agent_preference(a, s)
    agent: (2,3),(0,1),(1,2)
    """
    first = find_favorite_slice(agent, slices)
    second = find_favorite_slice(agent, slices, exclude_slices=[first])
    third = find_favorite_slice(agent, slices, exclude_slices=[first, second])

    return AgentPreference(agent, first, second, third)


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
    >>> prefs.try_get_preference_for_agent(a)
    agent: (0,1),(1,2),(2,3)
    >>> s = [CakeSlice(0, 1), CakeSlice(1, 2), CakeSlice(2, 3)]
    >>> a = PiecewiseConstantAgent([33, 11, 1], "agent")
    >>> a2 = PiecewiseConstantAgent([33, 11, 66], "agent")
    >>> prefs = get_preferences_for_agents([a,a2], s)
    >>> prefs.try_get_preference_for_agent(a)
    agent: (0,1),(1,2),(2,3)
    >>> prefs.try_get_preference_for_agent(a2)
    agent: (2,3),(0,1),(1,2)
    """
    agents_to_preferences = {agent: get_agent_preference(agent, slices) for agent in agents}
    return Preferences(agents_to_preferences)


if __name__ == "__main__":
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
