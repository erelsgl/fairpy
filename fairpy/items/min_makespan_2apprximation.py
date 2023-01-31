'''
Find 2 approximation min makespan on unrelated parallel machines.
Based on:

Jan Karel Lenstra, David B Shmoys and Eva Tardos.
[2-Approximation algorithm for a generalization of scheduling on unrelated parallel machines]
(https://link.springer.com/article/10.1007/BF01585745),

Programmers: Israel Yacobovich
Date: 2023-01
'''


from fairpy import ValuationMatrix, Allocation, AllocationMatrix, divide

import numpy as np
from numpy.random import randint, uniform
import cvxpy as cp
import networkx as nx

from typing import Callable, Iterator, Tuple
from itertools import product
from copy import copy
import logging

logger = logging.getLogger(__name__)

" The Main Method "

def min_makespan_2apprximation(input: ValuationMatrix) -> Allocation:

    ''' 
        This method returns a 2-approximation of the optimal min makespan.
        Both as the actual scheduling and the makespan.

        >>> min_makespan_2apprximation(ValuationMatrix([[1, 5, 1, 10], [2, 4, 4, 3], [2, 5, 3, 3], [3, 3, 7, 10]]))
        Agent #0 gets { 100.0% of 0, 100.0% of 2} with value 2.
        Agent #1 gets { 100.0% of 3} with value 3.
        Agent #2 gets {} with value 0.
        Agent #3 gets { 100.0% of 1} with value 3.
        <BLANKLINE>
        >>> min_makespan_2apprximation(ValuationMatrix([[1, 2, 5], [2, 2, 1],[2, 3, 5]]))
        Agent #0 gets { 100.0% of 1} with value 2.
        Agent #1 gets { 100.0% of 2} with value 1.
        Agent #2 gets { 100.0% of 0} with value 2.
        <BLANKLINE>
        >>> divide(min_makespan_2apprximation, ValuationMatrix([[1, 1.1], [0.5, 1.2]]))
        Agent #0 gets { 100.0% of 1} with value 1.1.
        Agent #1 gets { 100.0% of 0} with value 0.5.
        <BLANKLINE>
    '''

    # executing algorithm
    output = schedule()
    MinMakespan(apprx, input, output)

    # casting output
    assignments = output.assignments
    allocations = np.zeros(output.shape)
    for job in assignments: allocations[assignments[job], job] = 1

    return Allocation(agents = input, bundles = AllocationMatrix(allocations))



" Auxiliaries "


class schedule:

    ''' 
        custom output class to wrap the libraries ValuationMatrix for this programs needs

        >>> scd = schedule()
        >>> scd.build(ValuationMatrix(np.eye(2)))
        >>> for mechine, job in scd:    print(mechine, job, end = ' ')
        0 0 0 1 1 0 1 1 
        >>> print(scd.jobs)
        2
        >>> print(scd.mechines)
        2
        >>> print(scd.shape)
        (2, 2)
        >>> scd.scedual(0, 0)
        >>> scd.scedual(1, 1)
        >>> print(scd.makespan)
        1.0
        >>> print(scd.assignments)
        {0: 0, 1: 1}

     '''

    def __init__(self) -> None:

        self.costs : ValuationMatrix
        self._assignments : dict


    @property
    def jobs(self) -> int: return len(self.costs.objects())

    @property
    def mechines(self) -> int: return len(self.costs.agents())

    @property
    def shape(self) -> Tuple[int]: return self.mechines, self.jobs

    @property
    def assignments(self) -> dict: return copy(self._assignments)

    @assignments.setter
    def assignments(self, new_assignments: dict): self._assignments = copy(new_assignments)

    @property
    def makespan(self) -> float:

        return max(sum(
                            self.costs[mechine, job]
                            for job in self.costs.objects()
                            if job in self._assignments.keys() and self._assignments[job] == mechine
                       )
                        for mechine in self.costs.agents()
                   )


    # iterator for indexes covering exactly the data structure
    def __iter__(self) -> Iterator[int]:
        return iter(product(self.costs.agents(), self.costs.objects()))

    # lazy initialization
    def build(self, cost_matrix: ValuationMatrix):

        # different algorithms can use an instance with the same cost matrix, Flyweight design
        self.costs = cost_matrix
        self._assignments = {}

    # assigning a job to a machine to process
    def scedual(self, mechine: int, job: int):

        if job in self._assignments.keys() : raise KeyError('assignment already scedualed')
        self._assignments[job] = mechine

    # delete all assignments, start over
    def clear(self): self._assignments.clear()

    # are all jobs scedualed
    def complete(self) -> bool: return len(self._assignments) == self.jobs

    # current workload of specific machine
    def loadOf(self, mechine: int) -> float:
        return sum(self.costs[mechine, job]  for job in self.costs.objects() if job in self._assignments.keys() and self._assignments[job] == mechine)



""" Algorithms """

MinMakespanAlgo = Callable[[schedule], None]


def optimal(output: schedule) -> None:

    ''' 
        naive algo, goes through all options, mostly for testing

        >>> output = schedule()
        >>> output.build(ValuationMatrix([[1, 2, 5], [2, 2, 1],[2, 3, 5]]))
        >>> optimal(output)
        >>> print(output.makespan)
        2
        >>> print(output.assignments)
        {0: 2, 1: 0, 2: 1}
    '''

    output.clear()

    best_makespan = float('inf')
    best_assignment = output.assignments

    for assign in product(range(output.mechines), repeat = output.jobs):

        output.clear()

        for job in range(output.jobs):  output.scedual(assign[job], job)

        if output.makespan < best_makespan:

            best_makespan = output.makespan
            best_assignment = output.assignments

    output.assignments = best_assignment


def greedy(output: schedule) -> None:
    
    ''' 
    greedy scheduling. Iterate through all jobs, at each iteration:
    assign to the machine that minimizes the current makespan.

    >>> output = schedule()
    >>> output.build(ValuationMatrix([[1, 2, 5], [2, 2, 1],[2, 3, 5]]))
    >>> greedy(output)
    >>> print(output.makespan)
    3
    >>> print(output.assignments)
    {0: 0, 1: 1, 2: 1}
    >>> output.build(ValuationMatrix([[1, 2, 1], [4, 2, 4],[2, 3, 2]]))
    >>> greedy(output)
    >>> print(output.makespan)
    2
    >>> print(output.assignments)
    {0: 0, 1: 1, 2: 0}
    >>> output.build(ValuationMatrix([[1, 2, 1], [4, 2, 4],[2, 3, 2], [3, 1, 2]]))
    >>> greedy(output)
    >>> print(output.makespan)
    2
    >>> print(output.assignments)
    {0: 0, 1: 3, 2: 0}
    >>> output.build(ValuationMatrix([[1, 5, 1, 10], [2, 4, 4, 3], [2, 5, 3, 3], [3, 3, 7, 10]]))
    >>> greedy(output)
    >>> print(output.makespan)
    3
    >>> print(output.assignments)
    {0: 0, 1: 3, 2: 0, 3: 1}
    '''

    output.clear()

    for job in range(output.jobs):
        output.scedual(min(range(output.mechines), key = lambda mechine : output.costs[mechine, job] + output.loadOf(mechine)), job)


def apprx(output: schedule) -> None:

    '''
    closing in on the optimal solution with binary search
    using a LP and a spacial rounding algo

    >>> output = schedule()
    >>> output.build(ValuationMatrix([[1, 2], [2, 1]]))
    >>> apprx(output)
    >>> print(output.makespan)
    1
    >>> print(output.assignments)
    {0: 0, 1: 1}
    >>> output.build(ValuationMatrix([[1, 2, 3], [2, 1, 2], [3, 3, 1]]))
    >>> apprx(output)
    >>> print(output.makespan)
    1
    >>> output.build(ValuationMatrix([[0.5, 2, 0.6], [1, 0.5, 2], [0.25, 0.8, 1]]))
    >>> apprx(output)
    >>> print(output.makespan <= 1.21)
    True
    >>> output.build(ValuationMatrix([[1, 2, 1, 10], [2, 5, 3, 3], [3, 3, 7, 10]]))
    >>> apprx(output)
    >>> print(output.makespan <= 6.1)
    True
    '''

    output.clear()

    # bounds on solution via a greedy solution
    greedy(output)

    upper = output.makespan
    lower = upper / output.mechines

    # extreme case
    if output.mechines == 1: return

    # homing on the best solution with binary search

    while lower <= upper:

        middle = (upper + lower) / 2

        feasable = LinearProgram(output, middle)

        if not feasable:    lower = middle + 0.001
        else:               upper = middle - 0.001



def LinearProgram(output: schedule, apprx_bound: float) -> bool:

    ''' The linear program fashioned in the paper '''

    variables = cp.Variable(output.shape)
    # all variables are at least 0
    constraints = [variables >= 0]

    # out of all mechines that can do job j in time <= aprrx_bound
    # only 1 may be assigned to handle it, for j in all Jobs
    for job in range(output.jobs):

        mask = output.costs.submatrix(list(output.costs.agents()), [job])[:] <= apprx_bound
        
        if not (mask == False).all(): constraints.append(cp.sum(variables[:, job][mask[:, 0]]) == 1)
        else:   return False

    # out of all jobs that mechine m can do in time <= aprrx_bound
    # m can handle at most deadline-m worth of processing time of'em, for m in all Mechines
    for mechine in range(output.mechines):

        mask = output.costs.submatrix([mechine], list(output.costs.objects()))[:] <= apprx_bound

        if not (mask == False).all(): constraints.append(cp.sum(variables[mechine, :][mask[0, :]]) <= apprx_bound)


    prob = cp.Problem(cp.Minimize(variables[0, 0]), constraints)
    # simplex solver version opt to find most sparse solutions
    prob.solve(solver = cp.SCIPY, scipy_options = {"method" : "highs"})
    
    if prob.status != 'optimal':
        logger.info('LP status: %s', prob.status)
        return False

    # program possible
    output.clear()
    #rounding
    relaxed_sol = np.round(variables.value, decimals = 5)
    relaxed_sol[relaxed_sol > 0.98] = 1
    relaxed_sol[relaxed_sol < 0.02] = 0
    Round(output, relaxed_sol)
    return True



def Round(output: schedule, fractional_sol: np.ndarray):

    ''' The rounding theorem for the LP's solution fashioned in the paper '''

    logger.info('fractional solution for the LP: \n%s', fractional_sol)

    def node_to_ind(name: str) -> int: return int(name[1:])
    def ind_to_node(num: int, job: bool) -> str: return 'J' + str(num) if job else 'M' + str(num)

    mechine_nodes = ['M' + str(i) for i in range(output.mechines)]
    job_nodes =     ['J' + str(i) for i in range(output.jobs)]

    G = nx.Graph()
    G.add_nodes_from(mechine_nodes, bipartite = 0)
    G.add_nodes_from(job_nodes, bipartite = 1)
    G.add_edges_from({
                        ('M' + str(mechine), 'J' + str(job)) : fractional_sol[mechine, job]
                        for mechine, job in output
                        if fractional_sol[mechine, job] > 0
                     })

    # adopting integral assignments
    for mechine, job in output:
        if fractional_sol[mechine, job] == 1:

            try: output.scedual(mechine, job)
            except Exception: logger.exception('Exception while scedualing\n', exc_info = True)
            
            G.remove_edge(ind_to_node(mechine, False), ind_to_node(job, True))


    if not nx.bipartite.is_bipartite(G):    logger.debug('G[x] should be bipartite, relaxed sol: %s', fractional_sol)
    logger.info('E(G[x]): %s', G.edges())

    # assigning the rest acording to the algo, via max match
    for component in nx.connected_components(G):

        if len(component) < 2: continue

        matching = nx.algorithms.bipartite.maximum_matching(G.subgraph(component)).items()
        logger.info('* part of the max matching in G[x]: %s', matching)

        for mechine, job in filter(lambda edge : edge[0][0] == 'M', matching):

            try: output.scedual(node_to_ind(mechine), node_to_ind(job))
            except Exception: logger.exception('Excaption while scedualing\n', exc_info = True)



def MinMakespan(algo: MinMakespanAlgo, input: ValuationMatrix, output: schedule, **kwargs):

    '''
    generic function for the min-makespan problem

    >>> scd = schedule()
    >>> MinMakespan(greedy, ValuationMatrix([[10, 5, 7], [10, 2, 5],[1, 6, 6]]), scd)
    >>> print(scd.makespan)
    7
    >>> print(scd.assignments)
    {0: 2, 1: 1, 2: 0}
    >>> MinMakespan(apprx, ValuationMatrix([[10, 5, 7], [10, 2, 5],[1, 6, 6]]), scd)
    >>> print(scd.makespan)
    5
    >>> print(scd.assignments)
    {1: 0, 2: 1, 0: 2}
    '''

    try:

        output.build(input)
        algo(output, **kwargs)

    except Exception:   logger.exception('min makespan algo failed, algo: %s, input: %s, output: %s', algo.__name__, input, output.assignments)



if __name__ == '__main__':

    import doctest

    logging_format = '%(levelname)s - %(message)s'
    logging.basicConfig(level = logging.DEBUG, filename = 'pyproject.log', filemode = 'w', format = logging_format)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(logging_format)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    failures, tests = doctest.testmod(report = True)
    print("{} failures, {} tests".format(failures, tests))