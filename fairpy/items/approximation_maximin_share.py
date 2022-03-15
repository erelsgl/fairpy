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
from fairpy.agents import AdditiveAgent, agent_names_from
from typing import Any, List
from fairpy.items.bag_filling import Bag
from copy import deepcopy
import logging
logger = logging.getLogger(__name__)
three_quarters = 0.75


def willing_agent(agents:List[AdditiveAgent], bundel: List[str], threshhold):
#returns none also if len(agents) is 0
    num_agents=len(agents)
    for i in range(0,num_agents):
        if agents[i].value(bundel)>=threshhold:
            return i
    return None



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
>>> ### allocation for 1 agent, 1 object (this pass!)
    >>> a = AdditiveAgent({"x": 1}, name="Alice")
    >>> agents=[a]
    >>> a1 = initial_assignment_alpha_MSS(agents,['x'],0.75)
    >>> print(a1, agents)
    Alice gets {x} with value 1.
     []
    >>> ### allocation for 1 agent, 2 object
    >>> b = AdditiveAgent({"x": 0.5, "y": 0.4}, name="Blice")
    >>> agents=[b]
    >>> a1 = initial_assignment_alpha_MSS(agents,['x','y'],0.6)
    >>> print(a1, agents)
    Blice gets {x,y} with value 0.9.
     []
    >>> ### allocation for 2 agent, 2 object
    >>> a = AdditiveAgent({"x": 0.8, "y": 0.7}, name="Alice")
    >>> b = AdditiveAgent({"x": 0.7, "y": 0.7}, name="Blice")
    >>> agents=[a,b]
    >>> a1= initial_assignment_alpha_MSS(agents,['x','y'],0.6)
    >>> print(a1, agents)
    Alice gets {x} with value 0.8.
    Blice gets {y} with value 0.7.
     []
    >>> ### allocation for 2 agent, 8 object
    >>> a = AdditiveAgent({"x1": 0.647059, "x2": 0.588235, "x3": 0.470588, "x4": 0.411765, "x5": 0.352941, "x6": 0.294118, "x7": 0.176471, "x8": 0.117647}, name="A")
    >>> b = AdditiveAgent({"x1": 1.298701, "x2": 0.714286, "x3": 0.649351, "x4": 0.428571, "x5": 0.155844, "x6": 0.064935, "x7": 0.051948, "x8": 0.012987}, name="B")
    >>> c =  AdditiveAgent({"x1": 0.6, "x2": 0.6, "x3": 0.48, "x4": 0.36, "x5": 0.32, "x6": 0.32, "x7": 0.28, "x8": 0.04}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = initial_assignment_alpha_MSS(agents,['x1','x2','x3','x4','x5','x6','x7','x8'],0.75)
    >>> print(a1, agents) # x6, x7, x8 weren't divided
    A gets {x3,x4} with value 0.882353.
    B gets {x1} with value 1.298701.
    C gets {x2,x5} with value 0.92.
     []
    """

    ag_alloc = {} 
    n = len(agents)-1
    if(n+1>len(items)):
        return agents, ag_alloc, items
        #return None 
    names_agents=agent_names_from(agents)

    while(True):    # for every agents check if s1/s2/s3/s3>=alpha
        num_items=len(items)
        s1_bundle,s2_bundle,s3_bundle,s4_bundle=[],[],[],[]
        #check index not out of bound
        if num_items>0:
            s1_bundle=[items[0]]
        if num_items>n+1:
            s2_bundle=[items[n] , items[n+1]]
        if num_items>2*(n+1):
            if 2*(n+1)-2>0:
                s3_bundle=[items[(2*(n+1))-2], items[2*(n+1)-1] , items[2*(n+1)]]
            s4_bundle=[items[0], items[2*(n+1)]]


        s=[s1_bundle,s2_bundle,s3_bundle, s4_bundle]

        for si in s:
            willing_agent_index=willing_agent(agents,si,alpha)
            if willing_agent_index!=None:
                ag_alloc[agents[willing_agent_index]._name] = si #si.copy()
                for item in si:
                    items.remove(item)
                agents.pop(willing_agent_index)
                n = n - 1
                break
            elif si==s4_bundle:
                return  Allocation (names_agents,ag_alloc)





# def full_valuation_matrix(items: List[str],agents: List[AdditiveAgent]):
#     items_num =len(items)
#     values_list=[]
#     for agent in agents:
#         values_i=[]
#         for k in range (0,items_num): ##add lowest value objects
#             values_i.append(agent.value(items[k]))
#         values_list.append(values_i)
#     return values_list


# Algo 3

def bag_filling_algorithm_alpha_MMS(items: List[str],agents: List[AdditiveAgent], alpha: float) -> Allocation:
    """
    The algorithm allocates the remaining objects into the remaining agents so that each received at least α from his MMS.
    :param items: items names sorted from the highest valued to the lowest

    :param agents: Valuations of agents, normlized such that MMS=1 for all agents, 
    and valuation are ordered in assennding order
    :param alpha: parameter for how much to approximate MMS allocation
    :return allocation: allocation for the agents.

    >>> ### allocation for 1 agent, 0 object
    >>> a = AdditiveAgent({"x": 1}, name="Alice" )
    >>> agents=[a]
    >>> a1 = bag_filling_algorithm_alpha_MMS(['x'],agents, 1)
    >>> print(a1)
    Alice gets {x} with value 1.
    <BLANKLINE>
    >>> ### allocation for 1 agent, 3 object (high alpha)
    >>> a = AdditiveAgent({"x1": 0.54, "x2": 0.3, "x3": 0.12}, name="Alice")
    >>> agents=[a]
    >>> a1 = bag_filling_algorithm_alpha_MMS(['x1','x2','x3'],agents, 0.9)
    >>> print(a1)
    Alice gets {x1,x2,x3} with value 0.96.
    <BLANKLINE>
    >>> ### allocation for 2 agent, 9 object
    >>> a = AdditiveAgent({"x1": 0.25, "x2": 0.25, "x3": 0.25, "x4": 0.25, "x5": 0.25, "x6": 0.25, "x7": 0.25, "x8": 0.25, "x9": 0.25 }, name="A")
    >>> b = AdditiveAgent({"x1": 0.333333, "x2": 0.333333, "x3": 0.333333, "x4": 0.333333, "x5": 0.166667, "x6": 0.166667, "x7": 0.166667, "x8": 0.166667, "x9": 0.166667 }, name="B")
    >>> agents=[a,b]
    >>> a1 = bag_filling_algorithm_alpha_MMS(['x1','x2','x3','x4','x5','x6','x7','x8','x9'],agents,0.9)
    >>> print(a1)
    A gets {x1,x4,x8,x9} with value 1.
    B gets {x2,x3,x6,x7} with value 1.
    <BLANKLINE>
    """

    agents_num=len(agents)
    items_num =len(items)

    if (agents_num<=0 or items_num<=0):
        return None

    agents_names=agent_names_from(agents)       
    bundles={}
    

    while agents_num>0:
        mirror_index=2*agents_num-1
        if (len(items)>0 and len(items)>mirror_index ): #has to be both!!
            bundel_name_arr=[items[0],items[mirror_index]]
            w_agent=willing_agent(agents,bundel_name_arr,alpha)
            last_item=len(items)-1
            while(w_agent==None and last_item>=2*agents_num):
                bundel_name_arr.append(items[last_item])
                last_item-=1
                w_agent=willing_agent(agents,bundel_name_arr,alpha)
            if w_agent==None: #there is not any devison that will satisfy the any agent
                raise Exception("ERROR. Could not create an MMS allocation that satisfies agents.")
            bundles[agents[w_agent]._name]=bundel_name_arr
            agents.pop(w_agent)

            for obj_index in bundel_name_arr:
                items.remove(obj_index) 

            
            agents_num=len(agents) #update
        else:
            raise Exception("ERROR. Could not create an MMS allocation that satisfies agents.")



    return Allocation(agents=agents_names, bundles=bundles)



def normalize_algo1(agents: List[AdditiveAgent], mms_values: List[float],items: List[str]):
    normelized_agents={}
    #AdditiveAgent.list_from({"Alice":[1,2], "George":[3,4]})
    num_agents=len(agents)
    for i in range(0,num_agents):
        normelized_agents[agents[i]._name]={}
        for item in items:
            normelized_agents[agents[i]._name][item]=(agents[i].value(item))/mms_values[i]
    return AdditiveAgent.list_from(normelized_agents)

def combine_allocations(allocations: List[Allocation], agents: List[AdditiveAgent]):
    is_first=True
    combined_bundle=None
    for alloc in allocations:
        if is_first:
            combined_bundle=alloc.map_agent_to_bundle().copy()
            is_first=False
        else:
            map_agent_to_bundle=alloc.map_agent_to_bundle()
            for name,assignment in map_agent_to_bundle.items():
                if len(combined_bundle[name])==0:
                    combined_bundle[name]=assignment.copy()

    return Allocation(agents=agents, bundles=combined_bundle)


# algo 1
def alpha_MMS_allocation(agents: List[AdditiveAgent], alpha: float, mms_values: List[float], items: List[str]):
    """
    Find alpha_MMS_allocation for the given agents and valuations.
    :param agents: Valuations of agents, valuation are ordered in assennding order
    :param alpha: parameter for how much to approximate MMS allocation
    :param mms_values: mms_values of each agent inorder to normelize by them.
    :return allocation: alpha-mms Alloctaion to each agent.

    >>> ### allocation for 1 agent, 1 object
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> a1 = alpha_MMS_allocation(agents,0.5,[2],['x'])
    >>> print(a1)
    Alice gets {x} with value 2.
    <BLANKLINE>
    >>> ### allocation for 1 agent, 2 objects
    >>> b = AdditiveAgent({"x": 2, "y": 1}, name="Blice")
    >>> agents=[b]
    >>> a1 = alpha_MMS_allocation(agents,0.6,[3],['x','y'])
    >>> print(a1)
    Blice gets {x} with value 2.
    <BLANKLINE>
    >>> ### allocation for 2 agents, 2 objects
    >>> a = AdditiveAgent({"x": 2, "y": 1}, name="Alice")
    >>> agents = [a, b]
    >>> a1 = alpha_MMS_allocation(agents,1,[1,1],['x','y'])
    >>> print(a1)
    Alice gets {x} with value 2.
    Blice gets {y} with value 1.
    <BLANKLINE>
    >>> ### allocation for 3 agents, 3 objects (low alpha)
    >>> a = AdditiveAgent({"x1": 3, "x2": 2, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 4, "x2": 4, "x3": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 5, "x2": 2, "x3": 1}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alpha_MMS_allocation(agents,0.2,[1,4,1],['x1','x2','x3'])
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
    >>> a1 = alpha_MMS_allocation(agents,0.75,[17,77,25],['x1','x2','x3','x4','x5','x6','x7','x8'])
    >>> print(a1)
    A gets {x3,x4} with value 15.
    B gets {x1} with value 100.
    C gets {x2,x5} with value 23.
    <BLANKLINE>
    >>> ### allocation with 3 agents, 8 objects
    >>> a = AdditiveAgent({"x1": 1, "x2": 1, "x3": 1,"x4": 1, "x5": 1, "x6": 1,"x7": 1, "x8": 1, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 2, "x2": 2, "x3": 2,"x4": 2, "x5": 2, "x6": 2,"x7": 1, "x8": 1, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="B")
    >>> c = AdditiveAgent({"x1": 2, "x2": 2, "x3": 2,"x4": 2, "x5": 2, "x6": 2,"x7": 2, "x8": 2, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alpha_MMS_allocation(agents,0.9,[4,6,6],['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11','x12'])
    >>> print(a1)
    A gets {x1,x11,x12,x4} with value 4.
    B gets {x10,x2,x3,x9} with value 6.
    C gets {x5,x6,x7} with value 6.
    <BLANKLINE>
    """
    num_agents=len(agents)
    #names_agents=agent_names_from(agents)
    
    for i in range (0,num_agents):
        if mms_values[i]==0:
            mms_values.pop(i)
            agents.pop(i)
    if len(agents)==0 or len(agents)>len(items):
       return Allocation(agents=agents, bundles={})
    normelized_agents=normalize_algo1(agents,mms_values,items)
    alloc_initial_assignment=initial_assignment_alpha_MSS(normelized_agents,items,alpha)
    if(len(normelized_agents)==0):
        return combine_allocations([alloc_initial_assignment],agents)#use function to get value of alloc
    alloc_bag_filling=bag_filling_algorithm_alpha_MMS(items,normelized_agents,alpha)
        
     
   
    return combine_allocations([alloc_initial_assignment,alloc_bag_filling], agents)


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

def compute_n21(normelized_agents,items):
    agents_num=len(normelized_agents)

    #calculate l,h,sum of bundles of each agents
    l=[0] * agents_num
    h=[0] * agents_num
    sum=[0] * agents_num 
    for i in range(0,agents_num):
        mirror_index=2*agents_num-i-1
        assert (len(items)>0 and len(items)>mirror_index )#has to be both!!
        bundel_i=[items[0],items[mirror_index]]
        for agent_index in range(0,agents_num):
            bundle_val=normelized_agents[agent_index].value(bundel_i)
            if bundle_val<three_quarters:
                l[agent_index]+=1
                sum[agent_index]+=bundle_val
            elif bundle_val>1:
                h[agent_index]+=1
    

    #go through all agents, starts from lowest index, and check if belong to n21
    for agent_index in range(0,agents_num):
        x_agent=(0.75)*l[agent_index]-sum[agent_index]
        lowest_value_items=normelized_agents[agent_index].value_except_best_c_goods(agents_num)
        #if this agent belong to N21
        if(h[agent_index]>0 and h[agent_index]>l[agent_index] and (x_agent+l[agent_index]/8)>lowest_value_items): 
            return agent_index
    #if no agent belongs to N21
    return None 
def compute_alphas(normelized_agents,agent_index,items,remaining_items_after_tentative):
        agents_num=len(normelized_agents)

        #update_mms_bounds:
        alpha_array=[0]*5
        alpha_array[0]=(0.75)*normelized_agents[agent_index].value(items[0])
        alpha_array[1]=(0.75)*normelized_agents[agent_index].value({items[agents_num-1],items[agents_num]})
        alpha_array[2]=(0.75)*normelized_agents[agent_index].value({items[2*agents_num-2],items[2*agents_num-1],items[2*agents_num]})
        alpha_array[3]=(0.75)*normelized_agents[agent_index].value({remaining_items_after_tentative[0],remaining_items_after_tentative[2*len(remaining_items_after_tentative)]})

        multiplyer=max(alpha_array)


def update_mms_bounds(agent):
    


# algo 4
def three_quarters_MMS_allocation(agents: List[AdditiveAgent], items: List[str]):
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
    
    num_agents=len(agents)
    if num_agents==0 or num_agents>len(items):
       return Allocation(agents=agents, bundles={})

    divide_by_array=[]
    for i in range(0,num_agents):
        divide_by_array[i]=agents[i].total_value()/num_agents

    normelized_agents=normalize_algo1(agents,divide_by_array,items)
    alloc_fixed_assignment=fixed_assignment(normelized_agents,items)
    if(len(normelized_agents)==0):
        return combine_allocations([alloc_fixed_assignment],agents)#use function to get value of alloc
    remaining_agents, tentative_aloc, remaining_items_after_tentative=tentative_assignment(items,normelized_agents)
    agents_num=len(normelized_agents)

    lowest_index_agent_in_n21=compute_n21(normelized_agents,items)
    while lowest_index_agent_in_n21!=None:
 


            


   
    return combine_allocations([alloc_initial_assignment,alloc_bag_filling], agents)


##### algo 7
def agents_conversion_to_ordered_instance(agents: List[AdditiveAgent],items:List[str]) :
    """
    The function sorted the list of additive agents such that their valuations for objects are unordered will become ordered.
    :param agents: A list of additive agents such that their valuations for objects are unordered.
    :return agents_sorted: A list of additive agents such that their valuations for objects are in ascending order.
    >>> a = AdditiveAgent({"x1": 2, "x2": 7, "x3": 10,"x4": 8, "x5": 3, "x6": 4,"x7": 7, "x8": 11}, name="A")
    >>> b = AdditiveAgent({"x1": 8, "x2": 7, "x3": 5,"x4": 3, "x5": 10, "x6": 2,"x7": 1, "x8": 4}, name="B")
    >>> c =  AdditiveAgent({"x1": 1, "x2": 2, "x3": 3,"x4": 4, "x5": 5, "x6": 6,"x7": 7, "x8": 8}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = agents_conversion_to_ordered_instance(agents,['x1','x2','x3','x4','x5','x6','x7','x8'])
    >>> print(a1)
    [A is an agent with a Additive valuation: x1=11 x2=10 x3=8 x4=7 x5=7 x6=4 x7=3 x8=2., B is an agent with a Additive valuation: x1=10 x2=8 x3=7 x4=5 x5=4 x6=3 x7=2 x8=1., C is an agent with a Additive valuation: x1=8 x2=7 x3=6 x4=5 x5=4 x6=3 x7=2 x8=1.]
    """
    sorted_agents={}
    for agent in agents:
        values=[agent.value(item) for item in items] 
        values.sort(reverse=True)
        agent_val_dict={}
        for item,val in zip(items,values):
           agent_val_dict[item]=val 
        sorted_agents[agent._name]=agent_val_dict
    sorted_agents_list = AdditiveAgent.list_from(sorted_agents)
    return sorted_agents_list #sorted

    
##### algo 8
def get_alpha_MMS_allocation_to_unordered_instance(agents_unordered: List[AdditiveAgent], ag_alloc: dict(), ordered_items: List[str]) :
    """
    Get the MMS allocation for agents unordered valuations.
    :param agents_unordered: Unordered valuations agents.
    :param agents_ordered: Ordered valuations agents.
    :param ordered_allocation: MMS allocation for ordered valuations agents.
    :return allocation: return the real allocation (the allocation for the unordered items)
    >>> ### allocation for 2 agents 3 objects
    >>> a = AdditiveAgent({"x1": 3, "x2": 10, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 10, "x2": 10, "x3": 9}, name="B")
    >>> agents=[a,b]
    >>> ag_alloc = dict({'A': ['x1'], 'B': ['x2']})
    >>> items_ordered = list(["x1", "x2", "x3"]) 
    >>> real_alloc = get_alpha_MMS_allocation_to_unordered_instance(agents,  ag_alloc, items_ordered)
    >>> print(real_alloc)
    {'A': ['x2'], 'B': ['x1']}

    >>> ### allocation for 1 agent, 1 object
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> ag_alloc = dict({'Alice': ['x']})
    >>> items_ordered = list(["x"]) 
    >>> real_alloc = get_alpha_MMS_allocation_to_unordered_instance(agents,  ag_alloc, items_ordered)
    >>> print(real_alloc)
    {'Alice': ['x']}

    >>> ### allocation for 3 agents 8 objects
    >>> a = AdditiveAgent({"x1": 2, "x2": 7, "x3": 10,"x4": 8, "x5": 3, "x6": 4,"x7": 7, "x8": 11}, name="A")
    >>> b = AdditiveAgent({"x1": 8, "x2": 7, "x3": 5,"x4": 3, "x5": 10, "x6": 2,"x7": 1, "x8": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 1, "x2": 2, "x3": 3,"x4": 4, "x5": 5, "x6": 6,"x7": 7, "x8": 8}, name="C")
    >>> agents=[a,b,c]
    >>> items_ordered = list(["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8"]) 
    >>> ag_alloc = dict({'A': ['x3', 'x4'], 'B': ['x1'], 'C': ['x2', 'x5']})
    >>> real_alloc =  get_alpha_MMS_allocation_to_unordered_instance(agents,  ag_alloc, items_ordered)
    >>> print(real_alloc)
    {'A': ['x3', 'x4'], 'B': ['x5'], 'C': ['x8', 'x7']}
    """
    real_alloc = dict()
    for i in agents_unordered:
        real_alloc[i.name()] = []
    sorted_agents_by_values = dict() # sorted agent by values
    for i in agents_unordered: 
        sorted_agents_by_values[i.name()] = i.valuation.map_good_to_value
        sorted_agents_by_values[i.name()] = dict(reversed(sorted(sorted_agents_by_values[i.name()].items(), key=lambda item: item[1])))
    
    for i in ordered_items:
        for key, val in ag_alloc.items():
            if(i in val): #if this agent get the next item
                x=next(iter(sorted_agents_by_values[key])) #best item for agent number "key"
                real_alloc[key].append(x)
                for key2, val2 in sorted_agents_by_values.items(): # remove the x item from all the agents
                    val2.pop(x)

    return real_alloc #real allocation

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
    #doctest.run_docstring_examples(alpha_MMS_allocation, globals())
    # doctest.run_docstring_examples(fixed_assignment, globals())
    #doctest.run_docstring_examples(tentative_assignment, globals())
    #doctest.run_docstring_examples(three_quarters_MMS_allocation, globals())
    #doctest.run_docstring_examples(agents_conversion_to_ordered_instance, globals())
    #doctest.run_docstring_examples(get_alpha_MMS_allocation_to_unordered_instance, globals())
