#!python3

"""
Demonstration of the Deng_Qi_Saberi approximate cake-cutting algorithm.

Programmer: Dvir Fried
Since: 2020-01
"""


from fairpy.agents import *
from fairpy.cake import Deng_Qi_Saberi

import logging, sys

Deng_Qi_Saberi.logger.addHandler(logging.StreamHandler(sys.stdout))
Deng_Qi_Saberi.logger.setLevel(logging.INFO)

# Alice = PiecewiseConstantAgent([3, 6, 3], name="Alice")
George = PiecewiseConstantAgent([0, 2, 4, 6], name="George")
Abraham = PiecewiseConstantAgent([6, 4, 2, 0], name="Abraham")
Hanna = PiecewiseConstantAgent([3, 3, 3, 3], name="Hanna")

all_agents = [George, Abraham, Hanna]
for a in all_agents:
    print(a)

epsilon = 0.01
print(epsilon)

print("\n### Order: Alice, George, Abraham, Hanna")
print(Deng_Qi_Saberi.elaborate_simplex_solution(all_agents, epsilon))

print("\n### Order: Hanna, Abraham, George, Alice")
all_agents.reverse()
print(Deng_Qi_Saberi.elaborate_simplex_solution(all_agents, epsilon))
