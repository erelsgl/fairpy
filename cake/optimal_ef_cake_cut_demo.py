#!python3
"""
Demonstration of optimal-envy-free-cake-cutting protocol.

Programmer: Tom Goldenberg
Since: 2020-06
"""

from fairpy.agents import *
from fairpy.cake import optimal_ef_cake_cut

import logging, sys

optimal_ef_cake_cut.logger.addHandler(logging.StreamHandler(sys.stdout))
optimal_ef_cake_cut.logger.setLevel(logging.INFO)

"""
Piecewise constant demo
"""

print('\n\nPiecewise constant demo')
alice = PiecewiseConstantAgent([5], name='alice')
bob = PiecewiseConstantAgent([5], name='bob')
print(alice)
print(bob)
print('Optimal Envy Free Cake Cut for Piecewise Constant agents: Alice and Bob is\n')
print(optimal_ef_cake_cut.opt_piecewise_constant([alice, bob]))

alice = PiecewiseConstantAgent([3], name='alice')
bob = PiecewiseConstantAgent([5], name='bob')
print(alice)
print(bob)
print('Optimal Envy Free Cake Cut for Piecewise Constant agents: Alice and Bob is\n')
print(optimal_ef_cake_cut.opt_piecewise_constant([alice, bob]))

alice = PiecewiseConstantAgent([0, 1, 0, 2, 0, 3], name='alice')
bob = PiecewiseConstantAgent([1, 0, 2, 0, 3, 0], name='bob')
print(alice)
print(bob)
print('Optimal Envy Free Cake Cut for Piecewise Constant agents: Alice and Bob is\n')
print(optimal_ef_cake_cut.opt_piecewise_constant([alice, bob]))

alice = PiecewiseConstantAgent([0, 1, 0, 2, 0, 3], name='alice')
bob = PiecewiseConstantAgent([1, 0, 2, 0, 3, 0], name='bob')
gin = PiecewiseConstantAgent([1, 1, 2, 2, 3, 3], name='gin')
print(alice)
print(bob)
print(gin)
print('Optimal Envy Free Cake Cut for Piecewise Constant agents: Alice, Bob and Gin is\n')
print(optimal_ef_cake_cut.opt_piecewise_constant([alice, bob, gin]))

alice = PiecewiseConstantAgent([15, 15, 0, 30, 30], name='alice')
bob = PiecewiseConstantAgent([0, 30, 30, 30, 0], name='bob')
gin = PiecewiseConstantAgent([10, 0, 30, 0, 60], name='gin')
print(alice)
print(bob)
print(gin)

print('Optimal Envy Free Cake Cut for Piecewise Constant agents: Alice, Bob and Gin is\n')
print(optimal_ef_cake_cut.opt_piecewise_constant([alice, bob, gin]))

print('Optimal Envy Free Cake Cut for Piecewise Constant agents: Alice and Bob is\n')
print(optimal_ef_cake_cut.opt_piecewise_constant([alice, bob]))

print('Optimal Envy Free Cake Cut for Piecewise Constant agents: Alice and Gin is\n')
print(optimal_ef_cake_cut.opt_piecewise_constant([alice, gin]))

print('Optimal Envy Free Cake Cut for Piecewise Constant agents: Bob and Gin is\n')
print(optimal_ef_cake_cut.opt_piecewise_constant([gin, bob]))


print('\n\nPiecewise Linear demo')

alice = PiecewiseLinearAgent([5], [0], name='alice')
bob = PiecewiseLinearAgent([5], [0], name='bob')
print(alice)
print(bob)


print('Optimal Envy Free Cake Cut for Piecewise Linear agents: Alice and Bob is\n')
print(optimal_ef_cake_cut.opt_piecewise_linear([alice, bob]))

alice = PiecewiseLinearAgent([5], [-1], name='alice')
bob = PiecewiseLinearAgent([5], [0], name='bob')
print(alice)
print(bob)


print('Optimal Envy Free Cake Cut for Piecewise Linear agents: Alice and Bob is\n')
print(optimal_ef_cake_cut.opt_piecewise_linear([alice, bob]))

alice = PiecewiseLinearAgent([5], [-1], name='alice')
bob = PiecewiseLinearAgent([5], [-1], name='bob')
print(alice)
print(bob)


print('Optimal Envy Free Cake Cut for Piecewise Linear agents: Alice and Bob is\n')
print(optimal_ef_cake_cut.opt_piecewise_linear([alice, bob]))

alice = PiecewiseLinearAgent([0, 1, 0, 2, 0, 3], [0, 0, 0, 0, 0, 0], name='alice')
bob = PiecewiseLinearAgent([1, 0, 2, 0, 3, 0], [0, 0, 0, 0, 0, 0], name='bob')
print(alice)
print(bob)


print('Optimal Envy Free Cake Cut for Piecewise Linear agents: Alice and Bob is\n')
print(optimal_ef_cake_cut.opt_piecewise_linear([alice, bob]))

alice = PiecewiseLinearAgent([11, 22, 33, 44], [1, 0, 3, -2], name="alice")
bob = PiecewiseLinearAgent([11, 22, 33, 44], [-1, 0, -3, 2], name="bob")
print(alice)
print(bob)


print('Optimal Envy Free Cake Cut for Piecewise Linear agents: Alice and Bob is\n')
print(optimal_ef_cake_cut.opt_piecewise_linear([alice, bob]))
