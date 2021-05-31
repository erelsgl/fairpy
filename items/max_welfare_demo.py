#!python3

""" 
A demo program for finding welfare maximizing allocations.

Author: Erel Segal-Halevi
Since:  2021-05
"""

from fairpy.items.max_welfare import *
import numpy as np
import fairpy.valuations as valuations

def show(title, z, v):
    utility_profile = z.utility_profile(v)
    print(title, " = \n",z, "\nprofile = ", utility_profile, "\nsum = ", sum(utility_profile), "product = ", np.prod(z.utility_profile(v)))


print("\nThree identical goods:")
v = valuations.matrix_from([ [3,3,3] , [2,2,2] , [1,1,1] ])
print("v = \n",v)
z = max_sum_allocation(v).round(3)
show("max-sum",z,v)
z = max_product_allocation(v).round(3)
show("max-product",z,v)
z = max_power_sum_allocation(v, -100).round(3)
show("max-sum-of-powers-(-100)",z,v)
z = leximin_optimal_allocation(v).round(3)
show("leximin-optimal",z,v)


print("\nThree different goods:")
v = valuations.matrix_from({"Alice": [3,2,2] , "Bob": [1,2,1] , "Carl": [0,0,1] })
print("v = \n",v)
z = max_sum_allocation(v).round(3)
show("max-sum",z,v)
z = max_product_allocation(v).round(3)
show("max-product",z,v)
z = max_power_sum_allocation(v, -100).round(3)
show("max-sum-of-powers-(-100)",z,v)
z = leximin_optimal_allocation(v).round(3)
show("leximin-optimal",z,v)
