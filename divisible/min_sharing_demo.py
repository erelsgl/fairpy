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

print("\nThree identical goods:")
v = ValuationMatrix([ [3,3,3] , [2,2,2] , [1,1,1] ])
print("v = \n",v)
z = proportional_allocation_with_min_sharing(v).round(3)
print("z = \n",z)


print("\nThree different goods:")
v = ValuationMatrix([ [3,2,2] , [1,2,1] , [0,0,1] ])
print("v = \n",v)
z = proportional_allocation_with_min_sharing(v).round(3)
print("z = \n",z)


print("\nHard instances:")
v = ValuationMatrix([ [465,0,535] , [0,0,1000]  ])
z = proportional_allocation_with_min_sharing(v).round(3)
print("z = \n",z)

