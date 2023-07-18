#!python3

"""
Demonstration of Course allocation by proxy auction algorithm.

Programmer: Avihu Goren
Since: 2023-01
"""

import fairpy
from fairpy.agents import AdditiveAgent
from fairpy.courses.course_allocation_by_proxy_auction import course_allocation_by_proxy_auction
from fairpy.courses.adaptors import divide

print("Course Allocation Algorithm starting..\n")
valuations = {"Alice": {"c1": 1, "c2": 2, "c3": 3,} ,"Bob": {"c1": 1, "c2": 2, "c3": 3, }, "Eve": {"c2": 1, "c3": 2, "c1": 3, }}
print("Agents:")
for agn,valuation in valuations.items():
    print(agn, ": ", valuation)
print(divide(course_allocation_by_proxy_auction, valuations=valuations, item_capacities=2, agent_capacities=2))
