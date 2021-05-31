#!python3

""" 
Utility functions for solving optimization problems using a sequence of solvers.

Author: Erel Segal-Halevi
Since:  2021-05
"""

import cvxpy

DEFAULT_SOLVERS=[cvxpy.XPRESS, cvxpy.OSQP, cvxpy.SCS]

import logging
logger = logging.getLogger(__name__)

def solve(problem:cvxpy.Problem, solvers:list=DEFAULT_SOLVERS):
	"""
	Try to solve the given cvxpy problem using the given solvers, in order, until one succeeds.
    See here https://www.cvxpy.org/tutorial/advanced/index.html for a list of supported solvers.
	"""
	is_solved=False
	for solver in solvers[:-1]:  # Try the first n-1 solvers.
		try:
			problem.solve(solver=solver)
			logger.info("Solver %s succeeds",solver)
			is_solved = True
			break
		except cvxpy.SolverError as err:
			logger.info("Solver %s fails: %s", solver, err)
	if not is_solved:
		problem.solve(solver=solvers[-1])   # If the first n-1 fail, try the last one.
	if problem.status == "infeasible":
		raise ValueError("Problem is infeasible")
	elif problem.status == "unbounded":
		raise ValueError("Problem is unbounded")

def maximize(objective, constraints, solvers:list=DEFAULT_SOLVERS):
	"""
	A utility function for finding the maximum of a general objective function.

	>>> import numpy as np
	>>> x = cvxpy.Variable()
	>>> np.round(maximize(x, [x>=1, x<=3]),3)
	3.0
	"""
	problem = cvxpy.Problem(cvxpy.Maximize(objective), constraints)
	solve(problem, solvers=solvers)
	return objective.value.item()

def minimize(objective, constraints, solvers:list=DEFAULT_SOLVERS):
	"""
	A utility function for finding the minimum of a general objective function.

	>>> import numpy as np
	>>> x = cvxpy.Variable()
	>>> np.round(minimize(x, [x>=1, x<=3]),3)
	1.0
	"""
	problem = cvxpy.Problem(cvxpy.Minimize(objective), constraints)
	solve(problem, solvers=solvers)
	return objective.value.item()




if __name__ == '__main__':
	import sys
	logger.addHandler(logging.StreamHandler(sys.stdout))
	logger.setLevel(logging.INFO)

	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))
