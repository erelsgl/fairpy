#!python3

""" 
A demo program for the min-sharing algorithm.

Author: Erel Segal-Halevi
Since:  2021-03
"""

from fairpy.items.partitions import maximin_share_partition, logger
import logging
import sys

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

from fairpy import solve
solve.logger.addHandler(logging.StreamHandler(sys.stdout))
# solve.logger.setLevel(logging.INFO)	

import numpy as np

def show_mms_partition(numerator, c, valuation):
	(partition, part_values, value) = maximin_share_partition(c, valuation, numerator=numerator)
	print(f"{numerator}-out-of-{c} partition = {partition}, values = {part_values}, min-value = {value}")

def mms_demo(c, valuation):
	print("\nValuation: ", valuation)
	show_mms_partition(1, c, valuation)
	show_mms_partition(2, c, valuation)

def items_to_values(partition, valuation):
	return [
			[valuation[x] for x in part]
			for part in partition
	]

def check_example(valuation, c:int, verbose=True):
	(partition1, part_values1, value1) = maximin_share_partition(c, valuation, numerator=1)
	(partition12, part_values12, value12) = maximin_share_partition(c, valuation, numerator=2, fix_smallest_part_value=value1)
	(partition2, part_values2, value2) = maximin_share_partition(c, valuation, numerator=2)
	# if part_values2[0] < part_values1[0] and sum(part_values2[0:2]) > sum(part_values1[0:2]):
	if verbose or (part_values2[0] < part_values12[0] and sum(part_values2[0:2]) > sum(part_values12[0:2])):
		print("Found interesting example!")
		print(f"Valuation = {valuation}")
		print(f"1-out-of-{c} partition = {items_to_values(partition1,valuation)}, values = {part_values1}, min-value = {value1}")
		print(f"Better 1-out-of-{c} partition = {items_to_values(partition12,valuation)}, values = {part_values12}, min-value = {value12}")
		print(f"2-out-of-{c} partition = {items_to_values(partition2,valuation)}, values = {part_values2}, min-value = {value2}")


def find_example():
	for c in range(3,4):
		for size in range(c+1,20):
			print(f"\nc = {c}, size = {size}")
			for i in range(1000):
				print(".", end="", flush=True)
				valuation = np.random.randint(1,20, size=size)
				check_example(valuation, c, verbose=False)




mms_demo(3, [5, 5, 5, 7, 7, 7, 11, 17, 23, 23, 23, 31, 31, 31, 65])  # The APS example of Babaioff, Ezra and Feige (2021), Lemma C.3.
mms_demo(3, [29, 29, 28, 16, 2])
# check_example([5,5,5,7,8,11], c=3, verbose=False)
# # check_example([7,7,7,10,11,16], c=3, verbose=True)
# # find_example()

