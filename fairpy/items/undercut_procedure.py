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
from unittest import result
import fairpy
from fairpy import Agent 
from fairpy.allocations import Allocation
from more_itertools import powerset 
from sympy import group
import logging
logger = logging.getLogger(__name__)

Y=False

def undercut(agents: List[Agent], items: List[Any]) -> List:
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
    >>> allocation = undercut([Alice,Bob],items)
    >>> print(allocation)
    Alice gets ['a', 'c', 'd'] with value 12.
    Bob gets ['b'] with value 7.
    <BLANKLINE>
    >>> Y = A.is_EF({"a","d"}, [{"a","d"},{"b","c"}])
    >>> Y
    True
    >>> Y = B.is_EF({"a","d"}, [{"a","d"},{"b","c"}])
    >>> Y
    False
    >>> Y = B.is_EF({"b","c"}, [{"a","d"},{"b","c"}])
    >>> Y
    True
    >>> Y = A.is_EF({'a', 'c', 'd'}, [{"a","d"},{"b","c"},{'a', 'c', 'd'},{'b'}])
    >>> Y
    True
    >>> Y = B.is_EF({"a","d"}, [{"a","d"},{"b","c"}])
    >>> Y
    False
    >>> Y = B.is_EF({'a', 'c', 'd'}, [{'a'},{"a","d"},{"b","c"}])
    >>> Y
    False
    >>> Y = B.is_EF({'a', 'c', 'd'}, [{'b'},{'a'},{"a","d"},{"b","c"}])
    >>> Y
    False
    >>> Y = B.is_EF({'b'}, [{'a'},{"a","d"},{'a', 'c', 'd'}])
    >>> Y
    True
    >>> Y = B.is_EF({"b","c"}, [{'a'},{"a","d"},{"b","c"},{'a', 'c', 'd'}])
    >>> Y
    True
    >>> Alice = ({"a": 7, "b": 4, "c": 3, "d":2})
    >>> Bob =({"a": 7, "b": 1, "c": 3, "d":2})
    >>> items=['a','b','c','d']
    >>> A = fairpy.agents.AdditiveAgent({"a": 7, "b": 4, "c": 3, "d":2}, name="Alice")
    >>> B = fairpy.agents.AdditiveAgent({"a": 7, "b": 1, "c": 3, "d":2}, name="Bob")
    >>> allocation = undercut([Alice, Bob],items)
    >>> print(allocation)
    Alice gets ['b', 'c', 'd'] with value 9.
    Bob gets ['a'] with value 7.
    <BLANKLINE>
    >>> Y = A.is_EF({"b","c","d"}, [{"a"},{"b","c","d"}])
    >>> Y
    True
    >>> Y = B.is_EF({"a"}, [{"a"},{"b","c","d"}])
    >>> Y
    True
    >>> Alice = ({"a": 5, "b": 5, "c": 5, "d":5})
    >>> Bob = ({"a": 5, "b": 5, "c": 5, "d":5})
    >>> items=['a','b','c','d']
    >>> A = fairpy.agents.AdditiveAgent({"a": 5, "b": 5, "c": 5, "d":5}, name="Alice")
    >>> B = fairpy.agents.AdditiveAgent({"a": 5, "b": 5, "c": 5, "d":5}, name="Bob")
    >>> allocation = undercut([Alice, Bob],items)
    >>> print(allocation)
    Alice gets ['a', 'b'] with value 10.
    Bob gets ['c', 'd'] with value 10.
    <BLANKLINE>
    >>> Y = A.is_EF({"a","b"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}])
    >>> Y
    True
    >>> Y = B.is_EF({"c","d"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}])
    >>> Y
    True
    >>> Alice = ({"a": 8, "b": 7, "c": 6, "d":3})
    >>> Bob = ({"a": 8, "b": 7, "c": 6, "d":3})
    >>> items=['a','b','c','d']
    >>> A = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Alice")
    >>> B = fairpy.agents.AdditiveAgent({"a": 8, "b": 7, "c": 6, "d":3}, name="Bob")
    >>> allocation = undercut([Alice, Bob],items)
    >>> print(allocation)
    There is no envy-free division
    >>> Y = A.is_EF({"a","b"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]) and B.is_EF({"d","c"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}])
    >>> Y
    False
    >>> Y = B.is_EF({"a","c"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}]) and  A.is_EF({"b","d"}, [{"a","b"},{"a","d"},{"a","c"},{"b","c"},{"b","d"},{"c","d"}])
    >>> Y
    False
    >>> Alice = ({"a": 5})
    >>> Bob = ({"a": -4})
    >>> items=['a']
    >>> A = fairpy.agents.AdditiveAgent({"a": 5}, name="Alice")
    >>> B = fairpy.agents.AdditiveAgent({"a": -4}, name="Bob")
    >>> allocation = undercut([Alice,Bob],items)
    >>> print(allocation)
    Alice gets ['a'] with value 5.
    Bob gets [] with value 0.
    <BLANKLINE>
    >>> Y = A.is_EF({"a"}, [{},{"a"}])
    >>> Y
    True
    >>> Y = B.is_EF({},[{},{"a"}])
    >>> Y
    True
    >>> Alice = ({})
    >>> Bob = ({})
    >>> items = []
    >>> A = fairpy.agents.AdditiveAgent({}, name="Alice")
    >>> B = fairpy.agents.AdditiveAgent({}, name="Bob")
    >>> allocation = undercut([Alice,Bob],items)
    >>> print(allocation)
    Alice gets [] with value 0.
    Bob gets [] with value 0.
    <BLANKLINE>
    >>> Y = A.is_EF({}, [{}])
    >>> Y
    True
    >>> Y = B.is_EF({}, [{}])
    >>> Y
    True
    """
    """ Algorithm """
    result=""
    temp = []  
    temp2 = []
    val=0
    num_agents=len(agents)
    values={0:0,1:0} 
    
    logger.info("Checking if there are 0 items")
    if items==None:
        result=f"Alice gets {temp}  with value {0}.\n"     
        result+=f"Bob gets {temp2} with value {0}.\n"   
        return result
    num_of_items=len(items)
    if num_of_items==0:
        result=f"Alice gets {temp} with value {0}.\n"     #if there are no items then value is 0 for everyone
        result+=f"Bob gets {temp2} with value {0}.\n"  
        return result 
    
    logger.info("Checking if there is a single item") 
    if num_of_items==1:
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

    logger.info("Stage 1")    
    for group in all_combinations(items, num_agents):
            counter=0
            for item in group:
                for item_ in item:
                    val=values[counter]+ agents[counter][item_]
                    values[counter]=val
                counter+=1
            groupi2=group[0]
            groupi=group[1]
            counter_groupi2=len(groupi2)
            counter_groupi=len(groupi)
            counteri=0
            counter_=0
            val2=val22=0
            for item_ in groupi:
                    val2+=agents[0][item_]    
            for item_ in groupi2:
                    val22+=agents[1][item_]    
            if values[0]>=val2: #Alice weakly prefers X to Y
                for item_ in groupi2: #If any single item is moved from X to Y
                    if values[0]-agents[0][item_]>=val2+agents[0][item_]: #then Alice strictly prefers Y to X
                        break
                    counteri=counteri+1
                if counteri==counter_groupi2: #(X,Y) is almost-equal-cut for Alice (prefers X to Y)
                    logger.info("\t{} is almost-equal-cut for agent Alice (prefers {} to {})".format(group, groupi2,groupi))
                    #this partition is presented to George
                    if values[1]>=val22: #George accepts the partition if he prefers Y to X
                        logger.info("Bob accepts the offer because he has more benefit from {} than {}".format(groupi,groupi2))
                        for ite in groupi:
                            temp.append(ite)
                        for ite in groupi2:
                            temp2.append(ite)
                        temp.sort()
                        temp2.sort()   
                        result=f"Alice gets {temp2} with value {values[0]}.\n"     
                        result+=f"Bob gets {temp} with value {values[1]}.\n" 
                        logger.info(result)  
                        return result
                    
                    else: #George rejects the partition if he prefers X to Y
                        logger.info("Bob rejects the offer because he has more benefit from {} than {}".format(groupi2,groupi))
                        for item_ in groupi2: # check if there exists an item x in X such that: 
                            if val22-agents[1][item_]>=values[1]+agents[1][item_]:  # George prefers X \ x to Y U x
                                for i in groupi2:
                                    if  i is not item_:
                                        temp.append(i) #George reports X \ x
                                for i in groupi: 
                                        temp2.append(i) #Alice prefers Y U x to X \ x (Since (X,Y) is an almost-equal-cut for Alice).
                                temp2.append(item_) #Y U x
                                temp.sort()
                                temp2.sort()   
                                result=f"Alice gets {temp2} with value {val2+agents[0][item_]}.\n"     
                                result+=f"Bob gets {temp} with value {val22-agents[1][item_]}.\n"   
                                logger.info(result) 
                                return result                       
            if values[1]>=val22: #George weakly prefers Y to X
                for item_ in groupi: #If any single item is moved from Y to X
                    if values[1]-agents[1][item_]>=val22+agents[1][item_]:  #then George strictly prefers X to Y
                        break
                    counter_=counter_+1 
                if counter_==counter_groupi: #(X,Y) is almost-equal-cut for George (prefers Y to X)
                    logger.info("\t{} is almost-equal-cut for agent Bob (prefers {} to {})".format(group, groupi,groupi2))
                    #this partition is presented to Alice
                    if values[0]>=val2: #Alice accepts the partition if she prefers X to Y
                        logger.info("Alice accepts the offer because he has more benefit from {} than {}".format(groupi2,groupi))
                        result=f"Alice gets {groupi2} with value {values[0]}.\n"     
                        result+=f"Bob gets {groupi} with value {values[1]}.\n"   
                        logger.info(result)
                        return result                          
                    else: #Alice rejects the partition if she prefers Y to X
                        logger.info("Alice rejects the offer because she has more benefit from {} than {}".format(groupi,groupi2))
                        for item_ in groupi: # check if there exists an item y in Y such that: 
                            if val2-agents[0][item_]>=values[0]+agents[0][item_]:  # Alice prefers Y \ y to X U y
                                for i in groupi:
                                    if  i is not item_:
                                        temp.append(i) #Alice reports Y \ y
                                for i in groupi2: 
                                        temp2.append(i) #George prefers X U y to Y \ y (Since (X,Y) is an almost-equal-cut for George).
                                temp2.append(item_) #X U y
                                temp.sort()
                                temp2.sort()
                                result=f"Alice gets {temp} with value {val2-agents[0][item_]}.\n"     
                                result+=f"Bob gets {temp2} with value {val22+agents[1][item_]}.\n"   
                                logger.info(result) 
                                return result    
           
            values={0:0,1:0}  
    return "There is no envy-free division" #If we went through all the possible combinations -> no envy-free division

def all_combinations(gr, num_agents):
    """
    Returns all possible combinations of division into 2 groups
    >>> items=['a','b','c','d']
    >>> group_ = all_combinations(items, 2)
    >>> print(group_)
    [[('a',), ('b', 'c', 'd')], [('b',), ('a', 'c', 'd')], [('c',), ('a', 'b', 'd')], [('d',), ('a', 'b', 'c')], [('a', 'b'), ('c', 'd')], [('a', 'c'), ('b', 'd')], [('a', 'd'), ('b', 'c')]]
    """
    n = len(gr)
    groups = [] 
    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups))
        else:
            if n - i > num_agents - len(groups):
                for group in groups:
                    group.append(gr[i])
                    yield from generate_partitions(i + 1)
                    group.pop()
            if len(groups) < num_agents:
                groups.append([gr[i]])
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

    
 