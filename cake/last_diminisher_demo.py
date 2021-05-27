#!python3

"""
Demonstration of the last-diminisher protocol.

Programmer: Erel Segal-Halevi
Since: 2019-12
"""

from fairpy.agents import *
from fairpy.cake import last_diminisher

import logging, sys

last_diminisher.logger.addHandler(logging.StreamHandler(sys.stdout))
last_diminisher.logger.setLevel(logging.INFO)

Alice = PiecewiseConstantAgent([10,4,4,6], name="Eli")
George = PiecewiseConstantAgent([10,4,6,4], name="Beni")
Abraham = PiecewiseConstantAgent([10,6,4,4], name="Gadi")
Hanna = PiecewiseConstantAgent([3,3,3,3], name="Hanna")

# all_agents = [Alice, George, Abraham, Hanna]
all_agents = [Alice, George, Abraham]
for a in all_agents:
    print(a)

print(f"\n### Order: {[a.name() for a in all_agents]}")
print(last_diminisher.last_diminisher(all_agents))

all_agents.reverse()
print(f"\n### Order: {[a.name() for a in all_agents]}")
print(last_diminisher.last_diminisher(all_agents))

