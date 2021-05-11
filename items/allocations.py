#!python3

import numpy as np
from typing import *

from fairpy.valuations import ValuationMatrix

class AllocationMatrix:
	"""
	A matrix z in which each row represents an agent, each column represents an object, and z[i][j] is the fraction given to agent i from object j.

	>>> z = AllocationMatrix([[.2,.3,.5],[.8,.7,.5]])
	>>> z[0,1]
	0.3
	>>> z[0]
	array([0.2, 0.3, 0.5])
	>>> z
	[[0.2 0.3 0.5]
	 [0.8 0.7 0.5]]
	"""

	def __init__(self, allocation_matrix:np.ndarray):
		if isinstance(allocation_matrix,list):
			allocation_matrix = np.array(allocation_matrix)
		elif isinstance(allocation_matrix,AllocationMatrix):
			allocation_matrix = allocation_matrix._z
		self._z = allocation_matrix
		self.num_of_agents = len(allocation_matrix)
		self.num_of_objects = len(allocation_matrix[0])

	def agents(self):
		return range(self.num_of_agents)

	def objects(self):
		return range(self.num_of_objects)

	def num_of_sharings(self):
		"""
		Return the number of sharings in this allocation.
		>>> AllocationMatrix([ [1, 1, 0, 0] , [0, 0, 1, 0] , [0, 0, 0, 1] ]).num_of_sharings()   # No sharing
		0
		>>> AllocationMatrix([ [1, 0.5, 0, 0] , [0, 0.5, 1, 0] , [0, 0, 0, 1] ]).num_of_sharings()   # One sharing
		1
		>>> AllocationMatrix([ [1, 0.4, 0, 0] , [0, 0.4, 1, 0] , [0, 0.2, 0, 1] ]).num_of_sharings()   # Two sharings in same object
		2
		>>> AllocationMatrix([ [1, 0.4, 0, 0] , [0, 0.6, 0.3, 0] , [0, 0, 0.7, 1] ]).num_of_sharings()   # Two sharings in different objects
		2
		"""
		num_of_edges = 0
		for i in self.agents():
			for o in self.objects():
				num_of_edges += np.ceil(self._z[i][o])
		return int(num_of_edges - self.num_of_objects)

	def round(self, num_digits:int):
		"""
		Rounds the allocation to the given number of digits.

		WARNING: The rounding might change the sum of rows and columns.
		See here http://people.mpi-inf.mpg.de/~doerr/papers/unbimatround.pdf 
		for an unbiased matrix rounding algorithm
		"""
		for i in range(len(self._z)):
			for j in range(len(self._z[i])):
				fraction = np.round(self._z[i][j], num_digits)
				if fraction==0:
					fraction=0   # avoid "negative zero"
				self._z[i][j] = fraction
		return self

	def utility_profile(self, v:ValuationMatrix)->np.array:
		"""
		Returns a vector that maps each agent to its utility (=sum of values) under this allocation.

		>>> z = AllocationMatrix([[.2,.3,.5],[.8,.7,.5]])
		>>> v = ValuationMatrix([[0.5,1,0],[0.5,0,1]])
		>>> z.utility_profile(v)
		array([0.4, 0.9])
		"""
		return np.array([np.dot(v[i],self[i]) for i in self.agents()])


	def __getitem__(self, key):
		if isinstance(key,tuple):
			return self._z[key[0]][key[1]]
		else:
			return self._z[key]

	def __repr__(self):
		return np.array2string (self._z, max_line_width=100)		


if __name__ == '__main__':
	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))
