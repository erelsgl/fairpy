#!python3
import logging
import sys

from fairpy.cake import improve_ef4
from fairpy.agents import PiecewiseConstantAgent
from fairpy.cake.pieces import round_allocation

cases = [
    [
        PiecewiseConstantAgent([3, 6, 3], "agent1"),
        PiecewiseConstantAgent([0, 2, 4], "agent2"),
        PiecewiseConstantAgent([6, 4, 2], "agent3"),
        PiecewiseConstantAgent([3, 3, 3], "agent4")
    ],
    [
        PiecewiseConstantAgent([4, 3, 5], "agent1"),
        PiecewiseConstantAgent([2, 3, 3], "agent2"),
        PiecewiseConstantAgent([5, 11, 6], "agent3"),
        PiecewiseConstantAgent([4, 3, 5], "agent4")
    ],
    [
        PiecewiseConstantAgent([22, 33, 66], "test1"),
        PiecewiseConstantAgent([22, 33, 33], "test2"),
        PiecewiseConstantAgent([12, 13, 21], "test3"),
        PiecewiseConstantAgent([12, 13, 15], "test4")
    ],
    [
        PiecewiseConstantAgent([22, 33, 66], "test1"),
        PiecewiseConstantAgent([22, 33, 33], "test2"),
        PiecewiseConstantAgent([12, 13, 21], "test3"),
        PiecewiseConstantAgent([12, 13, 15], "test4")
    ]
]

improve_ef4.logger.addHandler(logging.StreamHandler(sys.stdout))
# improve_ef4.logger.setLevel(logging.INFO)

for agents in cases:
    allocation = improve_ef4.improve_ef4_protocol(agents)
    allocation = round_allocation(allocation)

    print()
    print(allocation)
    print("--------------------------------------------------")
