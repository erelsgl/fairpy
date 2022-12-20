
#!python3
"""
Tests to proportional_borda_allocations

Programmer: Shlomo Glick
Since:  2022-12
"""


from fairpy.items.proportional_borda_allocations import *
from fairpy import AgentList
import pytest
from itertools import permutations
from typing import Callable
from itertools import chain





def get_agents_with_permutations_of_valuations(n,k):
    ans = []
    for i in permutations(range(k)):
        ans.append(list(i))
        if len(ans) == n:
            break
    return AgentList(ans)

def is_proportional(alocation:Allocation, items, approximately:bool=False):
    k = len(items)
    n = alocation.num_of_agents
    value_of_all_items = k*(k-1)/2
    threshold = value_of_all_items/n
    if approximately:
        threshold = int(threshold)
    for sum in alocation.utility_profile():
        if sum < threshold:
            return False
    return True

def get_agents_without_borda():
    return AgentList({
        "Shlomo": {"itemA": 0, "itemB": 0, "itemC": 2}, 
        "Shira": {"itemA": 0, "itemB": 2, "itemC": 0}, 
        "Hadar": {"itemA": 2, "itemB": 0, "itemC": 0}
    }), AgentList({
        "Shlomo": {"itemA": 256, "itemB": 32, "itemC": 0}, 
        "Shira": {"itemA": 1, "itemB": 2, "itemC": 0}, 
        "Hadar": {"itemA": 2, "itemB": 1, "itemC": 0}
    })

def check_if_it_throws__error_if_without_borda(f:Callable):
    agents_without_borda1, agents_without_borda2 = get_agents_without_borda()
    with pytest.raises(ValueError):
        f(agents=agents_without_borda1)
    with pytest.raises(ValueError):
        f(agents=agents_without_borda2)

def test_proportional_division_equal_number_of_items_and_players():
    check_if_it_throws__error_if_without_borda(f=proportional_division_equal_number_of_items_and_players)
    size_big = 100
    big_agents = AgentList([list(range(size_big)) for i in range(size_big)])
    tBig = proportional_division_equal_number_of_items_and_players(agents=big_agents) 
    assert tBig is None  # Validation is the same for all agents

    for i in range(1,50):
        agentsI = get_agents_with_permutations_of_valuations(i,i)
        ansI = proportional_division_equal_number_of_items_and_players(agents=agentsI)
        assert ansI is None or is_proportional(ansI, agentsI.all_items())
  
    for i in range(1,50):
        agentsI = get_agents_with_permutations_of_valuations(i,i+1) # len(agents) != len(items)) 
        with pytest.raises(ValueError):
            proportional_division_equal_number_of_items_and_players(agents=agentsI)  
    
    agents = AgentList(
        {
            "Shlomo": {"itemA": 0, "itemB": 1, "itemC": 2}, 
            "Shira": {"itemA": 0, "itemB": 2, "itemC": 1}, 
            "Hadar": {"itemA": 2, "itemB": 0, "itemC": 1}
        })
    ans = proportional_division_equal_number_of_items_and_players(agents=agents)
    assert is_proportional(ans, agents.all_items())


def test_proportional_division_with_p_even():
    check_if_it_throws__error_if_without_borda(f=proportional_division_with_p_even)

    size3 = 3
    agents3 = AgentList([list(range(size3)) for i in range(size3)])
    agents9 = AgentList([list(range(3*size3)) for i in range(size3)])
    
    # Check for cases where p is odd
    with pytest.raises(ValueError):
        proportional_division_with_p_even(agents=agents3)  # p == 1
 
    with pytest.raises(ValueError):
        proportional_division_with_p_even(agents=agents9)  # p == 3

    size_big = 100
    for i in chain(range(50), [size_big]):
        for j in range(2,9,2):
            agentsI = get_agents_with_permutations_of_valuations(i,j*i)
            ansI = proportional_division_with_p_even(agents=agentsI)
            assert is_proportional(ansI, agentsI.all_items())


# def test_proportional_division_with_number_of_agents_odd():
#     size = 3
#     agents3 = AgentList([list(range(size)) for i in range(size)])

#     # if k/n=p not integer resies error
#     with pytest.raises(ValueError):
#         proportional_division_with_number_of_agents_odd(agents=agents3)

#     for i in range(1,50,2): # i odd
#         agentsI = get_agents_with_permutations_of_valuations(i))
#         for j in range(10):
#             itemsI = list(range(j*i))  # len(items)/i is integer
#             ansI = proportional_division_with_number_of_agents_odd(agents=agentsI)
#             assert is_proportional(ansI, agentsI.all_items())

#     ans_big = proportional_division_with_number_of_agents_odd(agents=big_agents)
#     assert is_proportional(ans_big, big_agents.all_items())

# def test_proportional_division():
    # size = 4
    # agents4 = AgentList([list(range(size)) for i in range(size)])

    # # if k/n=p not integer resies error
    # with pytest.raises(ValueError):
    #     proportional_division_with_number_of_agents_odd(agents=agents4)

    # for n in range(0,50,2): # n even
    #     agentsI = get_agents_with_permutations_of_valuations(n))
    #     for j in range(1,10,2):
    #         ansI = proportional_division_with_number_of_agents_odd(agents=agentsI)
    #         assert is_proportional(ansI, agentsI.all_items())


