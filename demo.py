#!python3

"""
The fairpy library is a library of data structures and algorithms for fair division.
Its primary design goal is ease of use for both users of existing algorithms,
and developers of new algorithms.
"""

import fairpy

"""
## For users

`fairpy` allows various input formats, so that you can easily use it on your own data,
whether for research or for application.

As an example application, suppose you want to allocate candies among your children.
You can ask them how much they like each kind of candy, and record the answers in a dict:
"""

items = ["green", "red", "blue", "yellow"]
agents = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }

"""
Then you can run various algorithms for indivisible item allocaiton, 
such as [round-robin item allocation](https://en.wikipedia.org/wiki/Round-robin_item_allocation):
"""

print(fairpy.items.round_robin(agents))

"""
To better understand how the algorithm works, you can use the logger, 
which is based on the standard python `logging` library:
"""

import sys, logging
fairpy.items.round_robin.logger.addHandler(logging.StreamHandler(sys.stdout))
fairpy.items.round_robin.logger.setLevel(logging.INFO)
print(fairpy.items.round_robin(agents))

"""
You can configure the `round_robin` method with optional arguments such as the order of agents, 
or the subset of items to allocate. This makes it easy to use it as a subroutine 
in more complex algorithms.
"""

print(fairpy.items.round_robin(agents, agent_order=[1,0], items=["green", "red", "blue"]))

"""
Passing a dict of dicts as a parameter may be too verbose.
You can call the same algorithm with only the values, or only the value matrix:
"""

fairpy.items.round_robin.logger.setLevel(logging.WARNING) # turn off INFO logging
print(fairpy.items.round_robin({"Ami": [8,7,6,5], "Tami": [12,8,4,2]}))
print(fairpy.items.round_robin([[8,7,6,5], [12,8,4,2]]))

"""
You can experiment with some other algorithms and see which of them gives better results:
"""

agents = {"Alice":  {"z":12, "y":10, "x":8, "w":7, "v":4, "u":1},
          "George": {"z":19, "y":16, "x":8, "w":6, "v":5, "u":1} }
print("Round robin:\n", fairpy.items.round_robin(agents))
print("Maximum matching:\n", fairpy.items.utilitarian_matching(agents))
print("Iterated maximum matching:\n", fairpy.items.iterated_maximum_matching(agents))
print("Max sum (aka utilitarian) allocation:\n", fairpy.items.max_sum_allocation(agents).round(3))
print("Max product (aka Nash welfare) allocation:\n", fairpy.items.max_product_allocation(agents).round(3))
print("Leximin allocation:\n", fairpy.items.leximin_optimal_allocation(agents).round(3))
print("PROPm allocation:\n", fairpy.items.propm_allocation(agents))

# print("Minimum-sharing envy-free allocation: \n", fairpy.items.envyfree_allocation_with_min_sharing(agents).round(3))
# print(fairpy.items.bidirectional_bag_filling(agents, thresholds=[13,12]))


