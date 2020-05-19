from agents import *

import improve_ef4.improve_ef4_impl as impl
import logging
import sys

impl.logger.addHandler(logging.StreamHandler(sys.stdout))
impl.logger.setLevel(logging.INFO)

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

for agents in cases:
    algorithm = impl.Algorithm(agents)
    allocation = algorithm.main()

    print('\n', allocation)

    satisfaction = {}
    for slice, agent in allocation._slice_allocations.items():
        if agent not in satisfaction:
            satisfaction[agent] = 0
        satisfaction[agent] += agent.eval(slice.start, slice.end)

    for agent, sat in satisfaction.items():
        print('Agent {} satisfaction: {}'.format(agent.name(), str(sat)))

    print("--------------------------------------------------")
