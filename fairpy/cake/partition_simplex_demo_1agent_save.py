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

    samples_per_side = 300
    figsize_in_inches=(8, 7)
    dpi=80


    pyplot.close('all')

    pyplot.clf()
    agent = PiecewiseConstantAgent([4, 3, 2, 1], "1")
    partition_simplex.plot_1_agent(agent, axes=pyplot, samples_per_side=samples_per_side)
    pyplot.axis("off")
    pyplot.savefig("1.png")
    sys.exit(0)

    pyplot.clf()
    agent = PiecewiseConstantAgent([-1, -2, -3, -4], "2")
    partition_simplex.plot_1_agent(agent, axes=pyplot, samples_per_side=samples_per_side)
    pyplot.axis("off")
    pyplot.savefig("2.png")

    pyplot.clf()
    agent = PiecewiseConstantAgent([-1, 2, -3, 4], "3")
    partition_simplex.plot_1_agent(agent, axes=pyplot, samples_per_side=samples_per_side)
    pyplot.axis("off")
    pyplot.savefig("3.png")

    pyplot.clf()
    agent = PiecewiseConstantAgent([1, -2, 3, -4], "4")
    partition_simplex.plot_1_agent(agent, axes=pyplot, samples_per_side=samples_per_side)
    pyplot.axis("off")
    pyplot.savefig("4.png")

    pyplot.clf()
    agent = PiecewiseConstantAgent([1, -2, 3, -4, 5, -6, 7, -8], "5")
    partition_simplex.plot_1_agent(agent, axes=pyplot, samples_per_side=samples_per_side)
    pyplot.axis("off")
    pyplot.savefig("5.png")

    pyplot.clf()
    agent = PiecewiseConstantAgent([1, 10, 100, 1000], "6")
    partition_simplex.plot_1_agent(agent, axes=pyplot, samples_per_side=samples_per_side)
    pyplot.axis("off")
    pyplot.savefig("6.png")

