#!python3

import fairpy

print("The output of a fair division allocation is usually an `Allocation` object.")
instance = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }
allocation = fairpy.items.round_robin(instance)

print("\nYou can see what bundle is given to each agent:")
print(allocation.map_agent_to_bundle())
print("\nYou can also see which agent/s holds each item:")
print(allocation.map_item_to_agents())
print("\nYou can see the utility profile:")
print(allocation.utility_profile())



