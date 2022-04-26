"""
Fairly Allocating Many Goods with Few Queries (2019)

Authors: Hoon Oh, Ariel D. Procaccia, Warut Suksompong. See https://ojs.aaai.org/index.php/AAAI/article/view/4046/3924

Programmer: Aviem Hadar
Since:  04/2022
"""
import doctest
from typing import List, Any

import fairpy
from fairpy import Agent
from fairpy.allocations import Allocation


def two_agents_ef1(agents: List[Agent], items: List[Any]) -> Allocation:
    """
    Algorithm No 1

    Allocates the given items(inside each agent) to the 2 given agents while satisfying EF1 condition.
    read more about EF1 here: https://en.wikipedia.org/wiki/Envy-free_item_allocation#EF1_-_envy-free_up_to_at_most_one_item

    :param agents: The agents who participate in the allocation.
    :param items: The items which are being allocated.
    :return: An allocation for each of the agents.


    >>> ### Using Agent objects:
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],set("abcdefg"))
    >>> allocation
    Alice gets {a,b,c,d,e,f} with value 20.
    George gets {g} with value 15.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":4,"f":7,"g":15}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":4,"f":7,"g":15}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],set("abcdefg"))
    >>> allocation
    Alice gets {f,g} with value 22.
    George gets {a,b,c,d,e} with value 16.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    >>> ### ONLY ONE OBJECT
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],set("a"))
    >>> allocation
    Alice gets {a} with value 2.
    George gets {} with value 0.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    >>> ### nothing to allocate
    >>> Alice = fairpy.agents.AdditiveAgent({}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],set())
    >>> allocation
    Alice gets {} with value 0.
    George gets {} with value 0.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    """
    return 0


def three_agents_IAV(agents: List[Agent], items: List[Any]) -> Allocation:
    """
    Algorithm No 2 - three agents with identical additive valuations
    Allocating the given items to three agents while satisfying EF1 condition
    >>> Alice = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],set("abcd"))
    >>> allocation
    Alice gets {a} with value 4.
    Bob gets {b} with value 3.
    George gets {c,d} with value 3.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],set("abcdefg"))
    >>> allocation
    Alice gets {a,b} with value 11.
    Bob gets {c,d,e} with value 5.
    George gets {f,g} with value 6.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4,"h":5,"i":0,"j":9,"k":8,"l":2,"m":8,"n":7}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4,"h":5,"i":0,"j":9,"k":8,"l":2,"m":8,"n":7}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4,"h":5,"i":0,"j":9,"k":8,"l":2,"m":8,"n":7}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],set("abcdefghijklmn"))
    >>> allocation
    Alice gets {a,b,c,d,e,f} with value 18.
    Bob gets {g,h,i,j} with value 18.
    George gets {k,l,m,n} with value 25.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> ### TOTALLY UNFAIR CASE BUT ACCEPTS EF1
    >>> Alice = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],,set("abcdefgh"))
    >>> allocation
    Alice gets {a} with value 30.
    Bob gets {b,c,d} with value 3.
    George gets {e,f,g,h} with value 4.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    """
    return 0


def three_agents_AAV(agents: List[Agent], items: List[Any]) -> Allocation:
    """
    Algorithm No 3 - three agents with arbitrary additive valuations
    Allocating the given items to three agents with different valuations for the items while satisfying EF1 condition
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":3,"f":2,"g":3}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":4,"b":5,"c":1,"d":2,"e":2,"f":3,"g":4}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],set("abcdefg"))
    >>> allocation
    Alice gets {c,d,e} with value 5.
    Bob gets {a,b} with value 11.
    George gets {f,g} with value 7.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    """
    return 0


if __name__ == "__main__":
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
