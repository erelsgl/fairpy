"""
All these algorithms are based on the paper: Two-player fair division of indivisible items: Comparison of algorithms
By: D. Marc Kilgour, Rudolf Vetschera

programmers: Itay Hasidi & Amichai Bitan
"""
import logging
from fairpy import AgentList, AdditiveAgent
from fairpy.items.two_players_fair_division_utils import *
from typing import Dict, Any, List

# from two_players_fair_division_utils import *
# from fairpy import fairpy
# from fairpy.agentlist import AgentList


# logging.basicConfig(level=loggining.DEBUG)

logger = logging.getLogger(__name__)


def sequential(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a OS. The algorithm returns envy-free allocations if they exist, does not return max-min allocation and returns
    one Pareto optimality allocation.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1 :
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> sequential([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [{'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}, {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}]

    # test 2:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> sequential([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [{'Alice': ['computer', 'tv'], 'George': ['phone', 'book']}, {'Alice': ['computer', 'book'], 'George': ['phone', 'tv']}, {'Alice': ['tv', 'phone'], 'George': ['computer', 'book']}, {'Alice': ['tv', 'book'], 'George': ['computer', 'phone']}, {'Alice': ['tv', 'computer'], 'George': ['phone', 'book']}, {'Alice': ['tv', 'book'], 'George': ['phone', 'computer']}]

    # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'c': 1, 'a': 2, 'd': 3, 'b': 4, 'f': 5, 'e': 6}, name = 'George')
    >>> sequential([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    [{'Alice': ['a', 'b', 'e'], 'George': ['c', 'd', 'f']}]

    # test 4:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 1, 'b': 3, 'c': 4, 'd': 2, 'e': 6, 'f': 5}, name = 'George')
    >>> sequential([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    [{'Alice': ['a', 'c', 'e'], 'George': ['d', 'b', 'f']}, {'Alice': ['b', 'c', 'e'], 'George': ['a', 'd', 'f']}, {'Alice': ['b', 'c', 'e'], 'George': ['d', 'a', 'f']}]

    # test 5: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> sequential([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    [{'Alice': ['a', 'b', 'd', 'f'], 'George': ['g', 'h', 'c', 'e']}, {'Alice': ['a', 'b', 'e', 'f'], 'George': ['g', 'h', 'c', 'd']}]

    # test 6: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> sequential([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h','i' , 'j'])
    [{'Alice': ['a', 'b', 'd', 'f', 'h'], 'George': ['i', 'j', 'c', 'e', 'g']}, {'Alice': ['a', 'b', 'd', 'g', 'h'], 'George': ['i', 'j', 'c', 'e', 'f']}, {'Alice': ['a', 'b', 'e', 'f', 'h'], 'George': ['i', 'j', 'c', 'd', 'g']}]

    """

    return recursive_sequential(agents, items, allocations=[[], []], end_allocation=[])


def recursive_sequential(agents: AgentList, items: List[Any], allocations: List[Any] = [[], []],
                     end_allocation=[], level: int = 1):
    """
    A recursive helper function to sequential()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far.
    :param end_allocation is the end allocation for each player.
    :param level is the depth level for item searching for each iteration.
    """
    logger.info("\nAlgorithm: OS\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    if not items:
        end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
        return end_allocation
    H_A_level, H_B_level = H_M_l(agents, items, level)
    logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(),
                allocations[0])
    if H_A_level and H_B_level and have_different_elements(H_A_level, H_B_level):
        for i in H_A_level:
            for j in H_B_level:
                if i != j:
                    _allocations = deep_copy_2d_list(allocations)
                    _items, _allocations = allocate(items.copy(), _allocations, i, j)
                    recursive_sequential(agents, _items, _allocations, end_allocation, level + 1)
    else:
        recursive_sequential(agents, items, allocations, end_allocation, level + 1)
    return end_allocation


def restricted_simple(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a RS. The algorithm does not return envy-free allocations, does not return max-min allocations and does not
    return one Pareto optimality allocations.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test1:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> restricted_simple([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [{'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}, {'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}]

    # test 2:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> restricted_simple([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [{'Alice': ['tv', 'book'], 'George': ['computer', 'phone']}, {'Alice': ['tv', 'phone'], 'George': ['computer', 'book']}, {'Alice': ['computer', 'book'], 'George': ['phone', 'tv']}, {'Alice': ['computer', 'tv'], 'George': ['phone', 'book']}]

   # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'c': 1, 'a': 2, 'd': 3, 'b': 4, 'f': 5, 'e': 6}, name = 'George')
    >>> restricted_simple([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    [{'Alice': ['a', 'b', 'e'], 'George': ['c', 'd', 'f']}]

    # test 4:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 1, 'b': 3, 'c': 4, 'd': 2, 'e': 6, 'f': 5}, name = 'George')
    >>> restricted_simple([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    [{'Alice': ['b', 'c', 'e'], 'George': ['a', 'd', 'f']}, {'Alice': ['a', 'c', 'e'], 'George': ['d', 'b', 'f']}]

     # test 5: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> restricted_simple([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    [{'Alice': ['a', 'b', 'd', 'f'], 'George': ['g', 'h', 'c', 'e']}]

     # test 6: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 ,'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> restricted_simple([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h','i' , 'j'])
    [{'Alice': ['a', 'b', 'd', 'f', 'h'], 'George': ['i', 'j', 'c', 'e', 'g']}]

    """
    logger.debug("\nAlgorithm: RS\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    return recursive_restricted_simple(agents, items, allocations=[[], []], end_allocation=[])


def recursive_restricted_simple(agents: AgentList, items: List[Any], allocations: List[Any] = [[], []],
                                end_allocation=[], level: int = 1):
    """
    A recursive helper function to restricted_simple()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far.
    :param end_allocation is the end allocation for each player.
    :param level is the depth level for item searching for each iteration.
    """
    if not items:
        end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
        return end_allocation
    H_A_level, H_B_level = H_M_l(agents, items, level)
    logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(),
                allocations[0])
    if H_A_level and H_B_level and have_different_elements(H_A_level, H_B_level):
        if H_A_level[0] != H_B_level[0]:
            _allocations = deep_copy_2d_list(allocations)
            _items, _allocations = allocate(items.copy(), _allocations, H_A_level[0], H_B_level[0])
            recursive_restricted_simple(agents, _items, _allocations, end_allocation=end_allocation, level=level + 1)
        else:
            if len(H_A_level) > 1:
                _allocations = deep_copy_2d_list(allocations)
                _items, _allocations = allocate(items.copy(), _allocations, H_A_level[1], H_B_level[0])
                recursive_restricted_simple(agents, _items, _allocations, end_allocation=end_allocation,
                                            level=level + 1)
            if len(H_B_level) > 1:
                _allocations = deep_copy_2d_list(allocations)
                _items, _allocations = allocate(items.copy(), _allocations, H_A_level[0], H_B_level[1])
                recursive_restricted_simple(agents, _items, _allocations, end_allocation=end_allocation,
                                            level=level + 1)
    else:
        recursive_restricted_simple(agents, items, allocations, end_allocation=end_allocation, level=level + 1)
    return end_allocation


def singles_doubles(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a SD. The algorithm returns envy-free allocations, returns max-min allocations and returns one Pareto
    optimality allocations.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> singles_doubles([Alice, George], ['computer', 'phone', 'tv', 'book'])
    []

    # test 2:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> singles_doubles([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    [{'Alice': ['e', 'a', 'd'], 'George': ['f', 'b', 'c']}, {'Alice': ['e', 'b', 'c'], 'George': ['f', 'a', 'd']}]

    # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> singles_doubles([Alice, George], ['a', 'b', 'c', 'd'])
    [{'Alice': ['a', 'd'], 'George': ['b', 'c']}, {'Alice': ['b', 'c'], 'George': ['a', 'd']}]

    # test 4: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> singles_doubles([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    []

    # test 6: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 ,'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> singles_doubles([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
    []
    """
    logger.debug("\nAlgorithm: SD\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    return singles_doubles_helper(agents, items, allocations=[[], []], end_allocation=[], do_single=True)


def singles_doubles_helper(agents: AgentList, items: List[Any] = None, allocations=[[], []], end_allocation=[],
                           do_single: bool = False) -> Dict:
    """
    A recursive helper function to singles_doubles()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far.
    :param end_allocation is the end allocation for each player.
    :param do_single is a boolean flag that indicates if the singles() algorithm should be used or not, in this function
     it will only be used the first time the function is called.
    """
    if do_single:
        A_items, B_items = get_valuation_list(agents, items)
        singles(A_items.copy(), B_items.copy(), items, allocations)
    if not items:
        if is_envy_free_partial_allocation(agents, allocations):
            end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
            return end_allocation
        return
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(items.copy(), _allocations, H_A_level[0], H_B_level[0])
        singles_doubles_helper(agents, _items, _allocations, end_allocation)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    singles_doubles_helper(agents, items_1, temp_allocation_1, end_allocation)
    singles_doubles_helper(agents, items_2, temp_allocation_2, end_allocation)
    logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(),
                allocations[0])
    return end_allocation


def iterated_singles_doubles(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a IS. The algorithm returns envy-free allocations, returns max-min allocations and returns one Pareto
    optimality allocations.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> iterated_singles_doubles([Alice, George], ['computer', 'phone', 'tv', 'book'])
    []

    # test 2:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> iterated_singles_doubles([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])


    # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> iterated_singles_doubles([Alice, George], ['a', 'b', 'c', 'd'])
    [{'Alice': ['a', 'd'], 'George': ['b', 'c']}, {'Alice': ['b', 'c'], 'George': ['a', 'd']}]

    # test 5: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> iterated_singles_doubles([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    []

    # test 6: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 ,'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> iterated_singles_doubles([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h','i' , 'j'])
    []
    """
    logger.debug("\nAlgorithm: IS\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    return iterated_singles_doubles_helper(agents, items, allocations=[[], []], end_allocation=[], do_single=True)


def iterated_singles_doubles_helper(agents: AgentList, items: List[Any] = None, allocations=[[], []], end_allocation=[],
                                    do_single: bool = False) -> Dict:
    """
    A recursive helper function to iterated_singles_doubles()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far.
    :param end_allocation is the end allocation for each player.
    :param do_single is a boolean flag that indicates if the singles() algorithm should be used or not, in this function
     it will only be used the first time the function is called as many times as possible.
    """
    if do_single:
        A_items, B_items = get_valuation_list(agents, items)
        flag = True
        while flag:
            flag, allocations = singles(A_items.copy(), B_items.copy(), items, allocations)
    if not items:
        if is_envy_free_partial_allocation(agents, allocations):
            end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
            return end_allocation
        return
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(items.copy(), _allocations, H_A_level[0], H_B_level[0])
        iterated_singles_doubles_helper(agents, _items, _allocations, end_allocation)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    iterated_singles_doubles_helper(agents, items_1, temp_allocation_1, end_allocation)
    iterated_singles_doubles_helper(agents, items_2, temp_allocation_2, end_allocation)
    logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(),
                allocations[0])
    return end_allocation


def s1(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    The algorithm returns envy-free allocations if they exist and returns max-min allocations.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> s1([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [{'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}, {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}]

    # test 2:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> s1([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    [{'Alice': ['e', 'a', 'c'], 'George': ['f', 'b', 'd']}, {'Alice': ['e', 'a', 'd'], 'George': ['f', 'b', 'c']}, {'Alice': ['e', 'b', 'c'], 'George': ['f', 'a', 'd']}, {'Alice': ['e', 'b', 'd'], 'George': ['f', 'a', 'c']}]

    # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> s1([Alice, George], ['a', 'b', 'c', 'd'])
    [{'Alice': ['a', 'c'], 'George': ['b', 'd']}, {'Alice': ['a', 'd'], 'George': ['b', 'c']}, {'Alice': ['b', 'c'], 'George': ['a', 'd']}, {'Alice': ['b', 'd'], 'George': ['a', 'c']}]

    # test 4: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> s1([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    [{'Alice': ['f', 'e', 'a', 'c'], 'George': ['h', 'g', 'b', 'd']}, {'Alice': ['f', 'e', 'a', 'd'], 'George': ['h', 'g', 'b', 'c']}, {'Alice': ['f', 'e', 'b', 'c'], 'George': ['h', 'g', 'a', 'd']}, {'Alice': ['f', 'e', 'b', 'd'], 'George': ['h', 'g', 'a', 'c']}]

    # test 5: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 ,'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> s1([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h','i' , 'j'])
    [{'Alice': ['h', 'g', 'a', 'c', 'e'], 'George': ['j', 'i', 'b', 'd', 'f']}, {'Alice': ['h', 'g', 'a', 'c', 'f'], 'George': ['j', 'i', 'b', 'd', 'e']}, {'Alice': ['h', 'g', 'a', 'd', 'e'], 'George': ['j', 'i', 'b', 'c', 'f']}, {'Alice': ['h', 'g', 'a', 'd', 'f'], 'George': ['j', 'i', 'b', 'c', 'e']}, {'Alice': ['h', 'g', 'b', 'c', 'e'], 'George': ['j', 'i', 'a', 'd', 'f']}, {'Alice': ['h', 'g', 'b', 'c', 'f'], 'George': ['j', 'i', 'a', 'd', 'e']}, {'Alice': ['h', 'g', 'b', 'd', 'e'], 'George': ['j', 'i', 'a', 'c', 'f']}, {'Alice': ['h', 'g', 'b', 'd', 'f'], 'George': ['j', 'i', 'a', 'c', 'e']}]
    """
    logger.debug("\nAlgorithm: S1\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    return s1_helper(agents, items, allocations=[[], []], end_allocation=[], do_single=True)


def s1_helper(agents: AgentList, items: List[Any] = None, allocations=[[], []], end_allocation=[],
              do_single: bool = False) -> Dict:
    """
    A recursive helper function to s1()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far.
    :param end_allocation is the end allocation for each player.
    :param do_single is a boolean flag that indicates if the singles() algorithm should be used or not, in this function
     it will only be used the first time the function is called.
    """
    if do_single:
        A_items, B_items = get_valuation_list(agents, items)
        singles(A_items.copy(), B_items.copy(), items, allocations)
    if not items:
        end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
        return end_allocation
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(items.copy(), _allocations, H_A_level[0], H_B_level[0])
        s1_helper(agents, _items, _allocations, end_allocation)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    s1_helper(agents, items_1, temp_allocation_1, end_allocation)
    s1_helper(agents, items_2, temp_allocation_2, end_allocation)
    logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(),
                allocations[0])
    return end_allocation


def l1(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    The algorithm returns envy-free allocations if they exist and returns max-min allocations.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> l1([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [{'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}, {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}]

    # test 2:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> l1([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    [{'Alice': ['e', 'b', 'a'], 'George': ['f', 'd', 'c']}]

    # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4}, name = 'George')
    >>> l1([Alice, George], ['a', 'b', 'c', 'd'])
    [{'Alice': ['a', 'c'], 'George': ['b', 'd']}, {'Alice': ['a', 'd'], 'George': ['b', 'c']}, {'Alice': ['b', 'c'], 'George': ['a', 'd']}, {'Alice': ['b', 'd'], 'George': ['a', 'c']}]

    # test 4: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> l1([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    [{'Alice': ['f', 'e', 'a', 'c'], 'George': ['h', 'g', 'b', 'd']}, {'Alice': ['f', 'e', 'a', 'd'], 'George': ['h', 'g', 'b', 'c']}, {'Alice': ['f', 'e', 'b', 'c'], 'George': ['h', 'g', 'a', 'd']}, {'Alice': ['f', 'e', 'b', 'd'], 'George': ['h', 'g', 'a', 'c']}]

    # test 5: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 ,'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> l1([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h','i' , 'j'])
    [{'Alice': ['h', 'g', 'a', 'c', 'e'], 'George': ['j', 'i', 'b', 'd', 'f']}, {'Alice': ['h', 'g', 'a', 'c', 'f'], 'George': ['j', 'i', 'b', 'd', 'e']}, {'Alice': ['h', 'g', 'a', 'd', 'e'], 'George': ['j', 'i', 'b', 'c', 'f']}, {'Alice': ['h', 'g', 'a', 'd', 'f'], 'George': ['j', 'i', 'b', 'c', 'e']}, {'Alice': ['h', 'g', 'b', 'c', 'e'], 'George': ['j', 'i', 'a', 'd', 'f']}, {'Alice': ['h', 'g', 'b', 'c', 'f'], 'George': ['j', 'i', 'a', 'd', 'e']}, {'Alice': ['h', 'g', 'b', 'd', 'e'], 'George': ['j', 'i', 'a', 'c', 'f']}, {'Alice': ['h', 'g', 'b', 'd', 'f'], 'George': ['j', 'i', 'a', 'c', 'e']}]
    """
    logger.debug("\nAlgorithm: L1\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    return l1_helper(agents, items, allocations=[[], []], end_allocation=[], do_single=True)


def l1_helper(agents: AgentList, items: List[Any] = None, allocations=[[], []], end_allocation=[],
              do_single: bool = False) -> Dict:
    """
     A recursive helper function to l1()

     :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
     player's name.
     :param items A list of all existing items (U).
     :param allocations is the allocation for each player so far.
     :param end_allocation is the end allocation for each player.
     :param do_single is a boolean flag that indicates if the singles() algorithm should be used or not,
     in this function it will only be used the first time the function is called as many times as possible.
     """
    if do_single:
        A_items, B_items = get_valuation_list(agents, items)
        flag = True
        while flag:
            flag, allocations = singles(A_items.copy(), B_items.copy(), items, allocations)
    if not items:
        end_allocation.append({agents[0].name(): allocations[0], agents[1].name(): allocations[1]})
        return end_allocation
    H_A_level, H_B_level = H_M_l(agents, items, len(agents[0].all_items()))
    if H_A_level[0] != H_B_level[0]:
        _allocations = deep_copy_2d_list(allocations)
        _items, _allocations = allocate(items.copy(), _allocations, H_A_level[0], H_B_level[0])
        s1_helper(agents, _items, _allocations, end_allocation)
    temp_allocation_1 = deep_copy_2d_list(allocations)
    temp_allocation_2 = deep_copy_2d_list(allocations)
    items_1, temp_allocation_1 = allocate(items.copy(), temp_allocation_1, H_A_level[0], H_B_level[1])
    items_2, temp_allocation_2 = allocate(items.copy(), temp_allocation_2, H_A_level[1], H_B_level[0])
    l1_helper(agents, items_1, temp_allocation_1, end_allocation)
    l1_helper(agents, items_2, temp_allocation_2, end_allocation)
    logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(),
                allocations[0])
    return end_allocation


def top_down(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a TD. The algorithm does not return envy-free allocations and returns max-min allocations.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> top_down([Alice, George], ['computer', 'phone', 'tv', 'book'])
    {'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}

    # test 2:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> top_down([Alice, George], ['computer', 'phone', 'tv', 'book'])
    {'Alice': ['computer', 'tv'], 'George': ['phone', 'book']}


    # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> top_down([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    {'Alice': ['a', 'b', 'e'], 'George': ['c', 'd', 'f']}

    # test 5: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> top_down([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    {'Alice': ['a', 'b', 'c', 'e'], 'George': ['g', 'h', 'd', 'f']}

    # test 6: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 ,'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> top_down([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h','i' , 'j'])
    {'Alice': ['a', 'b', 'c', 'e', 'g'], 'George': ['i', 'j', 'd', 'f', 'h']}
    """
    logger.debug("\nAlgorithm: TD\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    return top_down_helper(agents, items, allocations=[])


def top_down_helper(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None):
    """
    A helper function to top_down()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far.
    """
    length = int(len(items) / 2)
    allocations = [[], []]
    valuations = sorted_valuations(agents, items)
    for i in range(length):
        if valuations[0][0] in items:
            items, allocations = allocate(items, allocations, a_item=valuations[0][0], valuation_list=valuations)
        if valuations[1][0] in items:
            items, allocations = allocate(items, allocations, b_item=valuations[1][0], valuation_list=valuations)
        logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(),
                    allocations[0])
    end_allocation = {agents[0].name(): allocations[0], agents[1].name(): allocations[1]}
    return end_allocation


def top_down_alternating(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a TA. The algorithm does not return envy-free allocations and returns max-min allocations.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name. A-BB-AA...-B
    :param items A list of all existing items (U).

    # test 1:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> top_down_alternating([Alice, George], ['computer', 'phone', 'tv', 'book'])
    {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}

    # test 2:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> top_down_alternating([Alice, George], ['computer', 'phone', 'tv', 'book'])
    {'Alice': ['computer', 'book'], 'George': ['phone', 'tv']}

    # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> top_down_alternating([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    {'Alice': ['a', 'b', 'e'], 'George': ['c', 'd', 'f']}

      # test 5: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> top_down_alternating([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    {'Alice': ['a', 'b', 'c', 'f'], 'George': ['g', 'h', 'd', 'e']}

     # test 6: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 ,'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> top_down_alternating([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h','i' , 'j'])
    {'Alice': ['a', 'b', 'c', 'f', 'g'], 'George': ['i', 'j', 'd', 'e', 'h']}

    """
    logger.debug("\nAlgorithm: TA\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    return top_down_alternating_helper(agents, items, allocations=[])


def top_down_alternating_helper(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None):
    """
    A helper function to top_down_alternating()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far.
    """
    flag = True
    allocations = [[], []]
    valuations = sorted_valuations(agents, items)
    length = int(len(items) / 2)
    for _ in range(length):
        if flag:
            if valuations[0][0] in items:
                items, allocations = allocate(items, allocations, a_item=valuations[0][0], valuation_list=valuations)
            if valuations[1][0] in items:
                items, allocations = allocate(items, allocations, b_item=valuations[1][0], valuation_list=valuations)
            flag = False
        elif not flag:
            if valuations[1][0] in items:
                items, allocations = allocate(items, allocations, b_item=valuations[1][0], valuation_list=valuations)
            if valuations[0][0] in items:
                items, allocations = allocate(items, allocations, a_item=valuations[0][0], valuation_list=valuations)
            flag = True
        logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(),
                    allocations[0])

    end_allocation = {agents[0].name(): allocations[0], agents[1].name(): allocations[1]}
    return end_allocation


def bottom_up(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a BU. The algorithm does not return envy-free allocations and does not return max-min allocations.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> bottom_up([Alice, George], ['computer', 'phone', 'tv', 'book'])
    {'Alice': ['computer', 'phone'], 'George': ['book', 'tv']}

    # test 2:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> bottom_up([Alice, George], ['computer', 'phone', 'tv', 'book'])
    {'Alice': ['tv', 'computer'], 'George': ['book', 'phone']}

    # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> bottom_up([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    {'Alice': ['e', 'b', 'a'], 'George': ['f', 'd', 'c']}

    # test 5: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> bottom_up([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    {'Alice': ['f', 'e', 'c', 'a'], 'George': ['h', 'g', 'd', 'b']}

    # test 6: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 ,'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> bottom_up([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h','i' , 'j'])
    {'Alice': ['h', 'g', 'e', 'c', 'a'], 'George': ['j', 'i', 'f', 'd', 'b']}

    """
    logger.debug("\nAlgorithm: BU\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    return bottom_up_helper(agents, items, allocations=[])


def bottom_up_helper(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None):
    """
    A helper function to bottom_up()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far.
    """
    length = int(len(items) / 2)
    allocations = [[], []]
    valuations = sorted_valuations(agents, items)
    for i in range(length):
        if valuations[0][len(valuations[0]) - 1] in items:
            items, allocations = allocate(items, allocations, b_item=valuations[0][len(valuations[0]) - 1],
                                          valuation_list=valuations)
        if valuations[1][len(valuations[1]) - 1] in items:
            items, allocations = allocate(items, allocations, a_item=valuations[1][len(valuations[1]) - 1],
                                          valuation_list=valuations)
        logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(),
                    allocations[0])

    end_allocation = {agents[0].name(): allocations[0], agents[1].name(): allocations[1]}
    return end_allocation


def bottom_up_alternating(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a BA. The algorithm does not return envy-free allocations and does not return max-min allocations.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> bottom_up_alternating([Alice, George], ['computer', 'phone', 'tv', 'book'])
    {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}

    # test 2:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> bottom_up_alternating([Alice, George], ['computer', 'phone', 'tv', 'book'])
    {'Alice': ['tv', 'phone'], 'George': ['book', 'computer']}

    # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> bottom_up_alternating([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    {'Alice': ['e', 'b', 'a'], 'George': ['f', 'd', 'c']}

    # test 5: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> bottom_up_alternating([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    {'Alice': ['f', 'e', 'c', 'b'], 'George': ['h', 'g', 'd', 'a']}

    # test 6: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 ,'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> bottom_up_alternating([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h','i' , 'j'])
    {'Alice': ['h', 'g', 'e', 'd', 'a'], 'George': ['j', 'i', 'f', 'c', 'b']}
    """
    logger.debug("\nAlgorithm: BA\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    return bottom_up_alternating_helper(agents, items, allocations=[])


def bottom_up_alternating_helper(agents: AgentList, items: List[Any] = None, allocations: List[Any] = None):
    """
    A helper function to bottom_up_alternating()

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far.
    """
    flag = True
    allocations = [[], []]
    valuations = sorted_valuations(agents, items)
    length = int(len(items) / 2)
    for _ in range(length):
        if flag:
            if valuations[0][len(valuations[0]) - 1] in items:
                items, allocations = allocate(items, allocations, b_item=valuations[0][len(valuations[0]) - 1], valuation_list=valuations)
            if valuations[1][len(valuations[1]) - 1] in items:
                items, allocations = allocate(items, allocations, a_item=valuations[1][len(valuations[1]) - 1], valuation_list=valuations)
            flag = False
        elif not flag:
            if valuations[1][len(valuations[1]) - 1] in items:
                items, allocations = allocate(items, allocations, a_item=valuations[1][len(valuations[1]) - 1], valuation_list=valuations)
            if valuations[0][len(valuations[0]) - 1] in items:
                items, allocations = allocate(items, allocations, b_item=valuations[0][len(valuations[0]) - 1], valuation_list=valuations)
            flag = True
        logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(),
                    allocations[0])

    end_allocation = {agents[0].name(): allocations[0], agents[1].name(): allocations[1]}
    return end_allocation


def trump(agents: AgentList, items: List[Any] = None) -> Dict:
    """
    a.k.a TR. The algorithm returns envy-free allocations, does not return max-min allocations and returns one Pareto
    optimality allocations.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    # test 1:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> trump([Alice, George], ['computer', 'phone', 'tv', 'book'])
    {'Alice': ['computer', 'tv'], 'George': ['book', 'phone']}

    # test 2:
    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> trump([Alice, George], ['computer', 'phone', 'tv', 'book'])
    []

    # test 3:
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}, name = 'Alice')
    >>> George = AdditiveAgent({'a': 2, 'b': 4, 'c': 1, 'd': 3, 'e': 6, 'f': 5}, name = 'George')
    >>> trump([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f'])
    {'Alice': ['a', 'b', 'e'], 'George': ['c', 'd', 'f']}

    # test 5: 8 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 , 'h' : 8}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :1 , 'h' : 2}, name='George')
    >>> trump([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h'])
    {'Alice': ['a', 'c', 'e', 'f'], 'George': ['g', 'h', 'b', 'd']}

    # test 6: 10 items
    >>> Alice = AdditiveAgent({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6,'g' :7 ,'h' : 8, 'i' : 9 ,'j': 10}, name='Alice')
    >>> George = AdditiveAgent({'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7, 'f': 8,'g' :9 , 'h' : 10, 'i' : 1 ,'j': 2}, name='George')
    >>> trump([Alice, George], ['a', 'b', 'c', 'd', 'e', 'f','g','h','i' , 'j'])
    {'Alice': ['a', 'c', 'e', 'g', 'h'], 'George': ['i', 'j', 'b', 'd', 'f']}
    """
    logger.debug("\nAlgorithm: TR\nTwo Agents %s %s and items %s", agents[0].name(), agents[1].name(), items)
    i = 1
    allocations = [[], []]
    end_allocation = []
    length = len(items)
    while i < length:
        for m in range(len(agents)):
            hm = H_M_l(agents, items, i)
            # if not hm[0] and not hm[1]:
            if not hm[m]:
                return end_allocation
            if m == 0:
                item = find_last_item(agents[1], hm[0])
                allocate(items, allocations, a_item=item)
            if m == 1:
                item = find_last_item(agents[0], hm[1])
                allocate(items, allocations, b_item=item)
            logger.info("current allocations: \n%s: %s\n%s: %s", agents[0].name(), allocations[0], agents[1].name(), allocations[0])
        i += 2
    end_allocation = {agents[0].name(): allocations[0], agents[1].name(): allocations[1]}
    return end_allocation


# if __name__ == '__main__':
#     Alice = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name='Alice')
#     George = fairpy.agents.AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name='George')
#     sequential([Alice, George], ['computer', 'phone', 'tv', 'book'])