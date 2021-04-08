#!python3

"""
A valuation matrix is a matrix v in which each row represents an agent, 
   each column represents an object, and v[i][j] is the value of agent i to object j.
It is used as an input to algorithms of fair division with additive valuations.

Author: Erel Segal-Halevi
Since:  2021-03
"""

import numpy as np

class ValuationMatrix:
	"""
	A valuation matrix is a matrix v in which each row represents an agent, 
		each column represents an object, and v[i][j] is the value of agent i to object j.
	
	It can be initialized by:

	* A 2-dimensional numpy array (np.ndarray);
	* A list of lists;
	* Another ValuationMatrix.

	>>> v = ValuationMatrix([[1,4,7],[6,3,0]])
	>>> v[0,1]
	4
	>>> v[0][1]
	4
	>>> v[0]
	array([1, 4, 7])
	>>> v
	[[1 4 7]
 	 [6 3 0]]
	>>> for agent in v.agents(): print(v[agent])
	[1 4 7]
	[6 3 0]
	"""
	def __init__(self, valuation_matrix: np.ndarray):
		if isinstance(valuation_matrix,list):
			valuation_matrix = np.array(valuation_matrix)
		elif isinstance(valuation_matrix,ValuationMatrix):
			valuation_matrix = valuation_matrix._v

		self._v = valuation_matrix
		self.num_of_agents = len(valuation_matrix)
		self.num_of_objects = len(valuation_matrix[0])

	def agents(self):
		return range(self.num_of_agents)

	def objects(self):
		return range(self.num_of_objects)

	def __getitem__(self, key):
		if isinstance(key,tuple):
			return self._v[key[0]][key[1]]
		else:
			return self._v[key]

	def equals(self, other)->bool:
		return np.array_equal(self._v, other._v)		

	def __repr__(self):
		return np.array2string (self._v, max_line_width=100)		





if __name__ == '__main__':
	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))

