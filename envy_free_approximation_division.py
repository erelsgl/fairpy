import doctest
import logging
import numpy as np
from fairpy import AllocationMatrix, Allocation, ValuationMatrix


def swap_columns(matrix: np.array, idx_1: int, idx_2: int) -> None:
    """
    >>> mat = np.array([[1,2,3],[4,5,6],[7,8,9]])
    >>> swap_columns(mat,0,2)
    >>> np.array_equal(mat, np.array([[3,2,1],[6,5,4],[9,8,7]]))
    True
    """
    logger.info('swap_columns( %s, %g , %g )', matrix, idx_1, idx_2)
    logger.debug('matrix before swap: %s', matrix)
    temp = np.copy(matrix[:, idx_1])
    matrix[:, idx_1] = matrix[:, idx_2]
    matrix[:, idx_2] = temp
    logger.debug('matrix after swap: %s', matrix)


def get_max(agent_valuation: np.array, payments: np.array) -> float:
    """
    >>> av = np.array([1.,2.,3.,4.])
    >>> p = np.array([2.,2.,1.,3.])
    >>> get_max(av,p)
    2.0
    >>> get_max(np.array([-1.,0.,2.,4.]),np.array([2.,-2.,-3.,1.5]))
    5.0
    """
    logger.info('get_max( %s, %s )', agent_valuation, payments)
    m = max(zip(agent_valuation, payments), key=lambda x: x[0] - x[1])
    logger.debug('get max (tuple): %s', m)
    return m[0] - m[1]


def get_argmax(agent_valuation: np.array, payments: np.array) -> int:
    """
    >>> get_argmax(np.array([1.,2.,3.,4.]),np.array([2.,2.,1.,3.]))
    2
    >>> get_argmax(np.array([-1.,2.,-3.,2.]),np.array([-5.,2.,1.,-1.]))
    0
    """
    logger.info('get_argmax( %s, %s )', agent_valuation, payments)
    return np.argmax([x[0] - x[1] for x in zip(agent_valuation, payments)])


def get_second_max(idx: int, agent_valuation: np.array, payments: np.array) -> float:
    """
    >>> get_second_max(2, np.array([1.,2.,3.,4.]),np.array([2.,2.,1.,3.]))
    1.0
    >>> get_second_max(0, np.array([-1.,2.,-3.,2.]),np.array([-5.,2.,1.,-1.]))
    3.0
    """
    logger.info('get_second_max( %g, %s, %s )', idx, agent_valuation, payments)
    temp_a = agent_valuation[np.arange(len(agent_valuation)) != idx]
    temp_p = payments[np.arange(len(payments)) != idx]
    m = max(zip(temp_a, temp_p), key=lambda x: x[0] - x[1])
    logger.debug('get second max (tuple): %s', m)
    return m[0] - m[1]


def envy_free_approximation(a: Allocation) -> dict:
    """
    "Achieving Envy-freeness and Equitability with Monetary Transfers" by Haris Aziz (2021),
    https://ojs.aaai.org/index.php/AAAI/article/view/16645

    Algorithm 2: ε-envy-free approximation division with payment function (based on Bertsekas algorithm).

    Programmers: Noamya Shani, Eitan Shankolevski.
    >>> v = [[20,15,24,35],
    ...      [12,30,18,24],
    ...      [20,10,15,25],
    ...      [15,25,22,20]]
    >>> a = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    >>> envy_free_approximation(Allocation(agents = ValuationMatrix(v), bundles=AllocationMatrix(a)))
    {'bundles': [[3], [1], [0], [2]], 'payments': [11.0, 12.0, 5.0, 0.0]}
    >>> v2 = [[0,50,0,0],
    ...       [0,40,0,0],
    ...       [0,30,0,0],
    ...       [0,45,0,0]]
    >>> envy_free_approximation(Allocation(agents = ValuationMatrix(v2), bundles=AllocationMatrix(a)))
    {'bundles': [[1], [0], [2], [3]], 'payments': [50.0, 0.0, 0.0, 0.0]}
    >>> v3 = [[-5,20,10,25],
    ...      [15,-15,-12,-15],
    ...      [-10,12,9,-5],
    ...      [12,20,30,-10]]
    >>> envy_free_approximation(Allocation(agents = ValuationMatrix(v3), bundles=AllocationMatrix(a)))
    {'bundles': [[3], [0], [1], [2]], 'payments': [5.0, 27.0, 3.0, 0.0]}
    """
    value_matrix = a.utility_profile_matrix()
    payments = np.zeros(a.num_of_agents)
    bundles = [[i] for i in range(a.num_of_agents)]
    flag = True
    while flag:
        flag = False
        for i in range(len(value_matrix)):
            if value_matrix[i][i] - payments[i] < get_max(value_matrix[i], payments):
                agent_j = get_argmax(value_matrix[i], payments)
                u1 = get_max(value_matrix[i], payments)
                u2 = get_second_max(agent_j, value_matrix[i], payments)
                logger.debug("u1,u2: %g, %g", u1, u2)
                # replace payment value
                temp_p = payments[i]
                payments[i] = payments[agent_j] + (u1 - u2)
                payments[agent_j] = temp_p
                # replace bundles
                swap_columns(value_matrix, i, agent_j)
                temp = bundles[i]
                bundles[i] = bundles[agent_j]
                bundles[agent_j] = temp
                flag = True

    return {"bundles": bundles, "payments": payments.tolist()}


if __name__ == '__main__':
    logging.basicConfig(filename="ev.log", level=logging.INFO)
    logger = logging.getLogger("")
    # console = logging.StreamHandler()
    # logger.handlers = [console]
    # logger.setLevel(logging.INFO)
    v = [[20, 15, 24, 35], [12, 30, 18, 24], [20, 10, 15, 25], [15, 25, 22, 20]]
    a = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
    envy_free_approximation(Allocation(agents=ValuationMatrix(v), bundles=AllocationMatrix(a)))
    doctest.testmod()
