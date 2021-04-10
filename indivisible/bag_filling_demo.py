#!python3

"""
A simple one-directional bag-filling algorithm.
   Demonstrates using the Bag class.

Programmer: Erel Segal-Halevi
Since:  2021-04
"""

from fairpy.valuations import ValuationMatrix
from fairpy.allocations import Allocation
from fairpy.indivisible.bag_filling import one_directional_bag_filling
from typing import List
import numpy as np

valuations = [[10,20,30,40,50,60],[60,50,40,30,20,10]]
thresholds = [100, 100]
print(one_directional_bag_filling(valuations, thresholds))

