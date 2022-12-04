from typing import List, Any

from fairpy import AllocationMatrix, Allocation, ValuationMatrix


def envy_free_approximation(a:Allocation) -> List[List[Any]]:
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
    >>> envy_free_approximation(Allocation(agents = ValuationMatrix(v), bundles=AllocationMatrix(a))
    {"items":[[3],[1],[0],[2]],"payments":[[10],[12],[5],[0]]}
    >>> v2 = [[0,50,0,0],
    ...       [0,40,0,0],
    ...       [0,30,0,0],
    ...       [0,45,0,0]]
    >>> envy_free_approximation(Allocation(agents = ValuationMatrix(v2), bundles=AllocationMatrix(a))
    {"items":[[1],[0],[2],[3]],"payments":[[50],[0],[0],[0]]}
    >>> v3 = [[-5,20,10,25],
    ...      [15,-15,-12,-15],
    ...      [-10,12,9,-5],
    ...      [12,20,30,-10]]
    >>> envy_free_approximation(Allocation(agents = ValuationMatrix(v3), bundles=AllocationMatrix(a))
    {"items":[[3],[0],[1],[2]],"payments":[[5],[27],[3],[0]]}
    """
    pass
