#!python3
"""
Demonstration of the envy free piecewise linear protocol.

Programmer: Guy Wolf
Since: 2020-2
"""

from fairpy.agents import *
from fairpy.cake import piecewise_linear_cake_division

import logging, sys

piecewise_linear_cake_division.logger.addHandler(logging.StreamHandler(sys.stdout))
piecewise_linear_cake_division.logger.setLevel(logging.INFO)

Alice = PiecewiseUniformAgent([(2,3)], "Alice")
George = PiecewiseUniformAgent([(4,7)], "George")
Benny = PiecewiseUniformAgent([(0,10)], "Benny")
Margaret = PiecewiseUniformAgent([(0,10)], "Margaret")

print(Alice)
print(George)
print(Benny)

print("\n### Cover of agents:")
print(piecewise_linear_cake_division.Cover(0, 10, [Alice, George, Benny, Margaret]))

print("\n### Envy free allocation:")
print(piecewise_linear_cake_division.EFAllocate([Alice, George, Benny, Margaret]))

#showing the effect of a very high rounding paramater which leads to wierd results, do not use normally.
"""
print("\n### Very high round paramater:")
print(piecewise_linear_cake_division.EFAllocate([Alice, George, Benny, Margaret], roundAcc=50))
"""
