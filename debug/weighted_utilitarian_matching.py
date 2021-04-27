#!python3 

"""
SETTING: 
* There are n=3 agents.
* There are k=2 categories of items, with n chores in each category.
* The capacity of each category is 1. 

GOAL: Prove/disprove the existence of an:
* EF1 allocation;
* EF1 allocation without cycles;
* EF1 allocation that is also PO.

IDEA: find a utilitarian (=maximum weight) matching in each category. This guarantees PO and no-cycles, but not EF1.
* But, we can give a different weight-factor to each agent. 
* Is there a vector of weights for which the utilitarian matching is EF1?
"""

from fairpy.indivisible.utilitarian_matching import utilitarian_matching
from typing import List,Any,Dict

def weighted_utilitarian_matching(categories: List[List[Any]], agents:Dict[str,Dict[Any,float]], agent_weights:Dict[str,float]):
	"""
	:param categories: a list of categories; each one contains a list of items.
	:param agents: maps an agent name to the agent's valuation. Each valuation is a map from item name to its value.
	:param agent_weights: maps an agent name to the agent's weight-factor.

	:return a matching in which each agent gets a single item from each category. 
	        It is a maximum-weight matching in each category, with each agent's weights multiplied by the agent's factor.
	"""
	for index,category in enumerate(categories):
		matching = utilitarian_matching(agents, item_capacities={item:1 for item in category}, agent_weights=agent_weights)[0]
		matching_values = {agent: agents[agent][matching[agent]] for agent in agent_names}
		print(f"Matching in category {index}: {matching}, values: {matching_values}")


"""
Agents are named A, B, C, ...
Categories are named 1, 2, ...
Items are named 1x, 1y, ... 2x, 2y, ...
"""



categories = [
	["0x","0y","0z"],
	["1x","1y","1z"]
]

agents = {
	"a": {"0x": 2, "0y": 3, "0z": 4,   "1x": 4, "1y": 3, "1z": 2},
	"b": {"0x": 20, "0y": 25, "0z": 30,   "1x": 30, "1y": 25, "1z": 20},
	"c": {"0x": 200, "0y": 205, "0z": 210,   "1x": 210, "1y": 205, "1z": 200},
}

agent_names = sorted(agents.keys())

agent_weights = {"a": 100, "b": 10, "c": 1}

for index,category in enumerate(categories):
	matching = utilitarian_matching(agents, item_capacities={item:1 for item in category}, agent_weights=agent_weights)[0]
	matching_values = {agent: agents[agent][matching[agent]] for agent in agent_names}
	print(f"Matching in category {index}: {matching}, values: {matching_values}")
