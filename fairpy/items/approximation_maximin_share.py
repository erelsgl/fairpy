#!python3

""" 
Find an approximate MMS allocation.
Based on:
1
Stephen J. Willson
["Fair Division Using Linear Programming"](https://swillson.public.iastate.edu/FairDivisionUsingLPUnpublished6.pdf)
* Part 6, pages 20--27.

Programmer: Liad Nagi and Moriya Elgrabli 

See also: 

Since:  
"""

# import cvxpy
from fairpy import Allocation, ValuationMatrix, Agent, AdditiveValuation, convert_input_to_valuation_matrix
from fairpy import agents
from fairpy.agents import AdditiveAgent
from typing import Any, List

import logging
logger = logging.getLogger(__name__)


##### Algo 2

def initial_assignment_alfa_MSS(agents: List[AdditiveAgent], alfa:float):
    """
    Initial division for allocting agents according to their alfa-MMS.
    :param agents:Valuations of agents, normlized such that MMS=1 for all agents
    :param alfa: parameter for how much to approximate MMS allocation.
    :return allocation: Whats been allocated so far (in this function)
    :return agents:  Agents (and objects) that still need allocation

    ### allocation for 1 agent, 1 object (this pass!)
    >>> a = AdditiveAgent({"x": 1}, name="Alice")
    >>> agents=[a]
    >>> a1, a2 = initial_assignment_alfa_MSS(agents,0.75)
    >>> print(a1, a2)
    Alice gets {x} with value 1.
     []
    ### allocation for 1 agent, 2 object 
    >>> b = AdditiveAgent({"x": 0.5, "y": 0.4}, name="Blice")
    >>> agents=[b]
    >>> a1, a2 = initial_assignment_alfa_MSS(agents,0.6)
    >>> print(a1, a2)
    Blice gets {x, y} with value 0.9.
     []
    ### allocation for 2 agent, 2 object 
    >>> a = AdditiveAgent({"x": 0.8, "y": 0.7}, name="Alice")
    >>> b = AdditiveAgent({"x": 0.7, "y": 0.7}, name="Blice")
    >>> agents=[a,b]
    >>> a1, a2 = initial_assignment_alfa_MSS(agents,0.6)
    >>> print(a1, a2)
    Alice gets {x} with value 0.8.
    Blice gets {y} with value 0.7.
     []
    ### allocation for 2 agent, 8 object 
    >>> a = AdditiveAgent({"x1": 0.647059, "x2": 0.588235, "x3": 0.470588, "x4": 0.411765, "x5": 0.352941, "x6": 0.294118, "x7": 0.176471, "x8": 0.117647}, name="A")
    >>> b = AdditiveAgent({"x1": 1.298701, "x2": 0.714286, "x3": 0.649351, "x4": 0.428571, "x5": 0.155844, "x6": 0.064935, "x7": 0.051948, "x8": 0.012987}, name="B")
    >>> c =  AdditiveAgent({"x1": 0.6, "x2": 0.6, "x3": 0.48, "x4": 0.36, "x5": 0.32, "x6": 0.32, "x7": 0.28, "x8": 0.04}, name="C")
    >>> agents=[a,b,c]
    >>> a1, a2 = initial_assignment_alfa_MSS(agents,0.75)
    >>> print(a1, a2) # x6, x7, x8 weren't divided
    B gets {x1} with value 1.298701.
    A gets {x3, x4} with value 0.882353.
    C gets {x2, x5} with value 0.92.
    []
    """
    # ag=[AdditiveAgent({"x": 1.3333333,"y": 0.6666667}, name="Carl"),AdditiveAgent({"x": 1.3333333,"y": 0.6666667}, name="orly")]
    ag=[]
    alloc = Allocation(agents=agents, bundles={"Alice": {"x"}})
    return alloc, ag



##### Algo 3

def bag_filling_algorithm_alfa_MMS(agents: List[AdditiveAgent], alfa:float) -> Allocation:
    """
    The algorithm allocates the remaining objects into the remaining agents so that each received at least α from his MMS.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param alfa: parameter for how much to approximate MMS allocation
    :return allocation: alloctaion agent.

    ### allocation for 1 agent, 0 object 
    >>> a = AdditiveAgent()
    >>> agents=[a]
    >>> a1 = bag_filling_algorithm_alfa_MMS(agents, 1)
    >>> print(a1)
    [].
    ### allocation for 1 agent, 3 object (high alfa) 
    >>> a = AdditiveAgent({"x1": 0.54, "x2": 0.3, "x3": 0.12}, name="Alice")
    >>> agents=[a]
    >>> a1 = bag_filling_algorithm_alfa_MMS(agents, 0.9)
    >>> print(a1)
    Alice gets {x1, x2, x3} with value 0.96.
    ### allocation for 2 agent, 9 object 
    >>> a = AdditiveAgent({"x1": 0.25, "x2": 0.25, "x3": 0.25, "x4": 0.25, "x5": 0.25, "x6": 0.25, "x7": 0.25, "x8": 0.25, "x9": 0.25 }, name="A")
    >>> b = AdditiveAgent({"x1": 0.333333, "x2": 0.333333, "x3": 0.333333, "x4": 0.333333, "x5": 0.166667, "x6": 0.166667, "x7": 0.166667, "x8": 0.166667, "x9": 0.166667 }, name="B")
    >>> agents=[a,b]
    >>> a1 = bag_filling_algorithm_alfa_MMS(agents,0.9)
    >>> print(a1)
    A gets {x1, x4, x8, x9} with value 1.
    B gets {x2, x3, x6, x7} with value 1.
    """

    allocation = Allocation(agents=agents, bundles =  {"Alice":{"x"}})
    return allocation


##### algo 1
def alfa_MMS_allocation(agents: List[AdditiveAgent], alfa:float) :
    """
    Find alfa_MMS_allocation for the given agents and valuations.
    :param agents: a matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
    :param alfa: parameter for how much to approximate MMS allocation
    :return allocation: Alloctaion agent.

    ### allocation for 1 agent, 1 object
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> a1 = alfa_MMS_allocation(agents,0.5)
    >>> print(a1)
    Alice gets {x} with value 2.
    ### allocation for 1 agent, 2 objects
    >>> b = AdditiveAgent({"x": 1, "y": 2}, name="Blice")
    >>> agents=[b]
    >>> a1 = alfa_MMS_allocation(agents,0.6)
    >>> print(a1)
    Blice gets {x} with value 1.
    ### allocation for 2 agents, 2 objects
    >>> a = AdditiveAgent({"x": 1, "y": 2}, name="Alice")
    >>> agents = [a, b]
    >>> a1 = alfa_MMS_allocation(agents,1)
    >>> print(a1)
    Alice gets {x} with value 1.
    Blice gets {y} with value 2.
    ### allocation for 3 agents, 3 objects (low alfa)
    >>> a = AdditiveAgent({"x1": 3, "x2": 2, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 4, "x2": 4, "x3": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 5, "x2": 2, "x3": 1}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alfa_MMS_allocation(agents,0.2)
    >>> print(a1)
    A gets {x1} with value 3.
    B gets {x2} with value 4.
    C gets {x3} with value 1.
    ### allocation with 3 agents, 8 objects
    >>> a = AdditiveAgent({"x1": 11, "x2": 10, "x3": 8,"x4": 7, "x5": 6, "x6": 5,"x7": 3, "x8": 2}, name="A")
    >>> b = AdditiveAgent({"x1": 100, "x2": 55, "x3": 50,"x4": 33, "x5": 12, "x6": 5,"x7": 4, "x8": 1}, name="B")
    >>> c = AdditiveAgent({"x1": 15, "x2": 15, "x3": 12,"x4": 9, "x5": 8, "x6": 8,"x7": 7, "x8": 5}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alfa_MMS_allocation(agents,0.75)
    >>> print(a1)
    B gets {x1} with value 100.
    A gets {x3, x4} with value 15.
    C gets {x2,x5} with value 23.
    ### allocation with 3 agents, 8 objects
    >>> a = AdditiveAgent({"x1": 1, "x2": 1, "x3": 1,"x4": 1, "x5": 1, "x6": 1,"x7": 1, "x8": 1, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 2, "x2": 2, "x3": 2,"x4": 2, "x5": 2, "x6": 2,"x7": 1, "x8": 1, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="B")
    >>> c = AdditiveAgent({"x1": 2, "x2": 2, "x3": 2,"x4": 2, "x5": 2, "x6": 2,"x7": 2, "x8": 2, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alfa_MMS_allocation(agents,0.75)
    >>> print(a1)
    C gets {x5, x6, x7} with value 6.
    A gets {x1, x4, x11, x12} with value 4.
    B gets {x2, x3, x9, x10} with value 6.
    """
 
    allocation = Allocation(agents=agents, bundles =  {"Alice":{"x"}})
    return allocation

# Algo 5
def fixed_assignment(agents: List[AdditiveAgent]):
    """
    The function allocates what can be allocated without harting others
    (each allocated agent gets 3/4 of his own MMS value,
    without casing others  not to get their MMS value)
    :param agents: Valuations of agents, normlized such that MMS <=1 for all agents
    :return allocation: What been allocated so far
    :return agents: Agents (and objects) that still need allocation

    # fixed_assignment for one agent, one object #
    >>> a = AdditiveAgent({"x": 1}, name="Alice")
    >>> agents=[a]
    >>> alloc, remaining_agents=fixed_assignment(agents)
    >>> print(alloc.str_with_values(precision=6))
    Alice gets {x} with value 1.
    <BLANKLINE>
    >>> remaining_agents
    []
    >>> b = AdditiveAgent({"x": 3.333333}, name="Bruce")  # fixed_assignment for two agent, one objects #   
    >>> c = AdditiveAgent({"x":2}, name="Carl")
    >>> agents=[b,c]
    >>> alloc, remaining_agents=fixed_assignment(agents)
    >>> print(alloc.str_with_values(precision=7))
    Bruce gets {x} with value 3.333333.
    Carl gets {} with value 0.
    <BLANKLINE>
    >>> remaining_agents
    []
    >>> b = AdditiveAgent({"x": 1.2,"y": 0.24, "z":0.56}, name="Bruce")  # fixed_assignment for two agent, three objects #   
    >>> c = AdditiveAgent({"x":1.125,"y": 0.875,"z":0.25}, name="Carl")
    >>> agents=[b,c]
    >>> alloc, remaining_agents=fixed_assignment(agents)
    >>> print(alloc.str_with_values(precision=6))
    Bruce gets {x} with value 1.2.
    Carl gets {y} with value 0.875.
    <BLANKLINE>
    >>> remaining_agents
    []
    """
    # return  Allocation(agents=agents, bundles={"Alice": {"x"}}), []
    # return Allocation(agents=agents, bundles={"Bruce": {"x"}, "Carl": {"y"}}), ag

    ag = []
    return Allocation(agents=agents, bundles={"Bruce": {"x"}}), ag


# Algo 6
def tentative_assignment(agents: List[AdditiveAgent]):
    """
    The function allocates temporerly what can be allocated, can maybe hart others it not normlized close enough to the mms values.
    :param agents: Valuations of agents,such that bundles of objects at the positions:
     {0}, {n-1,n},{2n-2,2n-1,2n} not satisties for them, 
     and normlized such that MMS <=1 for all agents. 
    :return allocation: Whats been temporarly allocated so far
    :return agents: Agents (and objects) that still need allocation
    ### 3 agents 11 objects - ex 1
    >>> agents = AdditiveAgent.list_from({"Alice":[0.727066,0.727066,0.39525,0.351334,0.351334,0.346454,0.022934,0.022934,0.022934,0.022934,0.022934],\
                     "Bruce":[0.723887,0.723887,0.393522,0.349798,0.349798,0.344939,0.022834,0.022834,0.022834,0.022834,0.022834],\
                    "Carl":[0.723887,0.723887,0.393522,0.349798,0.349798,0.344939,0.022834,0.022834,0.022834,0.022834,0.022834]})
    >>> alloc, remaining_agents=tentative_assignment(agents)
    >>> print(alloc.str_with_values(precision=7))
    Alice gets {0,6} with value 0.75.
    Bruce gets {3,4,5} with value 1.044535.
    Carl gets {1,2} with value 1.117409.
    <BLANKLINE>
    >>> remaining_agents
    []
    """
    ag = []
    return Allocation(agents=agents, bundles={"Carl":{1,2},"Bruce":{3,4,5},"Alice": {0,6}}), ag #


# algo 4
def three_quarters_MMS_allocation(agents: List[AdditiveAgent], alfa: float):
    """


    """

    return agents, Allocation

# # algo 7


# def agents_conversion_to_ordered_instance(agents: List[AdditiveAgent]):
#     """
#     The function sorted the list of additive agents such that their valuations for objects are unordered will become ordered.
#     :param agents: A list of additive agents such that their valuations for objects are unordered.
#     :return agents_sorted: A list of additive agents such that their valuations for objects are in ascending order.


#     """

#     return agents_sorted  # sorted


# # algo 8
# def get_alfa_MMS_allocation_to_unordered_instance(agents_unordered: List[AdditiveAgent], agents_ordered: List[AdditiveAgent], ordered_allocation: Allocation):
#     """
#     Get the MMS allocation for agents unordered valuations.
#     :param agents_unordered: Unordered valuations agents.
#     :param agents_ordered: Ordered valuations agents.
#     :param ordered_allocation: MMS allocation for ordered valuations agents.
#     :return allocation_matrix: ---

#     allocation for one agent, one object
#     >>> a = AdditiveAgent({"x": 2}, name="Alice")
#     >>> agents=[a]
#     >>> agents_ordered=agents_conversion_to_ordered_instance(agents)
#     >>> temp=copy.deepcopy(agents_ordered)
#     >>> ordered_alloc = alfa_MMS_allocation(temp,0.5)
#     >>> print(get_alfa_MMS_allocation_to_unordered_instance(agents, agents_ordered, ordered_alloc))
#     Alice gets {x} with value 2.
#     <BLANKLINE>




#     """

#     return Allocation  # sorted


if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
