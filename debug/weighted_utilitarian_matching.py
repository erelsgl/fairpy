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

from fairpy.items.utilitarian_matching import utilitarian_matching
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
	map_agent_to_final_bundle = {name:[] for name in agent_names}
	for index,category in enumerate(categories):
		alloc = utilitarian_matching(agents, item_capacities={item:1 for item in category}, agent_weights=agent_weights)
		map_agent_to_bundle = alloc.map_agent_to_bundle()
		print(f"Category {index}: {map_agent_to_bundle}")
		for name in agent_names:
			if map_agent_to_bundle[name] is not None:
				map_agent_to_final_bundle[name] += map_agent_to_bundle[name]

	return Allocation(agents, map_agent_to_final_bundle)


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
	# "b": {"0x": 1, "0y": 12.5,              	 "1x": 1, "1y": 10.7},
	# "b": {"0x": 2*11/27, "0y": 25*11/27,       "1x": 3*12/35, "1y": 32*12/35},
}

# Example showing that using a different weight in each category might lead to envy cycles.
agents2 = {
	"a": {"0x": -1, "0y": -10,                   "1x": -4, "1y": -5},
	"b": {"0x": -2, "0y": -3,                    "1x": -1, "1y": -12},
}

agent_weights2 = {"a": 1, "b": 1}

# allocation = weighted_utilitarian_matching(agents2, categories, agent_weights2)



# agents3 = {
# 	"a": {"0x": 2, "0y": 3, "0z": 4,         "1x": 4, "1y": 3, "1z": 2},
# 	"b": {"0x": 20, "0y": 25, "0z": 30,      "1x": 30, "1y": 25, "1z": 20},
# 	"c": {"0x": 200, "0y": 205, "0z": 210,   "1x": 210, "1y": 205, "1z": 200},
# }

# allocation = weighted_utilitarian_matching(agents3, categories, agent_weights3)


agents = {
	"agent1": {"t11": 0, "t12": -3,   "t23": 0, "t24": -9,   "t35": 0, "t36": -2},
	"agent2": {"t11": 0, "t12": -6,   "t23": 0, "t24": -9,   "t35": 0, "t36": -1},
}
categories = [
	["t11","t12"],
	["t23","t24"],
	["t35","t36"],
]
weight1 = 1/2-0.01
agent_weights = {"agent1": weight1, "agent2": 1-weight1}
allocation = weighted_utilitarian_matching(agents, categories, agent_weights=agent_weights)
print(allocation.str_with_value_matrix())

