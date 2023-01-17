"""
Utils file for two_player_fair_division.py

programmers: Itay Hasidi & Amichai Bitan
"""
from typing import List, Any, Dict
from fairpy import fairpy
from fairpy.agentlist import AgentList, AdditiveAgent


def find_last_item(agent, item_list):
    """
    Returns the last item a player wants in the given list.

    :param agent the agent for which the function checks the least valued item.
    :param item_list all the items that are being checked.

    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> find_last_item(Alice, ['computer', 'phone', 'tv', 'book'])
    'book'

    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> find_last_item(Alice, ['computer'])
    'computer'
    """
    max_score = -1
    max_item = ""
    for item in item_list:
        score = agent.value(item)
        if max_score < score:
            max_score = score
            max_item = item
    return max_item


def is_envy_free_partial_allocation(agents: AgentList, allocations: List[Any]):
    """
    Gets an allocation and determines if its envy free.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param allocations is the allocation for each player so far.

    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> is_envy_free_partial_allocation([Alice, George], [['computer', 'phone'], ['book', 'tv']])
    False

    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 3, 'tv': 2, 'book': 1}, name = 'George')
    >>> is_envy_free_partial_allocation([Alice, George], [['computer', 'phone'], ['book', 'tv']])
    True

    """
    A_A_sum = 0
    A_B_sum = 0
    B_A_sum = 0
    B_B_sum = 0
    for idx in range(len(allocations[0])):
        A_A_sum += agents[0].value(allocations[0][idx])
        A_B_sum += agents[0].value(allocations[1][idx])
        B_A_sum += agents[1].value(allocations[0][idx])
        B_B_sum += agents[1].value(allocations[1][idx])
    if A_A_sum <= A_B_sum and B_A_sum >= B_B_sum:
        return True
    return False


def deep_copy_2d_list(lst: list):
    """
    Deep copies a 2D list and returns it

    :param lst the list that is being deep copied.

    >>> deep_copy_2d_list([[1, 2, 3], [4, 5, 6]])
    [[1, 2, 3], [4, 5, 6]]
    """
    lst_copy = []
    for i in range(len(lst)):
        lst_temp = []
        for j in range(len(lst[0])):
            lst_temp.append(lst[i][j])
        lst_copy.append(lst_temp)
    return lst_copy


def allocate(items: List[Any], allocations: List[List] = [[], []], a_item=None, b_item=None, valuation_list=None):
    """
    Allocates the first item, to agent A and the second item to agent B.

    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far
    :param a_item the item that agent A gets
    :param b_item the item that agent B gets
    :param valuation_list a list with valuations for each agent, only used in BU BA TD TA algorithms

    >>> itm, alloc = allocate(items=['a', 'b', 'c', 'd'], allocations=[[], []], a_item='a', b_item='b')
    >>> itm
    ['c', 'd']
    >>> alloc
    [['a'], ['b']]

    >>> itm, alloc = allocate(items=['a', 'b', 'c', 'd'], allocations=[[], []], a_item='a')
    >>> itm
    ['b', 'c', 'd']
    >>> alloc
    [['a'], []]
    """
    if a_item:
        allocations[0].append(a_item)
        items.remove(a_item)
        if valuation_list:
            valuation_list[0].remove(a_item)
            valuation_list[1].remove(a_item)
    if b_item:
        allocations[1].append(b_item)
        items.remove(b_item)
        if valuation_list:
            valuation_list[0].remove(b_item)
            valuation_list[1].remove(b_item)
    return items, allocations


def H_M_l(agents: AgentList, items: List[Any] = None, level: int = 1):
    """
    Returns the items each player wants until level.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).
    :param level is the depth level for item searching for each iteration.

    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> H_M_l([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [['computer'], ['book']]
    >>> H_M_l([Alice, George], ['computer', 'phone', 'tv', 'book'], 2)
    [['computer', 'phone'], ['phone', 'book']]
    """
    desired_items = []
    for player in agents:
        player_items = []
        for item in player.all_items():
            if player.value(item) <= level and item in items:
                player_items.append(item)
        desired_items.append(player_items)
    return desired_items


def have_different_elements(items_A: List[Any], items_B: List[Any]):
    """
    Returns True if both lists different at at least one item.

    :param items_A the list of items of player A.
    :param items_B the list of items of player B.

    >>> have_different_elements(['a', 'b'], ['a', 'c'])
    True
    >>> have_different_elements(['a', 'b'], ['a', 'b'])
    True
    >>> have_different_elements(['a'], ['a'])
    False
    """
    if len(items_A) != len(items_B):
        return True
    for i in items_A:
        for j in items_B:
            if i != j:
                return True
    return False


def singles(A_items: List[Any], B_items: List[Any], items: List[Any], allocations: List[Any] = None):
    """
    Goes over both valuation list of the players and returns allocates all the singles to each player.
    Singles are object at the end of each lst that occur only in one player's list until a certain level.
    For instance: A = [1, 2, 3, 4], B = [1, 4, 3, 2] we see that 2 is single in B and 4 in A, but 3 is in both A and B
    so that means 3 is not a single.

    :param A_items A list that represent the items that player A wants.
    :param B_items A list that represent the items that player B wants.
    :param items A list of all existing items (U).
    :param allocations is the allocation for each player so far.

    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> items = ['computer', 'phone', 'tv', 'book']
    >>> A_items, B_items = get_valuation_list([Alice, George], items)
    >>> singles(A_items, B_items, items, [[], []])
    (True, [['computer'], ['book']])

    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 3, 'tv': 2, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> items = ['computer', 'phone', 'tv', 'book']
    >>> A_items, B_items = get_valuation_list([Alice, George], items)
    >>> singles(A_items, B_items, items, [[], []])
    (True, [['computer', 'tv'], ['book', 'phone']])

    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'George')
    >>> items = ['computer', 'phone', 'tv', 'book']
    >>> A_items, B_items = get_valuation_list([Alice, George], items)
    >>> singles(A_items, B_items, items, [[], []])
    (False, [[], []])
    """
    A_allocations = []
    B_allocations = []
    for i in range(len(allocations[0])):
        A_items.remove(allocations[0][i])
        A_items.remove(allocations[1][i])
        B_items.remove(allocations[0][i])
        B_items.remove(allocations[1][i])
    length = int(len(items))
    for i in range(length):
        # idx = len(A_items) - i
        if A_items[-1 - i] != B_items[-1 - i] and A_items[-1 - i] not in A_allocations and B_items[-1 - i] \
                not in B_allocations:
            A_allocations.append(B_items[-1 - i])
            B_allocations.append(A_items[-1 - i])
        else:
            break
    if not A_allocations and not B_allocations:
        return False, allocations
    for j in range(len(A_allocations)):
        if A_allocations[j] in items and B_allocations[j] in items:
            allocate(items, allocations, A_allocations[j], B_allocations[j])
    return True, allocations


def get_valuation_list(agents: AgentList, items: List[Any]):
    """
    Returns the valuation for each player sorted from most valubale item at index 0 and least valuable at last index.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> get_valuation_list([Alice, George], ['computer', 'phone', 'tv', 'book'])
    (['computer', 'phone', 'tv', 'book'], ['book', 'phone', 'tv', 'computer'])
    """
    A_items_Dict = {}
    B_items_Dict = {}
    A_items = []
    B_items = []
    for item in items:
        A_items_Dict[agents[0].value(item)] = item
        B_items_Dict[agents[1].value(item)] = item
    for i in range(1, len(agents[0].all_items()) + 1):
        if i in B_items_Dict:
            B_items.append(B_items_Dict[i])
        if i in A_items_Dict:
            A_items.append(A_items_Dict[i])
    return A_items, B_items


def sorted_valuations(agents: AgentList, items: List[Any]):
    """
    Returns the valuation of the agents in a sorted List format, where the first sub-list is the first agent,
    and the first item in a sub-list is the most valued item for that agent.

    :param agents A list that represent the players(agents) and for each player his valuation for each item, plus the
    player's name.
    :param items A list of all existing items (U).

    >>> Alice = AdditiveAgent({'computer': 1, 'phone': 2, 'tv': 3, 'book': 4}, name = 'Alice')
    >>> George = AdditiveAgent({'computer': 4, 'phone': 2, 'tv': 3, 'book': 1}, name = 'George')
    >>> sorted_valuations([Alice, George], ['computer', 'phone', 'tv', 'book'])
    [['computer', 'phone', 'tv', 'book'], ['book', 'phone', 'tv', 'computer']]
    """
    sorted_lst = [[], []]
    for agent in range(len(agents)):
        for i in range(1, len(items) + 1):
            for item in items:
                if agents[agent].value(item) == i:
                    sorted_lst[agent].append(item)
                    break
    return sorted_lst
