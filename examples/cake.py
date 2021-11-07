#!python3

"""
The fairpy library is a library of data structures and algorithms for fair division.
Its primary design goal is ease of use for both users of existing algorithms,
and developers of new algorithms.

This demo shows how to use cake-cutting algorithms in fairpy.
First, let us define some agents.
"""

from fairpy.cake.valuations import PiecewiseConstantValuation
from fairpy.agents import PiecewiseUniformAgent, PiecewiseConstantAgent, agents_from

Alice = PiecewiseUniformAgent ([(0,1),(3,6)], name="Alice")   # Alice has two desired intervals, 0..1 and 3..6. Each interval has value 1.
George = PiecewiseConstantAgent([1,3,5,7],    name="George")  # George has four desired intervals: 0..1 with value 1, 1..2 with value 3, etc.
print(Alice)
print(George)

"""
Now, we can let our agents play 'cut and choose'.
"""

from fairpy.cake import cut_and_choose

print("\n--- CUT AND CHOOSE ---")
print("\n### Alice cuts and George chooses:")
print(cut_and_choose.asymmetric_protocol([Alice, George]))

"""
To better understand what is going on, we can use logging:
"""

import logging, sys
cut_and_choose.logger.addHandler(logging.StreamHandler(sys.stdout))
cut_and_choose.logger.setLevel(logging.INFO)

print(cut_and_choose.asymmetric_protocol([Alice, George]))
print(cut_and_choose.asymmetric_protocol([George, Alice]))

print("\n### Symmetric protocol:")
print(cut_and_choose.symmetric_protocol([Alice, George]))

"""
Here is an algorithm for more than two agents:
"""
from fairpy.cake import last_diminisher

last_diminisher.logger.addHandler(logging.StreamHandler(sys.stdout))
last_diminisher.logger.setLevel(logging.INFO)

print("\n--- LAST DIMINISHER ---")
print(last_diminisher.last_diminisher(agents_from([
    PiecewiseConstantValuation([1,3,5,7]), 
    PiecewiseConstantValuation([7,5,3,1]),
    PiecewiseConstantValuation([4,4,4,4]),
    PiecewiseConstantValuation([16,0,0,0]),
    ])))

