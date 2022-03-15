#!python3

""" 
A demo program for finding leximin allocations.

Author: Erel Segal-Halevi
Since:  2021-06
"""

from fairpy.items.leximin import *

import sys

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

from fairpy import solve

solve.logger.addHandler(logging.StreamHandler(sys.stdout))
solve.logger.setLevel(logging.INFO)

import cvxpy_leximin

cvxpy_leximin.LOGGER.addHandler(logging.StreamHandler(sys.stdout))
cvxpy_leximin.LOGGER.setLevel(logging.INFO)


def show(title, v):
    print("\n", "###", title)
    z = leximin_optimal_allocation(v).round(3)
    utility_profile = z.utility_profile()
    print("allocation = \n", z, "\nprofile = ", utility_profile)


# show("3 agents, competitive", [[3,2,1],[1,2,3],[2,2,2]])
# show("3 agents, non-competitive", [[3,0,0],[0,4,0],[0,0,5]])
# show("3 agents, non-competitive", [[3,0,0],[0,3,0],[0,0,5]])
# show("4 agents, partially-competitive", [[4,0,0],[0,3,0],[5,5,10],[5,5,10]])
# show("6 agents, partially-competitive", [[3,0,0],[0,8,0],[0,8,0],[5,5,15],[5,5,15],[5,5,15]])


show(
    "2 parties",
    [
        [1 / 3, 0, 1 / 3, 1 / 3],
        [1, 1, 1, 0],
    ],
)
