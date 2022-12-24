# data structures
import numpy as np
from fairpy import ValuationMatrix
# psedu random functions
from numpy.random import randint, random
# convex optimization
import cvxopt as cvx
# oop
from abc import ABC, abstractclassmethod
# data types
from typing import Callable, Tuple


''' 
This is an implementation of 2 - approximating algorithm for the min-makespan problome.
That is: scedualing on unrelated unperallel mechines

Proposed in 1990 by:

Jan Karel LENSTRA
Eindhoven University of Technology, Eindhoven, The Netherlands, and
Centre for Mathematics and Computer Science, Amsterdam, The Netherlands
&
David B. SHMOYS and Eva Tardos
Cornell University, Ithaca, NY, USA
'''


class scedual(ABC):

    ''' custom output class '''

    def __init__(self) -> None:
        super().__init__()

        self.costs : ValuationMatrix
        self.assignments : np.ndarray.astype(bool)


    @property
    def Jobs(self) -> int: return self.costs.objects()

    @property
    def Mechines(self) -> int: return self.costs.agents()

    @property
    def resolution(self) -> float:

        ''' smallest entry '''

        if self.costs is None: raise RuntimeError('data hasn\'nt been initialised yet')

        return min(min(self.costs, key = min))

    @property
    def shape(self) -> Tuple[int]: return self.Mechines, self.Jobs


    # lazy initilization
    def build(self, cost_matrix: ValuationMatrix):

        # different algorithms can use an instance with the same cost matrix
        # flyweight design
        self.costs = cost_matrix
        self.assignments = np.zeros(self.shape).astype(bool)

    def scedual(self, mechine: int, job: int):

        if self.assignments[mechine, job]: raise KeyError('assignment already scedualed')
        self.assignments[mechine, job] = True

    def clear(self):
        ''' delet all assignments, start over '''
        self.assignments = np.zeros(self.shape).astype(bool) 


    @abstractclassmethod
    def extract_scedual(self): pass


class scedual_makespan(scedual):

    '''
    implementation that keeps track of the actuall makespan

    >>> scd = scedual_makespan()
    >>> scd.build(ValuationMatrix([[1, 1], [1, 1]]))
    >>> scd.scedual(0, 0)
    >>> scd.scedual(1, 1)
    >>> print(scd.extract_scedual())
    {0 : 0, 1 : 1}
    '''

    def extract_scedual(self): 
        return { 
                    mechine : job
                    for mechine in range(self.Mechines)
                    for job in range(self.Jobs)
                    if self.assignments[mechine, job]
                }

class scedual_assignment(scedual):

    '''
    implementation that keeps track of the assignment

    >>> scd = scedual_makespan()
    >>> scd.build(ValuationMatrix([[1, 1], [1, 1]]))
    >>> scd.scedual(0, 0)
    >>> scd.scedual(1, 1)
    >>> print(scd.extract_scedual())
    1
    >>> scd.scedual(0, 1)
    >>> print(scd.extract_scedual())
    2
    '''

    def extract_scedual(self):

        return max(sum((
                            self.costs[mechine, job]
                            for job in range(self.Jobs)
                            if self.assignments[mechine, job]
                        ))
                        for mechine in range(self.Mechines)
                    )



""" Algorithms """


MinMakespanAlgo = Callable[[scedual], None]


def greedy(output: scedual) -> None:
    
    ''' 
    greedy scedualing.
    Iterate through all jobs, at each iteration:
    assign to the mechine that minimises the current makspan.


    >>> print(greedy(np.array([[1, 2, 2], [2, 2, 3],[5, 1, 5]])).extract_scedual())
    3
    >>> print(greedy(np.array([[1, 4, 2], [2, 2, 3],[1, 4, 2]])).extract_scedual()) 
    2
    >>> print(greedy(np.array([[1, 4, 2, 3], [2, 2, 3, 1],[1, 4, 2, 2]])).extract_scedual())
    2
    >>> print(greedy(np.array([[1, 4, 2, 3], [2, 5, 5, 3],[1, 4, 3, 7], [10, 3, 3, 10]])).extract_scedual())
    4
    '''

    for job in range(output.costs.objects()):
        output.scedual(min((mechine for mechine in range(output.costs.agents())), key = lambda m : output.costs[m, job]), job)

def apprx(output: scedual) -> None:

    '''
    closing in on the optimal solution with binry search
    using a LP and a spacial rounding algo


    >>> print(apprx(np.array([[1, 2], [2, 1]])).extract_scedual())
    1
    >>> print(apprx(np.array([[1, 2, 3], [2, 1, 3], [3, 2, 1]])).extract_scedual())
    1
    >>> print(apprx(np.array([[0.5, 1, 0.25], [2, 0.5, 0.8], [0.6, 2, 1]])).extract_scedual() <= 1.2)
    True
    >>> print(apprx(np.array([[[1, 2, 3], [2, 5, 3],[1, 3, 7], [10, 3, 10]]])).extract_scedual() <= 6)
    True
    '''

    # bounds on solution via a greedy solution

    greedy_sol = scedual_makespan(output.costs)
    greedy(greedy_sol)

    upper = output.extract_scedual()
    lower = upper / output.costs.agents()

    del greedy_sol


    smallest_step = output.resolution

    while lower <= upper:

        middle = (upper + lower) / 2

        output.clear()
        feasable = LinearProgram(output)

        if not feasable:
            upper = middle
        else:
            lower = middle +smallest_step



def LinearProgram(output: scedual, deadlines: np.ndarray.astype(float), aprrx_bound: float) -> bool:


    ''' The linear program fassioned in the paper '''

    pass


def Round(output: scedual, fractional_sol: np.ndarray.astype(float)):

    ''' The rounding theorem for the LP's solution fassioned in the paper '''

    pass



def MinMakespan(algo: MinMakespanAlgo, input: ValuationMatrix, output: scedual, **kwargs):

    '''
    generic function for the min-makespan problome

    >>> print(MinMakespan(greedy, np.array([[1, 2, 2], [2, 2, 3],[5, 1, 5]], scedual_makespan()))
    3
    >>> print(MinMakespan(aprrx, np.array([[1, 2, 3], [2, 1, 3], [3, 2, 1]], scedual_makespan()))
    1
    '''

    output.build(input)
    algo(output, **kwargs)
    return output.extract_scedual()


def RandomTesting(algo: MinMakespanAlgo, output: scedual, iteration: int, **kwargs):

    '''spesefied amount of random tests generator'''

    mechines = randint(1, 500)
    jobs = randint(1, 500)

    for i in range(iteration):
        yield MinMakespan(algo, random(0, 3, (jobs, mechines)), output, **kwargs)



if __name__ == '__main__':

    import doctest
    doctest.testmod(verbose = True)