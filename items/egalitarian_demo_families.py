#!python3

""" 
A demo program for finding the fractional maximin (aka egalitarian) allocation.

Author: Erel Segal-Halevi
Since:  2021-05
"""

from fairpy.items.egalitarian import maximin_optimal_allocation_for_families
import fairpy.valuations as valuations

def show(v, families):
	v = valuations.matrix_from(v)
	z = maximin_optimal_allocation_for_families(v, families).round(3)  
	utility_profile = z.utility_profile_for_families(v, families)
	for f,family in enumerate(families):
		values = [list(v[i]) for i in family]
		utilities = [utility_profile[i] for i in family]
		print(f"    Family {family}: values {values}, allocation {z[f]}, utilities {utilities}")
	print()

families = [[0,1],[2]] 
# print("  No variability in family [0,1]:")
# show([[5,5],[5,5], [5,5]], families) # utility profile [5,5,5]
# show([[6,4],[5,5], [5,5]], families) # Leximin should be [[1 0],[0,1]] with utility profile [6,5,5]
for i in range(11):
	show([[i,10-i],[7,3], [5,5]], families) 

# print("  Slight Variability in family [0,1]:")
# show([[1,2],[1.5,1.5], [4,3]], families)

# print("  Variability in family [0,1]:")
# show([[1,2],[2,1], [4,3]], families)

# print("  More Variability in family [0,1]:")
# show([[0,3],[3,0], [4,3]], families)



