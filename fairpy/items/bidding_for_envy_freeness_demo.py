'''
Demonstration of the Bidding for Envy Freeness algorithm.

Programmers: Barak Amram, Adi Dahari.
Since: 2023-01
'''

import fairpy
from fairpy.items.bidding_for_envy_freeness import bidding_for_envy_freeness


# Example from article:
matrix1 = [[50, 20, 10, 20], [60, 40, 15, 10], [0, 40, 25, 35], [50, 35, 10, 30]]

print(fairpy.divide(bidding_for_envy_freeness, matrix1))

# Simple example:
matrix2 = [[50, 40, 35], [25, 25, 25], [10, 20, 25]]

print(fairpy.divide(bidding_for_envy_freeness, matrix2))