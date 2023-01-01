# data structures
import numpy as np
from fairpy import ValuationMatrix
# psedu random functions
from numpy.random import randint, uniform
# convex optimization
import cvxpy as cp
# graph search algorithms
import networkx as nx
# oop
from abc import ABC, abstractclassmethod
# data types
from typing import Callable, Iterable, Iterator, Tuple, Dict, Any
# iteration tool
from itertools import product
# debugging & monitoring
import logging

logger = logging.getLogger(__name__)

logging_format = '%(levelname)s - %(message)s'

logging.basicConfig(level = logging.DEBUG, filename = 'pyproject.log', filemode = 'w', format = logging_format)

file_handler = logging.FileHandler("pyproject.log")
file_handler.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)

formatter = logging.Formatter(logging_format)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
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


class scedual(ABC, Iterable):

    ''' custom output class to wrap the libraries ValuationMatrix for this programs needs '''

    def __init__(self) -> None:
        super().__init__()

        self.costs : ValuationMatrix
        self.assignments : np.ndarray.astype(bool)


    @property
    def Jobs(self) -> int: return len(self.costs.objects())

    @property
    def Mechines(self) -> int: return len(self.costs.agents())

    @property
    def shape(self) -> Tuple[int]: return self.Mechines, self.Jobs


    # iterator for indexes covering exactly the data structure
    def __iter__(self) -> Iterator[int]:
        return iter(product(self.costs.agents(), self.costs.objects()))

    # lazy initilization
    def build(self, cost_matrix: ValuationMatrix):

        # different algorithms can use an instance with the same cost matrix, Flyweight design
        self.costs = cost_matrix
        self.assignments = np.zeros(self.shape).astype(bool)

    # assigning a job to a mechine to process
    def scedual(self, mechine: int, job: int):

        if self.assignments[mechine, job]: raise KeyError('assignment already scedualed')
        self.assignments[mechine, job] = True

    # delet all assignments, start over
    def clear(self): self.assignments = np.zeros(self.shape).astype(bool)

    # are all jobs scedual
    def complete(self) -> bool: return np.add.reduce(self.assignments, axis = 0).all()

    # current workload of spesific mechine
    def loadOf(self, mechine: int) -> float:
        return sum(self.costs[mechine, job]  for job in self.costs.objects() if self.assignments[mechine, job])


    @abstractclassmethod
    def extract_result(self): pass


class scedual_assignment(scedual):

    '''
    implementation that keeps track of the actuall makespan

    >>> scd = scedual_assignment()
    >>> scd.build(ValuationMatrix([[1, 1], [1, 1]]))
    >>> scd.scedual(0, 0)
    >>> scd.scedual(1, 1)
    >>> print(scd.extract_result())
    {(1, 1), (0, 0)}
    '''

    def extract_result(self):
        return { 
                    (mechine, job)
                    for mechine, job in self
                    if self.assignments[mechine, job]
                }

class scedual_makespan(scedual):

    '''
    implementation that keeps track of the assignment

    >>> scd = scedual_makespan()
    >>> scd.build(ValuationMatrix([[1, 1], [1, 1]]))
    >>> scd.scedual(0, 0)
    >>> scd.scedual(1, 1)
    >>> print(scd.extract_result())
    1
    >>> scd.scedual(0, 1)
    >>> print(scd.extract_result())
    2
    '''

    def extract_result(self):

        return max(sum(
                            self.costs[mechine, job]
                            for job in range(self.Jobs)
                            if self.assignments[mechine, job]
                        )
                        for mechine in range(self.Mechines)
                    )



""" Algorithms """


MinMakespanAlgo = Callable[[scedual], None]


def optimal(output: scedual) -> None:

    ''' 
        naive algo, goes through all options, mostly for testing

        >>> output = scedual_makespan()
        >>> output.build(ValuationMatrix([[1, 2, 5], [2, 2, 1],[2, 3, 5]]))
        >>> optimal(output)
        >>> print(output.extract_result())
        2
        >>> output = scedual_assignment()
        >>> output.build(ValuationMatrix([[1, 2, 5], [2, 2, 1],[2, 3, 5]]))
        >>> optimal(output)
        >>> print(output.extract_result())
        {(0, 1), (1, 2), (2, 0)}
    '''

    output.clear()

    checker = scedual_makespan()
    checker.build(output.costs)
    best = float('inf')

    for assign in product(range(output.Mechines), repeat = output.Jobs):

        checker.clear()

        for job in range(output.Jobs):  checker.scedual(assign[job], job)

        if checker.extract_result() < best:

            output.clear()
            for job in range(output.Jobs):  output.scedual(assign[job], job)

            best = checker.extract_result()


def greedy(output: scedual) -> None:
    
    ''' 
    greedy scedualing.
    Iterate through all jobs, at each iteration:
    assign to the mechine that minimises the current makspan.

    >>> output = scedual_makespan()
    >>> output.build(ValuationMatrix([[1, 2, 5], [2, 2, 1],[2, 3, 5]]))
    >>> greedy(output)
    >>> print(output.extract_result())
    3
    >>> output.build(ValuationMatrix([[1, 2, 1], [4, 2, 4],[2, 3, 2]]))
    >>> greedy(output)
    >>> print(output.extract_result())
    2
    >>> output.build(ValuationMatrix([[1, 2, 1], [4, 2, 4],[2, 3, 2], [3, 1, 2]]))
    >>> greedy(output)
    >>> print(output.extract_result())
    2
    >>> output.build(ValuationMatrix([[1, 5, 1, 10], [2, 4, 4, 3], [2, 5, 3, 3], [3, 3, 7, 10]]))
    >>> greedy(output)
    >>> print(output.extract_result())
    3
    >>> output = scedual_assignment()
    >>> output.build(ValuationMatrix([[1, 2, 5], [2, 2, 1],[2, 3, 5]]))
    >>> greedy(output)
    >>> print(output.extract_result())
    {(1, 1), (1, 2), (0, 0)}
    >>> output.build(ValuationMatrix([[1, 2, 1], [4, 2, 4],[2, 3, 2]]))
    >>> greedy(output)
    >>> print(output.extract_result())
    {(1, 1), (0, 2), (0, 0)}
    >>> output.build(ValuationMatrix([[1, 2, 1], [4, 2, 4],[2, 3, 2], [3, 1, 2]]))
    >>> greedy(output)
    >>> print(output.extract_result())
    {(3, 1), (0, 2), (0, 0)}
    >>> output.build(ValuationMatrix([[1, 5, 1, 10], [2, 4, 4, 3], [2, 5, 3, 3], [3, 3, 7, 10]]))
    >>> greedy(output)
    >>> print(output.extract_result())
    {(3, 1), (0, 2), (1, 3), (0, 0)}
    '''

    output.clear()

    for job in range(output.Jobs):
        output.scedual(min(range(output.Mechines), key = lambda mechine : output.costs[mechine, job] + output.loadOf(mechine)), job)


def apprx(output: scedual) -> None:

    '''
    closing in on the optimal solution with binry search
    using a LP and a spacial rounding algo

    >>> output = scedual_makespan()
    >>> output.build(ValuationMatrix([[1, 2], [2, 1]]))
    >>> apprx(output)
    >>> print(output.extract_result())
    1
    >>> output.build(ValuationMatrix([[1, 2, 3], [2, 1, 2], [3, 3, 1]]))
    >>> apprx(output)
    >>> print(output.extract_result())
    1
    >>> output.build(ValuationMatrix([[0.5, 2, 0.6], [1, 0.5, 2], [0.25, 0.8, 1]]))
    >>> apprx(output)
    >>> print(output.extract_result() <= 1.21)
    True
    >>> output.build(ValuationMatrix([[1, 2, 1, 10], [2, 5, 3, 3], [3, 3, 7, 10]]))
    >>> apprx(output)
    >>> print(output.extract_result() <= 6.1)
    True
    >>> output = scedual_assignment()
    >>> output.build(ValuationMatrix([[1, 2], [2, 1]]))
    >>> apprx(output)
    >>> print(output.extract_result())
    {(1, 1), (0, 0)}
    '''

    output.clear()

    # extreme case
    if output.Mechines == 1: greedy(output); return

    # bounds on solution via a greedy solution

    greedy_sol = scedual_makespan()
    greedy_sol.build(output.costs)

    greedy(greedy_sol)
    greedy(output)

    upper = greedy_sol.extract_result()
    lower = upper / output.Mechines

    del greedy_sol

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
    # add a constraint that requires that at most #jobs + #mechines entries will be non 0
    actives = cp.Variable(output.shape, boolean = True)
    constraints.append(actives >= variables)
    constraints.append(cp.sum(actives) <= output.Jobs + output.Mechines)


    # out of all mechines that can do job j in time <= aprrx_bound
    # only 1 may be assigned to handle it, for j in all Jobs
    for job in range(output.Jobs):

        mask = output.costs.submatrix(list(output.costs.agents()), [job])[:] <= apprx_bound
        
        if not (mask == False).all(): constraints.append(cp.sum(variables[:, job][mask[:, 0]]) == 1)
        else:   return False

    # out of all jobs that mechine m can do in time <= aprrx_bound
    # m can handle at most deadline-m worth of processing time of'em, for m in all Mechines
    for mechine in range(output.Mechines):

        mask = output.costs.submatrix([mechine], list(output.costs.objects()))[:] <= apprx_bound

        if not (mask == False).all(): constraints.append(cp.sum(variables[mechine, :][mask[0, :]]) <= apprx_bound)


    # minimize: maximum workload aka makespan
    workloads = [cp.sum(variables[mechine, :]) for mechine in range(output.Mechines)]
    try: makespan = cp.maximum( * workloads )
    except Exception: logger.exception('workloads len: %s, shape of input: %s', len(workloads), output.shape, exc_info = True)
    constraints.append(makespan <= apprx_bound)

    objective = cp.Minimize(makespan)

    prob = cp.Problem(objective, constraints)
    prob.solve()
    
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

    mechine_nodes = ['M' + str(i) for i in range(output.Mechines)]
    job_nodes =     ['J' + str(i) for i in range(output.Jobs)]
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

    >>> print(MinMakespan(greedy, ValuationMatrix([[10, 5, 7], [10, 2, 5],[1, 6, 6]]), scedual_makespan()))
    7
    >>> print(MinMakespan(apprx, ValuationMatrix([[10, 5, 7], [10, 2, 5],[1, 6, 6]]), scedual_makespan()))
    5
    >>> print(MinMakespan(greedy, ValuationMatrix([[10, 5, 7], [10, 2, 5],[1, 6, 6]]), scedual_assignment()))
    {(1, 1), (0, 2), (2, 0)}
    >>> print(MinMakespan(apprx, ValuationMatrix([[10, 5, 7], [10, 2, 5],[1, 6, 6]]), scedual_assignment()))
    {(0, 1), (1, 2), (2, 0)}
    '''

    output.build(input)
    algo(output, **kwargs)
    return output.extract_result()


def RandomTesting(algo: MinMakespanAlgo, output: scedual, iterations: int, **kwargs):

    ''' spesefied amount of random tests generator '''

    for i in range(iterations):
        yield MinMakespan(algo, ValuationMatrix(uniform(1, 3, (randint(1, 20), randint(1, 20)))), output, **kwargs)


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
    for i in range(iterations):

        inpt = ValuationMatrix(uniform(1, 3, (randint(1, 20), randint(1, 20))))

        res1, res2 = MinMakespan(algo1[0], inpt, scedual_makespan(), **algo1[1]), MinMakespan(algo2[0], inpt, scedual_makespan(), **algo2[1])

        if res1 < res2: score1 += 1
        if res2 < res1: score2 += 1

    return score1, score2

if __name__ == '__main__':

    import doctest
    doctest.testmod(verbose = True) 