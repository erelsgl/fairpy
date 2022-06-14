#!python3
"""
Implementing the algorithm in the following article: "A note on the undercut procedure"
By Haris Aziz
2014
Link to the article: https://arxiv.org/pdf/1312.6444.pdf
Programmer: Helen Yonas
Date: 2022-05
The undercut procedure is a procedure for fair item assignment between *two* people.
"""

from typing import List, Any
import fairpy
from fairpy import Agent 
from fairpy.allocations import Allocation
import logging


logger = logging.getLogger(__name__)

def undercut(agents: List[Agent], items: List[Any]) -> str:
    """
    Undercut Procedure - An algorithm that returns a envy free allocation (if it exists)
    even when the agents may express indifference between objects.
    
    Note: The number of agents should be 2.
    
    :param agents: The agents who participate in the division
    :param items: The items which are divided
    :return: An envey free allocation if it exists
    
    >>> Alice = ({"a": 7, "b": 4, "c": 3, "d":2})
    >>> Bob = ({"a": 1, "b": 7, "c": 3, "d":2})
    >>> items=['a','b','c','d']
    >>> A = fairpy.agents.AdditiveAgent({"a": 7, "b": 4, "c": 3, "d":2}, name="Alice")
    >>> B = fairpy.agents.AdditiveAgent({"a": 1, "b": 7, "c": 3, "d":2}, name="Bob")
    >>> print(undercut([Alice,Bob],items))
    Alice gets ['a', 'd'] with value 9.
    Bob gets ['b', 'c'] with value 10.
    <BLANKLINE>
    >>> print(A.is_EF({"a","d"}, [{"b","c"}]))
    True
    >>> print(B.is_EF({"b","c"}, [{"a","d"}]))
    True
    
    >>> Alice = ({"a": 8, "b": 7, "c": 6, "d":3})
    >>> Bob = ({"a": 8, "b": 7, "c": 6, "d":3})
    >>> items=['a','b','c','d']
    >>> print(undercut([Alice, Bob],items))
    There is no envy-free division
    
    >>> Alice = ({"a": 1,"b": 2, "c": 3, "d":4,"e": 5, "f":14})
    >>> Bob = ({"a":1,"b": 1, "c": 1, "d":1,"e": 1, "f":7})
    >>> items=['a','b','c','d','e','f']
    >>> print(undercut([Alice, Bob],items))
    Alice gets ['a', 'b', 'c', 'd', 'e'] with value 15.
    Bob gets ['f'] with value 7.
    <BLANKLINE>
    
    >>> Alice=({})
    >>> Bob =({})
    >>> print(undercut([Alice,Bob],[]))
    Alice gets [] with value 0.
    Bob gets [] with value 0.
    <BLANKLINE>
    >>> Alice=({"a":-5})
    >>> Bob =({"a":5})
    >>> print(undercut([Alice,Bob],['a']))
    Alice gets [] with value 0.
    Bob gets ['a'] with value 5.
    <BLANKLINE>
    """
    
    """ Algorithm """

    val=0
    
    logger.info("Checking if there are no_items")
    if (items==None):
        return no_items()
    
    num_agents=len(agents)
    num_of_items=len(items)
    values_for_alice_and_bob={0:0,1:0}  #first initialize values to 0 for both agents
    
    
    logger.info("Checking if there are 0 items")
    if (num_of_items==0):
        return no_items()

    logger.info("Checking if there is a single item") 
    if num_of_items==1:
        return one_item(agents, items)
    
    logger.info("Stage 1 - find a almost equal cut")    
    for group_ in all_combinations(items, num_agents):
            for agent_num, subgroup_ in enumerate(group_):
                for item_ in subgroup_:
                    val=values_for_alice_and_bob[agent_num]+ agents[agent_num][item_]
                    values_for_alice_and_bob[agent_num]=val #calculate the values of the two agents for this particular combination
            items_for_alice=group_[0]
            items_for_bob=group_[1]
            num_of_items_for_alice=len(items_for_alice)
            num_of_items_for_bob=len(items_for_bob)
            counter_alice=counter_bob=0
            alice_val_for_bob_items=bob_val_for_alice_items=0
            for item_ in items_for_bob:
                    alice_val_for_bob_items+=agents[0][item_]    #calculating Alice's value for Bob's items
            for item_ in items_for_alice:
                    bob_val_for_alice_items+=agents[1][item_]    #calculating Bob's value for Alice's items
            if values_for_alice_and_bob[0]>=alice_val_for_bob_items: #Alice weakly prefers X to Y
                for item_ in items_for_alice: #and if any single item is moved from X to Y
                    if values_for_alice_and_bob[0]-agents[0][item_]>=alice_val_for_bob_items+agents[0][item_]: #then Alice strictly prefers Y to X
                        break
                    counter_alice+=1
                if counter_alice==num_of_items_for_alice:
                    result= almost_equal_cut(group_,"Alice",agents,values_for_alice_and_bob,items_for_alice,items_for_bob,bob_val_for_alice_items,alice_val_for_bob_items)                               
            else:
                if values_for_alice_and_bob[1]>=bob_val_for_alice_items: #George weakly prefers Y to X
                    for item_ in items_for_bob: #and if any single item is moved from Y to X
                        if values_for_alice_and_bob[1]-agents[1][item_]>=bob_val_for_alice_items+agents[1][item_]:  #then George strictly prefers X to Y
                            break
                        counter_bob+=1 
                    if counter_alice==num_of_items_for_bob:
                        result= almost_equal_cut(group_,"George", agents,values_for_alice_and_bob,items_for_bob,items_for_alice,bob_val_for_alice_items,alice_val_for_bob_items)      
            values_for_alice_and_bob={0:0,1:0}  #initialize values to 0 for both agents
    return result #if we went through all the possible combinations then there is no envy-free division


def almost_equal_cut(group_,Name: str, agents,values,items_for_bob,items_for_alice,bob_val_for_alice_items,alice_val_for_bob_items) -> str:
    """
    A function which checks whether the agents accept the offer of the almost equal groups
    Args:
        group_:  the combination
        Name (str): the agent
        agents (List): agents preferences
        values: the values of the two agents for this particular combination
        items_for_bob
        items_for_alice
        bob_val_for_alice_items
        alice_val_for_bob_items
    Returns:
        if there is a subgroup: envy-free division
        else: There is no envy-free division_
    """
    result="There is no envy-free division"
    logger.info("\t{} is almost-equal-cut for agent Alice (prefers {} to {})".format(group_, items_for_bob,items_for_alice))
    if Name=="Alice":
            #this partition is presented to George
        if values[1]>=bob_val_for_alice_items: #George accepts the partition if he prefers Y to X
            logger.info("Stage 2")  
            result= get_allocation(items_for_alice,items_for_bob,values)
        else: 
            logger.info("Stage 3 - find an unnecessary item in Alice's items")   
            #George rejects the partition if he prefers X to Y
            #check if there exists an item x in X such that George prefers X \ x to Y U x
            result= search_subgroup(agents,"George",items_for_bob,items_for_alice,bob_val_for_alice_items,alice_val_for_bob_items,values[1])
                
    elif Name=="George":
        if values[0]>=alice_val_for_bob_items: #Alice accepts the partition if she prefers X to Y
            logger.info("Stage 2")  
            result= get_allocation(items_for_alice,items_for_bob,values)
        else: 
            logger.info("Stage 3 - find an unnecessary item in Bob's items")  
            #Alice rejects the partition if she prefers Y to X
            #check if there exists an item y in Y such that Alice prefers Y \ y to X U y
            result= search_subgroup(agents,"Alice",items_for_alice,items_for_bob,alice_val_for_bob_items,bob_val_for_alice_items,values[0]) 
    return result
    
                    
def get_allocation(items_for_alice,items_for_bob,values) -> str:
    """ 
    A function that constructs the allocation of objects to Alice and Bob
    Args:
        items_for_alice
        items_for_bob
        values: Alice and Bob's values for the items
    Returns:
        envy free allocation
    """

    temp,temp2 = [], [] 
    logger.info("Bob accepts the offer because he has more benefit from {} than {}".format(items_for_alice,items_for_bob))
    for item_ in items_for_alice:
        temp.append(item_)
    for item__ in items_for_bob:
        temp2.append(item__)
    temp.sort()
    temp2.sort()   
    result=f"Alice gets {temp2} with value {values[0]}.\n"     
    result+=f"Bob gets {temp} with value {values[1]}.\n" 
    logger.info(result)  
    return result

def search_subgroup(agents,Name: str,items_for_alice,items_for_bob,val1,val2,value) -> str:
    """
    A function that searches for a subgroup so that there will be a envy-free division by 
    removing one item from the group of the agent who rejected the offer
    Args:
        agents (List): Agents preferences
        Name: the agent who rejected the offer
        items_for_alice 
        items_for_bob
        val1: Alice's value for Bob's items
        val2: Bob's value for Alice's items
        value: The value of the agent who rejected the offer
    Returns:
        envy free allocation (if it exists)
        else: There is no envy-free division
        
    """
    result="There is no envy-free division"
    temp,temp2 = [], [] 
    logger.info("{} rejects the offer because he has more benefit from {} than {}".format(Name,items_for_alice,items_for_bob))
    for item_ in items_for_alice: # check if there exists an item x in X such that: 
        if val1-agents[1][item_]>=value+agents[1][item_]:  # agent1 prefers X \ x to Y U x
            for i in items_for_alice:
                if  i is not item_:
                    temp.append(i) #agent1 reports X \ x
            for i in items_for_bob: 
                temp2.append(i) #agent2 prefers Y U x to X \ x (Since (X,Y) is an almost-equal-cut for agent2).
            temp2.append(item_) #Y U x
            temp.sort()
            temp2.sort()   
            result=f"Alice gets {temp2} with value {val2+agents[0][item_]}.\n"     
            result+=f"Bob gets {temp} with value {val1-agents[1][item_]}.\n"   
            logger.info(result) 
    return result      

def no_items() -> str:
    result=f"Alice gets {[]} with value {0}.\n"     #if there are no items then value is 0 for everyone
    result+=f"Bob gets {[]} with value {0}.\n"  
    return result 

def one_item(agents: List[Agent], items: List[Any]) -> str:
    temp,temp2 = [], []
    item_ = items.pop()
    valA_=agents[0][item_]
    valB_=agents[1][item_]  
    if(valA_<=0 and valB_ >=0 ):
        temp2.append(item_)
        result=f"Alice gets {temp} with value {0}.\n"     
        result+=f"Bob gets {temp2} with value {valB_}.\n"  
        logger.info("\tAgent Alice has a benefit of {} from the item which is negative so Bob who does have a benefit of {} from the item gets it".format(valA_, valB_))
        return result
    elif (valA_>=0 and valB_<=0):
        temp.append(item_)
        result=f"Alice gets {temp} with value {valA_}.\n"     
        result+=f"Bob gets {temp2} with value {0}.\n" 
        logger.info("\tAgent Bob has a benefit of {} from the item which is negative so Alice who does have a benefit of {} from the item gets it".format(valB_, valA_))
        return result
    elif (valA_<=0 and valB_<=0):
        result=f"Alice gets {temp} with value {0}.\n"     
        result+=f"Bob gets {temp2} with value {0}.\n" 
        logger.info("\tBoth agents have a negative benefit from the item so no one gets it")
        return result
    else:
        logger.info("\tIf both agents have a positive benefit from the object - there is no envy-free division")
        return "There is no envy-free division"
    
def all_combinations(items, num_agents) ->  List[List[tuple]]:
    """
    Returns all possible combinations of division into 2 groups
    >>> items=['a','b','c','d']
    >>> group_ = all_combinations(items, 2)
    >>> print(group_)
    [[('a',), ('b', 'c', 'd')], [('b',), ('a', 'c', 'd')], [('c',), ('a', 'b', 'd')], [('d',), ('a', 'b', 'c')], [('a', 'b'), ('c', 'd')], [('a', 'c'), ('b', 'd')], [('a', 'd'), ('b', 'c')]]
    """
    n = len(items)
    groups = [] 
    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups))
        else:
            if n - i > num_agents - len(groups):
                for group in groups:
                    group.append(items[i])
                    yield from generate_partitions(i + 1)
                    group.pop()
            if len(groups) < num_agents:
                groups.append([items[i]])
                yield from generate_partitions(i + 1)
                groups.pop()
    result = generate_partitions(0)
    result = [sorted(ps, key = lambda p: (len(p), p)) for ps in result]
    result = sorted(result, key = lambda ps: (*map(len, ps), ps))
    return result

if __name__ == "__main__":
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))