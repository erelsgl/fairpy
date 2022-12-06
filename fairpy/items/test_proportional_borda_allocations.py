from fairpy.items.proportional_borda_allocations import *
from fairpy import AgentList
import pytest
from itertools import permutations, combinations


# xx = proportional_division(agents=AgentList([[0,1,2,3,4,5,6,7,8,9],[0,1,2,3,4,5,6,7,8,9]]),items=[0,1,2,3,4,5,6,7,8,9]).map_agent_to_bundle()
# print(xx)
# print(proportional_division())

size_big = 1000
big_agents = AgentList([list(range(size_big)) for i in range(size_big)])
def get_matrix_permutations(n):
    ans = []
    for i in permutations(range(n)):
        ans.append(i)
        if len(ans) == n:
            break
    return ans

def is_proportional(alocation:Allocation,approximately:bool=False):
    n = len(alocation)
    value_of_all_items = n*(n-1)/2
    threshold = value_of_all_items/n
    if approximately:
        threshold = int(threshold)
    for sum in alocation.utility_profile():
        if sum < threshold:
            return False
    return True

def test_proportional_division_equal_number_of_items_and_players():
    items1000 = list(range(size_big))
    items2000 = list(range(2*size_big))
    items500 = list(range(size_big/2))
    t1000 = proportional_division_equal_number_of_items_and_players(agents=big_agents, items=items1000) 
    assert t1000 is None  # Validation is the same for all agents

    for i in range(50):
        agentsI = get_matrix_permutations(i)
        itemsI = list(range(i))
        ansI = proportional_division_equal_number_of_items_and_players(agents=agentsI, items=itemsI)
        assert ansI is None or is_proportional(ansI)


    with pytest.raises(ValueError):
        proportional_division_equal_number_of_items_and_players(agents=agents1000, items=items2000)
        proportional_division_equal_number_of_items_and_players(agents=agents1000, items=items500)
        proportional_division_equal_number_of_items_and_players(agents=agents1000, items=[0,1,2])

def test_proportional_division_with_p_even():
    size3 = 3
    agents3 = AgentList([list(range(size3)) for i in range(size3)])
    items9 = list(range(3*size3))
    items3 = list(range(size3))

    # check if 2<=p even
    with pytest.raises(ValueError):
        proportional_division_with_p_even(agents=agents3, items=items3)
        proportional_division_with_p_even(agents=agents3, items=items9)

    for i in range(50):
        agentsI = get_matrix_permutations(i)
        for j in range(2,9,2):
            itemsI = list(range(j*i))  # len(items)/i in (2,4,6,8) and is even
            ansI = proportional_division_with_p_even(agents=agentsI, items=itemsI)
            assert is_proportional(ansI)

    ans_big = proportional_division_equal_number_of_items_and_players(agents=big_agents, items=list(range(2*size_big)))
    assert is_proportional(ans_big)


 



def test_raise():
    with pytest.raises(TypeError):
        proportional_division('fdsf','ffdsd')



if __name__ == "__main__":

    # agents = get_matrix_permutations(100)
    # agents = get_matrix_permutations(3)
    # check_proportional(agents)
    # print(len(agents))
    # print(int((3+6)/2))