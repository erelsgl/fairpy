#!python3

""" 
A demo program for finding welfare maximizing allocations.

Author: Erel Segal-Halevi
Since:  2021-05
"""
import fairpy
divide = fairpy.divide
from fairpy.items.max_welfare import *
from fairpy.items.leximin import *
import numpy as np

import sys
logger.addHandler(logging.StreamHandler(sys.stdout))
# logger.setLevel(logging.INFO)


def show(title, z, v):
    utility_profile = z.utility_profile()
    print("\n", title, " = \n",z, "\nprofile = ", utility_profile, "\nsum = ", sum(utility_profile), "product = ", np.prod(utility_profile))


print("\nThree identical goods:")
v = [ [3,3,3] , [2,2,2] , [1,1,1] ]
print("v = \n",v)
z = divide(max_sum_allocation, v).round(3)
show("max-sum",z,v)
z = divide(max_product_allocation, v).round(3)
show("max-product",z,v)
z = divide(max_power_sum_allocation, v, -100).round(3)
show("max-sum-of-powers-(-100)",z,v)
z = divide(leximin_optimal_allocation, v).round(3)
show("leximin-optimal",z,v)


print("\nThree different goods:")
v = {"Alice": [3,2,2] , "Bob": [1,2,1] , "Carl": [0,0,1] }
print("v = \n",v)
z = divide(max_sum_allocation, v).round(3)
show("max-sum",z,v)
z = divide(max_product_allocation, v).round(3)
show("max-product",z,v)
z = divide(max_power_sum_allocation, v, -100).round(3)
show("max-sum-of-powers-(-100)",z,v)
z = divide(leximin_optimal_allocation, v).round(3)
show("leximin-optimal",z,v)
