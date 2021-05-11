#!python3 

"""
SETTING: 
* There are n=3 agents.
* There are k=2 categories of items, with n chores in each category.
* The capacity of each category is 1. 

GOAL: Prove/disprove the existence of an:
* EF1 allocation (for chores);
* EF1 allocation without cycles (for chores);
* EF1 allocation that is also PO (for goods, chores).

IDEA: find a utilitarian (=maximum weight) matching in each category. This guarantees PO and no-cycles, but not EF1.
* But, we can give a different weight-factor to each agent. 
* Is there a vector of weights for which the utilitarian matching is EF1?
"""

from fairpy.indivisible.utilitarian_matching import utilitarian_matching
from fairpy.allocations import Allocation
from typing import List,Any,Dict

def weighted_utilitarian_matching(agents:Dict[str,Dict[Any,float]], categories: List[List[Any]], agent_weights:Dict[str,float]):
	"""
	:param categories: a list of categories; each one contains a list of items.
	:param agents: maps an agent name to the agent's valuation. Each valuation is a map from item name to its value.
	:param agent_weights: maps an agent name to the agent's weight-factor.

	:return a matching in which each agent gets a single item from each category. 
	        It is a maximum-weight matching in each category, with each agent's weights multiplied by the agent's factor.
	"""
	agent_names = sorted(agents.keys())
	num_of_agents = len(agent_names)
	map_agent_to_bundle = {name:[] for name in agent_names}
	for index,category in enumerate(categories):
		map_agent_to_matched_good = utilitarian_matching(agents, item_capacities={item:1 for item in category}, agent_weights=agent_weights)[0]
		for name in agent_names:
			map_agent_to_bundle[name].append(map_agent_to_matched_good[name])
		# matching_values = {agent: agents[agent][matching[agent]] for agent in agent_names}
		# print(f"Matching in category {index}: {matching}, values: {matching_values}")

	allocation = num_of_agents*[None]
	for i_agent,name in enumerate(agent_names):
		allocation[i_agent] = map_agent_to_bundle[name]
	return Allocation(agents, allocation)


"""
Agents are named A, B, C, ...
Categories are named 1, 2, ...
Items are named 1x, 1y, ... 2x, 2y, ...
"""

categories = [
	["0x","0y","0z"],
	["1x","1y","1z"],
	["2x","2y","2z"],
]

agents2 = {
	"a": {"0x": -1, "0y": -10,                   "1x": -1, "1y": -11,      "2x": -1, "2y": -15},
	"b": {"0x": -2, "0y": -25,                   "1x": -3, "1y": -32,      "2x": -4, "2y": -25},
	# "b": {"0x": 1, "0y": 12.5,               "1x": 1, "1y": 10.7},
	# "b": {"0x": 2*11/27, "0y": 25*11/27,       "1x": 3*12/35, "1y": 32*12/35},
}

# Example showing that using a different weight in each category might lead to envy cycles.
# agents2 = {
# 	"a": {"0x": -1, "0y": -10,                   "1x": -4, "1y": -5},
# 	"b": {"0x": -2, "0y": -3,                    "1x": -1, "1y": -12},
# }


agent_weights2 = {"a": 1, "b": 1}

allocation = weighted_utilitarian_matching(agents2, categories, agent_weights2)
print(allocation.str_with_value_matrix())



agents3 = {
	"a": {"0x": 2, "0y": 3, "0z": 4,         "1x": 4, "1y": 3, "1z": 2},
	"b": {"0x": 20, "0y": 25, "0z": 30,      "1x": 30, "1y": 25, "1z": 20},
	"c": {"0x": 200, "0y": 205, "0z": 210,   "1x": 210, "1y": 205, "1z": 200},
}

agent_weights3 = {"a": 1, "b": 10, "c": 1}
# allocation = weighted_utilitarian_matching(agents3, categories, agent_weights3)
