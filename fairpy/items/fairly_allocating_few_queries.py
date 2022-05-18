"""
Fairly Allocating Many Goods with Few Queries (2019)

Authors: Hoon Oh, Ariel D. Procaccia, Warut Suksompong. See https://ojs.aaai.org/index.php/AAAI/article/view/4046/3924

Programmer: Aviem Hadar
Since: 2022
"""
import doctest
from copy import copy
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
    >>> allocation = two_agents_ef1([Alice,George],["a", "b", "c", "d", "e", "f", "g"])
    >>> allocation
    Alice gets {g} with value 15.
    George gets {a,b,c,d,e,f} with value 20.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":4,"f":7,"g":15}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":4,"f":7,"g":15}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],["a", "b", "c", "d", "e", "f", "g"])
    >>> allocation
    Alice gets {f,g} with value 22.
    George gets {a,b,c,d,e} with value 16.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    >>> ### ONLY ONE OBJECT
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],["a"])
    >>> allocation
    Alice gets {} with value 0.
    George gets {a} with value 2.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    >>> ### nothing to allocate
    >>> Alice = fairpy.agents.AdditiveAgent({}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],[])
    >>> allocation
    Alice gets {} with value 0.
    George gets {} with value 0.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    """
    first_agent_items = agents[0].all_items()
    left_value = 0
    right_value = agents[0].total_value()
    rightmost = None
    for agent_value in first_agent_items:
        if left_value <= right_value:
            left_value += agents[0].value(agent_value)
            right_value -= agents[0].value(agent_value)
            rightmost = agent_value
        else:
            break
    Lg = []
    Rg = []
    flag = False
    if rightmost is not None and left_value - agents[0].value(rightmost) <= right_value:
        for item in items:
            if flag is False:
                Lg.append(item)
                if item == rightmost:
                    flag = True
            else:
                Rg.append(item)
    else:
        for item in items:
            if item == rightmost:
                flag = True
            if flag is False:
                Lg.append(item)
            else:
                Rg.append(item)
    a = Allocation(agents=agents, bundles={agents[0].name(): Rg, agents[1].name(): Lg})
    return a


def three_agents_IAV(agents: List[Agent], items: List[Any]) -> Allocation:
    """
    Algorithm No 2 - three agents with identical additive valuations
    Allocating the given items to three agents while satisfying EF1 condition
    >>> Alice = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d"])
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
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g"])
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
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g","h","i","j","k","l","m","n"])
    >>> allocation
    Alice gets {a,b,c,d,e,f} with value 18.
    Bob gets {g,h,i,j,k} with value 26.
    George gets {l,m,n} with value 17.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> ### TOTALLY UNFAIR CASE BUT ACCEPTS EF1
    >>> Alice = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g","h"])
    >>> allocation
    Alice gets {a} with value 30.
    Bob gets {} with value 0.
    George gets {b,c,d,e,f,g,h} with value 7.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    """
    agent_items = agents[0].all_items()
    u_G = agents[0].total_value()
    Lg1_value = 0
    Lg3_value = 0
    Rg2_value = u_G
    g1 = None
    g2 = None
    g3 = None
    g1_found = False
    g3_found = False
    counter = u_G
    A = []
    Lg1 = []
    Rg2 = []
    Lg3 = []
    G = items.copy()
    for item in agent_items:
        if g1_found is False and Lg1_value + agents[0].value(item) > u_G / 3:
            g1 = item
            g1_found = True
            Lg1.append(item)
        if g1_found is True and Rg2_value > u_G / 3:
            g2 = item
            Rg2 = G.copy()
            for g in agent_items:
                counter -= agents[0].value(g)
                Rg2.remove(g)
                if g == g2:
                    break
            Rg2_value = counter
            counter = u_G
            if Rg2_value + agents[0].value(item) < u_G / 3:
                break
        Lg1_value += agents[0].value(item)
    # print("g1:", g1, "g2:", g2)
    if len(Lg1) != 0:
        for item in items:
            Lg3.append(item)
            g3 = item
            Lg3_value += agents[0].value(item)
            if Lg3_value >= Rg2_value:
                break
        A = Lg3
    # print("g3:", g3)
    C = Rg2
    B = G.copy()
    AuC = A.copy()
    AuC += C
    [B.remove(arg) for arg in AuC]
    if B.count(g2) == 0 and agents[0].value(C) >= agents[0].value(B):
        a = Allocation(agents=agents, bundles={agents[0].name(): A, agents[1].name(): B, agents[2].name(): C})
    elif agents[0].value(C) >= agents[0].value(copy(B).remove(g2)):
        a = Allocation(agents=agents, bundles={agents[0].name(): A, agents[1].name(): B, agents[2].name(): C})
    else:
        C_tag = copy(Rg2).add(g2)
        A_tag = set()
        B_tag = copy(G).remove(C_tag)
        for item in items:
            A_tag.add(item)
            B_tag.remove(item)
            if agents[0].value(A_tag) >= agents[0].value(B_tag):
                break
        a = Allocation(agents=agents,
                       bundles={agents[0].name(): A_tag, agents[1].name(): B_tag, agents[2].name(): C_tag})
    return a


def three_agents_AAV(agents: List[Agent], items: List[Any]) -> Allocation:
    """
    Algorithm No 3 - three agents with arbitrary additive valuations
    Allocating the given items to three agents with different valuations for the items while satisfying EF1 condition
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":3,"f":2,"g":3}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":4,"b":5,"c":1,"d":2,"e":2,"f":3,"g":4}, name="George")
    >>> allocation = three_agents_AAV([Alice,Bob,George],["a","b","c","d","e","f","g"])
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

    # Alice = fairpy.agents.AdditiveAgent({"a": 4, "b": 3, "c": 2, "d": 1}, name="Alice")
    # Bob = fairpy.agents.AdditiveAgent({"a": 4, "b": 3, "c": 2, "d": 1}, name="Bob")
    # George = fairpy.agents.AdditiveAgent({"a": 4, "b": 3, "c": 2, "d": 1}, name="George")
    # a = three_agents_IAV([Alice, Bob, George], ["a", "b", "c", "d"])
    # print(a)

    # Alice = fairpy.agents.AdditiveAgent({"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4}, name="Alice")
    # Bob = fairpy.agents.AdditiveAgent({"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4}, name="Bob")
    # George = fairpy.agents.AdditiveAgent({"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4}, name="George")
    # a = three_agents_IAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g"])
    # print(a)

    # Alice = fairpy.agents.AdditiveAgent(
    #     {"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4, "h": 5, "i": 0, "j": 9, "k": 8, "l": 2, "m": 8,
    #      "n": 7}, name="Alice")
    # Bob = fairpy.agents.AdditiveAgent(
    #     {"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4, "h": 5, "i": 0, "j": 9, "k": 8, "l": 2, "m": 8,
    #      "n": 7}, name="Bob")
    # George = fairpy.agents.AdditiveAgent(
    #     {"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4, "h": 5, "i": 0, "j": 9, "k": 8, "l": 2, "m": 8,
    #      "n": 7}, name="George")
    # a = three_agents_IAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"])
    # print(a)

    # Alice = fairpy.agents.AdditiveAgent({"a": 30, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1}, name="Alice")
    # Bob = fairpy.agents.AdditiveAgent({"a": 30, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1}, name="Bob")
    # George = fairpy.agents.AdditiveAgent({"a": 30, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 1},
    #                                      name="George")
    # a = three_agents_IAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g", "h"])
    # print(a)

    # Alice = fairpy.agents.AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 30}, name="Alice")
    # Bob = fairpy.agents.AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 30}, name="Bob")
    # George = fairpy.agents.AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1, "h": 30},
    #                                      name="George")
    # a = three_agents_IAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g", "h"])
    # print(a)
