#!python3

"""
Demonstration of the simplex of partitions.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""
import sys
if __name__ == "__main__" and (len(sys.argv) < 2 or sys.argv[1] != "quiet"):

    from fairpy.agents import *
    from fairpy.cake import partition_simplex

    import matplotlib.pyplot as pyplot
    import logging, sys
    partition_simplex.logger.addHandler(logging.StreamHandler(sys.stdout))
    partition_simplex.logger.setLevel(logging.INFO)

    samples_per_side = 100
    figsize_in_inches=(8, 7)
    dpi=80


    pyplot.close('all')

    _, subplots = pyplot.subplots(2, 2, figsize=figsize_in_inches)

    agent = PiecewiseConstantAgent([1, 2, 3, 4], "positive")
    partition_simplex.plot_1_agent(agent, axes=subplots[0,0], samples_per_side=samples_per_side)

    agent = PiecewiseConstantAgent([-1, -2, -3, -4], "negative")
    partition_simplex.plot_1_agent(agent, axes=subplots[0,1], samples_per_side=samples_per_side)

    agent = PiecewiseConstantAgent([1, -2, 3, -4], "mixed 1")
    partition_simplex.plot_1_agent(agent, axes=subplots[1,0], samples_per_side=samples_per_side)

    agent = PiecewiseConstantAgent([1, -2, 3, -4, 5, -6, 7, -8], "mixed 2")
    partition_simplex.plot_1_agent(agent, axes=subplots[1,1], samples_per_side=samples_per_side)

    pyplot.show()
