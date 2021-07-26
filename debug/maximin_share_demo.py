#!python3
"""
Calculate the maximin-share of an additive valuation function.

Author: Erel Segal-Halevi
Since : 2021-04
"""

from fairpy.items.partitions import *
from numpy.random import randint
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


def demo_fractions():
	types_capacity_pairs = [
		(1,16), (2,8), (4,4), (8,2), (16,1)
	]
	for num_of_types, capacity in types_capacity_pairs:
		valuation = random_valuation(num_of_types)
		print(f"{num_of_types} item-types with capacity {capacity}: c=", end=" ", flush=True)
		ordinal_mms_values = []
		for c in range(3, num_of_types*capacity+1):
			print(c, end=" ", flush=True)
			ordinal_mms_values.append(value_1_of_c_MMS(c, valuation, capacity=capacity))
		ordinal_mms_fractions = [v / ordinal_mms_values[0] for v in ordinal_mms_values]
		print(f" {ordinal_mms_fractions}", flush=True)
		"""
		1 item-types with capacity 16: c= 3 4 5 6 7 8 9 10 11 12 13 14 15 16  [1.0, 0.8, 0.6, 0.4, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]
		2 item-types with capacity 8: c= 3 4 5 6 7 8 9 10 11 12 13 14 15 16  [1.0, 0.7666666666666667, 0.5333333333333333, 0.4999999999999999, 0.38333333333333336, 0.38333333333333336, 0.26666666666666666, 0.26666666666666666, 0.23333333333333334, 0.23333333333333334, 0.11666666666666667, 0.11666666666666667, 0.11666666666666667, 0.11666666666666667]
		4 item-types with capacity 4: c= 3 4 5 6 7 8 9 10 11 12 13 14 15 16  [1.0, 0.7513812154696132, 0.5911602209944752, 0.4972375690607735, 0.3425414364640884, 0.32044198895026954, 0.292817679558011, 0.27071823204419876, 0.22651933701657537, 0.20441988950276244, 0.08839779005524862, 0.04419889502762431, 0.022099447513812154, 0.022099447513812154]
		8 item-types with capacity 2: c= 3 4 5 6 7 8 9 10 11 12 13 14 15 16  [1.0, 0.746212121212122, 0.5946969696969704, 0.48484848484848536, 0.4204545454545459, 0.30303030303030337, 0.2765151515151518, 0.25378787878787906, 0.2272727272727274, 0.20454545454545475, 0.1893939393939396, 0.16666666666666685, 0.045454545454545504, 0.022727272727272752]
		16 item-types with capacity 1: c= 3 4 5 6 7 8 9 10 11 12 13 14 15 16  [1.0, 0.7520661157024796, 0.5991735537190085, 0.49173553719008284, 0.4132231404958679, 0.34710743801652905, 0.2975206611570249, 0.25619834710743805, 0.22727272727272735, 0.18595041322314057, 0.12809917355371905, 0.07024793388429755, 0.05785123966942151, 0.037190082644628114]
		"""



# demo_times(value_1_of_c_MMS__bruteforce)
# demo_times(value_1_of_c_MMS__pulp)
# demo_times(value_1_of_c_MMS__cvxpy)
demo_fractions()

# valuation = [10, 10, 11, 13, 24, 26, 26, 28, 29, 35, 51, 62, 66, 69, 79, 80, 82, 87, 88, 94]
# c=3
# print(timeit("value_1_of_c_MMS(c, valuation, show_solver_log=True)", globals=globals(), number=1), "seconds")
# print(value_1_of_c_MMS(c, valuation, show_solver_log=True))

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

Times for pulp CBC implementation with symmetry-breaking constraints:
3 items with 1 capacity, 1-of-3 MMS: 0.014259789022617042 seconds.
4 items with 1 capacity, 1-of-3 MMS: 0.0240349390078336 seconds.
5 items with 1 capacity, 1-of-3 MMS: 0.04649520694511011 seconds.
6 items with 1 capacity, 1-of-3 MMS: 0.15005491400370374 seconds.
7 items with 1 capacity, 1-of-3 MMS: 0.18664571101544425 seconds.
8 items with 1 capacity, 1-of-3 MMS: 0.22112883802037686 seconds.
9 items with 1 capacity, 1-of-3 MMS: 0.35376442002598196 seconds.
10 items with 1 capacity, 1-of-3 MMS: 0.0299613390234299 seconds.
11 items with 1 capacity, 1-of-3 MMS: 0.853080946020782 seconds.
12 items with 1 capacity, 1-of-3 MMS: 1.1613088630256243 seconds.
13 items with 1 capacity, 1-of-3 MMS: 0.031560096016619354 seconds.
14 items with 1 capacity, 1-of-3 MMS: 1.4873867540154606 seconds.
15 items with 1 capacity, 1-of-3 MMS: 2.922457240987569 seconds.
16 items with 1 capacity, 1-of-3 MMS: 2.5505638069589622 seconds.
17 items with 1 capacity, 1-of-3 MMS: 0.06325867399573326 seconds.
18 items with 1 capacity, 1-of-3 MMS: 3.9337498919921927 seconds.
19 items with 1 capacity, 1-of-3 MMS: 197.19387467898196 seconds.
20 items with 1 capacity, 1-of-3 MMS: 0.041000975004862994 seconds.

3 items with 5 capacity, 1-of-3 MMS: 0.06587998400209472 seconds.
4 items with 5 capacity, 1-of-3 MMS: 0.13009417802095413 seconds.
5 items with 5 capacity, 1-of-3 MMS: 0.3152111049857922 seconds.
6 items with 5 capacity, 1-of-3 MMS: 8.209254641027655 seconds.
7 items with 5 capacity, 1-of-3 MMS: 9.310528420028277 seconds.
"""