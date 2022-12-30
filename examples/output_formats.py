#' # Output formats

import fairpy
divide = fairpy.divide

#' The output of a fair division allocation is usually an `Allocation` object.

agent_values = {"avi": {"x":5, "y": 4}, "beni": {"x":2, "y":3}, "gadi": {"x":3, "y":2}}
agent_capacities = {"avi":2,"beni":1,"gadi":1}
agent_weights = {"avi":1, "gadi":10, "beni":100}
item_capacities = {"x":2, "y":2}
allocation = divide(fairpy.items.utilitarian_matching, agent_values, item_capacities=item_capacities, agent_capacities=agent_capacities, agent_weights=agent_weights)

#' You can see what bundle is given to each agent:
print(allocation.map_agent_to_bundle())
#' and which agent/s hold/s each item:
print(allocation.map_item_to_agents())

#' You can see the utility profile:
print(allocation.utility_profile())
#' and the utility matrix:
print(allocation.utility_profile_matrix())
#' With this information, you can compute various metrics on the allocation, such as:
#' its utilitarian value, egalitarian value, number of envy-pairs or largest envy magnitude.

#' Some algorithms accept a valuation matrix and return an allocation matrix, where each element z[i,j] is the fraction given to agent i from item j:
allocation = divide(fairpy.items.leximin_optimal_allocation, [[4,5],[2,3],[3,2]])
print(allocation)

#' The allocation matrix is inaccurate due to floating point issues; you can round it:

allocation.round(3)
print(allocation)


