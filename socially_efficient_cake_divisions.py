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
import cvxpy as cp

def discretization_procedure(agents: List[Agent], epsilone):
    """

    :param agents: List of agents. assumption: for each agent: agent.eval(0, agent.cake_length()) == 1
    :param epsilone: A bound
    :return: A discrete approximation version of the cake

    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    >>> list = [a,b]
    >>> discretization_procedure(list, 0.2)
    [0, 0.8, 1.22, 1.5057142857142858, 1.7914285714285716, 2.3828571428571435, 3]
    """
    size_of_the_cake = max([agent.cake_length() for agent in agents])
    a = 0
    C = [0]
    condition = [agent.eval(a,size_of_the_cake) > epsilone for agent in agents]
    while any(condition):
        values = []
        for i in agents:
            x = i.mark(a, epsilone)
            if (x != None):
                values.append(x)
        b = min(values)
        C.append(b)
        a = b
        condition = [agent.eval(a, size_of_the_cake) > epsilone for agent in agents]
    C.append(size_of_the_cake)
    return C

def aprox_v(s,t,k,matrix):
    valuations = matrix[k]
    return sum(valuations[s:t+1])
def V(s,t, current_s, matrix):
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

def maximize_expression(t, num_of_players, S, T):
    max = 0
    k_tag = 0
    s_tag = 0
    for k in range(num_of_players):
        for s in range(t):
            value = aprox_v(s, t, k, matrix) - 2*(aprox_v(S[k], T[k], k, matrix) + V(s,t,S,matrix))
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
    #we count the items from 0 so if there r 6 items, the first one is 0 and the last one is 5
    num_of_players = len(matrix)
    num_of_items = len(items)
    S = [0] * num_of_players #i think that this is like current s
    T = [0] * num_of_players
    current_s = [0] * num_of_players #in the i'th cell there is the start of player i's start
    current_t = [0] * num_of_players

    for t in range(num_of_items):
        maximum = maximize_expression(t, num_of_players, S, T)
        while maximum[0] >= 0:
            maximum = maximize_expression(t, num_of_players, S, T)
            S[maximum[1]] = maximum[2]
            T[maximum[1]] = t
            for i in range(num_of_players):
                if(S[i] >= maximum[2]):
                    S[i] = 0
                    T[i] = 0
            for i in range(num_of_players):
                if (S[i] < maximum[2] and maximum[2] <= T[i]):
                    T[i] = maximum[2] - 1

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
    matrix = []
    for agent in agents:
        valuations = [agent.eval(c[i], c[i+1]) for i in range(len(c) - 1)]
        matrix.append(valuations)


    print(c)
    print('\n')
    print(aprox_v(0,5,0,matrix)) #all items
    print(aprox_v(0,0, 0, matrix))#just the first item
    print('\n')
    print(V(1,4,[0,3], matrix)) #a holds 0, 1, 2 b holds 3, 4, 5 and we wamd the value of 1+2+3+4
    print('\n')
    discrete_utilitarian_welfare_approximation(matrix, c, agents)