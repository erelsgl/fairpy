# data structures
import numpy as np
from fairpy import ValuationMatrix, Allocation, AllocationMatrix
# psedu random functions
from numpy.random import randint, uniform
# convex optimization
import cvxpy as cp
# graph search algorithms
import networkx as nx
# data types
from typing import Callable, Iterator, Tuple, Dict, Any
# iteration tool
from itertools import product
# deep copy
from copy import copy
# debugging & monitoring
import logging

logger = logging.getLogger(__name__)

logging_format = '%(levelname)s - %(message)s'

logging.basicConfig(level = logging.DEBUG, filename = 'pyproject.log', filemode = 'w', format = logging_format)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
formatter = logging.Formatter(logging_format)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


''' 
This is an implementation of 2 - approximating algorithm for the min-makespan problom.
That is: scedualing on unrelated unperallel mechines

Proposed in 1990 by:

Jan Karel LENSTRA
Eindhoven University of Technology, Eindhoven, The Netherlands, and
Centre for Mathematics and Computer Science, Amsterdam, The Netherlands
&
David B. SHMOYS and Eva Tardos
Cornell University, Ithaca, NY, USA
'''


class scedual:

    ''' 
        custom output class to wrap the libraries ValuationMatrix for this programs needs

        >>> scd = scedual()
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

    # lazy initilization
    def build(self, cost_matrix: ValuationMatrix):

        # different algorithms can use an instance with the same cost matrix, Flyweight design
        self.costs = cost_matrix
        self._assignments = {}

    # assigning a job to a mechine to process
    def scedual(self, mechine: int, job: int):

        if job in self._assignments.keys() : raise KeyError('assignment already scedualed')
        self._assignments[job] = mechine

    # delet all assignments, start over
    def clear(self): self._assignments.clear()

    # are all jobs scedualed
    def complete(self) -> bool: return len(self._assignments) == self.jobs

    # current workload of spesific mechine
    def loadOf(self, mechine: int) -> float:
        return sum(self.costs[mechine, job]  for job in self.costs.objects() if job in self._assignments.keys() and self._assignments[job] == mechine)



""" Algorithms """


MinMakespanAlgo = Callable[[scedual], None]


def optimal(output: scedual) -> None:

    ''' 
        naive algo, goes through all options, mostly for testing

        >>> output = scedual()
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


def greedy(output: scedual) -> None:
    
    ''' 
    greedy scedualing.
    Iterate through all jobs, at each iteration:
    assign to the mechine that minimises the current makspan.

    >>> output = scedual()
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


def apprx(output: scedual) -> None:

    '''
    closing in on the optimal solution with binry search
    using a LP and a spacial rounding algo

    >>> output = scedual()
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



def LinearProgram(output: scedual, apprx_bound: float) -> bool:

    ''' The linear program fassioned in the paper '''

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


    # minimize: maximum workload aka makespan
    workloads = [cp.sum(variables[mechine, :]) for mechine in range(output.mechines)]
    try: makespan = cp.maximum( * workloads )
    except Exception: logger.exception('workloads len: %s, shape of input: %s', len(workloads), output.shape, exc_info = True)
    constraints.append(makespan <= apprx_bound)

    objective = cp.Minimize(makespan)

    prob = cp.Problem(objective, constraints)
    # simplex solver version opt to find most sparse solutions
    prob.solve(solver = cp.GLPK)
    
    if prob.status != 'optimal':
        logger.info('LP status: %s', prob.status)
        return False

    output.clear()
    Round(output, np.round(variables.value, decimals = 7))
    return True



def Round(output: scedual, fractional_sol: np.ndarray):

    ''' The rounding theorem for the LP's solution fassioned in the paper '''

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
            except Exception: logger.exception('Excaption while scedualing\n', exc_info = True)
            
            G.remove_edge(ind_to_node(mechine, False), ind_to_node(job, True))


    if not nx.bipartite.is_bipartite(G):    raise RuntimeError('G[x] should be bipartite')

    logger.info('E(G[x]): %s', G.edges())

    # assigning the rest acording to the algo, via max match
    for component in nx.connected_components(G):

        if len(component) < 2: continue

        matching = nx.algorithms.bipartite.maximum_matching(G.subgraph(component)).items()
        logger.info('* part of the max matching in G[x]: %s', matching)

        for mechine, job in filter(lambda edge : edge[0][0] == 'M', matching):

            try: output.scedual(node_to_ind(mechine), node_to_ind(job))
            except Exception: logger.exception('Excaption while scedualing\n', exc_info = True)


def MinMakespan(algo: MinMakespanAlgo, input: ValuationMatrix, output: scedual, **kwargs):

    '''
    generic function for the min-makespan problome

    >>> scd = scedual()
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

    output.build(input)
    algo(output, **kwargs)


def RandomTesting(algo: MinMakespanAlgo, iterations: int, **kwargs):

    ''' spesefied amount of random tests generator '''

    scd = scedual()

    for i in range(iterations):
        MinMakespan(algo, ValuationMatrix(uniform(1, 3, (randint(1, 60), randint(1, 20)))), scd, **kwargs)
        yield scd.makespan


def compare(algo1: Tuple[MinMakespanAlgo, Dict[str, Any]], algo2: Tuple[MinMakespanAlgo, Dict[str, Any]], iterations: int) -> Tuple[int, int]:

    '''
        Comparing 2 algorithms, some times to get enough iterations so the
        avarge result would stabelize takes to much time.
    
        This method allows comparesion on the same inputs to get a sense of wich
        algo is better without wasting to much time


        >>> scr1, scr2 = compare((apprx, {}), (greedy, {}), 5)
        >>> print(type(scr1), type(scr2))
        <class 'int'> <class 'int'>
    '''


    score1 = score2 = 0
    scd1, scd2 = scedual(), scedual()

    for i in range(iterations):

        inpt = ValuationMatrix(uniform(1, 3, (randint(1, 60), randint(1, 20))))

        MinMakespan(algo1[0], inpt, scd1, **algo1[1])
        MinMakespan(algo2[0], inpt, scd2, **algo2[1])

        res1, res2 = scd1.makespan, scd2.makespan

        if res1 < res2: score1 += 1
        if res2 < res1: score2 += 1

    return score1, score2


" The Interface Method "

def min_makespan(input: ValuationMatrix) -> Allocation:

    ''' 
        This method returns a 2-approximation of the optimal minimum makespan.
        Both as the actuall scedualing and the makespan.

        >>> min_makespan(ValuationMatrix([[1, 5, 1, 10], [2, 4, 4, 3], [2, 5, 3, 3], [3, 3, 7, 10]]))
        Agent #0 gets { 100.0% of 0, 100.0% of 2} with value 2.
        Agent #1 gets { 100.0% of 3} with value 3.
        Agent #2 gets {} with value 0.
        Agent #3 gets { 100.0% of 1} with value 3.
        <BLANKLINE>
        >>> min_makespan(ValuationMatrix([[1, 2, 5], [2, 2, 1],[2, 3, 5]]))
        Agent #0 gets { 100.0% of 1} with value 2.
        Agent #1 gets { 100.0% of 2} with value 1.
        Agent #2 gets { 100.0% of 0} with value 2.
        <BLANKLINE>
    '''

    # executing algorithm
    output = scedual()
    output.build(input)
    apprx(output)

    # casting output
    assignments = output.assignments
    allocations = np.zeros(output.shape)
    for job in assignments: allocations[assignments[job], job] = 1

    return Allocation(agents = input, bundles = AllocationMatrix(allocations))

if __name__ == '__main__':

    import doctest
    
    failures, tests = doctest.testmod(report = True)
    print("{} failures, {} tests".format(failures, tests))