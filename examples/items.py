#' # Fair item allocation algorithms
#' Below are some algorithms for fair allocation of items,
#' both divisible and indivisible.

import fairpy

instance = {"Alice":  {"z":12, "y":10, "x":8, "w":7, "v":4, "u":1},
          "Dina":   {"z":14, "y":9, "x":15, "w":4, "v":9, "u":12},
          "George": {"z":19, "y":16, "x":8, "w":6, "v":5, "u":1},
           }
#' Round robin:
print(fairpy.items.round_robin(instance))
#' Utilitarian matching:
print(fairpy.items.utilitarian_matching(instance))
#' Iterated maximum matching:
print(fairpy.items.iterated_maximum_matching(instance))
#' PROPm allocation:
print(fairpy.items.propm_allocation(instance))
#' Utilitarian fractional allocation:
print(fairpy.items.max_sum_allocation(instance).round(3))
#' Max product (aka Nash optimal) fractional allocation:
print(fairpy.items.max_product_allocation(instance).round(3))
#' Leximin (aka egalitarian) fractional allocation:
print(fairpy.items.leximin_optimal_allocation(instance).round(3))
#' Efficient envy-free allocation with bounded sharing:
print(fairpy.items.efficient_envyfree_allocation_with_bounded_sharing(instance).round(3))
#' Efficient Envy-free allocation with minimum-sharing:
print(fairpy.items.envyfree_allocation_with_min_sharing(instance).round(3))

