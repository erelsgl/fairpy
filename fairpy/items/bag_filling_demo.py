#!python3

"""
A simple one-directional bag-filling algorithm.
   Demonstrates using the Bag class.

Programmer: Erel Segal-Halevi
Since:  2021-04
"""

import fairpy
from fairpy.items.bag_filling import one_directional_bag_filling

valuations = [[10,20,30,40,50,60],[60,50,40,30,20,10]]
thresholds = [100, 100]
print(fairpy.divide(one_directional_bag_filling, valuations, thresholds=thresholds))

