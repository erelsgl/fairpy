#!python3

""" 
A demo program for the min-sharing algorithm.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import numpy as np, cvxpy
from fairpy.divisible.min_sharing import *
from fairpy.divisible.ValuationMatrix import ValuationMatrix
from fairpy.divisible.AllocationMatrix import AllocationMatrix

import fairpy.divisible.min_sharing_impl.FairAllocationProblem as FairAllocationProblem

import logging, sys
FairAllocationProblem.logger.addHandler(logging.StreamHandler(sys.stdout))
FairAllocationProblem.logger.setLevel(logging.INFO)

print("\n## Four goods and three agents, value sum=30 ##")
v = ValuationMatrix([ [10,18,1,1] , [10,18,1,1] , [10,10,5,5] ])
print("v = \n",v)

z = proportional_allocation_with_min_sharing(v).round(3)
print("Allocation:\n",z)  # Should have 0 sharings

z = envyfree_allocation_with_min_sharing(v).round(3)
print("Allocation:\n",z)  # Should have 1 sharing

z = maxproduct_allocation_with_min_sharing(v).round(3)
print("Allocation:\n",z)  # Should have 2 sharings


print("\n## Some hard instances ##")
v = ValuationMatrix([ [465,0,535] , [0,0,1000]  ])
print("v = \n",v)
z = proportional_allocation_with_min_sharing(v).round(3)
print("z = \n",z)


print("\n## Some random instances ##")
num_of_agents = 4
num_of_items = 10
max_item_value = 100
v = ValuationMatrix(np.random.randint(max_item_value, size=(num_of_agents, num_of_items)))
print("v = \n",v)
z = proportional_allocation_with_min_sharing(v).round(3)
print("z = \n",z)


#     v =  [[150., 150. ,150. ,150., 150. ,250.],
#          [150., 150. ,150. ,150., 150. ,250.],
#          [150., 150. ,150. ,150., 150. ,250.]]


# fpap = FairEnvyFreeAllocationProblem(v)
# fpap1 =  FairProportionalAllocationProblem(v)
# print(v)
# start = datetime.datetime.now()
# # THE TEST EXECUTION
# ans = fpap.find_allocation_with_min_sharing()
# #ans = fpap1.find_allocation_with_min_sharing()
# print(ans)
# print(is_envy_free(v, ans))
# end = datetime.datetime.now()
# # print("the number of graph: {}".format(count))
# print("Total time for {} agents and {} items  :{}".format(num_of_agents, num_of_items, end - start))

