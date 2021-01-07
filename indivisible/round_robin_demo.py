#!python3

"""
Demonstration of the round-robin protocol.

Programmer: Erel Segal-Halevi
Since: 2020-11
"""

from fairpy.indivisible.agents import *
from fairpy.indivisible import round_robin

import logging, sys

round_robin.logger.addHandler(logging.StreamHandler(sys.stdout))
round_robin.logger.setLevel(logging.INFO)

Alice = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w": 0}, name="Alice")
George = AdditiveAgent({"x": 2, "y": 1, "z": 6, "w": 3}, name="George")
print(Alice)
print(George)

print("\n### Round-robin when Alice plays first:")
print(round_robin.round_robin("wxyz", [Alice, George], [0,1]))

print("\n### Round-robin when George plays first:")
print(round_robin.round_robin("wxyz", [Alice, George], [1,0]))
