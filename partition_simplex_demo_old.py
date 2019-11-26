#!python3

"""
Demonstration of the simplex of partitions.

Programmer: Erel Segal-Halevi
Since: 2019-11
"""

from agents import *
import matplotlib.pyplot as pyplot

from partition_simplex import plot_partition_simplex

def plotPositive3():
    fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

    for i in range(3):
        for j in range(3):
            agent = PiecewiseConstantAgent([1,1+i,1+j])
            plot_partition_simplex(agent, samples_per_side=0.01, axes=subplots[i,j])

    pyplot.legend(loc='lower right', prop={'size':10})
    pyplot.xlabel('knife 1-2')
    pyplot.ylabel('knife 2-3')
    pyplot.suptitle("partition simplexes of all-positive cakes")
    # pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/positive3.png')

def plotNegative3():
    fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

    for i in range(3):
        for j in range(3):
            agent = PiecewiseConstantAgent([-1,-1-i,-1-j])
            plot_partition_simplex(agent, samples_per_side=0.01, axes=subplots[i,j])

    pyplot.legend(loc='lower right', prop={'size':10})
    pyplot.xlabel('knife 1-2')
    pyplot.ylabel('knife 2-3')
    pyplot.suptitle("partition simplexes of all-negative cakes")
    # pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/negative3.png')

def plotMixed3():
    fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

    for i in range(3):
        for j in range(3):
            agent = PiecewiseConstantAgent([1,-5+i,1+j])
            plot_partition_simplex(agent, samples_per_side=0.01, axes=subplots[i,j])

    pyplot.legend(loc='lower right', prop={'size':10})
    pyplot.xlabel('knife 1-2')
    pyplot.ylabel('knife 2-3')
    pyplot.suptitle("partition simplexes of mixed cakes")
    # pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/mixed3.png')

def plotMixed3a():
    fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

    for i in range(3):
        for j in range(3):
            agent = PiecewiseConstantAgent([-1,1+i,-1-j])
            plot_partition_simplex(agent, samples_per_side=0.01, axes=subplots[i,j])

    pyplot.legend(loc='lower right', prop={'size':10})
    pyplot.xlabel('knife 1-2')
    pyplot.ylabel('knife 2-3')
    pyplot.suptitle("partition simplexes of mixed cakes")
    # pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/mixed3a.png')

def plotNegPos():
    fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

    for i in range(3):
        for j in range(3):
            agent = PiecewiseConstantAgent([-1-i,1+j])
            plot_partition_simplex(agent, samples_per_side=0.01, axes=subplots[i,j])

    pyplot.legend(loc='lower right', prop={'size':10})
    pyplot.xlabel('knife 1-2')
    pyplot.ylabel('knife 2-3')
    pyplot.suptitle("partition simplexes of mixed cakes")
    # pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/negpos.png')


def plotIndifferenceIntervals():
    fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

    for i in range(3):
        for j in range(3):
            agent = PiecewiseConstantAgent([3,i,-i,3,j,-j,3])
            plot_partition_simplex(agent, samples_per_side=0.01, axes=subplots[i,j])

    pyplot.legend(loc='lower right', prop={'size':10})
    pyplot.xlabel('knife 1-2')
    pyplot.ylabel('knife 2-3')
    pyplot.suptitle("partition simplexes of cakes with indifference-intervals")
    # pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/indif.png')

def plotSwitches3():
    fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

    for i in range(3):
        for j in range(3):
            agent = PiecewiseConstantAgent([-1+i,2,-7,2,-1+j])
            plot_partition_simplex(agent, samples_per_side=0.002, axes=subplots[i,j])

    pyplot.legend(loc='lower right', prop={'size':10})
    pyplot.xlabel('knife 1-2')
    pyplot.ylabel('knife 2-3')
    pyplot.suptitle("Partition simplexes with different kinds of switches")
    # pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/switches3.png')


pyplot.close('all')

plotPositive3()
#plotNegative3()
#plotMixed3()
#plotSwitches3()
#plot_partition_simplex(PiecewiseConstantAgent([1,2,3]))
#plot_partition_simplex(PiecewiseConstantAgent([-1,2,-2,2,-2,2,-2,2,-2]))
#plotIndifferenceIntervals()
#lotMixed3a()
#plotMixed3b()

pyplot.show()
