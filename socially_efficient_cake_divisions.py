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

    >>> a = PiecewiseConstantAgent([0.2, 0.4, 0.4])
    >>> discretization_procedure([a], 0.2)
    [0, 1.0, 1.5, 2.0, 2.5, 3]

    example for 2 players:

    >>> a = PiecewiseConstantAgent([0.2, 0.3, 0.5])
    >>> b = PiecewiseConstantAgent([0.3, 0.4, 0.3])
    >>> list = [a,b]
    >>> discretization_procedure(list, 0.2)
    [0, 0.6666666666666667, 1.25, 1.75, 2.25, 2.65, 3]
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
    if (s == -1):
        return 0
    valuations = matrix[k]
    return sum(valuations[s:t+1])


def V(s,t, current_s, current_t, matrix : List[List[float]], k):
    """
     this function calculates the sum
    of values that the other players to which the items s through t are assigned obtain from these
    items
    :param s: the first item in the sequence
    :param t: the last item in the sequence
    :param current_s: a list such that current_s[i] == which item {0,...,(num_of_items - 1)} is the first item of player i
    :param current_t: a list such that current_t[i] == which item {0,...,(num_of_items - 1)} is the last item of player i
    :param matrix: all the valuations of the players
    :param k: the player
    :return: the sum presented above



    """



    sum = 0
    for i in range(s, t + 1):
        for j in range(len(matrix)):
            if (i <= current_t[j] and i >= current_s[j]):
                if (j != k):
                    sum += matrix[j][i]
    return sum


def maximize_expression(t, num_of_players, S, T, matrix):
    max = -sys.maxsize - 1
    k_tag = 0
    s_tag = 0
    for k in range(num_of_players):
        for s in range(t + 1):
            v1 = aprox_v(s,t,k,matrix)
            v2 = aprox_v(S[k], T[k], k, matrix)
            #i think that this needs to be all the parts from s to t that other players than k obtain
            v3 = V(s,t,S,T,matrix, k)
            #value = aprox_v(s, t, k, matrix) - 2*(aprox_v(S[k], T[k], k, matrix) + V(s,t,S,matrix))
            value = v1 - 2 * (v2 + v3)
            if (value > max):
                max = value
                k_tag = k
                s_tag = s
    return [max, k_tag, s_tag]


def  discrete_utilitarian_welfare_approximation(matrix: List[List[float]], items, agents: List[Agent]):

    """
    :param matrix: row i is the valuations of player i of the items
    :param items: the cuts to create the items
    :param agents: list of the players
    :return:
    """
    
    #we count the items from 0 so if there are 6 items, the first one is 0 and the last one is 5
    num_of_players = len(matrix)
    num_of_items = len(items) - 1
    S = [-1] * num_of_players #i think that this is like current s in the i'th cell there is the start of player i's start
    T = [-1] * num_of_players

    for t in range(0, num_of_items):
        maximum = maximize_expression(t, num_of_players, S, T, matrix)
        while maximum[0] >= 0:
            k_tag = maximum[1]
            s_tag = maximum[2]
            S[k_tag] = s_tag
            T[k_tag] = t
            for i in range(num_of_players):
                #if its equal it will put minus one in S[k_tag]
                if(S[i] > s_tag):
                    S[i] = -1
                    T[i] = -1
            for i in range(num_of_players):
                if (S[i] < s_tag and s_tag <= T[i]):
                    T[i] = s_tag - 1

            maximum = maximize_expression(t, num_of_players, S, T, matrix)

    return [S,T]



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
    a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    agents = [a, b]
    c = discretization_procedure(agents, 0.2)
    for i in range(6):
        print("part {}: {},{}: a {}, b {}\n".format(i, c[i], c[i + 1],a.eval(c[i], c[i + 1]), b.eval(c[i], c[i + 1])))
    matrix = get_players_valuation(agents, c)
    d = discretization_procedure([a], 0.2)
    print(d)


    print(c)
    print('\n')
    print(aprox_v(0,5,0,matrix)) #all items
    print(aprox_v(0,0, 0, matrix))#just the first item
    print('\n')
    matrix = [[1,2,3,4,5,6], [4,5,1,2,3, 0]]
    print(V(0,2,[0,3], [2,5], matrix, 1)) #a holds 0, 1, 2 b holds 3, 4, 5 and we wamd the value of 1+2+3+4
    print('\n')
    matrix = get_players_valuation(agents, c)
    print(c)
    x = discrete_utilitarian_welfare_approximation(matrix, c, agents)
    print(x)
    print(agents[0].eval(c[0], c[1]))
    print(agents[1].eval(c[1], c[4]))

    #print('\n')
    #a = PiecewiseConstantAgent([0.2, 0.3, 0.5])
    #b = PiecewiseConstantAgent([0.3, 0.4, 0.3])
    #agents = [a, b]
    #c = discretization_procedure(agents, 0.2)
    #for i in range(6):
    #    print("part {}: {},{}: a {}, b {}\n".format(i, c[i], c[i + 1], a.eval(c[i], c[i + 1]), b.eval(c[i], c[i + 1])))

    #print(c)

    #a = PiecewiseConstantAgent([0.2, 0.4, 0.4])
    #c = discretization_procedure([a], 0.2)
    #print(c)
