#' # Fair item allocation algorithms

import fairpy
divide = fairpy.divide


#' `fairpy` contains various algorithms for fair allocation of items,
#' both divisible and indivisible.
#' Before starting the algorithms, let us create some inputs for them.

input_3_agents = {"Alice":  {"z":12, "y":10, "x":8, "w":7, "v":4, "u":1},
          "Dina":   {"z":14, "y":9, "x":15, "w":4, "v":9, "u":12},
          "George": {"z":19, "y":16, "x":8, "w":6, "v":5, "u":1},
           }

input_2_agents = {
    "Alice":  {"a": 2, "b": 6, "c": 3, "d":3,"e":1,"f":7,"g":15,"h":21,"i":4,"j":22,"k":7,"l":10,"m":11,"n":22,"o":6,"p":7,"q":16,"r":12,"s":3,"t":28,"u":39,"v":4,"w":9,"x":1,"y":17,"z":99},
    "George": {"a": 2, "b": 4, "c": 3, "d":1,"e":0,"f":7,"g":16,"h":21,"i":4,"j":23,"k":7,"l":10,"m":11,"n":22,"o":6,"p":9,"q":16,"r":10,"s":3,"t":24,"u":39,"v":2,"w":9,"x":5,"y":17,"z":100},
}

#' ## DISCRETE ALLOCATION:
#' Round robin:
print(divide(fairpy.items.round_robin, input_3_agents))
#' Utilitarian matching:
print(divide(fairpy.items.utilitarian_matching, input_3_agents))
#' Iterated maximum matching:
print(divide(fairpy.items.iterated_maximum_matching, input_3_agents))
#' PROPm allocation:
print(divide(fairpy.items.propm_allocation, input_3_agents))
#' Garg-Taki algorithm for 3/4 MMS allocation:
print(divide(fairpy.items.three_quarters_MMS_allocation, input_3_agents))
#' Oh-Procaccia-Suksompong algorithm for 2 agents EF1 allocation:
print(divide(fairpy.items.two_agents_ef1, input_2_agents))


#' ## FRACTIONAL ALLOCATION:
#' Utilitarian fractional allocation:
print(divide(fairpy.items.max_sum_allocation, input_3_agents).round(3))
#' Max product (aka Nash optimal) fractional allocation:
print(divide(fairpy.items.max_product_allocation, input_3_agents).round(3))
#' Leximin (aka egalitarian) fractional allocation:
print(divide(fairpy.items.leximin_optimal_allocation, input_3_agents).round(3))
#' Efficient envy-free allocation with bounded sharing:
print(divide(fairpy.items.efficient_envyfree_allocation_with_bounded_sharing, input_3_agents).round(3))
#' Efficient Envy-free allocation with minimum-sharing:
print(divide(fairpy.items.envyfree_allocation_with_min_sharing, input_3_agents).round(3))

#' For more information see:
#'
#' * [List of item allocation algorithms currently implemented](../fairpy/items/README.md).
#' * [List of item allocation algorithms for future work](../fairpy/items/README-future.md).
