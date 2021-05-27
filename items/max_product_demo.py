#!python3

""" 
A demo program for finding egalitarian (maximin / leximin) allocations.

Author: Erel Segal-Halevi
Since:  2021-05
"""

from fairpy.items.max_product import *
import fairpy.valuations as valuations

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


