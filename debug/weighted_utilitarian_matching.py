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

from fairpy.items.iterated_maximum_matching import iterated_maximum_matching_categories

agents = {
	"agent1": {"t11": 0, "t12": -3,   "t23": 0, "t24": -9,   "t35": 0, "t36": -2},
	"agent2": {"t11": 0, "t12": -6,   "t23": 0, "t24": -9,   "t35": 0, "t36": -1},
}
categories = [
	["t11","t12"],
	["t23","t24"],
	["t35","t36"],
]
weight1 = 1
agent_weights = {"agent1": weight1, "agent2": 1-weight1}
allocation = iterated_maximum_matching_categories(agents, categories, agent_weights=agent_weights)
print(allocation.str_with_value_matrix())

