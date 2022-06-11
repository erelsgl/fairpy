"""
Fairly Allocating Many Goods with Few Queries (2019)

Authors: Hoon Oh, Ariel D. Procaccia, Warut Suksompong. See https://ojs.aaai.org/index.php/AAAI/article/view/4046/3924

Programmer: Aviem Hadar
Since: 2022
"""
import sys
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
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15,"h":21,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":12,"s":3,"t":28,"u":39,"v":2,"w":9,"x":1,"y":17,"z":100}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15,"h":21,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":12,"s":3,"t":28,"u":39,"v":2,"w":9,"x":1,"y":17,"z":100}, name="George")
    >>> allocation = two_agents_ef1([Alice,George],["a", "b", "c", "d", "e", "f", "g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
    >>> allocation
    Alice gets {t,u,v,w,x,y,z} with value 196.
    George gets {a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s} with value 179.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and George.is_EF1(allocation[1], allocation)
    True
    """
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
    # partitioning the items
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
    allocation = Allocation(agents=agents, bundles={agents[0].name(): Rg, agents[1].name(): Lg})
    return allocation


def three_agents_IAV(agents: List[Agent], items: List[Any]) -> Allocation:
    """
    Algorithm No 2 - three agents with Identical Additive Valuations
    Allocating the given items to three agents while satisfying EF1 condition
    >>> Alice = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d"])
    >>> allocation
    Alice gets {c,d} with value 3.
    Bob gets {b} with value 3.
    George gets {a} with value 4.
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
    Bob gets {g,h,i,j} with value 18.
    George gets {k,l,m,n} with value 25.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> ### TOTALLY UNFAIR CASE
    >>> Alice = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":30,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":1}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g","h"])
    >>> allocation
    Alice gets {e,f,g,h} with value 4.
    Bob gets {b,c,d} with value 3.
    George gets {a} with value 30.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> ### TOTALLY UNFAIR CASE
    >>> Alice = fairpy.agents.AdditiveAgent({"a":1,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":30}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":1,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":30}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a":1,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":30}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a","b","c","d","e","f","g","h"])
    >>> allocation
    Alice gets {a,b,c,d} with value 4.
    Bob gets {e,f,g} with value 3.
    George gets {h} with value 30.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[2], allocation)
    True
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15,"h":21,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":12,"s":3,"t":28,"u":39,"v":2,"w":9,"x":1,"y":17,"z":100}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a":1,"b":1,"c":1,"d":1,"e":1,"f":1,"g":1,"h":30,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":12,"s":3,"t":28,"u":39,"v":2,"w":9,"x":1,"y":17,"z":100}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a": 2, "b": 6, "c": 3, "d":1,"e":1,"f":7,"g":15,"h":21,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":12,"s":3,"t":28,"u":39,"v":2,"w":9,"x":1,"y":17,"z":100}, name="George")
    >>> allocation = three_agents_IAV([Alice,Bob,George],["a", "b", "c", "d", "e", "f", "g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
    >>> allocation
    Alice gets {x,y,z} with value 118.
    Bob gets {o,p,q,r,s,t,u,v,w} with value 124.
    George gets {a,b,c,d,e,f,g,h,i,j,k,l,m,n} with value 133.
    <BLANKLINE>
    >>> Alice.is_EF1(allocation[0], allocation) and Bob.is_EF1(allocation[1], allocation) and George.is_EF1(allocation[1], allocation)
    True
    """
    A = []
    G = items.copy()
    g1, Lg1, Lg1_value = find_g1(agents[0], items)
    g2, Rg2, Rg2_value = find_g2(agents[0], items)
    # if u(Lg1) >= u(Rg2)
    if Lg1_value < Rg2_value:
        G.reverse()
        g1, Lg1, Lg1_value = find_g1(agents[0], G)
        g2, Rg2, Rg2_value = find_g2(agents[0], G)
    # STEP 2 #
    if len(Lg1) != 0:
        A, Lg3_value = find_g3(agents[0], G, Rg2_value)
    C = Rg2
    B = G.copy()
    AuC = A.copy() + C  # A u C
    [B.remove(arg) for arg in AuC]  # B = G\(A u C)
    B_copy = B.copy()
    if B_copy.count(g2) != 0:
        B_copy.remove(g2)
    if agents[0].value(C) >= agents[0].value(B_copy):  # if u(C) >= u(B\{g2})
        allocation = Allocation(agents=agents, bundles={agents[0].name(): A, agents[1].name(): B, agents[2].name(): C})
    else:
        C_tag = Rg2.copy()  # C' = Rg2 u {g2}
        C_tag.append(g2)
        remaining_goods = G.copy()
        [remaining_goods.remove(arg) for arg in C_tag]  # G \ C'
        A_tag, B_tag = Lemma4_1(remaining_goods, agents[0])
        allocation = Allocation(agents=agents,
                                bundles={agents[0].name(): A_tag, agents[1].name(): B_tag, agents[2].name(): C_tag})
    return allocation


def find_g1(agent, items):
    """
    this function finds the leftmost good such that
    u(Lg1 u {g1}) > u(G)/3
    >>> Alice = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Alice")
    >>> partition = find_g1(Alice,{"a":4,"b":3,"c":2,"d":1})
    >>> partition # u(G) is 10
    ('a', [], 0)
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> partition = find_g1(Alice,{"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4})
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


def find_g2(agent, items):
    """
    this function finds the rightmost good such that
    u(Rg2 u {g2}) > u(G)/3
    >>> Alice = fairpy.agents.AdditiveAgent({"a":4,"b":3,"c":2,"d":1}, name="Alice")
    >>> partition = find_g2(Alice,{"a":4,"b":3,"c":2,"d":1})
    >>> partition # u(G) is 10
    ('c', ['d'], 1)
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> partition = find_g2(Alice,{"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4})
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


def find_g3(agent, items, Rg2_value):
    """
    this function finds the leftmost good such that
    u(Lg3 u {g3}) > u(Rg2)
    >>> Alice = fairpy.agents.AdditiveAgent({"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4}, name="Alice")
    >>> partition = find_g3(Alice,{"a":5,"b":6,"c":1,"d":2,"e":2,"f":2,"g":4},4)
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


def Lemma4_1(remaining_goods: list, agent):
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


# this algorithm isn't done, steps 1,2 finished.
def three_agents_AAV(agents: List[Agent], items: List[Any]) -> Allocation:
    """
    Algorithm No 3 - three agents with Arbitrary Additive Valuations
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
    >>> #NOT EQUAL BUNDLES
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 1, "g": 1}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a": 5, "b": 6, "c": 6, "d": 2, "e": 3, "f": 2, "g": 3}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a": 1, "b": 1, "c": 1, "d": 1, "e": 1, "f": 3, "g": 4}, name="George")
    >>> allocation = three_agents_AAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g"])
    >>> allocation
    >>> # EQUAL BUNDLES
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 5, "b": 6, "c": 1, "d": 2, "e": 2, "f": 2, "g": 4}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a": 5, "b": 6, "c": 1, "d": 2, "e": 3, "f": 2, "g": 3}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a": 4, "b": 5, "c": 1, "d": 2, "e": 2, "f": 3, "g": 4}, name="George")
    >>> allocation = three_agents_AAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g"])
    >>> allocation
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 10, "b": 8, "c": 9, "d": 2, "e": 7, "f": 1, "g": 4, "h": 6}, name="Alice")
    >>> Bob = fairpy.agents.AdditiveAgent({"a": 4, "b": 2, "c": 1, "d": 2, "e": 7, "f": 2, "g": 3, "h": 5}, name="Bob")
    >>> George = fairpy.agents.AdditiveAgent({"a": 4, "b": 4, "c": 1, "d": 2, "e": 2, "f": 9, "g": 3, "h": 3},
                                         name="George")
    >>> allocation = three_agents_AAV([Alice, Bob, George], ["a", "b", "c", "d", "e", "f", "g", "h"])
    >>> allocation
    """
    # STEP 1:
    u1_valuation = {}
    u2_valuation = {}
    u3_valuation = {}
    a1 = agents[0]
    a2 = agents[1]
    a3 = agents[2]
    for item in items:
        u1_valuation[item] = a1.value(item)
        u2_valuation[item] = a2.value(item)
        u3_valuation[item] = a3.value(item)
    initial_allocation = Identical_EF1(u1_valuation, items)
    A, B, C = initial_allocation[0], initial_allocation[1], initial_allocation[2]
    a2_favorite_value = 0
    a3_favorite_value = 0
    for alloc in A, B, C:
        if a2_favorite_value < a2.value(alloc.items):
            a2_bundle = alloc.items
            a2_favorite_value = a2.value(a2_bundle)
        if a3_favorite_value < a3.value(alloc.items):
            a3_bundle = alloc.items
            a3_favorite_value = a3.value(a3_bundle)
    a1_bundle = items.copy()
    if a2_bundle != a3_bundle:
        [a1_bundle.remove(arg) for arg in a2_bundle]
        [a1_bundle.remove(arg) for arg in a3_bundle]
        # print("Different bundles", a1_bundle, a2_bundle, a3_bundle)
    # else:
    # print("Same bundles:", a1_bundle, a2_bundle, a3_bundle)
    if A.items != a2_bundle:
        temp = A.items
        A.items = a2_bundle
        if B.items == A.items:
            B.items = temp
        else:
            C.items = temp
    # STEP 2:
    A_tag = []
    T = A.items.copy()
    # print("before splitting A:\n", "A:", A, "B:", B, "C:", C)
    u2_val_A = {}
    for k, v in u2_valuation.items():
        if A.items.count(k) != 0:
            u2_val_A[k] = v
    A_sort_by_val = {k: v for k, v in sorted(u2_val_A.items(), key=lambda good: good[1])}
    for item in A_sort_by_val:
        A_tag.append(item)
        T.remove(item)
        flag = False
        if a2.value(A_tag) <= a2.value(B):
            for g in T:
                temp_set = A_tag.copy()
                temp_set.append(g)
                if a2.value(temp_set) > a2.value(B):
                    flag = True
                    break
        else:
            break
        if flag:
            break
    # print("A_tag:", A_tag, "T:", T)
    if a3.value(A_tag) >= max(a3.value(B), a3.value(C)):
        second_allocation = Identical_EF1(u2_valuation, T)
        T1, T2, T3 = second_allocation[0], second_allocation[1], second_allocation[2]
        # print("T1, T2, T3", T1, T2, T3)
        a1_favorite_value = 0
        a3_favorite_value = 0
        alloc = {T1, T2, T3}
        while len(alloc) != 0 and len(alloc) != 1:
            # print("start:", alloc)
            pop = alloc.pop()
            if a3_favorite_value < a3.value(pop):
                alloc.add(a3_bundle)
                a3_bundle = pop
                a3_favorite_value = a3.value(a3_bundle)
            if a1_favorite_value < a1.value(pop):
                alloc.add(a1_bundle)
                a1_bundle = pop
                a1_favorite_value = a1.value(a1_bundle)
            # print("end:", alloc)
        a3_bundle += A_tag
        a2_bundle += B
        a1_bundle += C
    # print(A_tag, T, B, C)
    return 0


def Identical_EF1(valuation, items):
    """
    the function calculates EF1 allocation with same valuation for using
    in three_agents_AAV algorithm
    """
    a1 = fairpy.agents.AdditiveAgent(valuation, name="a1")
    a2 = fairpy.agents.AdditiveAgent(valuation, name="a2")
    a3 = fairpy.agents.AdditiveAgent(valuation, name="a3")
    allocation = three_agents_IAV([a1, a2, a3], items)
    return allocation


if __name__ == "__main__":
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
