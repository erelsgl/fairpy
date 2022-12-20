
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


def test_proportional_division_equal_number_of_items_and_players():
    check_if_it_throws_error_if_without_borda(f=proportional_division_equal_number_of_items_and_players)
    big_size = 100
    big_agents = AgentList([list(range(big_size)) for i in range(big_size)])
    tBig = proportional_division_equal_number_of_items_and_players(agents=big_agents) 
    assert tBig is None  # Validation is the same for all agents

    for i in range(1,50):
        agentsI = get_agents_with_permutations_of_valuations(i,i)
        allocationI = proportional_division_equal_number_of_items_and_players(agents=agentsI)
        assert allocationI is None or is_proportional(allocationI, agentsI.all_items())
  
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
    sizeA = 3
    agents3 = AgentList([list(range(sizeA)) for i in range(sizeA)])
    agents9 = AgentList([list(range(3*sizeA)) for i in range(sizeA)])
    
    # Check for cases where p is odd
    with pytest.raises(ValueError):
        proportional_division_with_p_even(agents=agents3)  # p == 1
 
    with pytest.raises(ValueError):
        proportional_division_with_p_even(agents=agents9)  # p == 3

def test_proportional_division_with_number_of_agents_odd():
    sizeA = 2
    agentsA = AgentList([list(range(2*sizeA)) for i in range(sizeA)])
    sizeB = 4
    agentsB = AgentList([list(range(3*sizeB)) for i in range(sizeB)])    
    
    # Check for cases where n is even
    with pytest.raises(ValueError):
        proportional_division_with_number_of_agents_odd(agents=agentsA) # n == 2
 
    with pytest.raises(ValueError):
        proportional_division_with_number_of_agents_odd(agents=agentsB) # n == 4

def test_general():
    for func in [proportional_division_with_p_even, proportional_division_with_number_of_agents_odd, proportional_division]:
        check_if_it_throws_error_if_without_borda(f=func)
        check_if_throws_error_when_k_is_not_multiple_of_n(f=func)
    # big_size = 100
    big_size = 50
    for n in chain(range(1, 20)):
        for p in chain(range(2,15), [big_size, big_size+1]):
            agentsI = get_agents_with_permutations_of_valuations(n, n*p)
            if isEven(p):
                allocationI = proportional_division_with_p_even(agents=agentsI)
                assert is_proportional(allocationI, agentsI.all_items())
            if not isEven(n):
                allocationI = proportional_division_with_number_of_agents_odd(agents=agentsI)
                assert is_proportional(allocationI, agentsI.all_items())
            allocationI = proportional_division(agents=agentsI)
            if isEven(n) and not isEven(p):
                assert is_proportional(allocationI, agentsI.all_items(), approximately=True)
            else:
                assert is_proportional(allocationI, agentsI.all_items())

#################    Helper function    #################
def get_agents_with_permutations_of_valuations(n,k):
    ans = []
    if n == 0 or k == 0:
        raise ValueError(f"n and k must be at least 0, but n={n}, k={k}")
    for i in permutations(range(k)):
        ans.append(list(i))
        if len(ans) == n:
            break
    return AgentList(ans)

def is_proportional(allocation:Allocation, items, approximately:bool=False):
    k = len(items)
    n = allocation.num_of_agents
    value_of_all_items = k*(k-1)/2
    threshold = value_of_all_items/n
    if approximately:
        threshold = int(threshold)
    for sum in allocation.utility_profile():
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

def check_if_it_throws_error_if_without_borda(f:Callable):
    agents_without_borda1, agents_without_borda2 = get_agents_without_borda()
    with pytest.raises(ValueError):
        f(agents=agents_without_borda1)
    with pytest.raises(ValueError):
        f(agents=agents_without_borda2)

def check_if_throws_error_when_k_is_not_multiple_of_n(f:Callable):
    size = 3
    with pytest.raises(ValueError):
        agents3 = get_agents_with_permutations_of_valuations(size, size*4+1)   # 13 % 3 != 0
        f(agents=agents3)