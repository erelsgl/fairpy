#!python3

print("""
Below are some algorithms for fair allocation of items,
both divisible and indivisible.
""")

import fairpy

instance = {"Alice":  {"z":12, "y":10, "x":8, "w":7, "v":4, "u":1},
          "Dina":   {"z":14, "y":9, "x":15, "w":4, "v":9, "u":12},
          "George": {"z":19, "y":16, "x":8, "w":6, "v":5, "u":1},
           }
print("Valuations: \n",instance,"\n")
print("Round robin:\n", fairpy.items.round_robin(instance))
print("Maximum matching:\n", fairpy.items.utilitarian_matching(instance))
print("Iterated maximum matching:\n", fairpy.items.iterated_maximum_matching(instance))
print("PROPm allocation:\n", fairpy.items.propm_allocation(instance))
print("Max sum (aka utilitarian) fractional allocation:\n", fairpy.items.max_sum_allocation(instance).round(3))
print("Max product (aka Nash optimal) fractional allocation:\n", fairpy.items.max_product_allocation(instance).round(3))
print("Leximin (aka egalitarian) fractional allocation:\n", fairpy.items.leximin_optimal_allocation(instance).round(3))
print("Efficient envy-free allocation with bounded sharing: \n", fairpy.items.efficient_envyfree_allocation_with_bounded_sharing(instance).round(3))
print("Efficient Envy-free allocation with minimum-sharing: \n", fairpy.items.envyfree_allocation_with_min_sharing(instance).round(3))

