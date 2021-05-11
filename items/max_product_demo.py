#!python3

""" 
A demo program for finding the fractional max-product (aka Max Nash Welfare) allocation.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import numpy as np, cvxpy
from fairpy.items.max_product import *
import fairpy.valuations as valuations
from fairpy.items.allocations import AllocationMatrix

print("\nThree identical goods:")
v = valuations.matrix_from([ [3,3,3] , [2,2,2] , [1,1,1] ])
print("v = \n",v)
z = max_product_allocation(v)
print("z = \n",z, "product = ", product_of_utilities(z, v))


print("\nThree different goods:")
v = valuations.matrix_from({"Alice": [3,2,2] , "Bob": [1,2,1] , "Carl": [0,0,1] })
print("v = \n",v)
z = max_product_allocation(v)
print("z = \n",z, "product = ", product_of_utilities(z, v))


