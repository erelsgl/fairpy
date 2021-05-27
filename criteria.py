#!python3

"""
Defines fairness criteria for both divisible and indivisible allocations.

Programmer: Erel Segal-Halevi
Since: 2021-04
"""

def is_envyfree(agents, bundles, roundAcc:int=2)->bool:
	"""
	checks whether or not the allocation is envy free.

	:param roundAcc: the accuracy in digits of the envy free check.
	:return: True is the allocation is envy free, otherwise False.

	>>> from fairpy.agents import PiecewiseUniformAgent
	>>> agents = [PiecewiseUniformAgent([(2,3)], "Alice"), PiecewiseUniformAgent([(0,10)], "George")]
	>>> pieces = [[(1,2),(2,3)], [(4,5),(0,1)]]
	>>> is_envyfree(agents, pieces, roundAcc=2)
	True
	>>> pieces = [[(4,5),(0,1)], [(1,2),(2,3)]]
	>>> is_envyfree(agents, pieces, roundAcc=2)
	False
	"""
	for i in range(len(agents)):
		selfVal = agents[i].value(bundles[i])
		for j in range(len(bundles)):
			otherVal = agents[i].value(bundles[j])
			if round(otherVal-selfVal, roundAcc) > 0:
				return False
	return True

if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
