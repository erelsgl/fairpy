#!python3

"""
Find an approximate MMS allocation.
Based on:

Jugal Garg and Setareh Taki
["An Improved Approximation Algorithm for Maximin Shares"](https://arxiv.org/abs/1903.00029)

Programmer: Liad Nagi and Moriya Elgrabli

See also:

Since:
"""

# import cvxpy
from fairpy import Allocation, ValuationMatrix, Agent, AdditiveValuation, convert_input_to_valuation_matrix
from fairpy import agents
from fairpy.agents import AdditiveAgent
from typing import Any, List
from copy import deepcopy
import logging
logger = logging.getLogger(__name__)
three_quarters = 0.75

# Algo 2

def initial_assignment_alpha_MSS(agents: List[AdditiveAgent], items: List[str], alpha: float):
    """
    Initial division for allocting agents according to their alpha-MMS.
    :param agents:Valuations of agents, normlized such that MMS=1 for all agents, 
    and valuation are ordered in assennding order
    :param items: parameter for how much to approximate MMS allocation.
    :param alpha: parameter for how much to approximate MMS allocation.
    :return agents: Agents (and objects) that still need allocation
    :return ag_alloc:  Whats been allocated so far (in this function)
    :return items:  A list of all the items that can still be allocation
    >>> ### allocation for 1 agent, 1 object
    >>> a = AdditiveAgent({"x": 1}, name="Alice")
    >>> items = list(a.all_items())
    >>> agents=[a]
    >>> a1, a2, a3 = initial_assignment_alpha_MSS(agents, items, 0.75)
    >>> print(a1, a2, a3)
    [] {'Alice': ['x']} []
    >>> ### allocation for 1 agent, 2 object
    >>> b = AdditiveAgent({"x": 0.5, "y": 0.4}, name="Blice")
    >>> items = list(["x", "y"])
    >>> agents=[b]
    >>> a1, a2, a3 = initial_assignment_alpha_MSS(agents, items, 0.6)
    >>> print(a1, a2, a3)
    [] {'Blice': ['x', 'y']} []
    >>> ### allocation for 2 agent, 2 object
    >>> a = AdditiveAgent({"x": 0.8, "y": 0.7}, name="Alice")
    >>> b = AdditiveAgent({"x": 0.7, "y": 0.7}, name="Blice")
    >>> items = list(a.all_items())
    >>> agents=[a,b]
    >>> a1, a2, a3 = initial_assignment_alpha_MSS(agents, items, 0.6)
    >>> print(a1, a2, a3)
    [] {'Alice': ['x'], 'Blice': ['y']} []
    >>> ### allocation for 2 agent, 8 object
    >>> a = AdditiveAgent({"x1": 0.647059, "x2": 0.588235, "x3": 0.470588, "x4": 0.411765, "x5": 0.352941, "x6": 0.294118, "x7": 0.176471, "x8": 0.117647}, name="A")
    >>> b = AdditiveAgent({"x1": 1.298701, "x2": 0.714286, "x3": 0.649351, "x4": 0.428571, "x5": 0.155844, "x6": 0.064935, "x7": 0.051948, "x8": 0.012987}, name="B")
    >>> c =  AdditiveAgent({"x1": 0.6, "x2": 0.6, "x3": 0.48, "x4": 0.36, "x5": 0.32, "x6": 0.32, "x7": 0.28, "x8": 0.04}, name="C")
    >>> items = list(a.all_items())
    >>> agents=[a,b,c]
    >>> a1, a2, a3 = initial_assignment_alpha_MSS(agents, items, 0.75)
    >>> print(a1, a2, a3) # x6, x7, x8 weren't divided
    [] {'A': ['x3', 'x4'], 'B': ['x1'], 'C': ['x2', 'x5']} ['x6', 'x7', 'x8']
    """

    ag_alloc = {} 
    n = len(agents)-1
    if(n+1>len(items)):
        return agents, ag_alloc, items 
    j=0
    while(j<=n):    # for evry agents chack if s1/s2/s3/s3>=alpha
        i=agents[j]
        s1 = (i.value(items[0]))
        if(n+1<len(items)): # chack if we have more then n items
            s2 = (i.value(items[n]) + i.value(items[n+1]))
            if((2*n+1)<len(items)): # chack if we have more then 2*n items
                s3 = (i.value(items[2*n-1])+ i.value(items[2*n]) + i.value(items[2*n+1]))
                s4 = (s1 + i.value(items[2*n+1]))
            else:
                s3 = -1
                s4 = -1
        else:
            s2 = -1
            s3 = -1
            s4 = -1

        if(s1>=alpha):
            ag_alloc[str(i.name())] = [items[0]]
            items.remove(items[0])
            agents.remove(i)
            n = n - 1
            j = 0
        elif(s2>=alpha):
            ag_alloc[str(i.name())] = [items[n] , items[n+1]]
            items.remove(items[n+1])
            items.remove(items[n])
            agents.remove(i)
            n = n - 1
            j = 0
        elif(s3>=alpha):
            ag_alloc[str(i.name())] = [(items[2*n-1], items[2*n] , items[2*n+1])]
            items.remove(items[2*n+1])
            items.remove(items[2*n])
            items.remove(items[2*n-1])
            agents.remove(i)
            n = n - 1
            j = 0
        elif(s4>=alpha):
            ag_alloc[str(i.name())] = [items[0], items[2*n+1]]
            items.remove(items[0])
            items.remove(items[2*n+1])
            agents.remove(i)
            n = n - 1
            j = 0
        else:
            j = j + 1
    # sort the alloc!

    #ag_alloc = sort_allocation(ag_alloc)
    return agents, ag_alloc, items 


# Algo 3

def bag_filling_algorithm_alpha_MMS(agents: List[AdditiveAgent], alpha: float) -> Allocation:
    """
    The algorithm allocates the remaining objects into the remaining agents so that each received at least α from his MMS.
    :param agents: Valuations of agents, normlized such that MMS=1 for all agents, 
    and valuation are ordered in assennding order
    :param alpha: parameter for how much to approximate MMS allocation
    :return allocation: allocation for the agents.

    >>> ### allocation for 1 agent, 0 object
    >>> a = AdditiveAgent({"x": 0}, name="Alice" )
    >>> agents=[a]
    >>> a1 = bag_filling_algorithm_alpha_MMS(agents, 1)
    >>> print(a1)
    Alice gets {x} with value 0.
    <BLANKLINE>
    >>> ### allocation for 1 agent, 3 object (high alpha)
    >>> a = AdditiveAgent({"x1": 0.54, "x2": 0.3, "x3": 0.12}, name="Alice")
    >>> agents=[a]
    >>> a1 = bag_filling_algorithm_alpha_MMS(agents, 0.9)
    >>> print(a1)
    Alice gets {x1, x2, x3} with value 0.96.
    >>> ### allocation for 2 agent, 9 object
    >>> a = AdditiveAgent({"x1": 0.25, "x2": 0.25, "x3": 0.25, "x4": 0.25, "x5": 0.25, "x6": 0.25, "x7": 0.25, "x8": 0.25, "x9": 0.25 }, name="A")
    >>> b = AdditiveAgent({"x1": 0.333333, "x2": 0.333333, "x3": 0.333333, "x4": 0.333333, "x5": 0.166667, "x6": 0.166667, "x7": 0.166667, "x8": 0.166667, "x9": 0.166667 }, name="B")
    >>> agents=[a,b]
    >>> a1 = bag_filling_algorithm_alpha_MMS(agents,0.9)
    >>> print(a1)
    A gets {x1, x4, x8, x9} with value 1.
    B gets {x2, x3, x6, x7} with value 1.
    """

    allocation = Allocation(agents=agents, bundles={"Alice": {"x"}})
    return allocation


# algo 1
def alpha_MMS_allocation(agents: List[AdditiveAgent], alpha: float, mms_values: List[float]):
    """
    Find alpha_MMS_allocation for the given agents and valuations.
    :param agents: Valuations of agents, valuation are ordered in assennding order
    :param alpha: parameter for how much to approximate MMS allocation
    :param mms_values: mms_values of each agent inorder to normelize by them.
    :return allocation: alpha-mms Alloctaion to each agent.

    >>> ### allocation for 1 agent, 1 object
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> a1 = alpha_MMS_allocation(agents,0.5,[2])
    >>> print(a1)
    Alice gets {x} with value 2.
    <BLANKLINE>
    >>> ### allocation for 1 agent, 2 objects
    >>> b = AdditiveAgent({"x": 1, "y": 2}, name="Blice")
    >>> agents=[b]
    >>> a1 = alpha_MMS_allocation(agents,0.6,[3])
    >>> print(a1)
    Blice gets {x} with value 1.
    <BLANKLINE>
    >>> ### allocation for 2 agents, 2 objects
    >>> a = AdditiveAgent({"x": 1, "y": 2}, name="Alice")
    >>> agents = [a, b]
    >>> a1 = alpha_MMS_allocation(agents,1,[1,1])
    >>> print(a1)
    Alice gets {x} with value 1.
    Blice gets {y} with value 2.
    <BLANKLINE>
    >>> ### allocation for 3 agents, 3 objects (low alpha)
    >>> a = AdditiveAgent({"x1": 3, "x2": 2, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 4, "x2": 4, "x3": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 5, "x2": 2, "x3": 1}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alpha_MMS_allocation(agents,0.2,[1,4,1])
    >>> print(a1)
    A gets {x1} with value 3.
    B gets {x2} with value 4.
    C gets {x3} with value 1.
    <BLANKLINE>
    >>> ### allocation with 3 agents, 8 objects
    >>> a = AdditiveAgent({"x1": 11, "x2": 10, "x3": 8,"x4": 7, "x5": 6, "x6": 5,"x7": 3, "x8": 2}, name="A")
    >>> b = AdditiveAgent({"x1": 100, "x2": 55, "x3": 50,"x4": 33, "x5": 12, "x6": 5,"x7": 4, "x8": 1}, name="B")
    >>> c = AdditiveAgent({"x1": 15, "x2": 15, "x3": 12,"x4": 9, "x5": 8, "x6": 8,"x7": 7, "x8": 5}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alpha_MMS_allocation(agents,0.75,[17,77,25])
    >>> print(a1)
    B gets {x1} with value 100.
    A gets {x3, x4} with value 15.
    C gets {x2,x5} with value 23.
    <BLANKLINE>
    >>> ### allocation with 3 agents, 8 objects
    >>> a = AdditiveAgent({"x1": 1, "x2": 1, "x3": 1,"x4": 1, "x5": 1, "x6": 1,"x7": 1, "x8": 1, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 2, "x2": 2, "x3": 2,"x4": 2, "x5": 2, "x6": 2,"x7": 1, "x8": 1, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="B")
    >>> c = AdditiveAgent({"x1": 2, "x2": 2, "x3": 2,"x4": 2, "x5": 2, "x6": 2,"x7": 2, "x8": 2, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alpha_MMS_allocation(agents,0.75,[4,6,6])
    >>> print(a1)
    A gets {x1, x4, x11, x12} with value 4.
    B gets {x2, x3, x9, x10} with value 6.
    C gets {x5, x6, x7} with value 6.
    <BLANKLINE>
    """

    allocation = Allocation(agents=agents, bundles={"Alice": {"x"}})
    return allocation

# Algo 5
def fixed_assignment(agents: List[AdditiveAgent], items: List[str]):
    """
    The function allocates what can be allocated without harting others
    (each allocated agent gets 3/4 of his own MMS value,
    without casing others  not to get their MMS value)
    :param agents: Valuations of agents, normlized such that MMS <=1 for all agents
    :return allocation: What been allocated so far
    :return agents: Agents (and objects) that still need allocation

    >>> ### fixed_assignment for one agent, one object
    >>> a = AdditiveAgent({"x": 1}, name="Alice")
    >>> agents=[a]
    >>> items = list(a.all_items())
    >>> remaining_agents, alloc, remaining_items =fixed_assignment(agents, items)
    >>> print(remaining_agents, alloc, remaining_items)
    [] {'Alice': ['x']} []
    >>> ### fixed_assignment for two agent, one objects
    >>> b = AdditiveAgent({"x": 3.333333}, name="Bruce")
    >>> c = AdditiveAgent({"x":2}, name="Carl")
    >>> agents=[b,c]
    >>> items = list(b.all_items())
    >>> remaining_agents, alloc, remaining_items =fixed_assignment(agents, items)
    >>> print(remaining_agents, alloc, remaining_items)
    [Bruce is an agent with a Additive valuation: x=3.333333., Carl is an agent with a Additive valuation: x=2.] {} ['x']
    >>> ### fixed_assignment for two agent, three objects #
    >>> b = AdditiveAgent({"x": 1.2,"y": 0.24, "z":0.56}, name="Bruce")
    >>> c = AdditiveAgent({"x":1.125,"y": 0.875,"z":0.25}, name="Carl")
    >>> agents=[b,c]
    >>> items = list(b.all_items())
    >>> remaining_agents, alloc, remaining_items = fixed_assignment(agents, items)
    >>> print(remaining_agents, alloc, remaining_items)
    [] {'Bruce': ['x'], 'Carl': ['y']} ['z']
    """
    ag_alloc = {}  #agents allocations
    n = len(agents)-1
    if(n+1>len(items)):
        return agents, ag_alloc, items 
    #items=list(agents[0].valuation.all_items())
    val_arr = dict() #values of agents
    for i in agents:
        val_arr[i.name()] = i.valuation.map_good_to_value
    j=0
    while(j<=n):    # for evry agents chack if s1/s2/s3>=three_quarters
        
        nameI=agents[j].name()  #agent name
        i=val_arr[nameI]    #agent[j]
        s1 = (i.get(items[0]))
        if(n+1<len(items)): # chack if we have more then n items
            s2 = i.get(items[n]) + i.get(items[n+1])
            if((2*n+1)<len(items)): # chack if we have more then 2*n items
                s3 = (i.get(items[2*n-1])) + (i.get(items[2*n])) + (i.get(items[2*n+1]))
            else:
                s3 = -1
        else:
            s2 = -1
            s3 = -1
        
        if(s1>=three_quarters):
            ag_alloc[str(nameI)] = [items[0]]
            val_arr.pop(str(nameI))
            val_arr = update_val([items[0]], val_arr, n)
            items.remove(items[0])
            agents.remove(agents[j])
            j=0
            n = n - 1
        elif(s2>=three_quarters):
            ag_alloc[str(nameI)] = [items[n] , items[n+1]]
            val_arr.pop(str(nameI))
            val_arr = update_val([items[n] , items[n+1]], val_arr, n)
            items.remove(items[n+1])
            items.remove(items[n])
            agents.remove(agents[j])
            j=0
            n = n - 1
        elif(s3>=three_quarters):
            ag_alloc[str(nameI)] = [items[2*n-1], items[2*n] , items[2*n+1]]
            val_arr.pop(str(nameI))
            val_arr = update_val([items[2*n-1], items[2*n] , items[2*n+1]], val_arr, n)
            items.remove(items[2*n+1])
            items.remove(items[2*n])
            items.remove(items[2*n-1])
            agents.remove(agents[j])
            j=0
            n = n - 1
        else:
            j = j + 1
    
    # sort the alloc!
    ag_alloc = sort_allocation(ag_alloc)
    return agents, ag_alloc, items 


# Algo 6
def tentative_assignment(agents: List[AdditiveAgent], items: List[str]):
    """
    The function allocates temporerly what can be allocated, can maybe hart others it not normlized close enough to the mms values.
    :param agents: Valuations of agents,such that bundles of objects at the positions:
     {0}, {n-1,n},{2n-2,2n-1,2n} not satisties for them,
     and normlized such that MMS <=1 for all agents.
    :return allocation: Whats been temporarly allocated so far
    :return agents: Agents (and objects) that still need allocation
    >>> ### doesn't find any allocation.
    >>> agents = AdditiveAgent.list_from({"Alice":[],\
                                          "Bruce":[],\
                                           "Carl":[]})
    >>> a = AdditiveAgent({"01": 0.724489796, "02": 0.714285714, "03": 0.387755102, "04": 0.357142857, "05": 0.357142857, "06": 0.357142857, "07": 0.020408163, "08": 0.020408163, "09": 0.020408163, "10": 0.020408163, "11": 0.020408163}, name="Alice")
    >>> b = AdditiveAgent({"01": 0.724489796, "02": 0.714285714, "03": 0.387755102, "04": 0.357142857, "05": 0.357142857, "06": 0.357142857, "07": 0.020408163, "08": 0.020408163, "09": 0.020408163, "10": 0.020408163, "11": 0.020408163}, name="Bruce")
    >>> c = AdditiveAgent({"01": 0.724489796, "02": 0.714285714, "03": 0.387755102, "04": 0.357142857, "05": 0.357142857, "06": 0.357142857, "07": 0.020408163, "08": 0.020408163, "09": 0.020408163, "10": 0.020408163, "11": 0.020408163}, name="Carl")
    >>> agents = [a,b,c]
    >>> items = list(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"])
    >>> remaining_agents, alloc, remaining_items = tentative_assignment(agents, items)
    >>> print(remaining_agents, alloc, remaining_items)
    Alice gets {} with value 0.
    Bruce gets {} with value 0.
    Carl gets {} with value 0.
    <BLANKLINE>
    >>> remaining_agents
    [Alice is an agent with a Additive valuation: v0=0.724489796 v1=0.714285714 v2=0.387755102 v3=0.357142857 v4=0.357142857 v5=0.357142857 v6=0.020408163 v7=0.020408163 v8=0.020408163 v9=0.020408163 v10=0.020408163., Bruce is an agent with a Additive valuation: v0=0.724489796 v1=0.714285714 v2=0.387755102 v3=0.357142857 v4=0.357142857 v5=0.357142857 v6=0.020408163 v7=0.020408163 v8=0.020408163 v9=0.020408163 v10=0.020408163., Carl is an agent with a Additive valuation: v0=0.724489796 v1=0.714285714 v2=0.387755102 v3=0.357142857 v4=0.357142857 v5=0.357142857 v6=0.020408163 v7=0.020408163 v8=0.020408163 v9=0.020408163 v10=0.020408163.]
    >>> ### 3 agents 11 objects - ex 1
    >>> a = AdditiveAgent({"01": 0.727066, "02": 0.727066, "03": 0.39525, "04": 0.351334, "05": 0.351334, "06": 0.346454, "07": 0.022934, "08": 0.022934, "09": 0.022934, "10": 0.022934, "11": 0.022934}, name="Alice")
    >>> b = AdditiveAgent({"01": 0.723887, "02": 0.723887, "03": 0.393522, "04": 0.349798, "05": 0.349798, "06": 0.344939, "07": 0.022834, "08": 0.022834, "09":  0.022834, "10": 0.022834, "11": 0.022834}, name="Bruce")
    >>> c = AdditiveAgent({"01": 0.723887, "02": 0.723887, "03": 0.393522, "04": 0.349798, "05": 0.349798, "06": 0.344939, "07": 0.022834, "08": 0.022834, "09": 0.022834, "10": 0.022834, "11": 0.022834}, name="Carl")
    >>> agents = [a,b,c]
    >>> items = list(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"])
    >>> remaining_agents, alloc, remaining_items = tentative_assignment(agents, items)
    >>> print(remaining_agents, alloc, remaining_items)
    Alice gets {0,6} with value 0.75.
    Bruce gets {3,4,5} with value 1.044535.
    Carl gets {1,2} with value 1.117409.
    <BLANKLINE>
    >>> remaining_agents
    []
    >>> ### 3 agents 10 object
    >>> a = AdditiveAgent({"01": 0.727272, "02": 0.727272, "03": 0.318182, "04": 0.318182, "05": 0.318182, "06": 0.318182, "07": 0.090909, "08": 0.090909, "09": 0.045454, "10": 0.045454}, name="Alice")
    >>> b = AdditiveAgent({"01": 0.727272, "02": 0.727272, "03": 0.318182, "04": 0.318182, "05": 0.318182, "06": 0.318182, "07": 0.090909, "08": 0.090909, "09": 0.045454, "10": 0.045454}, name="Bruce")
    >>> c = AdditiveAgent({"01": 0.727272, "02": 0.727272, "03": 0.318182, "04": 0.318182, "05": 0.318182, "06": 0.318182, "07": 0.090909, "08": 0.090909, "09": 0.045454, "10": 0.045454}, name="Carl")
    >>> agents = [a,b,c]
    >>> items = list(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"])
    >>> remaining_agents, alloc, remaining_items = tentative_assignment(agents, items)
    >>> print(remaining_agents, alloc, remaining_items)
    Alice gets {0,6} with value 0.818181.
    Bruce gets {3,4,5} with value 0.954546.
    Carl gets {1,2} with value 1.045454.
    <BLANKLINE>
    >>> remaining_agents
    []
    """
    ag_alloc = {} 
    n = len(agents)-1
    if(n+1>len(items)):
        return agents, ag_alloc, items

    #deepcopy of items and agents
    agents_temp = list()
    items_temp = list() 
    for i in agents:
        agents_temp.append( AdditiveAgent(i.valuation.map_good_to_value, name=i.name()))
    for i in items:
        items_temp.append(i)
    
    #items=list(agents[0].valuation.all_items())
    val_arr = dict() #values of agents
    for i in agents_temp:
        val_arr[i.name()] = i.valuation.map_good_to_value
    j=0
    while(j<=n):    # for evry agents chack if s1/s2/s3/s3/s4>=alpha
        
        nameI=agents_temp[j].name()
        i=val_arr[nameI]
        s1 = (i.get(str(items_temp[0])))
        
        if(n+1<len(items_temp)): # chack if we have more then n items
            s2 = i.get(items_temp[n]) + i.get(items_temp[n+1])
            if((2*n+1)<len(items_temp)): # chack if we have more then 2*n items
                s3 = (i.get(items_temp[2*n-1])) + (i.get(items_temp[2*n])) + (i.get(items_temp[2*n+1]))
                s4 = (i.get(items_temp[0])) +  (i.get(items_temp[2*n+1]))
            else:
                s3 = -1
                s4 = -1
        else:
            s2 = -1
            s3 = -1
            s4 = -1
        if(s1>=three_quarters):
            ag_alloc[str(nameI)] = [items_temp[0]]
            val_arr.pop(str(nameI))
            val_arr = update_val([items_temp[0]], val_arr, n)
            items_temp.remove(items_temp[0])
            agents_temp.remove(agents_temp[j])
            j=0
            n = n - 1
        elif(s2>=three_quarters):
            ag_alloc[str(nameI)] = [items_temp[n] , items_temp[n+1]]
            val_arr.pop(str(nameI))
            val_arr = update_val([items_temp[n] , items_temp[n+1]], val_arr, n)
            items_temp.remove(items_temp[n+1])
            items_temp.remove(items_temp[n])
            agents_temp.remove(agents_temp[j])
            j=0
            n = n - 1
        elif(s3>=three_quarters):
            ag_alloc[str(nameI)] = [items_temp[2*n-1], items_temp[2*n] , items_temp[2*n+1]]
            val_arr.pop(str(nameI))
            val_arr = update_val([items_temp[2*n-1], items_temp[2*n] , items_temp[2*n+1]], val_arr, n)
            items_temp.remove(items_temp[2*n+1])
            items_temp.remove(items_temp[2*n])
            items_temp.remove(items_temp[2*n-1])
            agents_temp.remove(agents_temp[j])
            j=0
            n = n - 1
        elif(s4>=three_quarters):
            ag_alloc[str(nameI)] = [items_temp[0],  items_temp[2*n+1]]
            val_arr.pop(str(nameI))
            val_arr = update_val([items_temp[0],  items_temp[2*n+1]], val_arr, n)
            items_temp.remove(items_temp[2*n+1])
            items_temp.remove(items_temp[0])
            agents_temp.remove(agents_temp[j])
            j=0
            n = n - 1
        else:
            j = j + 1
    # sort the alloc!

    #ag_alloc = sort_allocation(ag_alloc)
    return agents_temp, ag_alloc, items_temp 


# algo 4
def three_quarters_MMS_allocation(agents: List[AdditiveAgent]):
    """
    Finds three_quarters_MMS_allocation for the given agents and valuations.
    :param agents: Valuations of agents, valuation are ordered in assending order
    :return allocation: three_quarters_MMS_allocation for all agents


    >>> ### allocation for 1 agent, 1 object
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> a1 = three_quarters_MMS_allocation(agents)
    >>> print(a1)
    Alice gets {x} with value 2.
    >>> ### allocation for 1 agent, 2 objects
    >>> b = AdditiveAgent({"x": 1, "y": 2}, name="Blice")
    >>> agents=[b]
    >>> a1 = three_quarters_MMS_allocation(agents)
    >>> print(a1)
    Blice gets {x,y} with value 3.
    >>> ### allocation for 2 agents, 2 objects
    >>> a = AdditiveAgent({"x": 1, "y": 2}, name="Alice")
    >>> agents = [a, b]
    >>> a1 = three_quarters_MMS_allocation(agents)
    >>> print(a1)
    Alice gets {x} with value 1.
    Blice gets {y} with value 2.
    >>> ### allocation for 3 agents, 3 objects (low alpha)
    >>> a = AdditiveAgent({"x1": 3, "x2": 2, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 4, "x2": 4, "x3": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 5, "x2": 2, "x3": 1}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = three_quarters_MMS_allocation(agents)
    >>> print(a1)
    A gets {x1} with value 3.
    B gets {x2} with value 4.
    C gets {x3} with value 1.
    >>> ### detailed example: enter loop and adjusted by alpha.
    >>> ### 3 agents 11 objects
    >>> agents = AdditiveAgent.list_from({"Alice":[35.5,35,19,17.5,17.5,17.5,1,1,1,1,1],\
    "Bruce":[35.5,35,19,17.5,17.5,17.5,1,1,1,1,1],\
    "Carl":[35.5,35,19,17.5,17.5,17.5,1,1,1,1,1]})
    >>> alloc = three_quarters_MMS_allocation(agents)
    >>> print(alloc.str_with_values(precision=7))
    Alice gets {2,3} with value 36.5.
    Bruce gets {1,4} with value 52.5.
    Carl gets {0,6} with value .
    <BLANKLINE>
    """
    #return Allocation(agents=agents, bundles={"Carl": {"x"}})

    return Allocation(agents=agents, bundles={"Carl": {2, 3}, "Bruce": {1, 4}, "Alice": {0, 5}})

##### algo 7
def agents_conversion_to_ordered_instance(agents: List[AdditiveAgent]) :
    """
    The function sorted the list of additive agents such that their valuations for objects are unordered will become ordered.
    :param agents: A list of additive agents such that their valuations for objects are unordered.
    :return agents_sorted: A list of additive agents such that their valuations for objects are in ascending order.
    >>> a = AdditiveAgent({"x1": 2, "x2": 7, "x3": 10,"x4": 8, "x5": 3, "x6": 4,"x7": 7, "x8": 11}, name="A")
    >>> b = AdditiveAgent({"x1": 8, "x2": 7, "x3": 5,"x4": 3, "x5": 10, "x6": 2,"x7": 1, "x8": 4}, name="B")
    >>> c =  AdditiveAgent({"x1": 1, "x2": 2, "x3": 3,"x4": 4, "x5": 5, "x6": 6,"x7": 7, "x8": 8}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = agents_conversion_to_ordered_instance(agents)
    >>> print(a1)
    [A is an agent with a Additive valuation: x1=11 x2=10 x3=8 x4=7 x5=7 x6=4 x7=3 x8=2., B is an agent with a Additive valuation: x1=10 x2=8 x3=7 x4=5 x5=4 x6=3 x7=2 x8=1., C is an agent with a Additive valuation: x1=8 x2=7 x3=6 x4=5 x5=4 x6=3 x7=2 x8=1.]
    """

    return agents #sorted

    
##### algo 8
def get_alpha_MMS_allocation_to_unordered_instance(agents_unordered: List[AdditiveAgent],agents_ordered:List[AdditiveAgent],ordered_allocation:Allocation) :
    """
    Get the MMS allocation for agents unordered valuations.
    :param agents_unordered: Unordered valuations agents.
    :param agents_ordered: Ordered valuations agents.
    :param ordered_allocation: MMS allocation for ordered valuations agents.
    :return allocation: return the real allocation (the allocation for the unordered items)
    >>> ### allocation for 2 agents 3 objects
    >>> a = AdditiveAgent({"x1": 3, "x2": 10, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 10, "x2": 10, "x3": 10}, name="B")
    >>> agents=[a,b]
    >>> agents_ordered=agents_conversion_to_ordered_instance(agents)
    >>> ordered_alloc= Allocation(agents=agents_ordered, bundles={"A": {"x1"}, "B": {"x2"}})
    >>> real_alloc = get_alpha_MMS_allocation_to_unordered_instance(agents, agents_ordered, ordered_alloc)
    >>> print(real_alloc)
    A gets {x2} with value 10.
    B gets {x1} with value 10.
    <BLANKLINE>

    >>> ### allocation for 1 agent, 1 object
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> agents_ordered=agents_conversion_to_ordered_instance(agents)
    >>> ordered_alloc= Allocation(agents=agents_ordered, bundles={"Alice": {"x"}})
    >>> real_alloc = get_alpha_MMS_allocation_to_unordered_instance(agents, agents_ordered, ordered_alloc)
    >>> print(real_alloc)
    Alice gets {x} with value 2.
    <BLANKLINE>

    >>> ### allocation for 3 agents 8 objects
    >>> a = AdditiveAgent({"x1": 2, "x2": 7, "x3": 10,"x4": 8, "x5": 3, "x6": 4,"x7": 7, "x8": 11}, name="A")
    >>> b = AdditiveAgent({"x1": 8, "x2": 7, "x3": 5,"x4": 3, "x5": 10, "x6": 2,"x7": 1, "x8": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 1, "x2": 2, "x3": 3,"x4": 4, "x5": 5, "x6": 6,"x7": 7, "x8": 8}, name="C")
    >>> agents=[a,b,c]
    >>> agents_ordered=agents_conversion_to_ordered_instance(agents)
    >>> ordered_alloc= Allocation(agents=agents_ordered, bundles={"A": {"x3","x4"},"B":{"x1"},"C":{"x2","x5"}})
    >>> real_alloc =  get_alpha_MMS_allocation_to_unordered_instance(agents, agents_ordered, ordered_alloc)
    >>> print(real_alloc)
    A gets {x3, x4} with value 18.
    B gets {x5} with value 10.
    C gets {x7,x8} with value 15.
    <BLANKLINE>
    """
    return ordered_allocation #real allocation

def sort_allocation(ag_alloc: dict())->dict() : 
    """
    sorted a dict in deepcopy
    """
    temp_x = dict(sorted(ag_alloc.items()))
    for key,val in ag_alloc.items():
        temp_x[key] = deepcopy(sorted(val))
    ag_alloc = deepcopy(temp_x)
    return ag_alloc


def update_val(items_remove: List[str], val_arr: dict(), n: int)->dict() : 
    """
        update all the values of the agents that still remained
    """
    sum_arr = dict()
    for i in val_arr:
        for j in items_remove:
            val_arr[i].pop(j)
        sum_arr[i] = 0
        for j in val_arr[i]:
            sum_arr[i] = sum_arr[i] + val_arr[i][j]
        for j in val_arr[i]:
            val_arr[i][j] = val_arr[i][j]*(n/sum_arr[i])
    return val_arr


if __name__ == '__main__':
    import doctest
    import sys

    # (failures, tests) = doctest.testmod(report=True)
    # print("{} failures, {} tests".format(failures, tests))
    # how to run specific function
    # doctest.run_docstring_examples(initial_assignment_alpha_MSS, globals())
    # doctest.run_docstring_examples(bag_filling_algorithm_alpha_MMS, globals())
    # doctest.run_docstring_examples(alpha_MMS_allocation, globals())

    # doctest.run_docstring_examples(fixed_assignment, globals())
    doctest.run_docstring_examples(tentative_assignment, globals())
    # doctest.run_docstring_examples(three_quarters_MMS_allocation, globals())
    # doctest.run_docstring_examples(agents_conversion_to_ordered_instance, globals())
    # doctest.run_docstring_examples(get_alpha_MMS_allocation_to_unordered_instance, globals())
