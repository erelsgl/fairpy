from typing import Callable
import numpy as np
from numpy.random import randint, random
from abc import ABC, abstractclassmethod

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


CostMatrix =   np.ndarray.astype(float)
ScedualMatrix = np.ndarray.astype(bool)


class scedual(ABC):

    ''' custom output class '''

    def __init__(self) -> None:
        super().__init__()

    # lazy initilization
    def build(self, cost_matrix: CostMatrix):

        # different algorithms can use an instance with the same cost matrix
        # flyweight desighn
        self.costs = cost_matrix
        self.assignments = np.zeros(cost_matrix.shape)


    @abstractclassmethod
    def scedual(self, mechine: int, job: int): pass

    @abstractclassmethod
    def extract_scedual(self): pass

class scedual_makespan(scedual):

    '''
    implementation that keeps track of the actuall makespan
    '''

    def scedual(self, nechine: int, job: int): pass
    def extract_scedual(self): pass

class scedual_assignment(scedual):

    '''
    implementation that keeps track of the assignment
    '''

    def scedual(self, nechine: int, job: int): pass
    def extract_scedual(self): pass
    


MinMakespanAlgo = Callable[[CostMatrix], scedual]


def greedy(input: CostMatrix) -> scedual:
    
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

    pass

def apprx(input: CostMatrix) -> scedual:

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
    
    pass


def MinMakespan(algo: MinMakespanAlgo, input: CostMatrix, output: scedual, **kwargs):

    '''
    generic function for the min-makespan problome

    >>> print(MinMakespan(greedy, np.array([[1, 2, 2], [2, 2, 3],[5, 1, 5]], scedual_makespan()))
    3
    >>> print(MinMakespan(aprrx, np.array([[1, 2, 3], [2, 1, 3], [3, 2, 1]], scedual_makespan()))
    1
    '''

    output.build(input)
    return algo(output, **kwargs).extract_scedual()


def RandomTesting(algo: MinMakespanAlgo, output: scedual, iteration: int, **kwargs):

    '''spesefied amount of random tests generator'''

    mechines = randint(1, 300)
    jobs = randint(mechines // 5, mechines * 5)

    for i in range(iteration):
        yield MinMakespan(algo, random(0, 3, (jobs, mechines)), output, **kwargs)



if __name__ == '__main__':

    import doctest
    doctest.testmod(verbose = True)