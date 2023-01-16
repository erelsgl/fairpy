########## algo 1 ##############
from typing import List

from fairpy.agentlist import AgentList
import math
import operator
import logging
logger = logging
logger.basicConfig(format='[%(levelname)s - %(asctime)s] - %(message)s', level=logging.INFO)


"""
    "Fair allocation of indivisible goods and chores" by  Ioannis Caragiannis ,
    Ayumi Igarashi, Toby Walsh and Haris Aziz.(2021) ,
    Programmers: Yair Raviv , Rivka Strilitz
"""

def  Double_RoundRobin_Algorithm(agent_list :AgentList)->dict:
    """
    Algorithm 1: Finding an EF1 allocation
    >>> Double_RoundRobin_Algorithm(AgentList({"Agent1":{"1":-2,"2":1,"3":0,"4":1,"5":-1,"6":4},"Agent2":{"1":1,"2":-3,"3":-4,"4":3,"5":2,"6":-1},"Agent3":{"1":1,"2":0,"3":0,"4":6,"5":0,"6":0}}))
    {'Agent1': ['3', '6'], 'Agent2': ['5', '2'], 'Agent3': ['4', '1']}

    >>> Double_RoundRobin_Algorithm(AgentList({"Agent1":{"1":-2,"2":-2,"3":1,"4":0,"5":5,"6":3,"7":-2},"Agent2":{"1":3,"2":-1,"3":0,"4":0,"5":7,"6":2,"7":-1},"Agent3":{"1":4,"2":-3,"3":6,"4":-2,"5":4,"6":1,"7":0},"Agent4":{"1":3,"2":-4,"3":2,"4":0,"5":3,"6":-1,"7":-4}}))
    {'Agent1': ['4', '6'], 'Agent2': ['5'], 'Agent3': ['7', '3'], 'Agent4': ['2', '1']}

    >>> Double_RoundRobin_Algorithm(AgentList({"Agent1":{"1t":-2,"2d":-2,"3":1,"4":0,"5":5,"6":3,"7":-2},"Agent2":{"1t":3,"2d":-1,"3":0,"4":0,"5":7,"6":2,"7":-1},"Agent3":{"1t":4,"2d":-3,"3":6,"4":-2,"5":4,"6":1,"7":0},"Agent4":{"1t":3,"2d":-4,"3":2,"4":0,"5":3,"6":-1,"7":-4}}))
    {'Agent1': ['4', '6'], 'Agent2': ['5'], 'Agent3': ['7', '3'], 'Agent4': ['2d', '1t']}
    """

    if not agent_list:
        logger.error("Invalid arguments")
        return {}

    N = agent_list.agent_names()
    O = agent_list.all_items()
    logger.info(f'Agents : {[agent.name() for agent in agent_list]}')
    logger.info(f'chores : {[o for o in O]}')
    # Initialize the allocation for each agent
    allocation = {i: [] for i in N}

    # Partition the items into O+ and O-
    o_plus = []
    o_minus = []

    for chore in O:
        for agent in agent_list:
            flag = False
            # if any agent values chore for more than 0
            if agent.value(str(chore)) > 0 :
                o_plus.append(str(chore))
                flag = True
                break;
        # if all agent values chore for less than or equal 0
        if flag is False :
            o_minus.append(str(chore))


    logger.info(f'O plus contains : {[o for o in o_plus]}')
    logger.info(f'O minus contains : {[o for o in o_minus]}')


    # Add k dummy items to O- such that |O- | = an
    k = len(N)-(len(o_minus) % len(N))
    o_minus += [None] * k
    logger.info(f'there are k dummy items k= : {k}')


    # Allocate items in O- to agents in round-robin sequence

    while len(o_minus) != 0:
        for agent in agent_list:
            best_val = -math.inf
            allocate_chore = 0
            for chore in o_minus[0:len(o_minus)-k]:

                curr_agent_val = agent.value(str(chore))
                if curr_agent_val > best_val:
                    best_val = curr_agent_val
                    allocate_chore = chore
            if best_val < 0 and k > 0:
                allocate_chore = None
                k -= 1
            allocation[agent.name()].append(allocate_chore)
            o_minus.remove(allocate_chore)

            if len(o_minus) == 0:
                break



    # Allocate items in O+ to agents in reverse round-robin sequence
    while len(o_plus) != 0:
        for agent in reversed(agent_list):
            best_val = -math.inf
            allocate_chore = 0
            for chore in o_plus:
                curr_agent_val = agent.value(str(chore))
                if curr_agent_val > best_val:
                    best_val = curr_agent_val
                    allocate_chore = str(chore)

            allocation[agent.name()].append(allocate_chore)
            o_plus.remove(allocate_chore)

            if len(o_plus) == 0:
                break

    # Remove dummy items from allocation
    for i in N:
        allocation[i] = [o for o in allocation[i] if o is not None]

    logger.info(f'after alocating O alocation contains : {allocation}')
    return allocation



def is_EF1(winner, looser, Winner_bundle, Looser_bundle):

    looser_total = sum([looser.value(x) for x in Looser_bundle])
    winner_total = sum([looser.value(x) for x in Winner_bundle])

    if looser_total >= winner_total:
        return True

    for item in Winner_bundle:
        if (looser_total + looser.value(item) >= (winner_total - looser.value(item))):
            return True

    for item in Looser_bundle:
        if (looser_total - looser.value(item) >= (winner_total + looser.value(item))):
            return True
    return False


def  Generalized_Adjusted_Winner_Algorithm(agent_list :AgentList)->dict:
    """
    Algorithm 2:  Finding an EF1 and PO allocation
    Example 1:
    >>> Generalized_Adjusted_Winner_Algorithm(AgentList({"Agent1":{"1":1,"2":-1,"3":-2,"4":3,"5":5,"6":0,"7":0,"8":-1,"9":2,"10":3},"Agent2":{"1":-3,"2":4,"3":-6,"4":2,"5":4,"6":-3,"7":2,"8":-2,"9":4,"10":5}}))
    {'Agent1': ['1', '10', '4', '5', '6', '9'], 'Agent2': ['2', '3', '7', '8']}

    Example 2:
    >>> Generalized_Adjusted_Winner_Algorithm(AgentList({"Agent1":{"1":1,"2":-1,"3":-2}, "Agent2":{"1":-3,"2":4,"3":-6}}))
    {'Agent1': ['1'], 'Agent2': ['2', '3']}
    """
    if not agent_list:
        logger.error("Invalid arguments")
        return {}

    if len(agent_list) != 2:
        raise "Invalid agents number"

    winner = agent_list[0]
    looser = agent_list[1]
    all_items = list(winner.all_items())

    O_plus = [x for x in all_items if winner.value(x) > 0 and looser.value(x) > 0]
    O_minus = [x for x in all_items if winner.value(x) < 0 and looser.value(x) < 0]
    O_w = [x for x in all_items if winner.value(x) >= 0 and looser.value(x) <= 0]
    O_l = [x for x in all_items if winner.value(x) <= 0 and looser.value(x) >= 0]


    for x in O_l:
        if x in O_w:
            O_l.remove(x)

    Winner_bundle = [x for x in O_plus]
    for x in O_w:
        if x not in Winner_bundle:
            Winner_bundle.append(x)

    Looser_bundle = [x for x in O_minus]
    for x in O_l:
        if x not in Looser_bundle:
            Looser_bundle.append(x)

    O_plus_O_minus = sorted((O_plus + O_minus) , key=lambda x : (abs(looser.value(x)) / abs(winner.value(x))) , reverse=True)

    for t in O_plus_O_minus:
        if is_EF1(winner , looser , Winner_bundle , Looser_bundle):
            return {"Agent1" : sorted(Winner_bundle , key=lambda x: x) , "Agent2" : sorted(Looser_bundle , key=lambda x: x)}
        if t in O_plus:
            Winner_bundle.remove(t)
            Looser_bundle.append(t)
        else:
            Winner_bundle.append(t)
            Looser_bundle.remove(t)









def Generalized_Moving_knife_Algorithm(agent_list :AgentList , items:list):
    """
    Algorithm 3:  Finding a Connected PROP1 Allocation
    Example 1: Non-Negative Proportional Utilities
    >>> Generalized_Moving_knife_Algorithm(AgentList({"Agent1":{"1":0,"2":-1,"3":2,"4":1},"Agent2":{"1":1,"2":3,"3":1,"4":-2},"Agent3":{"1":0,"2":2,"3":0,"4":-1}}) , ['1' , '2' , '3' , '4'])
    {'Agent1': ['3', '4'], 'Agent2': ['1'], 'Agent3': ['2']}

    Example 2: Positive and Negative Proportional Utilities
    >>> Generalized_Moving_knife_Algorithm(AgentList({"Agent1":{"1":0,"2":2,"3":0,"4":-4},"Agent2":{"1":1,"2":-2,"3":1,"4":-2},"Agent3":{"1":0,"2":-4,"3":1,"4":1}}),['1' , '2' , '3' , '4'])
    {'Agent1': ['1', '2', '3'], 'Agent2': [], 'Agent3': ['4']}

    """
    if not agent_list or not items:
        logger.error("Invalid arguments")
        return {}
    result = {}
    agents_num = len(agent_list)
    if agents_num <= 0:
        logger.warning("Empty Agent list")
        return {}
    prop_values = {}
    for agent in agent_list:
        prop_values[agent.name()] = (sum([agent.value(item) for item in items]) / agents_num)
        result[agent.name()] = []

    logger.info(f'Agents : {[agent.name() for agent in agent_list]} , Prop values : {prop_values}')
    res = Generalized_Moving_knife_Algorithm_Recursive(agent_list= agent_list ,prop_values= prop_values , remain_items=items ,result= result)

    return res

def  Generalized_Moving_knife_Algorithm_Recursive(agent_list :AgentList , prop_values: dict , remain_items:list , result : dict)->dict:

    all_items = remain_items
    # N+ is a set of agent with positive total value for the items
    N_plus = [agent for agent in agent_list if sum([agent.value(item) for item in all_items]) > 0]
    logger.info(f'N plus contains : {[agent.name() for agent in N_plus]}')
    if len(N_plus) > 0:
        if len(N_plus) == 1:
            # allocate all items to the single agent
            result[N_plus[0].name()] = [item for item in all_items]
            # sort the result by agent number
            return dict(sorted(result.items() , key= lambda agent: agent[0]))
        sums = {}
        for agent in N_plus:
            sums[agent.name()] = 0
        curr_bundle = []
        for item in all_items:
            curr_bundle.append(item)
            # check if there is an agent who claims the current bundle at this iteration
            for agent in N_plus:
                sums[agent.name()] += agent.value(item)
                if sums[agent.name()] >= prop_values[agent.name()]:
                    logger.info(f'Agent : {agent.name()} with prop value : {prop_values[agent.name()]} claims bundle {curr_bundle} , agent utility : {sums[agent.name()]}')
                    result[agent.name()] = curr_bundle
                    agent_list.remove(agent)
                    # recursive call with : updated result , remain interval (items) and without the current agent
                    index = all_items.index(item)
                    # print(f'agent {agent.name()} claim bundle {curr_bundle} , remain items are : {all_items[index +1 :len(all_items)]}')
                    logger.info(f'Allocate the rest of the items : {all_items[index +1 :len(all_items)]} for the rest of the agents : {[agent.name() for agent in agent_list]}')
                    return Generalized_Moving_knife_Algorithm_Recursive(agent_list=agent_list , prop_values=prop_values , remain_items = all_items[index +1 :len(all_items)] , result=result)

    # if there is no agent with positive total value for the items
    else:
        logger.info(f'N Minus contains : {[agent.name() for agent in agent_list]}')
        if len(agent_list) == 1:
            # allocate all items to the single agent
            result[agent_list[0].name()] = [item for item in all_items]
            # sort the result by agent number
            return dict(sorted(result.items(), key=lambda agent: agent[0]))
        sums = {}
        for agent in agent_list:
            sums[agent.name()] = sum([agent.value(item) for item in all_items])
        curr_bundle = [item for item in all_items]
        while len(curr_bundle) > 0:
            # check if there is an agent who claims the current bundle at this iteration
            for agent in agent_list:
                if sums[agent.name()] >= (-1 * prop_values[agent.name()]):
                    logger.info(
                        f'Agent : {agent.name()} with prop value : {prop_values[agent.name()]} claims bundle {curr_bundle} , agent utility : {sums[agent.name()]}')
                    result[agent.name()] = curr_bundle
                    agent_list.remove(agent)
                    index = all_items.index(curr_bundle[len(curr_bundle) -1])
                    logger.info(
                        f'Allocate the rest of the items : {all_items[index + 1:len(all_items)]} for the rest of the agents : {[agent.name() for agent in agent_list]}')
                    return Generalized_Moving_knife_Algorithm_Recursive(agent_list=agent_list, prop_values=prop_values,
                                                              remain_items=all_items[index +1 :len(all_items)],
                                                              result=result)
                sums[agent.name()] -= agent.value(curr_bundle[len(curr_bundle) -1])
            # if no agent claims the current bundle - remove the last item from the bundle'
            curr_bundle.pop()
    return result

if __name__ == '__main__':
    import doctest

    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS)
    print("{} failures, {} tests".format(failures, tests))
