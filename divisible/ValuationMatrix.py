#!python3

import numpy as np

class ValuationMatrix:
	"""
	A matrix v in which each row represents an agent, each column represents an object, and v[i][j] is the value of agent i to object j.
	"""

	def __init__(self, valuation_matrix:np.ndarray):
		if isinstance(valuation_matrix,list):
			valuation_matrix = np.array(valuation_matrix)
		self.v = valuation_matrix
		self.num_of_agents = len(valuation_matrix)
		self.agents = range(self.num_of_agents)
		self.num_of_objects = len(valuation_matrix[0])
		self.objects = range(self.num_of_objects)

	def __repr__(self):
		return np.array2string (self.v, max_line_width=100)		



if __name__ == '__main__':
	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))

