#!python3

"""
Demonstration of Course allocation by proxy auction algorithm.

Programmer: Avihu Goren
Since: 2023-01
"""

from fairpy.agents import AdditiveAgent
from fairpy.items import course_allocation_by_proxy_auction

print("Course Allocation Algorithm starting..\n")
Alice = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3,}, name="Alice")
Bob = AdditiveAgent({"c1": 1, "c2": 2, "c3": 3, }, name="Bob")
Eve = AdditiveAgent({"c2": 1, "c3": 2, "c1": 3, }, name="Eve")
agents = [Alice,Bob,Eve]
print("Agents:")
for agn in agents:
    print(agn)
allocation = course_allocation_by_proxy_auction.course_allocation(agents,2,["c1","c2","c3"],2)
print(allocation)
