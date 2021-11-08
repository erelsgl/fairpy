#' # Output formats
#' The output of a fair division allocation is usually an `Allocation` object.

from fairpy.items.utilitarian_matching import utilitarian_matching
agent_values = {"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}, "gadi": {"x":3, "y":2}}
agent_capacities = {"avi":2,"beni":1,"gadi":1}
agent_weights = {"avi":1, "gadi":10, "beni":100}
item_capacities = {"x":2, "y":2}
allocation = utilitarian_matching(agent_values, item_capacities=item_capacities, agent_capacities=agent_capacities, agent_weights=agent_weights)

#' You can see what bundle is given to each agent:
print(allocation.map_agent_to_bundle())
#' and which agent/s hold/s each item:
print(allocation.map_item_to_agents())

#' You can see the utility profile:
print(allocation.utility_profile())
#' and the utility matrix:
print(allocation.utility_profile_matrix())
