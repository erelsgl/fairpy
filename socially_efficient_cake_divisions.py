"""
Implementation of an Approximation Algorithm for computing continuous
division of a cake among n agents in order to maximize the welfare.

Reference:

    Yonatan Aumann, Yair Dombb, Avinatan Hassidim (2012). "Computing socially-efficient cake divisions".
    Proceedings of AAMAS 2013, 343--350. Algorithms 1 and 2.

Programmer: Jonathan Diamant
Since: 2019-12
"""
from agents import *
import sys
def discretization_procedure(agents: List[Agent], epsilon):
    """
    reduce the continuous cake into a sequence of discrete items.
    the algorithm below receives a list of agents and a parameter epsilon,
    and produces a set of cut positions that partition the cake into a
    set of items. each item's value is epsilon by any player.
    :param agents: List of agents. assumption: for each agent: agent.eval(0, agent.cake_length()) == 1
    :param epsilon: A bound
    :return: A discrete approximation version of the cake

    example for one player:

    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> discretization_procedure([a], 0.2)
    [0, 0.8, 1.3, 1.7000000000000002, 2.2, 3]

    example for 2 players:

    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    >>> list = [a,b]
    >>> discretization_procedure(list, 0.2)
    [0, 0.8, 1.22, 1.5057142857142858, 1.7914285714285716, 2.3828571428571435, 3]
    """

    size_of_the_cake = max([agent.cake_length() for agent in agents])
    a = 0
    C = [0]
    condition = [agent.eval(a,size_of_the_cake) > epsilon for agent in agents]
    while any(condition):
        values = []
        for i in agents:
            x = i.mark(a, epsilon)
            if (x != None):
                values.append(x)
        b = min(values)
        C.append(b)
        a = b
        condition = [agent.eval(a, size_of_the_cake) > epsilon for agent in agents]
    C.append(size_of_the_cake)
    return C



def get_players_valuation(agents: List[Agent], c):
    """
    this function calculates for each player its valuation of a discrete cut of the cake.
    for each player, it calulates the valuation of each item.
    :param agents: list of players
    :param c: list of item, the discrete approximation version of the cake
    :return: a matrix with all the valuations

    note: the i row in the matrix represents the valuations of player i
    len(matrix[i]) == number of items
    matrix[i][j] == the value of item j according to player i

    """
    matrix = []
    for agent in agents:
        valuations = [agent.eval(c[i], c[i + 1]) for i in range(len(c) - 1)]
        matrix.append(valuations)
    return matrix

def aprox_v(s,t,k,matrix: List[List[float]]):
    """
    this function calculates the value of the items from s to t according to the valuation
    of player k.
    :param s: the left cut of the first item
    :param t: the right cut of the last item
    :param k: which player we relate to
    :param matrix: the valuations for each item according to all the players
    :return: the valuation of an items sequence

    note: the valuation of player i is a list l.
    len(l) == number of items
    l[j] == the value of item j according to player i
    """
    valuations = matrix[k]
    return sum(valuations[s:t+1])


def V(s,t, current_s, matrix : List[List[float]]):
    """
     this function calculates the sum
    of values that the other players to which the items s through t are assigned obtain from these
    items
    :param s: the first item in the sequence
    :param t: the last item in the sequence
    :param current_s: a list such that current_s[i] == which item {0,...,(num_of_items - 1)} holds player i
    :param matrix: all the valuations of the players
    :return: the sum presented above

    example:
    2 player, player 0 holds the 0, 1, 2 items, player 1 holds the 3, 4, 5 items
    we are looking for the value of items 0, 1, 2 (the sum of 1+2+3)

    >>> matrix = [[1,2,3,4,5,6], [4,5,1,2,3, 0]]
    >>> V(0,2,[0,3], matrix)
    6

    2 player, player 0 holds the 0, 1, 2 items, player 1 holds the 3, 4, 5 items
    we are looking for the value of items 1, 2, 3, 4 (the sum of 2+3+2+3)

    >>> matrix = [[1,2,3,4,5,6], [4,5,1,2,3, 0]]
    >>> V(1, 4, [0,3], matrix)
    10

    """
    sum = 0
    for i in range(s,t + 1):
        j = i
        while j >= 0:
            try:
                player_s = current_s.index(j)
                x = aprox_v(i, i, player_s, matrix)
                sum += x
                break
            except:
                j -= 1


    return sum
"""
def maximize_expression(t, num_of_players, S, T):
    max = -sys.maxint - 1
    k_tag = 0
    s_tag = 0
    for k in range(num_of_players):

        for s in range(t + 1):
            value = aprox_v(s, t, k, matrix) - 2*(aprox_v(S[k], T[k], k, matrix) + V(s,t,S,matrix))
            if (value > max):
                max = value
                k_tag = k
                s_tag = s
    return [max, k_tag, s_tag]


def  discrete_utilitarian_welfare_approximation(matrix: List[List[float]], items, agents: List[Agent]):


    :param matrix: row i is the valuations of player i of the items
    :param items: the cuts to create the items
    :param agents: list of the players
    :return:
    
    #we count the items from 0 so if there r 6 items, the first one is 0 and the last one is 5
    num_of_players = len(matrix)
    num_of_items = len(items) - 1
    S = [0] * num_of_players #i think that this is like current s
    T = [0] * num_of_players
    current_s = [0] * num_of_players #in the i'th cell there is the start of player i's start
    current_t = [0] * num_of_players

    for t in range(num_of_items):
        maximum = maximize_expression(t, num_of_players, S, T)
        while maximum[0] >= 0:
            S[maximum[1]] = maximum[2]
            T[maximum[1]] = t
            for i in range(num_of_players):
                if(S[i] >= maximum[2]):
                    S[i] = 0
                    T[i] = 0
            for i in range(num_of_players):
                if (S[i] < maximum[2] and maximum[2] <= T[i]):
                    T[i] = maximum[2] - 1

            maximum = maximize_expression(t, num_of_players, S, T)

    return [S,T]
"""


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
    a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    agents = [a, b]
    c = discretization_procedure(agents, 0.2)
    #for i in range(6):
    #    print("part {}: {},{}: a {}, b {}\n".format(i, c[i], c[i + 1],a.eval(c[i], c[i + 1]), b.eval(c[i], c[i + 1])))
    matrix = get_players_valuation(agents, c)
    d = discretization_procedure([a], 0.2)
    print(d)


    print(c)
    print('\n')
    print(aprox_v(0,5,0,matrix)) #all items
    print(aprox_v(0,0, 0, matrix))#just the first item
    print('\n')
    matrix = [[1,2,3,4,5,6], [4,5,1,2,3, 0]]
    print(V(0,2,[0,3], matrix)) #a holds 0, 1, 2 b holds 3, 4, 5 and we wamd the value of 1+2+3+4
    print('\n')