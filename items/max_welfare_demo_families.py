#!python3

""" 
A demo program for finding the fractional maximin (aka egalitarian) allocation.

Author: Erel Segal-Halevi
Since:  2021-05
"""

from fairpy.items.max_welfare import *
import fairpy.valuations as valuations

def show(v, families):
	v = valuations.matrix_from(v)
	z = leximin_optimal_allocation_for_families(v, families).round(3)  
	utility_profile = z.utility_profile_for_families(v, families)
	for f,family in enumerate(families):
		values = [list(v[i]) for i in family]
		utilities = [utility_profile[i] for i in family]
		print(f"    Family {family}: values {values}, allocation {z[f]}, utilities {utilities}")
	print()

families = [[0,1],[2,3]] 


# for i in range(10):
# 	show([[i+0.5,10-i-0.5],[7.5,2.5], [5,5],[5,5]], families)



for i in range(10):
	show([[i+0.5,10-i-0.5],[5.5,4.5], [7,3],[7,3]], families)

