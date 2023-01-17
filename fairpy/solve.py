#!python3

""" 
Utility functions for solving optimization problems using a sequence of solvers.

Author: Erel Segal-Halevi
Since:  2021-05
"""

import cvxpy
from typing import List, Dict, Tuple

DEFAULT_SOLVERS = [ 
	(cvxpy.SCIPY, {'method':'highs'}),   # for linear programs
	(cvxpy.SCS, {}),                     # for convex programs
	(cvxpy.OSQP, {}),       # should be installed by: pip install osqp
	(cvxpy.XPRESS, {}),     # should be installed from their website
]

import logging
logger = logging.getLogger(__name__)

def solve(problem:cvxpy.Problem, solvers:List[Tuple[str, Dict]] = DEFAULT_SOLVERS):
	"""
	Try to solve the given cvxpy problem using the given solvers, in order, until one succeeds.
    See here https://www.cvxpy.org/tutorial/advanced/index.html for a list of supported solvers.

	:param solvers list of tuples. Each tuple is (name-of-solver, keyword-arguments-to-solver)
	"""
	is_solved=False
	for (solver, solver_kwargs) in solvers:  # Try the first n-1 solvers.
		try:
			if solver==cvxpy.SCIPY:
				problem.solve(solver=solver, scipy_options=dict(solver_kwargs))  # WARNING: solve changes both its arguments!
			else:
				problem.solve(solver=solver, **solver_kwargs)
			logger.info("Solver %s [%s] succeeds", solver, solver_kwargs)
			is_solved = True
			break
		except cvxpy.SolverError as err:
			logger.info("Solver %s [%s] fails: %s", solver, solver_kwargs, err)
	if not is_solved:
		raise cvxpy.SolverError(f"All solvers failed: {solvers}")
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
	>>> np.round(minimize(x, [x>=1, x<=3], solvers=[(cvxpy.MOSEK,{}),(cvxpy.SCS,{}),(cvxpy.SCIPY,{})]),3)
	1.0
	>>> np.round(minimize(x, [x>=1, x<=3], solvers=[(cvxpy.SCS,{}),(cvxpy.SCIPY,{}),(cvxpy.MOSEK,{})]),2)
	1.0
	>>> np.round(minimize(x, [x>=1, x<=3], solvers=[(cvxpy.MOSEK,{'bfs':True}),(cvxpy.SCIPY,{'method':'highs'})]),3)
	1.0
	"""
	problem = cvxpy.Problem(cvxpy.Minimize(objective), constraints)
	solve(problem, solvers=solvers)
	return objective.value.item()

solve.logger = logger


if __name__ == '__main__':
	import sys
	logger.addHandler(logging.StreamHandler(sys.stdout))
	logger.setLevel(logging.INFO)

	import doctest
	(failures, tests) = doctest.testmod(report=True)
	print("{} failures, {} tests".format(failures, tests))
