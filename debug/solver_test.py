#!python3
"""
Calculate the maximin-share of an additive valuation function.

Author: Erel Segal-Halevi
Since : 2021-04
"""

import cvxpy

x = cvxpy.Variable()
problem = cvxpy.Problem(cvxpy.Maximize(x), [x<=1])
problem.solve(solver=cvxpy.SCIPY, scipy_options={'method':'highs-ds'})
print(problem.status)
