#!python3

"""
Demonstration of the cut-and-choose protocol.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""

from fairpy.agents import PiecewiseConstantAgent, PiecewiseUniformAgent
from fairpy.cake import cut_and_choose

import logging, sys

cut_and_choose.logger.addHandler(logging.StreamHandler(sys.stdout))
cut_and_choose.logger.setLevel(logging.INFO)

Alice = PiecewiseUniformAgent ([(0,1),(3,6)], name="Alice")   # Alice has two desired intervals, 0..1 and 3..6. Each interval has value 1.
George = PiecewiseConstantAgent([1,3,5,7],    name="George")  # George has four desired intervals: 0..1 with value 1, 1..2 with value 3, etc.

print(Alice)
print(George)

print("\n### Alice cuts and George chooses:")
print(cut_and_choose.asymmetric_protocol([Alice, George]))

print("\n### George cuts and Alice chooses:")
print(cut_and_choose.asymmetric_protocol([George, Alice]))

print("\n### Symmetric protocol:")
print(cut_and_choose.symmetric_protocol([Alice, George]))
