#!python3

""" 
A demo program for finding the fractional max-product (aka Max Nash Welfare) allocation.

Author: Erel Segal-Halevi
Since:  2021-03
"""

from fairpy.items.egalitarian import maximin_optimal_allocation, maximin_optimal_allocation_for_families
import fairpy.valuations as valuations

print("\nThree different goods:")
v = valuations.matrix_from({"Alice": [3,2,1] , "Bob": [1,2,3] , "Carl": [2,2,2] })
print("v = \n",v)
z = maximin_optimal_allocation(v).round(3)
print("z = \n",z, "utility profile = ", z.utility_profile(v))

families = [[0,1],[2]] 
z = maximin_optimal_allocation_for_families(v,families).round(3)
print("z = \n",z, "utility profile = ", z.utility_profile_for_families(v, families))



