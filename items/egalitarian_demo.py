#!python3

""" 
A demo program for finding the maximin (aka egalitarian) allocation.

Author: Erel Segal-Halevi
Since:  2021-05
"""

from fairpy.items.egalitarian import maximin_optimal_allocation
import fairpy.valuations as valuations

print("\nThree identical goods:")
v = valuations.matrix_from([ [3,3,3] , [2,2,2] , [1,1,1] ])
print("v = \n",v)
z = maximin_optimal_allocation(v)
print("z = \n",z, "profile = ", z.utility_profile(v))


print("\nThree different goods:")
v = valuations.matrix_from({"Alice": [3,2,2] , "Bob": [1,2,1] , "Carl": [0,0,1] })
print("v = \n",v)
z = maximin_optimal_allocation(v)
print("z = \n",z, "profile = ", z.utility_profile(v))



