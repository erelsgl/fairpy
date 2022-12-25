# data structures
import numpy as np
from fairpy import ValuationMatrix
# psedu random functions
from numpy.random import randint, random
# convex optimization
import cvxpy as cvx
# graph search algorithms
import networkx as nx
# oop
from abc import ABC, abstractclassmethod
# data types
from typing import Callable, Tuple, Iterable, Iterator
# other
from itertools import product


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

    ''' custom output class '''

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

    # a mesure of the smallest value that may make a difference in the instance
    @property
    def resolution(self) -> float:

        if self.costs is None: raise RuntimeError('data hasn\'nt been initialised yet')

        def accuracy(num: float) -> int: return len(str(float(num)).split('.')[1])

        return 1 / 10 ** max(accuracy(self.costs[mechine, job])  for mechine, job in self)

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

    for job in range(output.Jobs):
        output.scedual(min(range(output.Mechines), key = lambda mechine : output.costs[mechine, job] + output.loadOf(mechine)), job)


def apprx(output: scedual) -> None:

    '''
    closing in on the optimal solution with binry search
    using a LP and a spacial rounding algo


    #>>> print(apprx(np.array([[1, 2], [2, 1]])).extract_result())
    1
    #>>> print(apprx(np.array([[1, 2, 3], [2, 1, 3], [3, 2, 1]])).extract_result())
    1
    #>>> print(apprx(np.array([[0.5, 1, 0.25], [2, 0.5, 0.8], [0.6, 2, 1]])).extract_result() <= 1.2)
    True
    #>>> print(apprx(np.array([[[1, 2, 3], [2, 5, 3],[1, 3, 7], [10, 3, 10]]])).extract_result() <= 6)
    True
    '''

    # bounds on solution via a greedy solution

    greedy_sol = scedual_makespan()
    greedy_sol.build(output.costs)
    greedy(greedy_sol)

    upper = output.extract_result()
    lower = upper / output.Mechines

    del greedy_sol

    # homing on the best solution with binary search

    smallest_step = output.resolution

    while lower <= upper:

        middle = (upper + lower) / 2

        output.clear()
        feasable = LinearProgram(output, np.array([middle] * output.Mechines), middle)

        if not feasable:    upper = middle
        else:               lower = middle + smallest_step



def LinearProgram(output: scedual, deadlines: np.ndarray, aprrx_bound: float) -> bool:


    ''' The linear program fassioned in the paper '''

    variables = cvx.Variable(output.shape)

    constraints = [variables >= np.zeros(output.shape)]

    # out of all mechines that can do job j in time <= aprrx_bound
    # only 1 may be assigned to handle it, for j in all Jobs
    constraints += [
                    sum(
                            variables[mechine, job]
                            for mechine in range(output.Mechines)
                            if output.costs[mechine, job] <= aprrx_bound
                        )
                        == 1
                    for job in range(output.Jobs)
                    ]
    # out of all jobs that mechine m can do in time <= aprrx_bound
    # m can handle at most deadline-m worth of processing time of'em, for m in all Mechines
    constraints += [
                    sum(
                            variables[mechine, job]
                            for job in range(output.Jobs)
                            if output.costs[mechine, job] <= aprrx_bound
                        )
                        <= deadlines[mechine]
                    for mechine in range(output.Mechines)
                    ]

    # minimise maximum workload aka makespan
    objective = cvx.Minimize(max(sum(
                                        variables[mechine, job]
                                        for job in range(output.Jobs)
                                    )
                                    for mechine in range(output.Mechines)
                                ))

    prob = cvx.Problem(objective, constraints)
    prob.solve()
    # rounding to an integral solution
    Round(output, prob)



def Round(output: scedual, fractional_sol: cvx.Problem):

    ''' The rounding theorem for the LP's solution fassioned in the paper '''

    G : nx.Graph = nx.union(nx.Graph(range(output.Mechines)), nx.Graph(range(output.Jobs)), rename = ('M', 'J'))
    G.add_weighted_edges_from({
                                 (mechine, job, fractional_sol[mechine, job])
                                 for mechine, job in zip(range(output.Mechines), range(output.Jobs))
                                 if fractional_sol[mechine, job > 0]
                              })

    # adopting integral assignments
    for mechine, job in zip(range(output.Mechines), range(output.Jobs)):
        if fractional_sol[mechine, job] == 1:

            output.scedual(mechine, job)
            G.remove_edge(mechine, job)


    if not nx.bipartite.is_bipartite(G):    raise RuntimeError('G[fractional solution] should be bipartite')

    # assigning the rest acording to the algo, via max match
    for mechine, job in nx.algorithms.bipartite.maximum_matching(G).items():   output.scedual(mechine, job)



def MinMakespan(algo: MinMakespanAlgo, input: ValuationMatrix, output: scedual, **kwargs):

    '''
    generic function for the min-makespan problome

    #>>> print(MinMakespan(greedy, np.array([[1, 2, 2], [2, 2, 3],[5, 1, 5]], scedual_makespan()))
    3
    #>>> print(MinMakespan(aprrx, np.array([[1, 2, 3], [2, 1, 3], [3, 2, 1]], scedual_makespan()))
    1
    '''

    output.build(input)
    algo(output, **kwargs)
    return output.extract_result()


def RandomTesting(algo: MinMakespanAlgo, output: scedual, iteration: int, **kwargs):

    ''' spesefied amount of random tests generator '''

    mechines = randint(1, 500)
    jobs = randint(1, 500)

    for i in range(iteration):
        yield MinMakespan(algo, random(0, 3, (jobs, mechines)), output, **kwargs)



if __name__ == '__main__':

    import doctest
    doctest.testmod(verbose = True)    