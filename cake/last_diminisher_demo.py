#!python3

"""
Demonstration of the last-diminisher protocol.

Programmer: Erel Segal-Halevi
Since: 2019-12
"""

from fairpy.cake.agents import *
from fairpy.cake import last_diminisher

import logging, sys

last_diminisher.logger.addHandler(logging.StreamHandler(sys.stdout))
last_diminisher.logger.setLevel(logging.INFO)

Alice = PiecewiseConstantAgent([3,6,3], name="Alice")
George = PiecewiseConstantAgent([0,2,4,6], name="George")
Abraham = PiecewiseConstantAgent([6,4,2,0], name="Abraham")
Hanna = PiecewiseConstantAgent([3,3,3,3], name="Hanna")

all_agents = [Alice, George, Abraham, Hanna]
for a in all_agents:
    print(a)

print("\n### Order: Alice, George, Abraham, Hanna")
print(last_diminisher.last_diminisher(all_agents))

print("\n### Order: Hanna, Abraham, George, Alice")
all_agents.reverse()
print(last_diminisher.last_diminisher(all_agents))

