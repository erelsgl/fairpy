#!python3

"""
Demonstration of the cut-and-choose protocol.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""

from agents import *

import cut_and_choose, logging, sys

cut_and_choose.logger.addHandler(logging.StreamHandler(sys.stdout))
cut_and_choose.logger.setLevel(logging.INFO)

Alice = PiecewiseConstantAgent ([1,2,1], name="Alice")
George = PiecewiseConstantAgent([0,1,2,3],    name="George")

print(Alice)
print(George)

print("\n### Alice cuts and George chooses:")
print(cut_and_choose.asymmetric_protocol([Alice, George]))

print("\n### George cuts and Alice chooses:")
print(cut_and_choose.asymmetric_protocol([George, Alice]))

print("\n### Symmetric protocol:")
print(cut_and_choose.symmetric_protocol([Alice, George]))
