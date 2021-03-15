#!python3

""" 
A demo program for the min-sharing algorithm.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import numpy as np, cvxpy
from fairpy.divisible.max_product import *
from fairpy.divisible.ValuationMatrix import ValuationMatrix
from fairpy.divisible.AllocationMatrix import AllocationMatrix

print("\nThree identical goods:")
v = ValuationMatrix([ [3,3,3] , [2,2,2] , [1,1,1] ])
print("v = \n",v)
z = max_product_allocation(v)
print("z = \n",z, "product = ", product_of_utilities(z, v))


print("\nThree different goods:")
v = ValuationMatrix([ [3,2,2] , [1,2,1] , [0,0,1] ])
print("v = \n",v)
z = max_product_allocation(v)
print("z = \n",z, "product = ", product_of_utilities(z, v))


