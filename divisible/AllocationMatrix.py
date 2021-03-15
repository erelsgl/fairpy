#!python3

import numpy as np
from typing import *

class AllocationMatrix:
	"""
	A matrix z in which each row represents an agent, each column represents an object, and z[i][j] is the fraction given to agent i from object j.
	"""

	def __init__(self, allocation_matrix:np.ndarray):
		if isinstance(allocation_matrix,list):
			allocation_matrix = np.array(allocation_matrix)
		self.z = allocation_matrix
		self.num_of_agents = len(allocation_matrix)
		self.agents = range(self.num_of_agents)
		self.num_of_objects = len(allocation_matrix[0])
		self.objects = range(self.num_of_objects)
		
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
		for i in self.agents:
			for o in self.objects:
				num_of_edges += np.ceil(self.z[i][o])
		return int(num_of_edges - self.num_of_objects)

	def __repr__(self):
		return np.array2string (self.z, max_line_width=100)		


if __name__ == '__main__':
	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))
