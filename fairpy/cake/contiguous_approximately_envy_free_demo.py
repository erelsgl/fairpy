#!python3

"""
Demonstration of "Contiguous Cake Cutting: Hardness Results and Approximation Algorithms".

Programmer: Shalev Goldshtein

Since: 2020-03
"""

from fairpy.agents import *
from fairpy.cake import contiguous_approximately_envy_free

import logging, sys

contiguous_approximately_envy_free.logger.addHandler(logging.StreamHandler(sys.stdout))
contiguous_approximately_envy_free.logger.setLevel(logging.INFO)


print("\n### Example 1: \n")
Erel = PiecewiseConstantAgentNormalized([2, 8, 2], name="Erel")
Shalev = PiecewiseConstantAgentNormalized([4, 2, 6], name="Shalev")
lstES = [Erel,Shalev]
print(Erel)
print(Shalev)
print()

print(contiguous_approximately_envy_free.algor1(lstES))



#################################################################################################


print("\n### Example 2: \n")
ALICE = PiecewiseConstantAgentNormalized([11, 22, 33, 44], "ALICE")
BOB = PiecewiseConstantAgentNormalized([7, 13, 51, 12], "BOB")
CHARLIE = PiecewiseConstantAgentNormalized([60, 31, 18, 3], "CHARLIE")
DANY = PiecewiseConstantAgentNormalized([4, 10, 43, 63], "DANY")
lstABCD = [ALICE, BOB, CHARLIE, DANY]
print(ALICE)
print(BOB)
print(CHARLIE)
print(DANY)
print()

print(contiguous_approximately_envy_free.algor1(lstABCD))


# the cake for example 2

# 0.0           0.15                            0.55                 0.77               1.0
#  ---------------------------------------------------------------------------------------
#  |             |                               |                     |                 |
#  |             |                               |                     |                 |
#  |             |                               |                     |                 |
#  |   CHARLIE   |              BOB              |         DANY        |      ALICE      |
#  |             |                               |                     |                 |
#  |             |                               |                     |                 |
#  |             |                               |                     |                 |
#  |             |                               |                     |                 |
#  ---------------------------------------------------------------------------------------


####################################################################################################


print("\n### Example 3: \n")

BEN = PiecewiseConstantAgentNormalized([4, 10, 20], name="BEN")
GUR = PiecewiseConstantAgentNormalized([14, 42, 9, 17], name="GUR")
ION = PiecewiseConstantAgentNormalized([30, 1, 12], name="ION")
lstaaa = [BEN,GUR,ION]

print(BEN)
print(GUR)
print(ION)
print()

print(contiguous_approximately_envy_free.algor1(lstaaa))
