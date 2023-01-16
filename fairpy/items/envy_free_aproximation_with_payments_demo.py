from fairpy import ValuationMatrix
from fairpy.items.envy_free_approximation_with_payments import find_envy_free_approximation_with_payments, logger
import logging
import sys

logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

valuation_matrix = ValuationMatrix([[1, 2, 5],
                                    [0, 6, 3],
                                    [5, 7, 4]])

print("Envy-free_approximation Algorithm starting..\n")
results = find_envy_free_approximation_with_payments(v=valuation_matrix, eps=0.01)
allocation = results["allocation"]
payments = results["payments"]
i = 0
for a, p, v in zip(allocation, payments, valuation_matrix):
    print(f'agent #{i} get bundle {a} with valuation {v[a[0]]} and pay {p}')
    i += 1
