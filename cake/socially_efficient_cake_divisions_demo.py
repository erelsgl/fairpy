#!python3
"""
Demonstration of the socially efficient cake divisions

Programmer: Jonathan Diamant
Since: 2019-12
"""

from fairpy.agents import *
from fairpy.cake import socially_efficient_cake_divisions

import logging, sys

socially_efficient_cake_divisions.logger.addHandler(logging.StreamHandler(sys.stdout))
socially_efficient_cake_divisions.logger.setLevel(logging.INFO)




def print_result(result, items, agents):
    num_of_players = len(result[0])
    for j in range(num_of_players):
        print("player {} starts at: {} and ends at {}".format(j, result[0][j], result[1][j]))

    print('\n')
    for j in range(num_of_players):
        print("player {}'s value of his item is {}".format(j, agents[j].eval(items[result[0][j]], items[result[1][j] + 1])))


def demo_of_subroutines():
    print("------first example------")
    print("2 players and a part of the cake (2 items) remains unallocated")
    a = PiecewiseConstantAgent([0.25, 0.5, 0.25], name = "Alice")
    b = PiecewiseConstantAgent([0.23, 0.7, 0.07], name= "Bob")
    agents = [a,b]
    print("the players:", a, b)
    items = socially_efficient_cake_divisions.discretization_procedure([a, b], 0.2)
    print("the items:", items)
    #each player's values to the items
    for i in range(6):
        print("item {}: from {}, to {}: a's value {}, b's value {}\n".format(i, items[i], items[i + 1],a.eval(items[i], items[i + 1]), b.eval(items[i], items[i + 1])))
    matrix = socially_efficient_cake_divisions.get_players_valuation(agents, items)

    print('\n')
    #divide the cake
    x = socially_efficient_cake_divisions.discrete_utilitarian_welfare_approximation(matrix, items)
    print(x)
    print_result(x,items,agents)
    print('\n')

    print("------second example------")
    print("1 player and a part of the cake (1 item) remains unallocated")
    #the player
    a = PiecewiseConstantAgent([0.2, 0.4, 0.4], name="Alice")
    print("the player:")
    print(a)
    agents = [a]
    #get the items
    items = socially_efficient_cake_divisions.discretization_procedure(agents, 0.2)
    print("the items:")
    print(items)
    matrix = socially_efficient_cake_divisions.get_players_valuation(agents, items)
    #divide the cake
    x = socially_efficient_cake_divisions.discrete_utilitarian_welfare_approximation(matrix, items)
    print(x)
    print_result(x,items,agents)
    print('\n')




Alice = PiecewiseConstantAgent([0.25, 0.5, 0.25], name = "Alice")
Bob = PiecewiseConstantAgent([0.23, 0.7, 0.07], name= "Bob")
print(Alice, "\n", Bob)
print("\nepsilon 0.2")
print(socially_efficient_cake_divisions.divide([Alice, Bob], epsilon=0.2))
print("\nepsilon 0.1")
print(socially_efficient_cake_divisions.divide([Alice, Bob], epsilon=0.1))
print("\nepsilon 0.01")
print(socially_efficient_cake_divisions.divide([Alice, Bob], epsilon=0.01))


print("\nNew agents")

Alice = PiecewiseConstantAgent([1/4, 1/4, 1/4, 1/4], name = "Alice")
Bob = PiecewiseConstantAgent([1/8, 1/8, 3/8, 1/2], name= "Bob")
print(Alice, "\n", Bob)
print("\nOrder Alice-Bob")
print(socially_efficient_cake_divisions.divide([Alice, Bob], epsilon=1/8))
print("\nOrder Bob-Alice")
print(socially_efficient_cake_divisions.divide([Bob, Alice], epsilon=1/8))

print("\nDebug mode")
socially_efficient_cake_divisions.logger.setLevel(logging.DEBUG)
print(socially_efficient_cake_divisions.divide([Bob, Alice], epsilon=1/4))
