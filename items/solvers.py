#!python3

""" 
Utility functions for solving optimization problems using a sequence of solvers.

Author: Erel Segal-Halevi
Since:  2021-05
"""

import cvxpy

def solve(problem:cvxpy.Problem, solvers:list):
	"""
	Try to solve the given cvxpy problem using the given solvers, in order, until one succeeds.
    See here https://www.cvxpy.org/tutorial/advanced/index.html for a list of supported solvers.
	"""
	for solver in solvers[:-1]:  # Try the first n-1 solvers.
		try:
			problem.solve(solver=solver)
		except cvxpy.SolverError:
			pass
	problem.solve(solvers[-1])   # If the first n-1 fail, try the last one.
	if problem.status == "infeasible":
		raise ValueError("Problem is infeasible")
	elif problem.status == "unbounded":
		raise ValueError("Problem is unbounded")
	