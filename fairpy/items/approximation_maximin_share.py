"""
Find an approximate MMS allocation.

Based on:
Jugal Garg and Setareh Taki,
["An Improved Approximation Algorithm for Maximin Shares"](https://www.sciencedirect.com/science/article/abs/pii/S0004370221000989),
Artificial Intelligence, 2021.

Programmers: Liad Nagi and Moriya Elgrabli
Date: 2022-05
"""

from fairpy import AdditiveAgent, AgentList
from typing import List,Any,Tuple,Dict
from copy import deepcopy
import logging
import math

logger = logging.getLogger(__name__)
three_quarters = 0.75                # The approximation ratio of the algorithm


def three_quarters_MMS_allocation(agents: AgentList, items:List[Any]=None)-> Dict[str,List[Any]]:
    """
        Compute a 3/4-mms allocation (all items are allocated)

        >>> data=AgentList({'agent0': {'x0': 1000.0, 'x1': 0.0, 'x2': 0.0}, 'agent1': {'x0': 0.0, 'x1': 1000.0, 'x2': 0.0}})
        >>> alloc_after_dividing_remaining_items=three_quarters_MMS_allocation(data)
        >>> alloc_after_dividing_remaining_items
        {'agent0': ['x0'], 'agent1': ['x1']}

        >>> data=AgentList([[1000.0,0.0,0.0],[0.0,1000.0,0.0]])
        >>> alloc_after_dividing_remaining_items=three_quarters_MMS_allocation(data)
        >>> alloc_after_dividing_remaining_items
        {'Agent #0': [0], 'Agent #1': [1]}
        """
    if items is None: items = agents.all_items()
    items = list(items)

    alloc, remaining_items = three_quarters_MMS_allocation_algorithm(agents, items) 

    # Build the real allocations with the values    
    # Map the result to somting like this "{'Alice': ['x3'], 'Bruce': ['x2'], 'Carl': ['x1']}"
    # dict_alloc=dict(alloc.map_agent_to_bundle())
   
    alloc_with_dividing_remaining_items=assign_remaining_items(alloc,remaining_items,agents)
    return alloc_with_dividing_remaining_items


def assign_remaining_items(alloc:dict, remaining_items:List[str], agents:AgentList)->dict:
    alloc=deepcopy(alloc)
    flag_some_agent_want=True

    while(flag_some_agent_want):
        #if there is round where no agent want any item- end 
        flag_some_agent_want=False
        for agent in reversed(agents):
            for item in remaining_items:
                val_for_item=agent.value(item)
                if val_for_item>0:
                    flag_some_agent_want=True
                    alloc[agent._name].append(item)
                    remaining_items.remove(item)
                    break
    return alloc


def three_quarters_MMS_allocation_algorithm(agents: AgentList, items:List[Any]=None)-> Tuple[List[List[Any]],List[Any]]:
    """
        Compute a 3/4-mms allocation, and possibly some remaining items.

        :param agents: list of agents in diffrent formattes, to preform alloction to
        :param items: list of items names, if wants to assing only some the items the agents has valuations to.
        :return allocation: alpha-mms allocation to each agent.  
        :return remaining_items: items tha remained after each agent got at least 3/4 of it's mms allocations. 

        ### allocation for 2 agents, 3 objects, with 0 valuations.
        >>> data={'agent0': {'x0': 1000.0, 'x1': 0.0, 'x2': 0.0}, 'agent1': {'x0': 0.0, 'x1': 1000.0, 'x2': 0.0}}
        >>> agents=AgentList(data)
        >>> alloc, remaining_items=three_quarters_MMS_allocation_algorithm(agents)
        >>> alloc
        {'agent0': ['x0'], 'agent1': []}
        >>> remaining_items
        ['x1', 'x2']

        ### allocation for 1 agent, 1 object
        >>> a = AdditiveAgent({"x": 2}, name="Alice")
        >>> agents=AgentList([a])
        >>> alloc, remaining_items = three_quarters_MMS_allocation_algorithm(agents)
        >>> alloc
        {'Alice': ['x']}
        >>> remaining_items
        []

        ### allocation for 2 agents, 2 objects 
        >>> a = AdditiveAgent({"x": 2, "y": 1}, name="Alice")
        >>> b = AdditiveAgent({"x": 1, "y": 2}, name="Blice")
        >>> agents = AgentList([a, b])
        >>> alloc, remaining_items  =  three_quarters_MMS_allocation_algorithm(agents)
        >>> print(alloc)
        {'Alice': ['x'], 'Blice': ['y']}
        >>> remaining_items
        []
        
        ### A different input format:
        ### allocation for 3 agents, 3 objects 
        >>> alloc, remaining_items = three_quarters_MMS_allocation_algorithm(AgentList([[2,3,1],[4,4,4],[2,5,3]]))
        >>> print(alloc)
        {'Agent #0': [1], 'Agent #1': [0], 'Agent #2': [2]}
        >>> remaining_items
        []

        ### detailed example: enter loop and adjusted by alpha.
        ### different agents preffer different items
        ### 3 agents 11 objects
        >>> agents =AgentList({"Alice":{"x1":17.5,"x2":35,"x3":17.5,"x4":17.5,"x5":35.5,"x6":19,"x7":1,"x8":1,"x9":1,"x10":1,"x11":1},\
        "Bruce":{"x1":1,"x2":35,"x3":17.5,"x4":17.5,"x5":17.5,"x6":19,"x7":1,"x8":1,"x9":1,"x10":35.5,"x11":1},\
        "Carl":{"x1":35.5,"x2":35,"x3":1,"x4":17.5,"x5":17.5,"x6":1,"x7":17.5,"x8":1,"x9":19,"x10":1,"x11":1}})
        >>> alloc,remaining_items =  three_quarters_MMS_allocation_algorithm(agents)
        >>> print(alloc)
        {'Alice': ['x5', 'x2'], 'Bruce': ['x10', 'x6'], 'Carl': ['x1', 'x9']}
        >>> remaining_items
        ['x3', 'x4', 'x7', 'x8', 'x11']
    """
    if items is None: items = agents.all_items()
    items = list(items)

    # algo 7 - sort valuations from largest to smallest
    ordered_agents = agents_conversion_to_ordered_instance(agents, items)

    # algo 4 
    alloc_for_ordered_valuations = three_quarters_MMS_subroutine(ordered_agents, items)

    # Map the result to somting like this "{'Alice': ['x3'], 'Bruce': ['x2'], 'Carl': ['x1']}"
    # alloc_for_ordered_valuations=dict(alloc_for_ordered_valuations.map_agent_to_bundle())
    
    # algo 8 - Get the real allocation
    real_alloc, remaining_items=get_alpha_MMS_allocation_to_unordered_instance(agents, alloc_for_ordered_valuations, items)

    return real_alloc, remaining_items

####
#### Algorithm 1
####

def alpha_MMS_allocation(agents: List[AdditiveAgent], alpha: float, mms_values: List[float], items: List[str])->Dict[str,List[Any]]:
    """
    Find alpha_MMS_allocation for the given agents and valuations.
    :param agents: valuations of agents, valuation are ordered in ascending order
    :param alpha: parameter for how much to approximate MMS allocation
    :param mms_values: mms_values of each agent inorder to normalize by them.
    :param items: items names sorted from the highest valued to the lowest
    :return allocation: alpha-mms allocation to each agent.

    ### allocation for 1 agent, 1 object
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> a1 = alpha_MMS_allocation(agents,0.5,[2],['x'])
    >>> print(a1)
    {'Alice': ['x']}

    ### allocation for 1 agent, 2 objects
    >>> b = AdditiveAgent({"x": 2, "y": 1}, name="Blice")
    >>> agents=[b]
    >>> a1 = alpha_MMS_allocation(agents,0.6,[3],['x','y'])
    >>> print(a1)
    {'Blice': ['x']}

    ### allocation for 2 agents, 2 objects
    >>> a = AdditiveAgent({"x": 2, "y": 1}, name="Alice")
    >>> agents = [a, b]
    >>> a1 = alpha_MMS_allocation(agents,1,[1,1],['x','y'])
    >>> print(a1)
    {'Alice': ['x'], 'Blice': ['y']}

    ### allocation for 3 agents, 3 objects (low alpha)
    >>> a = AdditiveAgent({"x1": 3, "x2": 2, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 4, "x2": 4, "x3": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 5, "x2": 2, "x3": 1}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alpha_MMS_allocation(agents,0.2,[1,4,1],['x1','x2','x3'])
    >>> print(a1)
    {'A': ['x1'], 'B': ['x2'], 'C': ['x3']}
        
    ### allocation with 3 agents, 8 objects
    >>> a = AdditiveAgent({"x1": 11, "x2": 10, "x3": 8,"x4": 7, "x5": 6, "x6": 5,"x7": 3, "x8": 2}, name="A")
    >>> b = AdditiveAgent({"x1": 100, "x2": 55, "x3": 50,"x4": 33, "x5": 12, "x6": 5,"x7": 4, "x8": 1}, name="B")
    >>> c = AdditiveAgent({"x1": 15, "x2": 15, "x3": 12,"x4": 9, "x5": 8, "x6": 8,"x7": 7, "x8": 5}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alpha_MMS_allocation(agents,0.75,[17,77,25],['x1','x2','x3','x4','x5','x6','x7','x8'])
    >>> print(a1)
    {'B': ['x1'], 'A': ['x3', 'x4'], 'C': ['x2', 'x5']}
        
    ### allocation with 3 agents, 8 objects
    >>> a = AdditiveAgent({"x1": 1, "x2": 1, "x3": 1,"x4": 1, "x5": 1, "x6": 1,"x7": 1, "x8": 1, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 2, "x2": 2, "x3": 2,"x4": 2, "x5": 2, "x6": 2,"x7": 1, "x8": 1, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="B")
    >>> c = AdditiveAgent({"x1": 2, "x2": 2, "x3": 2,"x4": 2, "x5": 2, "x6": 2,"x7": 2, "x8": 2, "x9": 1, "x10": 1,"x11": 1, "x12": 1}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = alpha_MMS_allocation(agents,0.9,[4,6,6],['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11','x12'])
    >>> print(a1)
    {'C': ['x5', 'x6', 'x7'], 'A': ['x1', 'x4', 'x12', 'x11'], 'B': ['x2', 'x3', 'x10', 'x9']}
    """
    num_agents=len(agents)
   
    for i in range (0,num_agents):
        if mms_values[i]==0:
            mms_values.pop(i)
            agents.pop(i)
    if len(agents)==0 or len(agents)>len(items):
       return {}
    normelized_agents=normalize(agents,mms_values,items)
    alloc_initial_assignment = initial_assignment_alpha_MSS(normelized_agents,items,alpha)
    if(len(normelized_agents)==0):
        return combine_allocations([alloc_initial_assignment],agents) #use function to get value of alloc
    alloc_bag_filling=bag_filling_algorithm_alpha_MMS(items,normelized_agents,alpha)

    return combine_allocations([alloc_initial_assignment,alloc_bag_filling], agents)




def willing_agent(agents:List[AdditiveAgent], bundle: List[str], threshold)->int:
    """
    return the lowest index agent that will be satisfied with bundle (the value of bundle is >= threshold)
    :param agents: valuations of agents
    :param bundle: the bundle of item to be given
    :param threshold: parameter for how much the bag mast be worth for agent to willing to accept it.
    
    :return index: the index of the lowest index agent that will be satisfied with the bundle
    >>> #
    >>> a = AdditiveAgent({"x": 0.5, "y": 0.3 ,"z":0.2}, name="Alice")
    >>> b = AdditiveAgent({"x": 0.4, "y": 0.8 ,"z":0.2}, name="Blice")    
    >>> agents=[a,b]
    >>> # empty bundle,insufficient - returns None
    >>> willing_agent(agents,[], 0.5)
    >>> # insufficient bundle - returns None
    >>> willing_agent(agents,["z"], 0.5)
    >>> # lowest index agent
    >>> willing_agent(agents,["x","z"], 0.6)
    0
    >>> # first agent isn't satisfied
    >>> willing_agent(agents,["x","y"],0.9)
    1
    """
    num_agents=len(agents)
    for i in range(0,num_agents):
        if agents[i].value(bundle)>=threshold:
            return i
    # returns none if no one is satisfied with the bundle or if len(agents) is 0 
    return None





####
#### Algorithm 2 
####

def initial_assignment_alpha_MSS(agents: List[AdditiveAgent], items: List[str], alpha: float)->Dict[str,List[Any]]:
    """
    Initial division for allocting agents according to their alpha-MMS.
    :param agents: valuations of agents, normalized such that MMS=1 for all agents, 
     and valuation are ordered in ascending order
    :param items: items names sorted from the highest valued to the lowest
    :param alpha: parameter for how much to approximate MMS allocation.
    :return allocation:  whats been allocated so far (in this function), items and agents are updated during function

    ### allocation for 1 agent, 1 object (this pass!)
    >>> a = AdditiveAgent({"x": 1}, name="Alice")
    >>> agents=[a]
    >>> a1 = initial_assignment_alpha_MSS(agents,['x'],0.75)
    >>> print(a1, agents)
    {'Alice': ['x']} []
    
    ### allocation for 1 agent, 2 object
    >>> b = AdditiveAgent({"x": 0.5, "y": 0.4}, name="Blice")
    >>> agents=[b]
    >>> a1 = initial_assignment_alpha_MSS(agents,['x','y'],0.6)
    >>> print(a1, agents)
    {'Blice': ['x', 'y']} []

    ### allocation for 2 agent, 2 object
    >>> a = AdditiveAgent({"x": 0.8, "y": 0.7}, name="Alice")
    >>> b = AdditiveAgent({"x": 0.7, "y": 0.7}, name="Blice")
    >>> agents=[a,b]
    >>> a1= initial_assignment_alpha_MSS(agents,['x','y'],0.6)
    >>> print(a1, agents)
    {'Alice': ['x'], 'Blice': ['y']} []
    
    ### allocation for 2 agent, 8 object
    >>> a = AdditiveAgent({"x1": 0.647059, "x2": 0.588235, "x3": 0.470588, "x4": 0.411765, "x5": 0.352941, "x6": 0.294118, "x7": 0.176471, "x8": 0.117647}, name="A")
    >>> b = AdditiveAgent({"x1": 1.298701, "x2": 0.714286, "x3": 0.649351, "x4": 0.428571, "x5": 0.155844, "x6": 0.064935, "x7": 0.051948, "x8": 0.012987}, name="B")
    >>> c =  AdditiveAgent({"x1": 0.6, "x2": 0.6, "x3": 0.48, "x4": 0.36, "x5": 0.32, "x6": 0.32, "x7": 0.28, "x8": 0.04}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = initial_assignment_alpha_MSS(agents,['x1','x2','x3','x4','x5','x6','x7','x8'],0.75)
    >>> print(a1, agents) # x6, x7, x8 weren't divided
    {'B': ['x1'], 'A': ['x3', 'x4'], 'C': ['x2', 'x5']} []
    """

    ag_alloc = {} 
    n = len(agents)-1
    #if thereare less object than agents, mms is 0 for every one.
    if(n+1>len(items)):
        return ag_alloc
        #return None 
    agent_names=[agent.name() for agent in agents]

    while(True):    # for every agents check if s1/s2/s3/s3>=alpha
        num_items=len(items)

        #fill si bundles
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
                # give bundle to agent
                ag_alloc[agents[willing_agent_index]._name] = si
                # remove given items agent 
                for item in si:
                    items.remove(item)
                agents.pop(willing_agent_index)
                # update number of agents
                n = n - 1
                # go to begining of outside loop and redefine the si bundles
                break
            elif si==s4_bundle:
                # no agent is satisfied by any of the si bundles
                return  ag_alloc #end of function



####
#### Algorithm 3
####

def bag_filling_algorithm_alpha_MMS(items: List[str],agents: List[AdditiveAgent], alpha: float) -> Dict[str,List[Any]]:
    """
    The algorithm allocates the remaining objects into the remaining agents so that each received at least α from his MMS.
    :param items: items names sorted from the highest valued to the lowest
    :param agents: valuations of agents, normalized such that MMS=1 for all agents, 
    and valuation are ordered in ascending order
    :param alpha: parameter for how much to approximate MMS allocation
    :return allocation: allocation for the agents. agents and items are updated during function.
    
    ### allocation for 1 agent, 0 object
    >>> a = AdditiveAgent({"x": 1}, name="Alice" )
    >>> agents=[a]
    >>> a1 = bag_filling_algorithm_alpha_MMS(['x'],agents, 1)
    Traceback (most recent call last):
    ...
    Exception: ERROR. Could not create an MMS allocation that satisfies agents.
    
    ### allocation for 1 agent, 3 object (high alpha)
    >>> a = AdditiveAgent({"x1": 0.54, "x2": 0.3, "x3": 0.12}, name="Alice")
    >>> agents=[a]
    >>> a1 = bag_filling_algorithm_alpha_MMS(['x1','x2','x3'],agents, 0.9)
    >>> print(a1)
    {'Alice': ['x1', 'x2', 'x3']}

    ### allocation for 2 agent, 9 object
    >>> a = AdditiveAgent({"x1": 0.25, "x2": 0.25, "x3": 0.25, "x4": 0.25, "x5": 0.25, "x6": 0.25, "x7": 0.25, "x8": 0.25, "x9": 0.25 }, name="A")
    >>> b = AdditiveAgent({"x1": 0.333333, "x2": 0.333333, "x3": 0.333333, "x4": 0.333333, "x5": 0.166667, "x6": 0.166667, "x7": 0.166667, "x8": 0.166667, "x9": 0.166667 }, name="B")
    >>> agents=[a,b]
    >>> a1 = bag_filling_algorithm_alpha_MMS(['x1','x2','x3','x4','x5','x6','x7','x8','x9'],agents,0.9)
    >>> print(a1)
    {'A': ['x1', 'x4', 'x9', 'x8'], 'B': ['x2', 'x3', 'x7', 'x6']}
    """

    agents_num=len(agents)
    items_num =len(items)


    if (agents_num<=0 or items_num<=0):
        return None

    agent_names=[agent.name() for agent in agents]  #kept for returning alloation at the end      
    bundles={}
    

    while agents_num>0:
        mirror_index=2*agents_num-1
        # has to be both index- because if the agent remained after initial assignment,
        # it means no single item is enough, so there are at least 2*agents_num items
        # may no be if tried alpha bigger then 0.75
        if (len(items)>0 and len(items)>mirror_index ): 
            bundle_name_arr=[items[0],items[mirror_index]]
            w_agent=willing_agent(agents,bundle_name_arr,alpha)
            last_item=len(items)-1
            while(w_agent==None and last_item>=2*agents_num): 
                bundle_name_arr.append(items[last_item]) #add another item to bundle
                last_item-=1
                w_agent=willing_agent(agents,bundle_name_arr,alpha)
            
            if w_agent==None: #there is not any devison that will satisfy any agent
                raise Exception("ERROR. Could not create an MMS allocation that satisfies agents. ")
            
            bundles[agents[w_agent]._name]=bundle_name_arr #give bundle to agent
            #remove agent
            agents.pop(w_agent)
            #remove items
            for obj_index in bundle_name_arr:
                items.remove(obj_index) 
            
            agents_num=len(agents) #update
        else:
            raise Exception("ERROR. Could not create an MMS allocation that satisfies agents.")

    return bundles


def normalize(agents: List[AdditiveAgent], divided_by_values: List[float],items: List[str])->List[AdditiveAgent]:
    """
    normalize agents by deviding them in theirvalue in the given mms_values list
    :param agents: valuations of agents, valuation are ordered in assenting order
    :param divided_by_values: mms_value of each agents / values fo each agents valuations to be divided by.
    :param items: items names sorted from the highest valued to the lowest
    :return agents: new list of agents with normelized valuations
    >>> a = AdditiveAgent({"x1": 3, "x2": 2, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 4, "x2": 4, "x3": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 5, "x2": 2, "x3": 1}, name="C")
    >>> agents=[a,b,c]
    >>> list_agents= normalize(agents, [1,4,2],['x1','x2','x3'])
    >>> list_agents[0]
    A is an agent with a Additive valuation: x1=3.0 x2=2.0 x3=1.0.
    >>> list_agents[1]
    B is an agent with a Additive valuation: x1=1.0 x2=1.0 x3=1.0.
    >>> list_agents[2]
    C is an agent with a Additive valuation: x1=2.5 x2=1.0 x3=0.5.
    >>> normalize([a], [0,0,0],['x1','x2','x3'])
    Traceback (most recent call last):
    ZeroDivisionError: division by zero
    """
    normelized_agents={}
    num_agents=len(agents)
    for i in range(0,num_agents):
        normelized_agents[agents[i]._name]={}
        for item in items:
            normelized_agents[agents[i]._name][item]=(agents[i].value(item))/divided_by_values[i]
    return AdditiveAgent.list_from(normelized_agents)

def combine_allocations(allocations: List[ Dict[str,List[Any]] ], agents: List[AdditiveAgent])->Dict[str,List[Any]]:
    """
    combine list of allocations to a single alloation,
    also allows for different valuations of agents in the returned allcation.

    Assume:
    1. if agents is allocated in one allocation, there isn't another allocation for him
    2. no item is allocated twice

    :param allocations: list of allocations to be combined
    :param agents: valuations of agents, valuation are ordered in ascending order (the full list of agents from all the different allocations)
    :return allocation: the combined allocations

    ### combine a few allocation
    >>> from dicttools import stringify
    >>> a = AdditiveAgent({"x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6}, name="Alice")
    >>> b = AdditiveAgent({"x1": 1, "x2": 2, "x3": 3, "x4": 4, "x5": 5, "x6": 6}, name="Bruce")
    >>> a1 = {"Alice":[], "Bruce": ["x1","x5","x3"]}
    >>> a2 = {"Alice":["x2","x6"], "Bruce": {}}
    >>> combined = combine_allocations([a1,a2], [a,b])
    >>> stringify(combined)
    "{Alice:['x2', 'x6'], Bruce:['x1', 'x5', 'x3']}"

    # ### same allcations, different valuations
    # >>> c = AdditiveAgent({"x1": 0.1, "x2": 0.2, "x3": 0.3, "x4": 0.4, "x5": 0.5, "x6": 0.6}, name="Alice")
    # >>> d = AdditiveAgent({"x1": 0.1, "x2": 0.2, "x3": 0.3, "x4": 0.4, "x5": 0.5, "x6": 0.6}, name="Bruce")
    # >>> combine_allocations([a1,a2], [c,d])
    # Alice gets {x2,x6} with value 0.8.
    # Bruce gets {x1,x3,x5} with value 0.9.
    # <BLANKLINE>
    """
    from copy import copy
    combined_allocation=None
    for alloc in allocations:
        if alloc is None: continue
        if combined_allocation is None:
            combined_allocation=copy(alloc)
        else:
            for name,assignment in alloc.items():
                if name not in combined_allocation or len(combined_allocation[name])==0:
                    combined_allocation[name]=copy(assignment)
    return combined_allocation





####
#### Algorithm 4
####

def three_quarters_MMS_subroutine(agents: List[AdditiveAgent], items: List[str])->Dict[str,List[Any]]:
    """
    Finds three-quarters MMS-allocation for the given agents and valuations.
    :param agents: valuations of agents, valuation are ordered in assending order
    :param items: items names sorted from the highest valued to the lowest
    :return allocation: three-quarters MMS-allocation for all agents for ordered valuations.
    
    ### allocation for 1 agent, 1 object
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> a1 = three_quarters_MMS_subroutine(agents,["x"])
    >>> print(a1)
    {'Alice': ['x']}

    ### allocation for 1 agent, 2 objects
    >>> b = AdditiveAgent({"x": 2, "y": 1}, name="Blice")
    >>> agents=[b]
    >>> a1 = three_quarters_MMS_subroutine(agents,["x","y"])
    >>> print(a1)
    {'Blice': ['x', 'y']}

    ### allocation for 2 agents, 2 objects
    >>> a = AdditiveAgent({"x": 2, "y": 1}, name="Alice")
    >>> agents = [a, b]
    >>> a1 = three_quarters_MMS_subroutine(agents,["x","y"])
    >>> print(a1)
    {'Alice': ['x'], 'Blice': ['y']}

    ### allocation for 3 agents, 3 objects (low alpha)
    >>> a = AdditiveAgent({"x1": 3, "x2": 2, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 4, "x2": 4, "x3": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 5, "x2": 2, "x3": 1}, name="C")
    >>> agents=[a,b,c]
    >>> a1 = three_quarters_MMS_subroutine(agents,["x1","x2","x3"])
    >>> print(a1)
    {'A': ['x1'], 'B': ['x2'], 'C': ['x3']}
        
    ### detailed example: enter loop and adjusted by alpha.
    ### 3 agents 11 objects
    >>> agents = AdditiveAgent.list_from({"Alice":{"x1":35.5,"x2":35,"x3":19,"x4":17.5,"x5":17.5,"x6":17.5,"x7":1,"x8":1,"x9":1,"x10":1,"x11":1},\
    "Bruce":{"x1":35.5,"x2":35,"x3":19,"x4":17.5,"x5":17.5,"x6":17.5,"x7":1,"x8":1,"x9":1,"x10":1,"x11":1},\
    "Carl":{"x1":35.5,"x2":35,"x3":19,"x4":17.5,"x5":17.5,"x6":17.5,"x7":1,"x8":1,"x9":1,"x10":1,"x11":1}})
    >>> alloc = three_quarters_MMS_subroutine(agents,['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11'])
    >>> print(alloc)
    {'Alice': ['x3', 'x4'], 'Bruce': ['x2', 'x5'], 'Carl': ['x1', 'x6']}
    """
    items=deepcopy(items)
    num_agents=len(agents)
    if num_agents==0 or num_agents>len(items):
       return {}
    
    #normalize
    divide_by_array=[0]*num_agents
    for i in range(0,num_agents):
        divide_by_array[i]=agents[i].total_value()/num_agents

    normelized_agents=normalize(agents,divide_by_array,items)

    #algo 5
    alloc_fixed_assignment=fixed_assignment(normelized_agents,items)
    if(len(normelized_agents)==0):
        return combine_allocations([alloc_fixed_assignment],agents)#use function to get value of alloc

    #algo 6
    remaining_agents,tentative_alloc,remaining_items_after_tentative=tentative_assignment(items=items,agents=normelized_agents)
    
    lowest_index_agent_in_n21=compute_n21(normelized_agents,items)
    while lowest_index_agent_in_n21!=None:
        #update mms bounds
        alpha=compute_max_alphas(normelized_agents,remaining_agents,lowest_index_agent_in_n21,items,remaining_items_after_tentative)
        normelized_agents=update_bound(normelized_agents,alpha,items,lowest_index_agent_in_n21) 

        #algo 5
        alloc_fixed_assignment=fixed_assignment(normelized_agents,items)
        if(len(normelized_agents)==0):
            return combine_allocations([alloc_fixed_assignment],agents) #use function to get value of alloc
        
        #algo 6
        remaining_agents,tentative_alloc,remaining_items_after_tentative=tentative_assignment(items=items,agents=normelized_agents)
        #update val for loop
        lowest_index_agent_in_n21=compute_n21(normelized_agents,items)

    #make all tentative assignments final
    normelized_agents=remaining_agents
    items=remaining_items_after_tentative

    bag_filling_alloc=bag_filling_algorithm_alpha_MMS(items=items,agents=normelized_agents,alpha=0.75)
    return combine_allocations([alloc_fixed_assignment,tentative_alloc,bag_filling_alloc],agents) 






####
#### Algorithm 5
####

def fixed_assignment(agents: List[AdditiveAgent], items: List[str])->Dict[str,List[Any]]:
    """
    The function allocates what can be allocated without harting others
    (each allocated agent gets 3/4 of his own MMS value,
    without casing others not to get their MMS value)
    :param agents: valuations of agents, normalized such that MMS <=1 for all agents
    :param items: items names sorted from the highest valued to the lowest
    :return allocation: What been allocated so far, and changes values of agents and items 
    
    ### fixed_assignment for one agent, one object
    >>> a = AdditiveAgent({"x": 1}, name="Alice")
    >>> agents=[a]
    >>> alloc=fixed_assignment(agents,["x"])
    >>> print(alloc)
    {'Alice': ['x']}
    >>> agents #check agents changed
    []

    ### fixed_assignment for two agent, one objects
    >>> b = AdditiveAgent({"x": 3.333333}, name="Bruce")
    >>> c = AdditiveAgent({"x":2}, name="Carl")
    >>> agents=[b,c]
    >>> alloc=fixed_assignment(agents,["x"])
    >>> print(alloc)
    {}

    >>> agents #check agents hasn't changed
    [Bruce is an agent with a Additive valuation: x=3.333333., Carl is an agent with a Additive valuation: x=2.]
    
    ### fixed_assignment for two agent, three objects #
    >>> b = AdditiveAgent({"x": 1.2,"y": 0.24, "z":0.56}, name="Bruce")
    >>> c = AdditiveAgent({"x":1.125,"y": 0.875,"z":0.25}, name="Carl")
    >>> agents=[b,c]
    >>> alloc=fixed_assignment(agents,["x","y","z"])
    >>> print(alloc)
    {'Bruce': ['x'], 'Carl': ['y']}
    >>> agents #check agents changed
    []
    """
    ag_alloc = {}  #agents allocations
    agent_names=[agent.name() for agent in agents]
    n = len(agents)
    if(n>len(items)): #if there are more agents then object- mms is 0 for everyone.
        return ag_alloc #return empty alloc 
    
    val_arr = dict() #values of agents
    i=0
    flag_n_changed=False
    while i< n:
        agent=agents[i]
        #remove agents with 0 valuations to all items
        if is_sum_valuations_zero(agent,None,items):
            agents.remove(agent)
            n-=1
            flag_n_changed=True
        else:
            val_arr[agent.name()] = agent.valuation.map_good_to_value
            i+=1

    if flag_n_changed: #if number of agents change, need to update valuations.
        val_arr = update_val([], val_arr, n)

        
    si=0
    while(si<3):
        agent_index=0
        while(agent_index<n):    # for every agents check if s1/s2/s3>=three_quarters
      
            nameI=agents[agent_index].name()  #agent name
            agent=val_arr[nameI]    #agent[agent_index]


            if(si==0):
                bag_si = (agent.get(items[0]))
            elif(si==1 and n<len(items)): # check if we have more then n items
                bag_si = agent.get(items[n-1]) + agent.get(items[n])
            elif(si==2 and 2*n<len(items)): # check if we have more then 2*n items
                bag_si = (agent.get(items[(2*n-1)-1])) + (agent.get(items[(2*n)-1])) + (agent.get(items[(2*n+1)-1]))
            else:
                bag_si = -1

            if(bag_si>=three_quarters):
                if(si==0):
                    ag_alloc[str(nameI)] = [items[0]]
                    val_arr.pop(str(nameI))
                    val_arr = update_val([items[0]], val_arr, n-1)
                    items.remove(items[0])
                    agents.remove(agents[agent_index])
                    n = n - 1
                    agent_index=n+1
                    si=-1
                elif(si==1):
                    ag_alloc[str(nameI)] = [items[n-1] , items[n]]
                    val_arr.pop(str(nameI))
                    val_arr = update_val([items[n-1] , items[n]], val_arr, n-1)
                    items.remove(items[n])
                    items.remove(items[n-1])
                    agents.remove(agents[agent_index])
                    n = n - 1
                    agent_index=n+1
                    si=-1
                elif(si==2):
                    ag_alloc[str(nameI)] = [items[(2*n-1)-1], items[(2*n)-1] , items[(2*n+1)-1]]
                    val_arr.pop(str(nameI))
                    val_arr = update_val([items[(2*n-1)-1], items[(2*n)-1] , items[(2*n+1)-1]], val_arr, n-1)
                    items.remove(items[(2*n+1)-1])
                    items.remove(items[(2*n)-1])
                    items.remove(items[(2*n-1)-1])
                    agents.remove(agents[agent_index])
                    n = n - 1
                    agent_index=n+1
                    si=-1
                
            else:
                agent_index = agent_index + 1
            #if items has been removed, 
            #check if some agents valuations become 0 and remove them
            if (bag_si>=three_quarters):
                i=0
                flag_removed_agents=False
                while i<n:
                    agent=agents[i]
                    name=agent.name()
                    agent_curr_val=val_arr[name]
                    if is_sum_valuations_zero(agent,agent_curr_val,items): #remove agent satisfied with 0
                        agents.remove(agents[i])
                        n-=1   
                        flag_removed_agents=True
                        val_arr.pop(name)
                    else:
                        i+=1  
                if (flag_removed_agents):         
                    val_arr = update_val([], val_arr, n) #if number of agents change, need to update valuations.
        
                 
        si=si+1

    return ag_alloc





####
#### Algorithm 6
####
def tentative_assignment(agents: List[AdditiveAgent], items: List[str])->Tuple[List[AdditiveAgent], Dict[str,List[Any]], List[str]]:
    """
    The function allocates temporarily what can be allocated, can maybe hart others it not normalized close enough to the mms values.
    :param agents: Valuations of agents,such that bundles of objects at the positions:
     {0}, {n-1,n},{2n-2,2n-1,2n} not satisties for them,
     and normalized such that MMS <=1 for all agents.
    :param agents: agents with  valuations, normalized such that MMS <=1 for all agents
    :param items: items names sorted from the highest valued to the lowest
    :return remaining_agents: agents (and objects) that still need allocation
    :return allocation: whats been temporarily allocated so far
    :return remaining_items: items that remained after  whats been allocated so far

    ### doesn't find any allocation.
    >>> a = AdditiveAgent({"01": 0.724489796, "02": 0.714285714, "03": 0.387755102, "04": 0.357142857, "05": 0.357142857, "06": 0.357142857, "07": 0.020408163, "08": 0.020408163, "09": 0.020408163, "10": 0.020408163, "11": 0.020408163}, name="Alice")
    >>> b = AdditiveAgent({"01": 0.724489796, "02": 0.714285714, "03": 0.387755102, "04": 0.357142857, "05": 0.357142857, "06": 0.357142857, "07": 0.020408163, "08": 0.020408163, "09": 0.020408163, "10": 0.020408163, "11": 0.020408163}, name="Bruce")
    >>> c = AdditiveAgent({"01": 0.724489796, "02": 0.714285714, "03": 0.387755102, "04": 0.357142857, "05": 0.357142857, "06": 0.357142857, "07": 0.020408163, "08": 0.020408163, "09": 0.020408163, "10": 0.020408163, "11": 0.020408163}, name="Carl")
    >>> agents = [a,b,c]
    >>> items = list(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"])
    >>> remaining_agents, alloc, remaining_items = tentative_assignment(agents, items)
    >>> print(remaining_agents)
    [Alice is an agent with a Additive valuation: 01=0.724489796 02=0.714285714 03=0.387755102 04=0.357142857 05=0.357142857 06=0.357142857 07=0.020408163 08=0.020408163 09=0.020408163 10=0.020408163 11=0.020408163., Bruce is an agent with a Additive valuation: 01=0.724489796 02=0.714285714 03=0.387755102 04=0.357142857 05=0.357142857 06=0.357142857 07=0.020408163 08=0.020408163 09=0.020408163 10=0.020408163 11=0.020408163., Carl is an agent with a Additive valuation: 01=0.724489796 02=0.714285714 03=0.387755102 04=0.357142857 05=0.357142857 06=0.357142857 07=0.020408163 08=0.020408163 09=0.020408163 10=0.020408163 11=0.020408163.]
    >>> print(alloc)
    {}
    >>> print(remaining_items)
    ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']
    
    ### 3 agents 11 objects - ex 1
    >>> a = AdditiveAgent({"01": 0.727066, "02": 0.727066, "03": 0.39525, "04": 0.351334, "05": 0.351334, "06": 0.346454, "07": 0.022934, "08": 0.022934, "09": 0.022934, "10": 0.022934, "11": 0.022934}, name="Alice")
    >>> b = AdditiveAgent({"01": 0.723887, "02": 0.723887, "03": 0.393522, "04": 0.349798, "05": 0.349798, "06": 0.344939, "07": 0.022834, "08": 0.022834, "09":  0.022834, "10": 0.022834, "11": 0.022834}, name="Bruce")
    >>> c = AdditiveAgent({"01": 0.723887, "02": 0.723887, "03": 0.393522, "04": 0.349798, "05": 0.349798, "06": 0.344939, "07": 0.022834, "08": 0.022834, "09": 0.022834, "10": 0.022834, "11": 0.022834}, name="Carl")
    >>> agents = [a,b,c]
    >>> items = list(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"])
    >>> remaining_agents, alloc, remaining_items = tentative_assignment(agents, items)
    >>> print(remaining_agents)
    []
    >>> agents #check tentative assignment hasn't changed agents.
    [Alice is an agent with a Additive valuation: 01=0.727066 02=0.727066 03=0.39525 04=0.351334 05=0.351334 06=0.346454 07=0.022934 08=0.022934 09=0.022934 10=0.022934 11=0.022934., Bruce is an agent with a Additive valuation: 02=0.6425184619754313 03=0.349288148831925 04=0.3104789462472484 05=0.3104789462472484 06=0.3061661222750834 08=0.020267343605765816 09=0.020267343605765816 10=0.020267343605765816 11=0.020267343605765816., Carl is an agent with a Additive valuation: 02=0.5988748660801078 03=0.32556246354690194 08=0.01889066759324754 09=0.01889066759324754 10=0.01889066759324754 11=0.01889066759324754.]
    >>> print (alloc)
    {'Alice': ['01', '07'], 'Bruce': ['04', '05', '06'], 'Carl': ['02', '03']}
    >>> print (remaining_items)
    ['08', '09', '10', '11']
    
    ### 3 agents 10 object
    >>> a = AdditiveAgent({"01": 0.727272, "02": 0.727272, "03": 0.318182, "04": 0.318182, "05": 0.318182, "06": 0.318182, "07": 0.090909, "08": 0.090909, "09": 0.045454, "10": 0.045454}, name="Alice")
    >>> b = AdditiveAgent({"01": 0.727272, "02": 0.727272, "03": 0.318182, "04": 0.318182, "05": 0.318182, "06": 0.318182, "07": 0.090909, "08": 0.090909, "09": 0.045454, "10": 0.045454}, name="Bruce")
    >>> c = AdditiveAgent({"01": 0.727272, "02": 0.727272, "03": 0.318182, "04": 0.318182, "05": 0.318182, "06": 0.318182, "07": 0.090909, "08": 0.090909, "09": 0.045454, "10": 0.045454}, name="Carl")
    >>> agents = [a,b,c]
    >>> items = list(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"])
    >>> remaining_agents, alloc, remaining_items = tentative_assignment(agents, items)
    >>> print(remaining_agents)
    []
    >>> print (alloc)
    {'Alice': ['01', '07'], 'Bruce': ['04', '05', '06'], 'Carl': ['02', '03']}
    >>> print ( remaining_items)
    ['08', '09', '10']
    """
    ag_alloc = {} 
    agent_names=[agent.name() for agent in agents]

    n = len(agents)
    if(n>len(items)):
        return agents, ag_alloc, items

    #deepcopy of items and agents
    agents_temp = list()
    items_temp = list() 
    flag_n_changed=False

    for agent in agents:
        if  not is_sum_valuations_zero(agent,None,items):    #remove agents with 0 valuations to all items
            agents_temp.append( AdditiveAgent(agent.valuation.map_good_to_value, name=agent.name()))
        else:
            n-=1
            flag_n_changed=True
    for i in items:
        items_temp.append(i)
    
    val_arr = dict() #values of agents
    for agent in agents_temp:
        val_arr[agent.name()] = agent.valuation.map_good_to_value
    
    if flag_n_changed: #if number of agents change, need to update valuations.
        val_arr = update_val([], val_arr, n)
     
    si=0
    while(si<4):
        agent_index=0 
        while(agent_index<n):    # for every agents check if s1/s2/s3>=three_quarters
            nameI=agents_temp[agent_index].name()
            agent=val_arr[nameI]
            
            if(si==0):
                bag_si = (agent.get(items_temp[0]))
            elif(si==1 and n<len(items)): # check if we have more then n items
                bag_si = agent.get(items_temp[n-1]) + agent.get(items_temp[n])
            elif(si==2 and (2*n)<len(items)): # check if we have more then 2*n items
                bag_si = (agent.get(items_temp[(2*n-1)-1])) + (agent.get(items_temp[(2*n)-1])) + (agent.get(items_temp[(2*n+1)-1]))
            elif(si==3 and (2*n)<len(items)): # check if we have more then 2*n+1 items
                bag_si = (agent.get(items_temp[0])) +  (agent.get(items_temp[(2*n+1)-1]))
            else:
                bag_si = -1

            if(bag_si>=three_quarters):
                if(si==0):
                    ag_alloc[str(nameI)] = [items_temp[0]]
                    val_arr.pop(str(nameI))
                    val_arr = update_val([items_temp[0]], val_arr, n-1)
                    items_temp.remove(items_temp[0])
                    agents_temp.remove(agents_temp[agent_index])
                    n = n - 1
                    agent_index=n+1
                    si=-1
                elif(si==1):
                    ag_alloc[str(nameI)] = [items_temp[n-1] , items_temp[n]]
                    val_arr.pop(str(nameI))
                    val_arr = update_val([items_temp[n-1] , items_temp[n]], val_arr, n-1)
                    items_temp.remove(items_temp[n])
                    items_temp.remove(items_temp[n-1])
                    agents_temp.remove(agents_temp[agent_index])
                    n = n - 1
                    agent_index=n+1
                    si=-1
                elif(si==2):
                    ag_alloc[str(nameI)] = [items_temp[(2*n-1)-1], items_temp[(2*n)-1] , items_temp[(2*n+1)-1]]
                    val_arr.pop(str(nameI))
                    val_arr = update_val([items_temp[(2*n-1)-1], items_temp[(2*n)-1] , items_temp[(2*n+1)-1]], val_arr, n-1)
                    items_temp.remove(items_temp[(2*n+1)-1])
                    items_temp.remove(items_temp[(2*n)-1])
                    items_temp.remove(items_temp[(2*n-1)-1])
                    agents_temp.remove(agents_temp[agent_index])
                    n = n - 1
                    agent_index=n+1
                    si=-1
                elif(si==3):
                    ag_alloc[str(nameI)] = [items_temp[0],  items_temp[(2*n+1)-1]]
                    val_arr.pop(str(nameI))
                    val_arr = update_val([items_temp[0],  items_temp[(2*n+1)-1]], val_arr, n-1)
                    items_temp.remove(items_temp[(2*n+1)-1])
                    items_temp.remove(items_temp[0])
                    agents_temp.remove(agents_temp[agent_index])
                    n = n - 1
                    agent_index=n+1
                    si=-1
            else:
                agent_index = agent_index + 1
            #if items has been removed, 
            #check if some agents valuations become 0 and remove them
            if (bag_si>=three_quarters):
                i=0
                flag_removed_agents=False
                while i<n:
                    agent=agents_temp[i]
                    name= agent.name()
                    agent_curr_val=val_arr[name]
                    if is_sum_valuations_zero(agent,agent_curr_val,items_temp): #remove agent satisfied with 0
                        
                        agents_temp.remove(agents_temp[i])
                        n-=1   
                        flag_removed_agents=True
                        val_arr.pop(name)

                    else:
                        i+=1  
                if (flag_removed_agents):         
                    val_arr = update_val([], val_arr, n) #if number of agents change, need to update valuations.

        si=si+1
        
    return agents_temp, ag_alloc, items_temp  

def compute_n21(normelized_agents,items)->int:
    """
    The function computes l,h in order to find if there are agents in the set n21.
    :param normelized_agents: valuations of agents, normalized such that MMS <=1 for all agents
    :param items: items names sorted from the highest valued to the lowest
    :return agent_index: the lowest index of agent in n21. if there isn't such agent, returns None 
    >>> # has agents in n21' returns lowest
    >>> normelized_agents = AdditiveAgent.list_from({"A":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163},\
    "B":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163},\
    "C":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163}})
    >>> compute_n21(normelized_agents,["x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","x11"])	
    0
    >>> #not has enough items						
    >>> normelized_agents = AdditiveAgent.list_from({"A":{"x1":0.735849057,"x2":0.679245283,"x3":0.367924528,"x4":0.367924528,"x5":0.367924528,"x6":0.283018868,"x7":0.198113208},\
    "B":{"x1":0.735849057,"x2":0.679245283,"x3":0.367924528,"x4":0.367924528,"x5":0.367924528,"x6":0.283018868,"x7":0.198113208},\
    "C":{"x1":0.735849057,"x2":0.679245283,"x3":0.367924528,"x4":0.367924528,"x5":0.367924528,"x6":0.283018868,"x7":0.198113208}})
    >>> compute_n21(normelized_agents,[])	
    Traceback (most recent call last):
    Exception: ERROR. not enough items if passed initial assignment
    """
 
    agents_num=len(normelized_agents)

    #calculate l,h,sum of bundles of each agents
    l=[0] * agents_num
    h=[0] * agents_num
    sum=[0] * agents_num 
    for i in range(0,agents_num):
        mirror_index=2*agents_num-i-1
        # has to be both index- because if the agent remained after initial assignment,
        # it means no single item is enough, so there are at least 2*agents_num items
        if not (len(items)>0 and len(items)>mirror_index ):
            raise Exception("ERROR. not enough items if passed initial assignment")

        bundle_i=[items[i],items[mirror_index]]
        for agent_index in range(0,agents_num):
            bundle_val=normelized_agents[agent_index].value(bundle_i)
            if bundle_val<three_quarters:
                l[agent_index]+=1
                sum[agent_index]+=bundle_val
            elif bundle_val>1:
                h[agent_index]+=1
    

    #go through all agents, starts from lowest index, and check if belong to n21
    for agent_index in range(0,agents_num):
        x_agent=(0.75)*l[agent_index]-sum[agent_index]
        all_items=normelized_agents[agent_index].valuation.map_good_to_value
        lowest_value_items=normelized_agents[agent_index].value_except_best_c_goods(bundle=all_items,c=2*agents_num) # v_i(M\J)
        #if this agent belong to N21
        if(h[agent_index]>0 and h[agent_index]>l[agent_index] and (x_agent+l[agent_index]/8)>lowest_value_items): 
            return agent_index
    #if no agent belongs to N21
    return None

def compute_sigma_for_given_alpha(bundles:List[float],alpha:float)->float:
    """
    This is a helper function to compute_alpha5_using_binary_search.
    the function computes one side of the inequality .
    :param bundles: valuations of the bags from B1 to Bk, were k is number of agents
    :param alpha: the potential alpha5- sigma is computed with it
    :return sigma: one side of the inequality
    >>> bundles=[0.74,0.75,0.50,1.02] 
    >>> alpha = 0.92
    >>> round(compute_sigma_for_given_alpha(bundles=bundles,alpha=alpha),6)
    0.331522
    >>> bundles=[0.74,0.75,0.72] 
    >>> alpha = 0.9
    >>> compute_sigma_for_given_alpha(bundles=bundles,alpha=alpha)
    0.0
    >>> bundles=[0.74,0.73] 
    >>> alpha = 0.99
    >>> round(compute_sigma_for_given_alpha(bundles=bundles,alpha=alpha),6)
    0.265152
    """
    sum=0
    count=0
    for bundle in bundles:
        if(bundle/alpha)<0.75:
           count+=1
           sum+=0.75-bundle/alpha
    return sum+(1/8)*count 
            
def compute_alpha5_using_binary_search(bundles:List[float],lowest_valued_items:float,rounds:int=20)->float:
    """
    This function computes an approximation of alpha5 by using binary search 
    we choose alpha, calculate vi(M\ J)/alpha and the sum from the other side
    if vi(M\ J)/alpha <= sum, we grow alpha, else- we lower it.
    :param bundles: valuations of the bags from B1 to Bk, were k is number of agents
    :param lowest_valued_items: the value of M\ J
    :param rounds: number of rounds the binary search is executed.
    :return alpha5: approximation of alpha 5
    >>> # for 3 agents, each with the following valuation's:
    >>> # x1=0.724489796	x2=0.714285714	x3=0.387755102	x4=0.357142857	x5=0.357142857	x6=0.357142857	
    >>> # x7=0.020408163 x8=0.020408163	x9=0.020408163	x10=0.020408163	x11=0.020408163
    >>> bundles=[0.744897959,1.071428571,1.081632653]
    >>> lowest_valued_items=0.102040816
    >>> alpha5=compute_alpha5_using_binary_search(bundles,lowest_valued_items)
    >>> alpha5 < 1
    True
    >>> alpha5 > 0
    True
    >>> sum=compute_sigma_for_given_alpha(bundles,alpha5)
    >>> sum<=(lowest_valued_items/alpha5)
    True
    >>> bundles=[0.74,1.02,1.03]
    >>> lowest_valued_items =0.198
    >>> alpha5=compute_alpha5_using_binary_search(bundles,lowest_valued_items)
    >>> alpha5 < 1
    True
    >>> alpha5 > 0
    True
    >>> sum=compute_sigma_for_given_alpha(bundles,alpha5)
    >>> sum<=(lowest_valued_items/alpha5)
    True
    """
    
    # Using binary search, in 20 iterations we can find alpha with accuracy of 1 to million.
    edges=[1,0]
    # alpha=0.5
    alpha=(edges[0]+edges[1])/2 

    i=0;
    while i<rounds:
        sum=compute_sigma_for_given_alpha(bundles,alpha)
        if sum<=(lowest_valued_items/alpha):
            edges[1]=alpha #make lower edge higher
        else:
            edges[0]=alpha #lower the upper edge
        alpha=(edges[0]+edges[1])/2 
        i+=1
    return alpha
    
    

def compute_max_alphas(agents,agents_after_tentative_assignment,agent_index,items,remaining_items_after_tentative)->float:
    """
    This is wrap function for a function computes alpha1 to alpha5 as part of updating mms upper bound
    the function returns the max valued alpha, inorder to allow for testing

    >>> ### before calling compute_alphas agent is in N21
    >>> ### after updating bound by dividing by alpha- agent not in n21
    >>> agents = AdditiveAgent.list_from({"Alice":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163},\
    "Bruce":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163},\
    "Carl":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163}})
    >>> agents_after_tentative_assignment = AdditiveAgent.list_from({"Alice":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163},\
    "Bruce":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163},\
    "Carl":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163}})
    >>> agent_index=0
    >>> items=['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11']
    >>> compute_n21(agents,items)
    0
    >>> remaining_items_after_tentative=['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11']
    >>> alpha=compute_max_alphas(agents,agents_after_tentative_assignment,agent_index,items,remaining_items_after_tentative)
    >>> normelized_agents=update_bound(agents,alpha,items,agent_index)
    >>> compute_n21(normelized_agents,items)
    1
 
    """
    return  max(compute_alphas(agents,agents_after_tentative_assignment,agent_index,items,remaining_items_after_tentative))

def compute_alphas(agents,agents_after_tentative_assignment,agent_index,items,remaining_items_after_tentative)->float:
    """
    The function computes alpha1 to alpha5 as part of updating mms upper bound
    :param agents: list of agents
    :param agents_after_tentative_assignment: agent remained after tentative assignment
    :param agent_index: index of current agent we calculate alpha for.
    :param items: items BEFORE tentative assignment, item names sorted from the highest valued to the lowest
    :param remaining_items_after_tentative: items AFTER tentative assignment, item names sorted from the highest valued to the lowest
    :return max_alpha:the highest alpha from all the calculated alphas,
    the alpha to be used in the mms bound updating
    >>> ### example when nothing was assigned in tentative assignment
    >>> agents = AdditiveAgent.list_from({"Alice":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163},\
    "Bruce":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163},\
    "Carl":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163}})
    >>> agents_after_tentative_assignment = AdditiveAgent.list_from({"Alice":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163},\
    "Bruce":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163},\
    "Carl":{"x1":0.724489796,"x2":0.714285714,"x3":0.387755102,"x4":0.357142857,"x5":0.357142857,"x6":0.357142857,"x7":0.020408163,"x8":0.020408163,"x9":0.020408163,"x10":0.020408163,"x11":0.020408163}})
    >>> agent_index=0
    >>> items=['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11']
    >>> remaining_items_after_tentative=['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10','x11']
    >>> alphas=compute_alphas(agents,agents_after_tentative_assignment,agent_index,items,remaining_items_after_tentative)
    >>> math.isclose(alphas[0],0.965986395,rel_tol=0.00001)
    True
    >>> math.isclose(alphas[1],0.993197279,rel_tol=0.00001)
    True
    >>> math.isclose(alphas[2],0.979591837,rel_tol=0.00001)
    True
    >>> math.isclose(alphas[3],0.993197279,rel_tol=0.00001)
    True
    >>> math.isclose(alphas[4],0.993197279,rel_tol=0.00001)
    True
    """
    agents_num=len(agents)
    agents_num_after_tentative_assignment=len(agents_after_tentative_assignment)

    #update_mms_bounds:
    alpha_array=[0]*5
    alpha_array[0]=(4/3)*agents[agent_index].value(items[0])
    alpha_array[1]=(4/3)*agents[agent_index].value({items[agents_num-1],items[agents_num]})
    alpha_array[2]=(4/3)*agents[agent_index].value({items[2*agents_num-2],items[2*agents_num-1],items[2*agents_num]})
    r=remaining_items_after_tentative
    alpha_array[3]=(4/3)*agents[agent_index].value({remaining_items_after_tentative[0],remaining_items_after_tentative[2*agents_num_after_tentative_assignment]})

    #create list of the B_k bundles
    bundles=[0]*agents_num
    for i in range(0,agents_num):
        mirror_index=2*agents_num-i-1
        assert (len(items)>0 and len(items)>mirror_index )#has to be both!!
        bundles[i]=agents[agent_index].value([items[i],items[mirror_index]])
        
    # list of all valuations of items still not assigned
    all_items=dict()
    for item in items:
        all_items.setdefault(item,agents[agent_index].value(item))
    alpha_array[4]=compute_alpha5_using_binary_search(bundles,agents[agent_index].value_except_best_c_goods(bundle=all_items,c=2*agents_num)) # v_i(M\J)

    return alpha_array
    
 
def update_bound(agents: List[AdditiveAgent],alpha: float,items: List[str],index_specific_agent:int)->List[AdditiveAgent]:
    """
    The algorithm update mms bound by dividing the valuations of the given agent in alpha.
    :param agents: Valuations of agents 
    :param alpha: parameter to divide the given agent valuations by
    :param items: items names sorted from the highest valued to the lowest and valuation are ordered in ascending order
    :param index_specific_agent: index of the agent to change valuations to in the agents list.
    :return agents: list of agents after after givens agent valuation have been updated. 
    >>> a = AdditiveAgent({"x1": 3, "x2": 2, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 4, "x2": 4, "x3": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 5, "x2": 2, "x3": 1}, name="C")
    >>> agents=[a,b,c]
    >>> list_agents= update_bound(agents, 4,['x1','x2','x3'],1)
    >>> list_agents[0]
    A is an agent with a Additive valuation: x1=3 x2=2 x3=1.
    >>> list_agents[1]
    B is an agent with a Additive valuation: x1=1.0 x2=1.0 x3=1.0.
    >>> list_agents[2]
    C is an agent with a Additive valuation: x1=5 x2=2 x3=1.
    >>> update_bound([a], 0,['x1','x2','x3'],1)
    Traceback (most recent call last):
    ZeroDivisionError: alpha can't be zero- causes division by zero
    """   
  
    if alpha==0:
        raise ZeroDivisionError(f"alpha can't be zero- causes division by zero")  
    
    updated_agents=[None]*len(agents)
    num_agents=len(agents)
    for i in range(0,num_agents):
        if(i!=index_specific_agent):
            updated_agents[i]=agents[i] #copy as it is
        else:
            #create agent with updated valuations
            item_value={}
            for item in items:
               item_value[item]=(agents[i].value(item))/alpha
            updated_agents[i]=AdditiveAgent(item_value,name=agents[i]._name)
    return updated_agents



####
#### Algorithm 7
####

def agents_conversion_to_ordered_instance(agents: List[AdditiveAgent],items:List[str])->List[AdditiveAgent]:
    """
    The function sorted the list of additive agents such that their valuations for objects are unordered will become ordered.
    :param agents: A list of additive agents such that their valuations for objects are unordered.
    :param items: items names inorder for agent values to be sorted such that the the values of first item is highest and so on 
    such that the value of the last item is the lowest
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

    


####
#### Algorithm 8
####

def get_alpha_MMS_allocation_to_unordered_instance(agents_unordered: List[AdditiveAgent], ag_alloc: dict(), ordered_items: List[str]) -> Tuple[dict,List[str]]:
    """
     Get the MMS allocation for agents unordered valuations.
    :param agents_unordered: Unordered valuations agents.
    :param ag_alloc: dictionary of the  MMS allocation for ordered valuations agents.
    :param ordered_items: list of the ordered items.
    :return allocation: return dictionary of the real allocation (the allocation for the unordered items)
    :return reamaining_items: items remaining after each agent got at least 3/4 his mms value 
    >>> ### allocation for 2 agents 3 objects
    >>> a = AdditiveAgent({"x1": 3, "x2": 10, "x3": 1}, name="A")
    >>> b = AdditiveAgent({"x1": 10, "x2": 10, "x3": 9}, name="B")
    >>> agents=[a,b]
    >>> ag_alloc = dict({'A': ['x1'], 'B': ['x2']})
    >>> items_ordered = list(["x1", "x2", "x3"]) 
    >>> real_alloc,remaining_items = get_alpha_MMS_allocation_to_unordered_instance(agents,  ag_alloc, items_ordered)
    >>> print(real_alloc)
    {'A': ['x2'], 'B': ['x1']}
    >>> print(remaining_items)
    ['x3']
    >>> ### allocation for 1 agent, 1 object
    >>> a = AdditiveAgent({"x": 2}, name="Alice")
    >>> agents=[a]
    >>> ag_alloc = dict({'Alice': ['x']})
    >>> items_ordered = list(["x"]) 
    >>> real_alloc,remaining_items  = get_alpha_MMS_allocation_to_unordered_instance(agents,  ag_alloc, items_ordered)
    >>> print(real_alloc)
    {'Alice': ['x']}
    >>> print(remaining_items)
    []
    >>> ### allocation for 3 agents 8 objects
    >>> a = AdditiveAgent({"x1": 2, "x2": 7, "x3": 10,"x4": 8, "x5": 3, "x6": 4,"x7": 7, "x8": 11}, name="A")
    >>> b = AdditiveAgent({"x1": 8, "x2": 7, "x3": 5,"x4": 3, "x5": 10, "x6": 2,"x7": 1, "x8": 4}, name="B")
    >>> c = AdditiveAgent({"x1": 1, "x2": 2, "x3": 3,"x4": 4, "x5": 5, "x6": 6,"x7": 7, "x8": 8}, name="C")
    >>> agents=[a,b,c]
    >>> items_ordered = list(["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8"]) 
    >>> ag_alloc = dict({'A': ['x3', 'x4'], 'B': ['x1'], 'C': ['x2', 'x5']})
    >>> real_alloc,remaining_items  =  get_alpha_MMS_allocation_to_unordered_instance(agents,  ag_alloc, items_ordered)
    >>> print(real_alloc)
    {'A': ['x3', 'x4'], 'B': ['x5'], 'C': ['x8', 'x7']}
    >>> print(remaining_items)
    ['x1', 'x2', 'x6']
    """
    real_alloc = dict()
    un_allocated_items=deepcopy(ordered_items) 
    dict_agents_unordered={} #keep in dictionary to allow access by
    for agent in agents_unordered:
        real_alloc[agent.name()] = []
        dict_agents_unordered[agent.name()]=agent
   
    for item in ordered_items:
        for name, agent_items in ag_alloc.items():
            if(item in agent_items): #if this agent get the next item
                index_item_to_allocate=dict_agents_unordered[name].best_index(un_allocated_items) #chose best item for agent from remaining items
                real_alloc[name].append(un_allocated_items[index_item_to_allocate])
                un_allocated_items.remove(un_allocated_items[index_item_to_allocate])
                break

    return real_alloc,un_allocated_items  #real allocation

def is_sum_valuations_zero(agent:AdditiveAgent,agent_curr_val:dict(), items:List[str])->bool:
    """
        Check if given agent valuation is zero for all the remaining items.
        only if agent_curr_val in dict format is None, the use agent- in AdditiveAgent format
        :param agent: agent in AdditiveAgent format
        :param agent_curr_val: agent in dict format
        :param items: list of remaining items
        :return ans: true if given agent valuation is zero for all the remaining items, otherwise false
        >>> a = AdditiveAgent({"x1": 2, "x2": 7, "x3": 10,"x4": 8, "x5": 3, "x6": 4,"x7": 7, "x8": 11}, name="A")
        >>> is_sum_valuations_zero(a,None,["x1","x2","x3","x4","x5","x6","x7","x8"])
        False
        >>> a = AdditiveAgent({"x1":0, "x2": 0, "x3": 0}, name="A")
        >>> is_sum_valuations_zero(a,None,["x1","x2","x3"])
        True
        >>> a_dict = {'01': 0.727272, '02': 0.727272, '03': 0.318182, '04': 0.318182}
        >>> is_sum_valuations_zero(None,a_dict,['01','02','03','04'])
        False
        >>> a_dict = {'01': 0.0, '02': 0.0, '03': 0.0, '04': 0.0}
        >>> is_sum_valuations_zero(None,a_dict,["01","02","03","04"])
        True
        """
    all_zero=True
    for item in items:
        if (agent_curr_val==None):
            if(agent.value(item)!=0):
                all_zero=False
                break
        else: 
            if(agent_curr_val[item]!=0):
                all_zero=False
                break
    
    return all_zero



def update_val(items_remove: List[str], val_arr: dict(), n: int)->dict() : 
    """
        Update  (and normalize) all the values of the agents that still remained
        :param items_remove: list of items to remove
        :param val_arr: dictionary off all agents valuations
        :param n: new amount of agents
        :return val_arr: dictionary of agents with valuation updated
        >>> items_remove = ['04', '05', '06'] 
        >>> val_arr = {'Bruce': {'01': 0.727272, '02': 0.727272, '03': 0.318182, '04': 0.318182, '05': 0.318182, '06': 0.318182, '07': 0.090909, '08': 0.090909, '09': 0.045454, '10': 0.045454}, 'Carl': {'01': 0.727272, '02': 0.727272, '03': 0.318182, '04': 0.318182, '05': 0.318182, '06': 0.318182, '07': 0.090909, '08': 0.090909, '09': 0.045454, '10': 0.045454}}
        >>> n = 2
        >>> after_update= update_val(items_remove, val_arr, n)
        >>> print(after_update)
        {'Bruce': {'01': 0.711111284938488, '02': 0.711111284938488, '03': 0.3111116760500858, '07': 0.088888910617311, '08': 0.088888910617311, '09': 0.04444396641915821, '10': 0.04444396641915821}, 'Carl': {'01': 0.711111284938488, '02': 0.711111284938488, '03': 0.3111116760500858, '07': 0.088888910617311, '08': 0.088888910617311, '09': 0.04444396641915821, '10': 0.04444396641915821}}
        >>> items_remove = ['02', '03'] 
        >>> val_arr = {'Carl': {'01': 0.711111284938488, '02': 0.711111284938488, '03': 0.3111116760500858, '07': 0.088888910617311, '08': 0.088888910617311, '09': 0.04444396641915821, '10': 0.04444396641915821}}
        >>> n = 1
        >>> after_update= update_val(items_remove, val_arr, n)
        >>> print(after_update)    
        {'Carl': {'01': 0.7272734545469091, '07': 0.09090918181836363, '08': 0.09090918181836363, '09': 0.04545409090818181, '10': 0.04545409090818181}}
        >>> items_remove = ['02', '03'] 
        >>> # when valuation is 0 for all objects
        >>> val_arr = {'Carl': {'01': 0.711111284938488, '02': 0.711111284938488, '03': 0.3111116760500858, '07': 0.088888910617311, '08': 0.088888910617311, '09': 0.04444396641915821, '10': 0.04444396641915821},'Ben': {'01': 0.0, '02': 0.0, '03': 0.0, '07': 0.0, '08': 0.0, '09': 0.0, '10': 0.0}}
        >>> n = 1
        >>> after_update= update_val(items_remove, val_arr, n)
        >>> print(after_update)    
        {'Carl': {'01': 0.7272734545469091, '07': 0.09090918181836363, '08': 0.09090918181836363, '09': 0.04545409090818181, '10': 0.04545409090818181}, 'Ben': {'01': 0.0, '07': 0.0, '08': 0.0, '09': 0.0, '10': 0.0}}
    """
    sum_arr = dict()
    agent_to_remove=[] #list of agents that valuate all objects at 0, which means their mms is 0, and they can be removed
    for i in val_arr:
        for j in items_remove:
            val_arr[i].pop(j)
        sum_arr[i] = 0
        for j in val_arr[i]:
            sum_arr[i] = sum_arr[i] + val_arr[i][j]
        if(sum_arr[i]!=0):
            for j in val_arr[i]:
                val_arr[i][j] = val_arr[i][j]*(n/sum_arr[i])
        else:
            agent_to_remove.append(i)
    return val_arr #,agent_to_remove



if __name__ == '__main__':
    import doctest

    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))

    # Testing specific functions:

    # doctest.run_docstring_examples(three_quarters_MMS_subroutine, globals())

    # doctest.run_docstring_examples(fixed_assignment, globals())

    # doctest.run_docstring_examples(initial_assignment_alpha_MSS, globals())
    # doctest.run_docstring_examples(bag_filling_algorithm_alpha_MMS, globals())
    # doctest.run_docstring_examples(combine_allocations, globals())
    # doctest.run_docstring_examples(alpha_MMS_allocation, globals())

    # doctest.run_docstring_examples(three_quarters_MMS_allocation_algorithm, globals())
    # doctest.run_docstring_examples(update_bound, globals())
    # doctest.run_docstring_examples(compute_alphas, globals())
    # doctest.run_docstring_examples(tentative_assignment, globals())
    # doctest.run_docstring_examples(three_quarters_MMS_allocation, globals())
    # doctest.run_docstring_examples(agents_conversion_to_ordered_instance, globals())
    # doctest.run_docstring_examples(get_alpha_MMS_allocation_to_unordered_instance, globals())

