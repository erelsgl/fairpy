#!python3

""" 
A demo program for finding leximin allocations.

Author: Erel Segal-Halevi
Since:  2021-06
"""

from fairpy.items.leximin import *
import numpy as np
import fairpy.valuations as valuations

import sys
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

from fairpy import solve
solve.logger.addHandler(logging.StreamHandler(sys.stdout))
# solve.logger.setLevel(logging.INFO)


def show(title, v):
    print("\n", title)
    z = leximin_optimal_allocation(v).round(3)
    utility_profile = z.utility_profile(v)
    print("allocation = \n",z, "\nprofile = ", utility_profile)


show("3 agents, competitive", [[3,2,1],[1,2,3],[2,2,2]])
show("3 agents, non-competitive", [[3,0,0],[0,4,0],[0,0,5]])
show("3 agents, non-competitive", [[3,0,0],[0,3,0],[0,0,5]])
show("6 agents", [[3,0,0],[0,8,0],[0,8,0],[5,5,15],[5,5,15],[5,5,15]])
