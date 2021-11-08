#!python3


print("The output of a fair division allocation is usually an `Allocation` object.")

from fairpy.items.utilitarian_matching import utilitarian_matching
agent_values = {"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}, "gadi": {"x":3, "y":2}}
agent_capacities = {"avi":2,"beni":1,"gadi":1}
agent_weights = {"avi":1, "gadi":10, "beni":100}
item_capacities = {"x":2, "y":2}
allocation = utilitarian_matching(agent_values, item_capacities=item_capacities, agent_capacities=agent_capacities, agent_weights=agent_weights)

print("\nYou can see what bundle is given to each agent, and which agent/s hold/s each item:")
print(allocation.map_agent_to_bundle())
print(allocation.map_item_to_agents())
print("\nYou can see the utility profile, and the utility matrix:")
print(allocation.utility_profile())
print(allocation.utility_profile_matrix())
