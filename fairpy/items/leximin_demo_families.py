#!python3

""" 
A demo program for finding the fractional maximin (aka egalitarian) allocation.

Author: Erel Segal-Halevi
Since:  2021-05
"""

import numpy as np
from fairpy.items.leximin import leximin_optimal_allocation_for_families


def leximin_utilities(v, families):
	z = leximin_optimal_allocation_for_families(v, families).round(3)  
	utility_profile = np.round(z.utility_profile(),3)
	for f,family in enumerate(families):
		values = [list(v[i]) for i in family]
		utilities = [utility_profile[i] for i in family]
		print(f"    Family {family}: values {values}, allocation {z[f]}, utilities {utilities}")
	print()
	return utility_profile

families = [[0,1],[2,3]]


for x in range(10):
	leximin_utilities([[x+0.5,10-x-0.5],[7.5,2.5], [5,5],[5,5]], families)


