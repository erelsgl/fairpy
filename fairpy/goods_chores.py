########## algo 1 ##############
from typing import List

from fairpy.agentlist import AgentList


def  Double_RoundRobin_Algorithm(agent_list :AgentList)->List:
    """
    "Fair allocation of indivisible goods and chores" by  Ioannis Caragiannis ,
        Ayumi Igarashi, Toby Walsh and Haris Aziz.(2021) , link
        Algorithm 1: Finding an EF1 allocation
        Programmer: Yair Raviv , Rivka Strilitz
        Example 1:
        >>> Double_RoundRobin_Algorithm(AgentList({"Agent1":{"1":-2,"2":1,"3":0,"4":1,"5":-1,"6":4},"Agent2":{"1":1,"2":-3,"3":-4,"4":3,"5":2,"6":-1},"Agent3":{"1":1,"2":0,"3":0,"4":6,"5":0,"6":0}}))
        {"Agent1":["6"],"Agent2":["5","2"],"Agent3":["1","3","4"]}
        Example 2:
        >>>>Double_RoundRobin_Algorithm(AgentList({"Agent1":{"1":-2,"2":-2,"3":1,"4":0,"5":5,"6":3,"7":-2},"Agent2":{"1":3,"2":-1,"3":0,"4":0,"5":7,"6":2,"7":-1},
        >>>"Agent3":{"1":4,"2":-3,"3":6,"4":-2,"5":4,"6":1,"7":0},"Agent4":{"1":3,"2":-4,"3":2,"4":0,"5":3,"6":-1,"7":-4}}))
        {"Agent1":["6"],"Agent2":["5"],"Agent3":["7","3"],"Agent4":["1","2","4"]}
    """
    pass
def  Generalized_Adjusted_Winner_Algorithm(agent_list :AgentList)->List:
    """
    "Fair allocation of indivisible goods and chores" by  Ioannis Caragiannis ,
        Ayumi Igarashi, Toby Walsh and Haris Aziz.(2021) , link
        Algorithm 2:  Finding an EF1 and PO allocation
        Programmer: Yair Raviv , Rivka Strilitz
        Example 1:
        >>> Generalized_Adjusted_Winner_Algorithm(AgentList({"Agent1":{"1":1,"2":-1,"3":-2,"4":3,"5":5,"6":0,"7":0,"8":-1,"9":2,"10":3},
        >>>"Agent2":{"1":-3,"2":4,"3":-6,"4":2,"5":4,"6":-3,"7":2,"8":-2,"9":4,"10":5}}))
        {"Agent1":["6","1","4","10","5"],"Agent2":["2","7","8","3","9"]}
        Example 2:
        >>> Generalized_Adjusted_Winner_Algorithm(AgentList({"Agent1":{"1":1,"2":-1,"3":-2},
        >>>"Agent2":{"1":-3,"2":4,"3":-6}}))
        {"Agent1":["1"],"Agent2":["2","3"]}

    """
    pass
def  Generalized_Moving_knife_Algorithm(agent_list :AgentList)->List:
    """
    "Fair allocation of indivisible goods and chores" by  Ioannis Caragiannis ,
        Ayumi Igarashi, Toby Walsh and Haris Aziz.(2021) , link
        Algorithm 3:  Finding a Connected PROP1 Allocation
        Programmer: Yair Raviv , Rivka Strilitz
        Example 1: Non-Negative Proportional Utilities
        >>> Generalized_Moving_knife_Algorithm(AgentList({"Agent1":{"1":0,"2":-1,"3":2,"4":1},"Agent2":{"1":1,"2":3,"3":1,"4":-2},"Agent3":{"1":0,"2":2,"3":0,"4":-1}})){"Agent1":["3","4"],"Agent2":["1"],"Agent3":["2"]}
        Example 2: Positive and Negative Proportional Utilities
        >>> Generalized_Moving_knife_Algorithm(AgentList({"Agent1":{"1":0,"2":2,"3":0,"4":-4},"Agent2":{"1":1,"2":-2,"3":1,"4":-2},"Agent3":{"1":0,"2":-4,"3":1,"4":1}})){"Agent1":["1","2","3"],"Agent2":[],"Agent3":["4"]}


    """
    pass



