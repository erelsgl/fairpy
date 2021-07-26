#!python3

""" 
A demo program for the min-sharing algorithm.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import logging
import sys

from fairpy.items.partitions import *

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

from fairpy import solve
solve.logger.addHandler(logging.StreamHandler(sys.stdout))
# solve.logger.setLevel(logging.INFO)	


def mms_demo(valuation):
	c = 3
	print("\nValuation: ", valuation)
	print("1 out of 3 MMS = ",value_1_of_c_MMS(c, valuation))
	print("2 out of 3 MMS = ",value_1_of_c_MMS(c, valuation, numerator=2))
	print("3 out of 3 MMS = ",value_1_of_c_MMS(c, valuation, numerator=3))


mms_demo([5, 5, 5, 7, 7, 7, 11, 17, 23, 23, 23, 31, 31, 31, 65])  # The APS example of Babaioff, Ezra and Feige (2021), Lemma C.3.

