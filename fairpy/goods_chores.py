########## algo 1 ##############
from typing import List

from fairpy.agentlist import AgentList


def  Double_RoundRobin_Algorithm(agent_list :AgentList)->dict:
    """
    "Fair allocation of indivisible goods and chores" by  Ioannis Caragiannis ,
        Ayumi Igarashi, Toby Walsh and Haris Aziz.(2021) , link
        Algorithm 1: Finding an EF1 allocation
        Programmer: Yair Raviv , Rivka Strilitz
        Example 1:
        >>> Double_RoundRobin_Algorithm(AgentList({"Agent1":{"1":-2,"2":1,"3":0,"4":1,"5":-1,"6":4},"Agent2":{"1":1,"2":-3,"3":-4,"4":3,"5":2,"6":-1},"Agent3":{"1":1,"2":0,"3":0,"4":6,"5":0,"6":0}}))
        {"Agent1":["6"],"Agent2":["5","2"],"Agent3":["1","3","4"]}
        Example 2:
        >>>Double_RoundRobin_Algorithm(AgentList({"Agent1":{"1":-2,"2":-2,"3":1,"4":0,"5":5,"6":3,"7":-2},"Agent2":{"1":3,"2":-1,"3":0,"4":0,"5":7,"6":2,"7":-1},
        >>>"Agent3":{"1":4,"2":-3,"3":6,"4":-2,"5":4,"6":1,"7":0},"Agent4":{"1":3,"2":-4,"3":2,"4":0,"5":3,"6":-1,"7":-4}}))
        {"Agent1":["6"],"Agent2":["5"],"Agent3":["7","3"],"Agent4":["1","2","4"]}
    """
    pass



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
    "Fair allocation of indivisible goods and chores" by  Ioannis Caragiannis ,
        Ayumi Igarashi, Toby Walsh and Haris Aziz.(2021) , link
        Algorithm 2:  Finding an EF1 and PO allocation
        Programmer: Yair Raviv , Rivka Strilitz
        Example 1:
        >>> Generalized_Adjusted_Winner_Algorithm(AgentList({"Agent1":{"1":1,"2":-1,"3":-2,"4":3,"5":5,"6":0,"7":0,"8":-1,"9":2,"10":3},"Agent2":{"1":-3,"2":4,"3":-6,"4":2,"5":4,"6":-3,"7":2,"8":-2,"9":4,"10":5}}))
        {'Agent1': ['1', '4', '5', '6', '9', '10'], 'Agent2': ['2', '3', '7', '8']}

        Example 2:
        >>> Generalized_Adjusted_Winner_Algorithm(AgentList({"Agent1":{"1":1,"2":-1,"3":-2}, "Agent2":{"1":-3,"2":4,"3":-6}}))
        {'Agent1': ['1'], 'Agent2': ['2', '3']}

    """
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
            return {"Agent1" : sorted(Winner_bundle , key=lambda x: int(x)) , "Agent2" : sorted(Looser_bundle , key=lambda x: int(x))}
        if t in O_plus:
            Winner_bundle.remove(t)
            Looser_bundle.append(t)
        else:
            Winner_bundle.append(t)
            Looser_bundle.remove(t)
    return {}










def  Generalized_Moving_knife_Algorithm(agent_list :AgentList , prop_values: dict , remain_interval:list , result : dict)->dict:
    """
    "Fair allocation of indivisible goods and chores" by  Ioannis Caragiannis ,
        Ayumi Igarashi, Toby Walsh and Haris Aziz.(2021) , link
        Algorithm 3:  Finding a Connected PROP1 Allocation
        Programmer: Yair Raviv , Rivka Strilitz
        Example 1: Non-Negative Proportional Utilities
        >>> Generalized_Moving_knife_Algorithm(AgentList({"Agent1":{"1":0,"2":-1,"3":2,"4":1},"Agent2":{"1":1,"2":3,"3":1,"4":-2},"Agent3":{"1":0,"2":2,"3":0,"4":-1}}) , {"Agent1":2/3, "Agent2" : 1, "Agent3" : 1/3} , [0,4] , {"Agent1":[] , "Agent2":[] , "Agent3": []})
        {'Agent1': ['3', '4'], 'Agent2': ['1'], 'Agent3': ['2']}

        Example 2: Positive and Negative Proportional Utilities
        >>> Generalized_Moving_knife_Algorithm(AgentList({"Agent1":{"1":0,"2":2,"3":0,"4":-4},"Agent2":{"1":1,"2":-2,"3":1,"4":-2},"Agent3":{"1":0,"2":-4,"3":1,"4":1}}),{"Agent1": (-1 * 2 / 3), "Agent2": (-1 * 2 / 3), "Agent3": (-1 * 2 / 3)},[0, 4], {"Agent1": [], "Agent2": [], "Agent3": []})
        {'Agent1': ['1', '2', '3'], 'Agent2': [], 'Agent3': ['4']}

    """

    agents_num = len(agent_list)
    if agents_num <= 0:
        return {}

    all_items = list(range(remain_interval[0] +1 ,remain_interval[1] +1))
    N_plus = []
    for agent in agent_list:
        # total value for all items
        evaluation = sum([agent.value(str(x)) for x in all_items])
        if evaluation > 0:
            N_plus.append(agent)
    if len(N_plus) > 0:
        if len(N_plus) == 1:
            # allocate all items to the single agent
            result[N_plus[0].name()] = [str(x) for x in all_items]
            # sort the result by agent number
            return dict(sorted(result.items() , key= lambda agent: int(agent[0][5])))
        sums = {}
        for agent in N_plus:
            sums[agent.name()] = 0
        curr_bundle = []
        for i in all_items:
            curr_bundle.append(str(i))
            # check if there is agent that claim the current bundle at this iteration
            for agent in N_plus:
                sums[agent.name()] += agent.value(str(i))
                if sums[agent.name()] >= prop_values[agent.name()]:
                    result[agent.name()] = curr_bundle
                    agent_list.remove(agent)
                    # recursive call with : updated result , remain interval (items) and without the current agent
                    return Generalized_Moving_knife_Algorithm(agent_list=agent_list , prop_values=prop_values , remain_interval=[i,all_items[len(all_items) -1]] , result=result)
    # if there is no agent with positive total value for the items
    else:
        if len(agent_list) == 1:
            # allocate all items to the single agent
            result[agent_list[0].name()] = [str(x) for x in all_items]
            # sort the result by agent number
            return dict(sorted(result.items(), key=lambda agent: int(agent[0][5])))
        sums = {}
        for agent in agent_list:
            sums[agent.name()] = sum([agent.value(str(x)) for x in all_items])
        curr_bundle = [str(x) for x in all_items]
        while len(curr_bundle) > 0:
            for agent in agent_list:
                if sums[agent.name()] >= (-1 * prop_values[agent.name()]):
                    result[agent.name()] = curr_bundle
                    agent_list.remove(agent)
                    return Generalized_Moving_knife_Algorithm(agent_list=agent_list, prop_values=prop_values,
                                                              remain_interval=[len(curr_bundle) , all_items[len(all_items) - 1]],
                                                              result=result)
                sums[agent.name()] -= agent.value(curr_bundle[len(curr_bundle) -1])
            curr_bundle.pop()
    return result

if __name__ == '__main__':
    import doctest

    (failures, tests) = doctest.testmod(report=True, optionflags=doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS)
    print("{} failures, {} tests".format(failures, tests))

    # print(Generalized_Adjusted_Winner_Algorithm(AgentList({"Agent1":{"1":1,"2":-1,"3":-2,"4":3,"5":5,"6":0,"7":0,"8":-1,"9":2,"10":3},"Agent2":{"1":-3,"2":4,"3":-6,"4":2,"5":4,"6":-3,"7":2,"8":-2,"9":4,"10":5}})))


    # print(Generalized_Moving_knife_Algorithm(AgentList({"Agent1":{"1":0,"2":-1,"3":2,"4":1},"Agent2":{"1":1,"2":3,"3":1,"4":-2},"Agent3":{"1":0,"2":2,"3":0,"4":-1}}) ,
    #                                    {"Agent1":2/3, "Agent2" : 1, "Agent3" : 1/3} , [0,4] , {"Agent1":[] , "Agent2":[] , "Agent3": []}))

    # print(Generalized_Moving_knife_Algorithm(AgentList(
    #     {"Agent1": {"1": 0, "2": 2, "3": 0, "4": -4}, "Agent2": {"1": 1, "2": -2, "3": 1, "4": -2},
    #      "Agent3": {"1": 0, "2": -4, "3": 1, "4": 1}}),
    #                                          {"Agent1": (-1 * 2 / 3), "Agent2": (-1 * 2 / 3), "Agent3": (-1 * 2 / 3)},
    #                                          [0, 4], {"Agent1": [], "Agent2": [], "Agent3": []}))
