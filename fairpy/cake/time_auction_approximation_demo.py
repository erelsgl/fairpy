#!python3

"""
Demonstration of the time auction algorithms.


Programmers: Naama Berman and Yonatan Lifshitz
Since: 2019-12
"""

from fairpy.agents import *
from fairpy.cake import time_auction_approximation

import logging, sys
logger = logging.getLogger(__name__)

time_auction_approximation.logger.addHandler(logging.StreamHandler(sys.stdout))
time_auction_approximation.logger.setLevel(logging.INFO)

# Alice has 2 desired intervals: 0..1 with value 100, 1..2 with value 1.
Alice = PiecewiseConstantAgent([100, 1], "Alice")
# Bob has 2 desired intervals: 0..1 with value 2, 1..2 with value 90.
Bob = PiecewiseConstantAgent([2, 90], "Bob")

print(Alice)
print(Bob)

print("\n### Preforming an auction with Alice and Bob where we cut the cake to equally sized pieces:")
print(time_auction_approximation.equally_sized_pieces([Alice, Bob], piece_size=0.5))

print("\n### Preforming an auction with Alice and Bob where we choose the pieces intervals:")
print(time_auction_approximation.discrete_setting([Alice, Bob], [(0.0, 1.0), (1.0, 2.0)]))

print("\n### Preforming an auction with Alice and Bob where the algorithm is choosing the pieces:")
print(time_auction_approximation.continuous_setting([Alice, Bob]))
