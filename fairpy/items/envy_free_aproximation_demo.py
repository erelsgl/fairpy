from fairpy import ValuationMatrix
from envy_free_approximation import find_envy_free_approximation
from fairpy.items import envy_free_approximation
import logging
import sys

envy_free_approximation.logger.addHandler(logging.StreamHandler(sys.stdout))
envy_free_approximation.logger.setLevel(logging.INFO)

valuation_matrix = ValuationMatrix([[1, 2, 5],
                                    [0, 6, 3],
                                    [5, 7, 4]])

print("Envy-free_approximation Algorithm starting..\n")
results = find_envy_free_approximation(v=valuation_matrix, eps=0.01)
allocation = results["allocation"]
payments = results["payments"]
i = 0
for a, p, v in zip(allocation, payments, valuation_matrix):
    print(f'agent #{i} get bundle {a} with valuation {v[a[0]]} and pay {p}')
    i += 1
