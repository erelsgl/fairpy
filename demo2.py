#!python3

"""
Demonstrates how to use fairpy for indivisible item allocation.

Programmer: Erel Segal-Halevi
Since: 2021-05
"""


import fairpy

agents = {
    "Avram": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Sarah": {"green": 12, "red":8, "blue": 4, "yellow": 2} }

print(fairpy.items.round_robin(agents))
print(fairpy.items.round_robin(agents, agent_order=[1,0], items={"green", "red", "yellow"}))

print(fairpy.items.max_product_allocation(agents))

import sys, logging
fairpy.items.round_robin.logger.addHandler(logging.StreamHandler(sys.stdout))
fairpy.items.round_robin.logger.setLevel(logging.INFO)
print(fairpy.items.round_robin(agents))

