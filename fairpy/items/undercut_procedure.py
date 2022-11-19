#!python3
"""
Implementing the algorithm in the following article: 
"A note on the undercut procedure", By Haris Aziz, 2014.
Link to the article: https://arxiv.org/pdf/1312.6444.pdf

Programmer: Helen Yonas
Date: 2022-05

The undercut procedure is a procedure for fair item assignment between *two* people.
"""


from fairpy import AgentList

from typing import List, Any
import logging
logger = logging.getLogger(__name__)

def undercut(agents:AgentList, items: List[Any]=None) -> List[List[Any]]:
    """
    Undercut Procedure - An algorithm that returns a envy free allocation 
    (if it exists) even when the agents may express indifference between objects.

    Note: The number of agents should be 2.

    :param agents: The agents who participate in the division
    :param items: The items which are divided
    :return: An envy-free allocation if it exists
        
    >>> import fairpy
    >>> Alice = fairpy.agents.AdditiveAgent({"a": 7, "b": 4, "c": 3, "d":2}, name="Alice")
    >>> George = fairpy.agents.AdditiveAgent({"a": 1, "b": 7, "c": 3, "d":2}, name="George")
    >>> items=['a','b','c','d']
    >>> allocation = undercut(AgentList([Alice,George]),items)
    >>> allocation
    [('a', 'd'), ('b', 'c')]
    >>> print(Alice.is_EF(allocation[0],allocation)) and George.is_EF(allocation[1], allocation)
    True
    
    >>> agent_dict = AgentList({"Alice":{"a": 8, "b": 7, "c": 6, "d":3},"Bob":{"a": 8, "b": 7, "c": 6, "d":3}})
    >>> items=['a','b','c','d']
    >>> print(undercut(agent_dict,items))
    There is no envy-free division
    
    >>> agent_dict = AgentList({"Alex":{"a": 1,"b": 2, "c": 3, "d":4,"e": 5, "f":14},"Bob":{"a":1,"b": 1, "c": 1, "d":1,"e": 1, "f":7}})
    >>> items=['a','b','c','d','e','f']
    >>> print(undercut(agent_dict,items))
    [['a', 'b', 'c', 'd', 'e'], ['f']]

    >>> agent_dict = AgentList({"Alice":{},"Bob":{}})
    >>> print(undercut(agent_dict,[]))
    [[], []]

    >>> agent_dict = AgentList({"Alice":{"a":-5},"Bob":{"a":5}})
    >>> print(undercut(agent_dict,['a']))
    [[], 'a']
    """
    assert isinstance(agents, AgentList)
    if (items==None): items = agents.all_items()
    items = list(items)

    num_agents=len(agents)
    if (num_agents!=2):
        raise ValueError('The number of agents should be 2')

    num_of_items=len(items)    
    logger.info("Checking if there are 0 items")
    if (num_of_items==0): #returns value 0 without having to continue the rest of the function
        return [[],[]]

    logger.info("Checking if there is a single item") 
    if num_of_items==1:
        return one_item(agents, items)
    
    logger.info("Stage 1 - find a almost equal cut")    
    for group_ in all_combinations(items, num_agents):
        values_for_alice_and_bob={0:0,1:0} #initialize values to 0 for both agents
        for agent_num, subgroup_ in enumerate(group_):
            values_for_alice_and_bob[agent_num]=agents[agent_num].value(subgroup_) #calculate the values of the two agents for this particular combination
        items_for_alice=group_[0]
        items_for_bob=group_[1]
        num_of_items_for_alice=len(items_for_alice)
        num_of_items_for_bob=len(items_for_bob)
        counter_alice=counter_bob=0
        alice_val_for_bob_items=agents[0].value(items_for_bob)  #calculating Alice's value for Bob's items
        bob_val_for_alice_items=agents[1].value(items_for_alice)  #calculating Bob's value for Alice's items
        if values_for_alice_and_bob[0]>=alice_val_for_bob_items: #if Alice weakly prefers X to Y
            for item_ in items_for_alice: #and if any single item is moved from X to Y
                if values_for_alice_and_bob[0]-agents[0].value(item_)>=alice_val_for_bob_items+agents[0].value(item_): #then Alice strictly prefers Y to X
                     break
                counter_alice+=1
            if counter_alice==num_of_items_for_alice: #this is an almost equal cut for Alice
                result= almost_equal_cut(group_,0,agents,values_for_alice_and_bob,bob_val_for_alice_items,alice_val_for_bob_items)                               
        else:
            if values_for_alice_and_bob[1]>=bob_val_for_alice_items: #George weakly prefers Y to X
                for item_ in items_for_bob: #and if any single item is moved from Y to X
                    if values_for_alice_and_bob[1]-agents[1].value(item_)>=bob_val_for_alice_items+agents[1].value(item_):  #then George strictly prefers X to Y
                        break
                    counter_bob+=1 
                if counter_alice==num_of_items_for_bob:  #this is an almost equal cut for George
                    result= almost_equal_cut(group_,1,agents,values_for_alice_and_bob,bob_val_for_alice_items,alice_val_for_bob_items)      
    return result #if we went through all the possible combinations then there is no envy-free division


def almost_equal_cut(group_,agent_num, agents,values,bob_val_for_alice_items,alice_val_for_bob_items) -> List[List[Any]]:
        
    """
    A function which checks whether the agents 
    accept the offer of the almost equal groups
    Args:
        group_:  the combination
        agent_num: the agent
        agents (List): agents preferences
        values: the values of the two agents for this particular combination
        items_for_bob
        items_for_alice
        bob_val_for_alice_items
        alice_val_for_bob_items
    Returns:
        if the agent accepted the offer or if there is a subgroup: envy-free division
        else: There is no envy-free division
    
    #The original group was {a,d} for Alice (A almost equal cut for Alice but not for George) and George rejects it.
    #Because the original group is not an almost equal cut for George there is an item (d) so he prefers {a,d}\\d over {b,c} U d.
    #Alice will accept the new offer because this is an almost equal cut for her
    >>> agent_dict = {"Alice":{"a": 7, "b": 4, "c": 3, "d":2},"George":{"a": 7, "b": 1, "c": 3, "d":2}}
    >>> agents = AgentList(agent_dict)
    >>> print(almost_equal_cut([('a','d'),('b','c')],0,agents,{0:9,1:4},9,7))
    [['b', 'c', 'd'], ['a']]
    
    #The {b,c} group is an almost equal cut for Alice and George
    #so George and Alice will reject the offer and there is no subgroup
    >>> agent_dict = {"Alice":{"a": 8, "b": 7, "c": 6, "d":3},"George":{"a": 8, "b": 7, "c": 6, "d":3}}
    >>> agents= AgentList(agent_dict)
    >>> print(almost_equal_cut([('b','c'),('a','d')],0,agents,{0:13,1:11},13,13))
    There is no envy-free division
    """
    result="There is no envy-free division"
    logger.info("\t{} is almost-equal-cut for agent Alice (prefers {} to {})".format(group_, group_[0],group_[1]))
    if agent_num==0:
        logger.info("Stage 2 - offer the division to George") 
        #this partition is presented to George
        if values[1]>=bob_val_for_alice_items: #George accepts the partition if he prefers Y to X
            result= [group_[0],group_[1]]
        else:  #George rejects the partition if he prefers X to Y
            logger.info("Stage 3 - find an unnecessary item in Alice's items")   
            #check if there exists an item x in X such that George prefers X \ x to Y U x
            result= search_subgroup(agents,"1",group_[0],group_[1],bob_val_for_alice_items,alice_val_for_bob_items,values[1])
                
    elif agent_num==1:
        logger.info("Stage 2 - offer the division to Alice") 
        if values[0]>=alice_val_for_bob_items: #Alice accepts the partition if she prefers X to Y
            result=[group_[0],group_[1]]
        else:  #Alice rejects the partition if she prefers Y to X
            logger.info("Stage 3 - find an unnecessary item in Bob's items")  
            #check if there exists an item y in Y such that Alice prefers Y \ y to X U y
            result= search_subgroup(agents,"0",group_[0],group_[1],alice_val_for_bob_items,bob_val_for_alice_items,values[0]) 
    return result
    
                    
def search_subgroup(agents,agent_num,items_for_alice,items_for_bob,val1,val2,value) -> List[List[Any]]:
    """
    A function that searches for a subgroup so that there will be a envy-free division by 
    removing one item from the group of the agent who rejected the offer
    Args:
        agents (List): Agents preferences
        agent_num: the agent who rejected the offer
        items_for_alice 
        items_for_bob
        val2: Alice's value for Bob's items
        val1: Bob's value for Alice's items
        value: The value of the agent who rejected the offer
    Returns:
        envy free allocation (if it exists)
        else: There is no envy-free division
        
    #The original group was {a,d} for Alice (A almost equal cut for Alice but not for George) and George rejects it.
    #Because the original group is not an almost equal cut for George there is an item (d) so he prefers {a,d}\\d over {b,c} U d.
    #Alice will accept the new offer because this is an almost equal cut for her
    >>> agent_dict = {"Alice":{"a": 7, "b": 4, "c": 3, "d":2},"George":{"a": 7, "b": 1, "c": 3, "d":2}}
    >>> agents= AgentList(agent_dict)
    >>> print(search_subgroup(agents,"1",('a','d'),('b','c'),9,7,4))
    [['b', 'c', 'd'], ['a']]
    
    #The {b,c} group is an almost equal cut for Alice and George
    #So George and Alice will reject the offer and there is no subgroup
    >>> agent_dict = {"Alice":{"a": 8, "b": 7, "c": 6, "d":3},"George":{"a": 8, "b": 7, "c": 6, "d":3}}
    >>> agents= AgentList(agent_dict)
    >>> print(search_subgroup(agents,"1",('b','c'),('a','d'),13,11,11))
    There is no envy-free division
    
    """
    result="There is no envy-free division"
    temp,temp2 = [], [] 
    logger.info("{} rejects the offer because he has more benefit from {} than {}".format(agent_num,items_for_alice,items_for_bob))
    for item_ in items_for_alice: # check if there exists an item x in X such that: 
        if val1-agents[1].value(item_)>=value+agents[1].value(item_):  # agent1 prefers X \ x to Y U x
            temp = sorted(set(items_for_alice) - set([item_]))  #agent1 reports X \ x
            temp2 = sorted(set(items_for_bob).union(set([item_])))  #agent2 prefers Y U x to X \ x (Since (X,Y) is an almost-equal-cut for agent2).
            result = [temp2,temp]
            logger.info(result) 
    return result      

def one_item(agents: AgentList, items: List[Any]) -> List[List[Any]]:
    """
    If there is one item there will be a envy free division only if for one of 
    the agents the benefit is negative
    Args:
        agents (AgentList): agents preferences
        items (List[Any]):  the items which are divided
    Returns:
        List[List[Any]]: a list of bundles, where each bundle is a list of items

    >>> agent_dict = {"Alice":{"a":-5},"Bob":{"a":5}}
    >>> agents= AgentList(agent_dict)
    >>> print(one_item(agents,['a']))
    [[], 'a']

    >>> agent_dict = {"Alice":{"a":6},"Bob":{"a":5}}
    >>> agents= AgentList(agent_dict)
    >>> print(one_item(agents,['a']))
    There is no envy-free division
    """
    item_ = items.pop()
    valA_=agents[0].value(item_)
    valB_=agents[1].value(item_)
    if(valA_<=0 and valB_ >=0 ):
        logger.info("\tAgent Alice has a benefit of {} from the item which is negative so Bob who does have a benefit of {} from the item gets it".format(valA_, valB_))
        return [[], item_]
    elif (valA_>=0 and valB_<=0):
        logger.info("\tAgent Bob has a benefit of {} from the item which is negative so Alice who does have a benefit of {} from the item gets it".format(valB_, valA_))
        return [item_,[]]
    elif (valA_<=0 and valB_<=0):
        logger.info("\tBoth agents have a negative benefit from the item so no one gets it")
        return [[],[]]
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

    # Testing specific functions:
    # doctest.run_docstring_examples(one_item, globals())
    # doctest.run_docstring_examples(all_combinations, globals())
    # doctest.run_docstring_examples(search_subgroup, globals())
    # doctest.run_docstring_examples(almost_equal_cut, globals())
    # doctest.run_docstring_examples(undercut, globals())

