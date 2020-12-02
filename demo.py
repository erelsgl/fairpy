#!python3

"""
Demonstrates how to use some cake-cutting protocols (cut-and-choose, last-diminisher)

Programmer: Erel Segal-Halevi
Since: 2020-10
"""


from cake.agents import PiecewiseUniformAgent, PiecewiseConstantAgent
from cake import cut_and_choose, last_diminisher

import logging, sys

cut_and_choose.logger.addHandler(logging.StreamHandler(sys.stdout))
cut_and_choose.logger.setLevel(logging.INFO)

last_diminisher.logger.addHandler(logging.StreamHandler(sys.stdout))
last_diminisher.logger.setLevel(logging.INFO)

Alice = PiecewiseUniformAgent ([(0,1),(3,6)], name="Alice")   # Alice has two desired intervals, 0..1 and 3..6. Each interval has value 1.
George = PiecewiseConstantAgent([1,3,5,7],    name="George")  # George has four desired intervals: 0..1 with value 1, 1..2 with value 3, etc.

print(Alice)
print(George)

print("\n--- CUT AND CHOOSE ---")

print("\n### Alice cuts and George chooses:")
print(cut_and_choose.asymmetric_protocol([Alice, George]))

print("\n### George cuts and Alice chooses:")
print(cut_and_choose.asymmetric_protocol([George, Alice]))

print("\n### Symmetric protocol:")
print(cut_and_choose.symmetric_protocol([Alice, George]))

print("\n--- LAST DIMINISHER ---")
print(last_diminisher.last_diminisher([Alice, George]))




print("\n--- ROUND ROBIN ---")

from indivisible.agents import AdditiveAgent
from indivisible import round_robin

Ami = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w": 0}, name="Ami")
Tami = AdditiveAgent({"x": 2, "y": 1, "z": 6, "w": 3}, name="Tami")
print(Ami)
print(Tami)

print("\n### Round-robin when Ami plays first:")
print(round_robin.round_robin("wxyz", [Ami, Tami], [0,1]))

print("\n### Round-robin when Tami plays first:")
print(round_robin.round_robin("wxyz", [Tami, Ami], [1,0]))
