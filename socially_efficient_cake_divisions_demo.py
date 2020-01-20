"""
Demonstration of the socially efficient cake divisions

Programmer: Jonathan Diamant
Since: 2019-12
"""

def print_result(result, items, agents):
    num_of_players = len(result[0])
    for j in range(num_of_players):
        print("player {} starts at: {} and ends at {}".format(j, result[0][j], result[1][j]))

    print('\n')
    for j in range(num_of_players):
        print("player {}'s value of his item is {}".format(j, agents[j].eval(items[result[0][j]], items[result[1][j] + 1])))


from socially_efficient_cake_divisions import *
print("------first example------")
#the players
a = PiecewiseConstantAgent([0.25, 0.5, 0.25], name = "Alice")
b = PiecewiseConstantAgent([0.23, 0.7, 0.07], name= "Bob")
print("the players:")
print(a)
print(b)
agents = [a, b]
#get the items
items = discretization_procedure(agents, 0.2)
print("the items:")
print(items)
#each player's values to the items
for i in range(6):
    print("item {}: from {}, to {}: a's value {}, b's value {}\n".format(i, items[i], items[i + 1],a.eval(items[i], items[i + 1]), b.eval(items[i], items[i + 1])))
matrix = get_players_valuation(agents, items)

print('\n')
#divide the cake
x = discrete_utilitarian_welfare_approximation(matrix, items)
print(x)
print_result(x,items,agents)
print('\n')

print("------second example------")
#the player
a = PiecewiseConstantAgent([0.2, 0.4, 0.4], name="Alice")
print("the player:")
print(a)
agents = [a]
#get the items
items = discretization_procedure(agents, 0.2)
print("the items:")
print(items)
matrix = get_players_valuation(agents, items)
#divide the cake
x = discrete_utilitarian_welfare_approximation(matrix, items)
print(x)
print_result(x,items,agents)
print('\n')