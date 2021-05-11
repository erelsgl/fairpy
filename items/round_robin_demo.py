#!python3

"""
Demonstration of the round-robin protocol.

Programmer: Erel Segal-Halevi
Since: 2020-11
"""

from fairpy.items.agents import AdditiveAgent
from fairpy.items.round_robin import round_robin

import logging, sys
round_robin.logger.addHandler(logging.StreamHandler(sys.stdout))
round_robin.logger.setLevel(logging.INFO)

Alice = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w": 0}, name="Alice")
George = AdditiveAgent({"x": 2, "y": 1, "z": 6, "w": 3}, name="George")
print(Alice)
print(George)

print("\n### Round-robin when Alice plays first:")
print(round_robin([Alice, George], [0,1], items="wxyz"))

print("\n### Round-robin when George plays first:")
print(round_robin([Alice, George], [1,0], items="wxyz"))

print("\n### One alternative input format:")
print(round_robin([[11,22,44,0],[22,11,66,33]], [1,0], items={0,1,2,3}))
