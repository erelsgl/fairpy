#!python3

"""
Demonstration of the simplex of partitions.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""

from agents import *
import matplotlib.pyplot as pyplot
from partition_simplex import plot_partition_simplex

pyplot.close('all')

# _, subplots = pyplot.subplots(2, 2, sharex='col', sharey='row')
_, subplots = pyplot.subplots(2, 2)

agent = PiecewiseConstantAgent([1, 2, 3, 4], "positive")
plot_partition_simplex(agent, axes=subplots[0,0], samples_per_side=200)

agent = PiecewiseConstantAgent([-1, -2, -3, -4], "negative")
plot_partition_simplex(agent, axes=subplots[0,1], samples_per_side=200)

agent = PiecewiseConstantAgent([1, -2, 3, -4], "mixed 1")
plot_partition_simplex(agent, axes=subplots[1,0], samples_per_side=200)

agent = PiecewiseConstantAgent([1, -2, 3, -4, 5, -6, 7, -8], "mixed 2")
plot_partition_simplex(agent, axes=subplots[1,1], samples_per_side=200)

pyplot.show()
