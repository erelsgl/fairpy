#!python3

import fairpy

#' fairpy allows various input formats, so that you can easily use it on your own data,
#' whether for applications or for research.
#' For example, suppose you want to divide candies among your children.
#' It is convenient to collect their preferences in a dict of dicts:

instance = {
    "Ami": {"green": 8, "red":7, "blue": 6, "yellow": 5},
    "Tami": {"green": 12, "red":8, "blue": 4, "yellow": 2} }
print(instance)
allocation = fairpy.items.round_robin(instance)

#' You can then see the resulting allocation with the agents' real names:

print(allocation)  

#' For research, passing a dict of dicts as a parameter may be too verbose.
#' You can call the same algorithm with only the values, or only the value matrix:

print(fairpy.items.round_robin({"Ami": [8,7,6,5], "Tami": [12,8,4,2]}))
print(fairpy.items.round_robin([[8,7,6,5], [12,8,4,2]]))


#' For experiments, you can use a numpy random matrix:

import numpy as np
instance = np.random.randint(1,100,[2,4])
print(instance)
allocation = fairpy.items.round_robin(instance)
print(allocation)
