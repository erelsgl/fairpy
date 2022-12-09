#!python3

"""
Represents a fraction allocation of a indivisible items among agents ---  the output of an item-allocation algorithm.
Used mainly for display purposes.

Programmer: Tom Latinn
Since: 2021-02
"""

from typing import *
from fairpy.agents import AdditiveAgent, Bundle


'''
A class that represents a fractional allocation, that is, an allocation in which several agents can be given parts of 
the same object.
'''
class FractionalAllocation:
    """
       >>> agent1 = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="agent1")
       >>> agent2 = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="agent2")
       >>> A = FractionalAllocation([agent1, agent2], [{'x':0.5, 'y':0.5, 'z':0.5},{'x':0.5, 'y':0.5, 'z':0.5}])
       >>> print(A)
       agent1's bundle: {x,y,z},  value: 3.0
       agent2's bundle: {x,y,z},  value: 3.0
       <BLANKLINE>
       >>> A.value_of_fractional_allocation()
       6.0
       >>> agent3 = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="agent3")
       >>> agent4 = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="agent4")
       >>> B = FractionalAllocation([agent3, agent4], [{'x':0.4, 'y':0, 'z':0.5},{'x':0.6, 'y':1, 'z':0.5}])
       >>> print(B)
       agent3's bundle: {x,z},  value: 1.9
       agent4's bundle: {x,y,z},  value: 4.3
       <BLANKLINE>
       >>> round(B.value_of_fractional_allocation(), 2)
       6.2
       >>> agent3 = AdditiveAgent({'x':1, 'y':-2, 'z':3}, name="agent3")
       >>> agent4 = AdditiveAgent({'x':3, 'y':2, 'z':-1}, name="agent4")
       >>> C = FractionalAllocation([agent3, agent4], [{'x':0.4, 'y':0, 'z':0.5},{'x':0.6, 'y':1, 'z':0.5}])
       >>> print(C)
       agent3's bundle: {x,z},  value: 1.9
       agent4's bundle: {x,y,z},  value: 3.3
       <BLANKLINE>
       >>> round(C.value_of_fractional_allocation(), 2)
       5.2
       >>> agent5 = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="agent5")
       >>> agent6 = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="agent6")
       >>> FractionalAllocation([agent5, agent6], [{'x':0.4, 'y':0, 'z':0.5}]) # doctest: +IGNORE_EXCEPTION_DETAIL
       Traceback (most recent call last):
       Exception: The amount of agents differs from the dictionaries that represent how much each agent received from each item.
       <BLANKLINE>
       >>> agent7 = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="agent7")
       >>> agent8 = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="agent8")
       >>> FractionalAllocation([agent7, agent8], [{'x':0.4, 'y':0, 'z':0.5},{'x':0.4, 'y':0, 'z':0.1},{'x':0.2, 'y':1, 'z':0.4}]) # doctest: +IGNORE_EXCEPTION_DETAIL
       Traceback (most recent call last):
       Exception: The amount of agents differs from the dictionaries that represent how much each agent received from each item.
       <BLANKLINE>
       >>> agent9 = AdditiveAgent({'x':1, 'y':2, 'z':3}, name="agent9")
       >>> agent10 = AdditiveAgent({'x':3, 'y':2, 'z':1}, name="agent10")
       >>> FractionalAllocation([agent9, agent10], [{'x':0, 'y':0, 'z':0.5},{'x':0.6, 'y':1, 'z':5}]) # doctest: +IGNORE_EXCEPTION_DETAIL
       Traceback (most recent call last):
       Exception: The values of the fractional allocation of items are not between 0 and 1
       <BLANKLINE>
    """

    # constructor
    def __init__(self, agents: List[AdditiveAgent], map_item_to_fraction: List[dict]):
        if len(agents) != len(map_item_to_fraction):
            raise Exception("The amount of agents differs from the dictionaries that represent how much each agent received from each item.")
        elif check_input(map_item_to_fraction):
            self.agents = agents
            self.map_item_to_fraction = map_item_to_fraction

    # A method that calculates the value of the whole allocation. Returns float number.
    def value_of_fractional_allocation(self) -> float:
        result = 0
        for i_agent, agent in enumerate(self.agents):
                agent_value = get_value_of_agent_in_alloc(self.agents[i_agent].valuation.map_good_to_value, self.map_item_to_fraction[i_agent])
                result += agent_value
        return result

    # A method that tests whether the allocation is complete (since all fractions are 0.0 or 1.0)
    def is_complete_allocation(self) -> bool:
        for d in self.map_item_to_fraction:
            for val in d.values():
                if val != 0.0 and val != 1.0:
                    return False
        return True

    # to string
    def __repr__(self):
        if self.agents is None and self.map_item_to_fraction is None:
            return ""
        else:
            result = ""
            for i_agent, agent in enumerate(self.agents):
                agent_bundle = stringify_bundle(get_items_of_agent_in_alloc(self.map_item_to_fraction[i_agent]))
                agent_value = get_value_of_agent_in_alloc(self.agents[i_agent].valuation.map_good_to_value, self.map_item_to_fraction[i_agent])
                result += "{}'s bundle: {},  value: {}\n".format(agent.name(),  agent_bundle, agent_value)
            return result


# -------------------------Help functions for the Fractional Allocation class--------------------------------------------
"""
The function checks the input value of the allocation.
That is, it checks:
1. All values of all items are between 0 and 1
2. There is no item whose sum of values is greater than 1
3. There is no item that has not been assigned to any agent, i.e. for each agent in the same item the value is 0
"""
def check_input(map_item_to_fraction: List[dict]) -> bool:
    """
    ### Examples of proper input
    >>> check_input([{'x':0.5, 'y':0.5, 'z':0.5},{'x':0.5, 'y':0.5, 'z':0.5}])
    True
    >>> check_input([{'x':0.4, 'y':0, 'z':0.5},{'x':0.6, 'y':1, 'z':0.5}])
    True

    ### Checks for values that are not in the range of 0 to 1
    >>> check_input([{'x':0.5, 'y':0.5, 'z':1.9},{'x':0.5, 'y':0.5, 'z':0.5}]) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    Exception: The values of the fractional allocation of items are not between 0 and 1

    >>> check_input([{'x':0.5, 'y':0.5, 'z':1},{'x':0.5, 'y':0.5, 'z':-0.1}]) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    Exception: The values of the fractional allocation of items are not between 0 and 1

    ### Checks for items whose sum of parts is greater than 1
    >>> check_input([{'x':0.7, 'y':0.5, 'z':0.5},{'x':0.9, 'y':0.5, 'z':0.5}]) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    Exception: There is an item whose sum of parts is greater than 1


    ### Checks for items that has not been assigned to any agent
    >>> check_input([{'x':0, 'y':0.5, 'z':0.5},{'x':0, 'y':0.5, 'z':0.5}]) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    Exception: There is an item that has not been assigned to any agent
    """
    sum_value_list = [0] * len(map_item_to_fraction[0])  # Help array
    for i in range(len(map_item_to_fraction)):
        for v, j in zip(map_item_to_fraction[i].values(), range(len(sum_value_list))):
            sum_value_list[j] += v
            if v > 1 or v < 0:
                raise Exception("The values of the fractional allocation of items are not between 0 and 1")

    for k in range(len(sum_value_list)):
        if sum_value_list[k] > 1:
            raise Exception("There is an item whose sum of parts is greater than 1")
        if sum_value_list[k] == 0:
            raise Exception("There is an item that has not been assigned to any agent")
    return True

'''
The function checks which objects the agent received by receiving map_item_to_fraction and then checks whether the value 
of the part he received from that item is greater than 1 if so he will add it to list another list no, and finally return the list of items.
'''
def get_items_of_agent_in_alloc(map_item_to_fraction: dict) -> List:
    """
    >>> print(get_items_of_agent_in_alloc({'x':0.4, 'y':0, 'z':0.5}))
    ['x', 'z']
    """
    result = []
    for key, val in zip(map_item_to_fraction.keys(), map_item_to_fraction.values()):
        if val > 0:
            result.append(key)
    return result

'''
Calculate the value of all the fractions of the items that a particular agent received
'''
def get_value_of_agent_in_alloc(value_of_the_whole_items: dict, amount_of_the_items: dict) -> float:
    """
    >>> get_value_of_agent_in_alloc({'x':1, 'y':2, 'z':3},{'x':0.5, 'y':0.5, 'z':0.5})
    3.0
    >>> get_value_of_agent_in_alloc({'x':1, 'y':2, 'z':3, 'p':9},{'x':0.1, 'y':0.5, 'z':0.8, 'p':0.7})
    9.8
    """
    value = 0
    for v1, v2 in zip(value_of_the_whole_items.values(), amount_of_the_items.values()):
        value += v1*v2
    return value



def stringify_bundle(bundle: Bundle):
    """
    Convert a bundle where each item is a character to a compact string representation.
    For testing purposes only.

    >>> stringify_bundle({'x','y'})
    '{x,y}'
    >>> stringify_bundle({'y','x'})
    '{x,y}'
    """
    return "{" + ",".join(sorted(bundle)) + "}"
    # return ",".join(["".join(item) for item in bundle])


if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))







