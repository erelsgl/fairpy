#!python3
"""
Calculate the maximin-share of an additive valuation function.

Author: Erel Segal-Halevi
Since : 2021-04
"""

from fairpy.indivisible.maximin_share import *
from numpy.random import randint
from timeit import timeit

MIN_ITEM_VALUE=1
MAX_ITEM_VALUE=99
def random_valuation(num_of_items:int):
	return randint(MIN_ITEM_VALUE,MAX_ITEM_VALUE, num_of_items)


def demo_times(implementation):
	MIN_ITEMS=3
	MAX_ITEMS=20
	for num_of_items in range(MIN_ITEMS,MAX_ITEMS+1):
		items = list(range(num_of_items))
		valuation = random_valuation(num_of_items)
		# for c in range(2, num_of_items):
		for c in range(3, 4):
			time = timeit("value_1_of_c_MMS(valuation, items, 3)", globals={"value_1_of_c_MMS": implementation, "items":items, "valuation":valuation}, number=1)
			print(f"{num_of_items} items, 1-of-{c} MMS: {time} seconds", flush=True)

def demo_fractions():
	MIN_ITEMS=3
	MAX_ITEMS=12
	for num_of_items in range(MIN_ITEMS,MAX_ITEMS+1):
		items = list(range(num_of_items))
		valuation = random_valuation(num_of_items)
		print(f"{num_of_items} items: ", end=" ", flush=True)
		ordinal_mms_values = []
		for c in range(3, num_of_items+1):
			print(".", end="", flush=True)
			ordinal_mms_values.append(value_1_of_c_MMS__pulp(valuation,items,c))
		ordinal_mms_fractions = [v / ordinal_mms_values[0] for v in ordinal_mms_values]
		print(f" {ordinal_mms_fractions}", flush=True)

# demo_times(value_1_of_c_MMS__bruteforce)
# demo_times(value_1_of_c_MMS__pulp)
demo_fractions()

"""
Times for brute-force implementation (the numbers for all c are similar):
3 items, 1-of-3 MMS: 4.281295696273446e-05 seconds
4 items, 1-of-3 MMS: 0.0001047170371748507 seconds
5 items, 1-of-3 MMS: 0.00028875598218292 seconds
6 items, 1-of-3 MMS: 0.001226068998221308 seconds
7 items, 1-of-3 MMS: 0.004211399995256215 seconds
8 items, 1-of-3 MMS: 0.013530048017855734 seconds
9 items, 1-of-3 MMS: 0.052871851017698646 seconds
10 items, 1-of-3 MMS: 0.13176676497096196 seconds
11 items, 1-of-3 MMS: 0.6238806559704244 seconds
12 items, 1-of-3 MMS: 2.938590817968361 seconds
13 items, 1-of-3 MMS: 16.571642202034127 seconds


Times for pulp CBC implementation:
3 items, 1-of-3 MMS: 0.014157891040667892 seconds
4 items, 1-of-3 MMS: 0.01578137301839888 seconds
5 items, 1-of-3 MMS: 0.07665285799885169 seconds
6 items, 1-of-3 MMS: 0.0756889620097354 seconds
7 items, 1-of-3 MMS: 0.1045813380042091 seconds
8 items, 1-of-3 MMS: 0.14012311899568886 seconds
9 items, 1-of-3 MMS: 0.15763994201552123 seconds
10 items, 1-of-3 MMS: 0.30275864101713523 seconds
11 items, 1-of-3 MMS: 0.07794797600945458 seconds
12 items, 1-of-3 MMS: 0.021765517012681812 seconds
13 items, 1-of-3 MMS: 0.2619396210066043 seconds
14 items, 1-of-3 MMS: 1.9780694110086188 seconds
15 items, 1-of-3 MMS: 4.981405056023505 seconds
16 items, 1-of-3 MMS: 6.115194728015922 seconds
17 items, 1-of-3 MMS: 0.025761344004422426 seconds
18 items, 1-of-3 MMS: 2.8230425239889883 seconds
19 items, 1-of-3 MMS: 23.04832062497735 seconds
20 items, 1-of-3 MMS: 0.055193491047248244 seconds
"""