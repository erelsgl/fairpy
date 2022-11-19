#!python3

""" 
A demo program for the min-sharing algorithm.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import fairpy
divide = fairpy.divide

import logging
import sys

from fairpy.items.min_sharing_impl import FairAllocationProblem
from fairpy.items.min_sharing import proportional_allocation_with_min_sharing, envyfree_allocation_with_min_sharing, maxproduct_allocation_with_min_sharing
from fairpy.items.max_welfare import max_product_allocation

from datetime import datetime;  now = datetime.now


FairAllocationProblem.logger.addHandler(logging.StreamHandler(sys.stdout))
FairAllocationProblem.logger.setLevel(logging.INFO)

def demo(title:str, v):
	print(f"\n## {title} ##")
	print("v = \n",v)
	start = now()
	z = divide(proportional_allocation_with_min_sharing, v).round(3)
	print("Allocation:\n",z, "Time: ", now()-start)
	start = now()
	z = divide(envyfree_allocation_with_min_sharing, v).round(3)
	print("Allocation:\n",z, "Time: ", now()-start)
	start = now()
	z = divide(max_product_allocation, v).round(3)
	print("\nAn arbitrary max-product allocation, with ",z.num_of_sharings()," sharings:\n",z, "Time: ", now()-start)
	start = now()
	z = divide(maxproduct_allocation_with_min_sharing, v).round(3)
	print("Allocation:\n",z, "Time: ", now()-start)
	z = divide(maxproduct_allocation_with_min_sharing, v, tolerance=0.001).round(3)
	print("Allocation:\n",z, "Time: ", now()-start)

demo(
	"Four objects, three agents. Each criterion has a different minimum number of sharings.",
	[ [10,18,1,1] , [10,18,1,1] , [10,10,5,5] ])

demo(
	"Ten objects, three agents, some zero values",
	[ [20,10,10, 5,5,0, 3,0,0,0] , [10,20,10, 5,0,5, 0,3,0,0] , [10,10,20, 0,5,5, 0,0,3,0] ])

# demo(
# 	"Three objects, two agents. An instance that broke many solvers.",
# 	[ [465,0,535] , [0,0,1000] ])


# num_of_agents = 4
# num_of_items = 10
# max_item_value = 100
# v = np.random.randint(max_item_value, size=(num_of_agents, num_of_items))
# demo("A random instance.", v)
