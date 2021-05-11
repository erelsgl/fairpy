#!python3
"""
Experiment comparing various MMS values.

Author: Erel Segal-Halevi
Since : 2021-04
"""

from fairpy.items.maximin_share import *
from numpy.random import randint
import numpy as np
from timeit import timeit

MIN_ITEM_VALUE=1
MAX_ITEM_VALUE=99
def random_valuation(num_of_items:int):
	return sorted(randint(MIN_ITEM_VALUE,MAX_ITEM_VALUE, num_of_items))


def demo_times(implementation):
	MIN_ITEMS=3
	MAX_ITEMS=100
	CAPACITY=1
	for num_of_items in range(MIN_ITEMS,MAX_ITEMS+1):
		valuation = random_valuation(num_of_items)
		# for c in range(2, num_of_items):
		for c in range(3, 4):
			time = timeit("value_1_of_c_MMS(c, valuation, capacity=CAPACITY)", globals={"c": c, "CAPACITY": CAPACITY, "value_1_of_c_MMS": implementation, "valuation":valuation}, number=1)
			print(f"{num_of_items} items with {CAPACITY} capacity, 1-of-{c} MMS: {time} seconds.\n    {valuation}", flush=True)


def experiment():
	types_capacity_pairs = [
		(1,60), (2,30), (3,20), (4,15), (5,12), (6,10), (10,6), (12,5), (15,4), (20,3), (30,2), (60,1)
	]

	for num_of_types, capacity in types_capacity_pairs:
		num_of_items = num_of_types*capacity
		valuation = random_valuation(num_of_types)
		print(f"\n{num_of_types} item-types with capacity {capacity}\n   {valuation}", flush=True)
		n = 4
		print(f"1-out-of-{n} MMS = ", end="", flush=True)
		mms_1_of_n = int(value_1_of_c_MMS(n, valuation, capacity=capacity))
		print(f"{mms_1_of_n} (100%)", flush=True)
		for L in range(1,5):
			D = int((L+1/2)*n)
			print(f"   {L}-out-of-{D} MMS = ", end="", flush=True)
			if D-L >= num_of_items:
				mms_L_of_D = 0
			else:
				mms_L_of_D = int(value_1_of_c_MMS(D, valuation, capacity=capacity, numerator=L))
			print(f"   {mms_L_of_D} ({int(mms_L_of_D/mms_1_of_n*100)}%) ", flush=True)

experiment()



"""


1 item-types with capacity 60
   [46]
1-out-of-4 MMS = 690 (100%)
   1-out-of-6 MMS =    460 (66%) 
   2-out-of-10 MMS =    552 (80%) 
   3-out-of-14 MMS =    552 (80%) 
   4-out-of-18 MMS =    552 (80%) 

2 item-types with capacity 30
   [79, 95]
1-out-of-4 MMS = 1298 (100%)
   1-out-of-6 MMS =    870 (67%) 
   2-out-of-10 MMS =    1044 (80%) 
   3-out-of-14 MMS =    1092 (84%) 
   4-out-of-18 MMS =    1076 (82%) 

3 item-types with capacity 20
   [12, 39, 49]
1-out-of-4 MMS = 500 (100%)
   1-out-of-6 MMS =    333 (66%) 
   2-out-of-10 MMS =    400 (80%) 
   3-out-of-14 MMS =    417 (83%) 
   4-out-of-18 MMS =    424 (84%) 

4 item-types with capacity 15
   [39, 56, 62, 84]
1-out-of-4 MMS = 903 (100%)
   1-out-of-6 MMS =    601 (66%) 
   2-out-of-10 MMS =    718 (79%) 
   3-out-of-14 MMS =    762 (84%) 
   4-out-of-18 MMS =    789 (87%) 

5 item-types with capacity 12
   [18, 23, 74, 93, 94]
1-out-of-4 MMS = 906 (100%)
   1-out-of-6 MMS =    604 (66%) 
   2-out-of-10 MMS =    718 (79%) 
   3-out-of-14 MMS =    771 (85%) 
   4-out-of-18 MMS = 
"""