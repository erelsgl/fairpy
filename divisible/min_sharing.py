#!python3

"""
Functions for finding fair allocations.
"""

import datetime, cvxpy, numpy as np
from time_limit import time_limit, TimeoutException

from max_product import find_max_product_allocation, product_of_utilities
from fairpy.divisible.ValuationMatrix import ValuationMatrix
from fairpy.divisible.AllocationMatrix import AllocationMatrix


def find_allocation_with_min_sharing(problem, time_limit_in_seconds=999)->(str,float,int):
    start = datetime.datetime.now()
    try:
        with time_limit(time_limit_in_seconds):
            problem.find_allocation_with_min_shering()
            num_sharing = problem.min_sharing_number
            allocation_matrix = problem.min_sharing_allocation
            status = "OK" if num_sharing<len(problem.valuation) else "Bug"
            valuation_matrix = problem.valuation
            prod_of_utils = product_of_utilities(AllocationMatrix(allocation_matrix), ValuationMatrix(valuation_matrix))
    except TimeoutException:
        status = "TimeOut"
        prod_of_utils = num_sharing = -1
        allocation_matrix = []
    except cvxpy.error.SolverError:
        status = "SolverError"
        prod_of_utils = num_sharing = -1
        allocation_matrix = []
    except SystemError:
        status = "SystemError"
        prod_of_utils = num_sharing = -1
        allocation_matrix = []
    end = datetime.datetime.now()
    time_in_seconds = (end - start).total_seconds()
    return (status, time_in_seconds, num_sharing, allocation_matrix, prod_of_utils)


def find_max_product_allocation_and_sharing(valuation_matrix: np.ndarray, time_limit_in_seconds=999)->(str,float,int):
    start = datetime.datetime.now()
    try:
        with time_limit(time_limit_in_seconds):
            valuation_matrix = ValuationMatrix(valuation_matrix)
            allocation_matrix = find_max_product_allocation(valuation_matrix)
            num_sharing = allocation_matrix.num_of_sharings()
            prod_of_utils = product_of_utilities(allocation_matrix, valuation_matrix)
            allocation_matrix = allocation_matrix.z
            status = "OK"
    except TimeoutException:
        status = "TimeOut"
        prod_of_utils = num_sharing = -1
        allocation_matrix = []
    except cvxpy.error.SolverError:
        status = "SolverError"
        prod_of_utils = num_sharing = -1
        allocation_matrix = []
    except SystemError:
        status = "SystemError"
        prod_of_utils = num_sharing = -1
        allocation_matrix = []
    end = datetime.datetime.now()
    time_in_seconds = (end - start).total_seconds()
    return (status, time_in_seconds, num_sharing, allocation_matrix, prod_of_utils)



if __name__ == '__main__':
    import doctest
    (failures, tests) = doctest.testmod(report=True)
    print("{} failures, {} tests".format(failures, tests))
