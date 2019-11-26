#!python3

import matplotlib.pyplot as pyplot
import numpy as np
exec(open("utils/ValueFunction1D.py").read())

class PartitionByBestPiece:
	def __init__(self, color, label, scale=100):
		self.color = color
		self.label = label
		self.scale = scale
		self.x = []
		self.y = []

	def addPoint(self, x, y):
		self.x.append(x)
		self.y.append(y)

	def plot(self, axes):
		axes.scatter(self.x, self.y, c=self.color, s=self.scale, label=self.label, edgecolors='none')


def plotPartitionSimplex(valueFunction, axes=None, fractionStep=0.01):
	length = valueFunction.length
	lengthStep = fractionStep * length
	scale = lengthStep*lengthStep*20000
	partitionsByBestPiece = [
		PartitionByBestPiece('blue', "piece 1", scale),
		PartitionByBestPiece('red',  "piece 2", scale),
		PartitionByBestPiece('green',"piece 3", scale)]
	for cut1 in np.arange(0, length-lengthStep, lengthStep):
		for cut2 in np.arange(cut1, length-lengthStep, lengthStep):
			bestPiece = valueFunction.partitionBestPiece([cut1,cut2])
			partitionsByBestPiece[bestPiece].addPoint(cut1, cut2)

	if axes is None:
		axes = pyplot
	for p in partitionsByBestPiece:
		p.plot(axes)
	if axes==pyplot:
		axes = pyplot.axes()
	axes.set_title("val="+str(valueFunction))
	axes.set_aspect('equal', 'datalim')
	axes.set_xticks(np.arange(0, length+1, 1.0))
	axes.set_yticks(np.arange(0, length+1, 1.0))
	#axes.grid(True)


pyplot.close('all')

def plotPositive3():
	fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

	for i in range(3):
		for j in range(3):
			valueFunction = ValueFunction1D([1,1+i,1+j])
			plotPartitionSimplex(valueFunction, fractionStep=0.01, axes=subplots[i,j])

	pyplot.legend(loc='lower right', prop={'size':10})
	pyplot.xlabel('knife 1-2')
	pyplot.ylabel('knife 2-3')
	pyplot.suptitle("partition simplexes of all-positive cakes")
	pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/positive3.png')

def plotNegative3():
	fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

	for i in range(3):
		for j in range(3):
			valueFunction = ValueFunction1D([-1,-1-i,-1-j])
			plotPartitionSimplex(valueFunction, fractionStep=0.01, axes=subplots[i,j])

	pyplot.legend(loc='lower right', prop={'size':10})
	pyplot.xlabel('knife 1-2')
	pyplot.ylabel('knife 2-3')
	pyplot.suptitle("partition simplexes of all-negative cakes")
	pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/negative3.png')

def plotMixed3():
	fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

	for i in range(3):
		for j in range(3):
			valueFunction = ValueFunction1D([1,-5+i,1+j])
			plotPartitionSimplex(valueFunction, fractionStep=0.01, axes=subplots[i,j])

	pyplot.legend(loc='lower right', prop={'size':10})
	pyplot.xlabel('knife 1-2')
	pyplot.ylabel('knife 2-3')
	pyplot.suptitle("partition simplexes of mixed cakes")
	pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/mixed3.png')

def plotMixed3a():
	fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

	for i in range(3):
		for j in range(3):
			valueFunction = ValueFunction1D([-1,1+i,-1-j])
			plotPartitionSimplex(valueFunction, fractionStep=0.01, axes=subplots[i,j])

	pyplot.legend(loc='lower right', prop={'size':10})
	pyplot.xlabel('knife 1-2')
	pyplot.ylabel('knife 2-3')
	pyplot.suptitle("partition simplexes of mixed cakes")
	pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/mixed3a.png')

def plotNegPos():
	fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

	for i in range(3):
		for j in range(3):
			valueFunction = ValueFunction1D([-1-i,1+j])
			plotPartitionSimplex(valueFunction, fractionStep=0.01, axes=subplots[i,j])

	pyplot.legend(loc='lower right', prop={'size':10})
	pyplot.xlabel('knife 1-2')
	pyplot.ylabel('knife 2-3')
	pyplot.suptitle("partition simplexes of mixed cakes")
	pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/negpos.png')


def plotIndifferenceIntervals():
	fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

	for i in range(3):
		for j in range(3):
			valueFunction = ValueFunction1D([3,i,-i,3,j,-j,3])
			plotPartitionSimplex(valueFunction, fractionStep=0.01, axes=subplots[i,j])

	pyplot.legend(loc='lower right', prop={'size':10})
	pyplot.xlabel('knife 1-2')
	pyplot.ylabel('knife 2-3')
	pyplot.suptitle("partition simplexes of cakes with indifference-intervals")
	pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/indif.png')

def plotSwitches3():
	fig,subplots = pyplot.subplots(3, 3, sharex='col', sharey='row')

	for i in range(3):
		for j in range(3):
			valueFunction = ValueFunction1D([-1+i,2,-7,2,-1+j])
			plotPartitionSimplex(valueFunction, fractionStep=0.002, axes=subplots[i,j])

	pyplot.legend(loc='lower right', prop={'size':10})
	pyplot.xlabel('knife 1-2')
	pyplot.ylabel('knife 2-3')
	pyplot.suptitle("Partition simplexes with different kinds of switches")
	pyplot.savefig('/home/erelsgl/Dropbox/papers/Bads/graphics/switches3.png')

plotPositive3()
#plotNegative3()
#plotMixed3()
#plotSwitches3()
#plot_partition_simplex(ValueFunction1D([1,2,3]))
#plot_partition_simplex(ValueFunction1D([-1,2,-2,2,-2,2,-2,2,-2]))
#plotIndifferenceIntervals()
#lotMixed3a()
#plotMixed3b()

pyplot.show()
