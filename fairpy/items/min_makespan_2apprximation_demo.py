""" 
A demo program for finding approximated min makespan schedule
for unrelated parallel machines.

Author: Israel-Yacobovich
Since:  2023-01
"""

from fairpy.items.min_makespan_2apprximation import min_makespan_2apprximation, logger
from fairpy import divide, ValuationMatrix
import numpy as np
import logging


logging_format = '%(levelname)s - %(message)s'
logging.basicConfig(level = logging.DEBUG, filename = 'pyproject.log', filemode = 'w', format = logging_format)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
formatter = logging.Formatter(logging_format)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


print('2 approximation min makespan', end = '\n\n')
print('the input for the algo is a matrix, rows for machines, columns for jobs\n')

input = ValuationMatrix([[7, 20, 7],
                        [20, 8, 6 ],
                        [30, 9, 12]])

print('classic input\n', input, '\nopt: 9\nresult:')
print(divide(min_makespan_2apprximation, input))


input = ValuationMatrix([[6, 2, 4],
                         [2, 1, 3],
                         [3, 2, 8]])

print('another input:\n', input, '\nopt: 4\nresult:')
print(divide(min_makespan_2apprximation, input))

print(divide(min_makespan_2apprximation, input))

print('deals well with dummy cases:\n')
print('indentity matrix, makespan:')
print(sum(divide(min_makespan_2apprximation, ValuationMatrix(np.eye(100))).utility_profile()))

print('1-matrix, utilty prophile:')
print(divide(min_makespan_2apprximation, ValuationMatrix(np.ones((10, 10)))).utility_profile(), '\n')

input = ValuationMatrix(np.random.uniform(1, 2, (10, 30)))
print('random 10x30 matrix, entries ~ U([1, 2]), \nmakespan:')
print(max(divide(min_makespan_2apprximation, input).utility_profile()))