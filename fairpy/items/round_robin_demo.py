#!python3

"""
Demonstration of the round-robin protocol.

Programmer: Erel Segal-Halevi
Since: 2020-11
"""

import fairpy
from fairpy.agents import *
from fairpy.items.round_robin import round_robin

import logging, sys
round_robin.logger.addHandler(logging.StreamHandler(sys.stdout))
round_robin.logger.setLevel(logging.INFO)

Alice = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w": 0}, name="Alice")
George = AdditiveAgent({"x": 2, "y": 1, "z": 6, "w": 3}, name="George")
print(Alice)
print(George)

print("\n### Round-robin when Alice plays first:")
print(fairpy.divide(round_robin, [Alice, George], agent_order=[0,1], items="wxyz"))

print("\n### Round-robin when George plays first:")
print(fairpy.divide(round_robin, [Alice, George], agent_order=[1,0], items="wxyz"))

print("\n### One alternative input format:")
print(fairpy.divide(round_robin, [[11,22,44,0],[22,11,66,33]], agent_order=[1,0], items={0,1,2,3}))


items = ["green", "red", "blue", "yellow"]
agents = {
    "Avi": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Batya": {"green": 12, "red":8, "blue": 4, "yellow": 2} }
print(fairpy.divide(round_robin, agents, agent_order=[0,1], items=items))
