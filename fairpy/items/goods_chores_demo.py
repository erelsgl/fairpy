"""
Demo for the Goods & Chores allocation algorithms
Reference:
"Fair allocation of indivisible goods and chores" by  Ioannis Caragiannis ,
Ayumi Igarashi, Toby Walsh and Haris Aziz.(2021).

Programmers: Yair Raviv , Rivka Strilitz
"""

import fairpy
from fairpy.items.goods_chores import *

DoubleRoundRobinInput = AgentList({"Agent1":{"1":-2,"2":1,"3":0},"Agent2":{"1":1,"2":-3,"3":-4},"Agent3":{"1":1,"2":0,"3":0}})
print(fairpy.divide(algorithm=Double_RoundRobin_Algorithm, input=DoubleRoundRobinInput))

GeneralizedAdjustedWinnerInput = AgentList({"Agent1":{"1":-2,"2":1},"Agent2":{"1":1,"2":-3}})
print(fairpy.divide(algorithm=Generalized_Adjusted_Winner_Algorithm, input=GeneralizedAdjustedWinnerInput))

GeneralizedMovingKnifeInput = AgentList({"Agent1":{"1":-2,"2":1,"3":0},"Agent2":{"1":1,"2":-3,"3":-4},"Agent3":{"1":-1,"2":-2,"3":-3}})
print(fairpy.divide(algorithm=Generalized_Moving_knife_Algorithm, input=GeneralizedMovingKnifeInput))


