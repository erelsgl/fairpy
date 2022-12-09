"""
Fairly Allocating Many Goods with Few Queries (2019)

Authors: Hoon Oh, Ariel D. Procaccia, Warut Suksompong. See https://ojs.aaai.org/index.php/AAAI/article/view/4046/3924

Programmer: Aviem Hadar
Since: 2022
"""
import logging
import sys

from typing import List, Dict, Any

import fairpy
from fairpy import AgentList

logger = logging.getLogger(__name__)


def two_agents_ef1(agents: AgentList, items: List[Any]=None) -> Dict[str,List[Any]]:
    """
    Algorithm No 1

    Allocates the given items(inside each agent) to the 2 given agents while satisfying EF1 condition.
    read more about EF1 here: https://en.wikipedia.org/wiki/Envy-free_item_allocation#EF1_-_envy-free_up_to_at_most_one_item

    :param agents: The agents who participate in the allocation.
    :param items: The items which are being allocated.
    :return: An allocation for each of the agents.

    ### identical valuations:
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],["a", "b", "c", "d", "e", "f", "g"])
    >>> allocation
    {'Alice': ['g'], 'George': ['a', 'b', 'c', 'd', 'e', 'f']}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":4,"f":7,"g":12}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 3, "b": 5, "c": 4, "d":1,"e":2,"f":10,"g":15}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],["a", "b", "c", "d", "e", "f", "g"])
    >>> allocation
    {'Alice': ['a', 'b', 'c', 'd', 'e'], 'George': ['f', 'g']}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True

    ### ONLY ONE OBJECT
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],["a"])
    >>> allocation
    {'Alice': [], 'George': ['a']}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True

    ### nothing to allocate
    >>> Alice = fairpy.agents.AdditiveAgent({}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],[])
    >>> allocation
    {'Alice': [], 'George': []}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":3,"e":1,"f":7,"g":15,"h":21,"i":4,"j":22,"k":7,"l":10,"m":11,"n":22,"o":6,"p":7,"q":16,"r":12,"s":3,"t":28,"u":39,"v":4,"w":9,"x":1,"y":17,"z":99}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2, "b": 4, "c": 3, "d":1,"e":0,"f":7,"g":16,"h":21,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":10,"s":3,"t":24,"u":39,"v":2,"w":9,"x":5,"y":17,"z":100}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],["a", "b", "c", "d", "e", "f", "g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
    >>> allocation
    {'Alice': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's'], 'George': ['t', 'u', 'v', 'w', 'x', 'y', 'z']}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True
    """
    if len(agents) != 2:
        raise ValueError("wrong number of agents")
    if items is None:
        items = agents.all_items()
    logger.info("\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    Lg_value = 0
    Rg_value = agents[0].total_value()
    rightmost = None
    Lg = []
    Rg = []
    for item in items:
        if Lg_value <= Rg_value:
            Lg_value += agents[0].value(item)
            Rg_value -= agents[0].value(item)
            rightmost = item
        else:
            break
    rightmost_found = False
    if rightmost is not None and Lg_value - agents[0].value(rightmost) <= Rg_value:
        for item in items:
            if rightmost_found is False:
                Lg.append(item)
                if item == rightmost:
                    rightmost_found = True
            else:
                Rg.append(item)
    else:
        for item in items:
            if item == rightmost:
                rightmost_found = True
            if rightmost_found is False:
                Lg.append(item)
            else:
                Rg.append(item)
    logger.info("g is %s, Lg = %s (total value %d), Rg = %s (total value %d)", rightmost, Lg, Lg_value, Rg,
                Rg_value)
    if agents[1].value(Rg) > agents[1].value(Lg):
        allocation = {agents[0].name(): Lg, agents[1].name(): Rg}
    else:
        allocation = {agents[0].name(): Rg, agents[1].name(): Lg}
    return allocation


def three_agents_IAV(agents: AgentList, items: List[Any]=None) -> Dict[str,List[Any]]:
    """
    Algorithm No 2 - three agents with Identical Additive Valuations
    Allocating the given items to three agents while satisfying EF1 condition

    >>> Alice = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d"])
    >>> allocation
    {'Alice': ['d', 'c'], 'Bob': ['b'], 'George': ['a']}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g"])
    >>> allocation
    {'Alice': ['a', 'b'], 'Bob': ['c', 'd', 'e'], 'George': ['g', 'f']}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4,"h":5,"i":0,"j":9,"k":8,"l":2,"m":8,"n":7}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4,"h":5,"i":0,"j":9,"k":8,"l":2,"m":8,"n":7}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4,"h":5,"i":0,"j":9,"k":8,"l":2,"m":8,"n":7}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g","h","i","j","k","l","m","n"])
    >>> allocation
    {'Alice': ['a', 'b', 'c', 'd', 'e', 'f'], 'Bob': ['g', 'h', 'i', 'j'], 'George': ['l', 'm', 'n', 'k']}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True

    ### TOTALLY UNFAIR CASE
    >>> Alice = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g","h"])
    >>> allocation
    {'Alice': ['h', 'g', 'f', 'e'], 'Bob': ['d', 'c', 'b'], 'George': ['a']}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True

    ### TOTALLY UNFAIR CASE
    >>> Alice = fairpy.agents.AdditiveAgent({"a":1,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":30}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":1,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":30}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":1,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":30}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g","h"])
    >>> allocation
    {'Alice': ['a', 'b', 'c', 'd'], 'Bob': ['e', 'f', 'g'], 'George': ['h']}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15,"h":21,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":12,"s":3,"t":28,"u":39,"v":2,"w":9,"x":1,"y":17,"z":100}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15,"h":21,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":12,"s":3,"t":28,"u":39,"v":2,"w":9,"x":1,"y":17,"z":100}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15,"h":21,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":12,"s":3,"t":28,"u":39,"v":2,"w":9,"x":1,"y":17,"z":100}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a", "b", "c", "d", "e", "f", "g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
    >>> allocation
    {'Alice': ['z', 'y', 'x'], 'Bob': ['w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o'], 'George': ['m', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a', 'n']}
    >>> _is_allocation_EF1(allocation, [Alice,George])
    True
    """
    if len(agents) != 3:
        raise Exception("wrong number of agents")
    if _are_identical_valuations(agents) is False:
        raise Exception("valuations are not identical")
    if items is None:
        items = agents.all_items()
    logger.info("\nThree Agents %s %s %s and items %s", agents[0].name(), agents[1].name(), agents[2].name(), items)
    A = []
    G = items.copy()
    g1, Lg1, Lg1_value = _find_g1(agents[0], items)
    g2, Rg2, Rg2_value = _find_g2(agents[0], items)
    if Lg1_value < Rg2_value:
        logger.info("u(Lg1) >= u(Rg2), reversing the items order")
        G.reverse()
        g1, Lg1, Lg1_value = _find_g1(agents[0], G)
        g2, Rg2, Rg2_value = _find_g2(agents[0], G)
    logger.info("g1 = %s, Lg1 = %s, (total value %d), g2 = %s, Rg2 = %s, (total value %d) \nStep 2:", g1, Lg1,
                Lg1_value, g2, Rg2, Rg2_value)
    if len(Lg1) != 0:
        A, Lg3_value = _find_g3(agents[0], G, Rg2_value)
    C = Rg2
    B = G.copy()
    AuC = A.copy() + C  # A u C
    [B.remove(arg) for arg in AuC]  # B = G\(A u C)
    B_copy = B.copy()
    if B_copy.count(g2) != 0:
        B_copy.remove(g2)
    logger.info("A = %s, B = %s, C = %s", A, B, C)
    if agents[0].value(C) >= agents[0].value(B_copy):
        logger.info("u(C) >= u(B\\{g2})")
        allocation = {agents[0].name(): A, agents[1].name(): B, agents[2].name(): C}
    else:
        C_tag = Rg2.copy()
        C_tag.append(g2)
        remaining_goods = G.copy()
        [remaining_goods.remove(arg) for arg in C_tag]  # G \ C'
        A_tag, B_tag = _Lemma4_1(remaining_goods, agents[0])
        logger.info("A' = %s, B' = %s, C' = %s", A_tag, B_tag, C_tag)
        allocation = {agents[0].name(): A_tag, agents[1].name(): B_tag, agents[2].name(): C_tag}
    return allocation


def _are_identical_valuations(agents: AgentList) -> bool:
    """
    this function make sure that the valuations entered by the user
    are equal for all agents
    """
    a1 = agents[0]
    a2 = agents[1]
    a3 = agents[2]
    for item in a1.all_items():
        first_two = (a1.value(item) == a2.value(item))
        if first_two is False or a1.value(item) != a3.value(item):
            return False
    return True


def _find_g1(agent, items):
    """
    this function finds the leftmost good such that
    u(Lg1 u {g1}) > u(G)/3
    >>> Alice = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Alice")
    >>> partition = _find_g1(Alice,{"a":4,"b":3,"c":2,"d":1})
    >>> partition # u(G) is 10
    ('a', [], 0)
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> partition = _find_g1(Alice,{"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4})
    >>> partition # u(G) is 22
    ('b', ['a'], 5)
    """
    g1 = ""
    Lg1 = []
    Lg1_value = 0
    uG = agent.value(items)
    for item in items:
        if Lg1_value + agent.value(item) > uG / 3:
            g1 = item
            break
        Lg1.append(item)
        Lg1_value += agent.value(item)
    return g1, Lg1, Lg1_value


def _find_g2(agent, items):
    """
    this function finds the rightmost good such that
    u(Rg2 u {g2}) > u(G)/3
    >>> Alice = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Alice")
    >>> partition = _find_g2(Alice,{"a":4,"b":3,"c":2,"d":1})
    >>> partition # u(G) is 10
    ('c', ['d'], 1)
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> partition = _find_g2(Alice,{"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4})
    >>> partition # u(G) is 22
    ('f', ['g'], 4)
    """
    g2 = ""
    uG = agent.value(items)
    Rg2_value = uG
    Rg2 = list(items.copy())
    for item in items:
        if Rg2_value + agent.value(item) <= uG / 3:
            break
        g2 = item
        Rg2.remove(item)
        Rg2_value -= agent.value(item)
        if Rg2_value + agent.value(item) <= uG / 3:
            break
    return g2, Rg2, Rg2_value


def _find_g3(agent, items, Rg2_value):
    """
    this function finds the leftmost good such that
    u(Lg3 u {g3}) > u(Rg2)
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> partition = _find_g3(Alice,{"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4},4)
    >>> partition # u(G) is 22
    (['a'], 5)
    """
    Lg3_value = 0
    Lg3 = []
    for item in items:
        Lg3.append(item)
        Lg3_value += agent.value(item)
        if Lg3_value >= Rg2_value:
            break
    return Lg3, Lg3_value


def _Lemma4_1(remaining_goods: list, agent):
    """
    partitioning the remaining goods into 2 parts, where the
    difference between them is small enough
    """
    A_tag = []
    B_tag = remaining_goods.copy()
    a_value = 0
    b_value = agent.value(remaining_goods)
    minimum = sys.maxsize
    for item in remaining_goods:
        a_value += agent.value(item)
        b_value -= agent.value(item)
        if abs(a_value - b_value) <= minimum:
            minimum = abs(a_value - b_value)
            A_tag.append(item)
            B_tag.remove(item)
        else:
            break
    return A_tag, B_tag


def _is_allocation_EF1(allocation:Dict[str,List[Any]], agents:AgentList):
    for agent in agents:
        if not agent.is_EF1(allocation[agent.name()], allocation.values()):
            return False
    return True


two_agents_ef1.logger = logger
three_agents_IAV.logger = logger

if __name__ == "__main__":
    # logger.addHandler(logging.StreamHandler(sys.stdout))
    # logger.setLevel(logging.INFO)

    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
