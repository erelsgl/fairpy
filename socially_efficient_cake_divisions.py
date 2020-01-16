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
import logging
logging.getLogger().setLevel(logging.INFO)
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
    #the partition:
    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    >>> agents = [a, b]
    >>> c = discretization_procedure(agents, 0.2)
    >>> [round(i,3) for i in discretization_procedure(agents, 0.2)]
    [0, 0.8, 1.22, 1.506, 1.791, 2.383, 3]
    >>> [round(i,3) for i in get_players_valuation(agents, c)[0]]
    [0.2, 0.16, 0.143, 0.143, 0.2, 0.154]
    >>> [round(i,3) for i in get_players_valuation(agents, c)[1]]
    [0.184, 0.2, 0.2, 0.2, 0.173, 0.043]
    """


    matrix = []
    for agent in agents:
        #found out that if I round agent.eval I get different outputs from the algorithm
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

    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    >>> agents = [a, b]
    >>> c = discretization_procedure(agents, 0.2)
    >>> matrix = get_players_valuation(agents, c)
    >>> aprox_v(0,5,0,matrix) #all the items according to player 0
    1.0
    >>> aprox_v(0,0,0,matrix) #the first item according to player 0
    0.2
    >>> round(aprox_v(0,1,1,matrix),3) #the first and the second items according to player 1 -> = 0.18400000000000002 + 0.20000000000000007
    0.384

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

    for example:
    if the matrix is [[1,2,3,4,5,6], [4,5,1,2,3, 0]]
    current_s is [0,3]
    current_t is [2,5]
    s is 0
    t is 3
    and k is 1
    that means that agent 0 holds items 0,1,2 (and their values are 1,2,3)
    agent 1 holds items 3,4,5 (and their values are 2,3,0)
    so we want the value of items 0,1,2,3 without what player 1 holds
    that means items 1,2,3 so the sum is 1+2+3 = 6

    >>> matrix = [[1,2,3,4,5,6], [4,5,1,2,3, 0]]
    >>> V(0,3,[0,3], [2,5], matrix, 1)
    6


    #2 items, 0 and 1, player 0 holds item 0, player 1 holds item 1 and we calculate the value of items 0 and 1 according to player 0
    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    >>> agents = [a, b]
    >>> c = discretization_procedure(agents, 0.2)
    >>> matrix = get_players_valuation(agents, c)
    >>> round(V(0,1,[0,1],[0,1],matrix,0),3) #2 items, 0 and 1, player 0 holds item 0, player 1 holds item 1 and we calculate the value of items
    0.2

    """



    sum = 0
    for i in range(s, t + 1):
        for j in range(len(matrix)):
            if (i <= current_t[j] and i >= current_s[j]):
                if (j != k):
                    sum += matrix[j][i]
    return sum


def maximize_expression(t, num_of_players, S, T, matrix):
    """
    ***I think that the problem might be here***
    this function maximizes the expression:
    aprox_v(s, t, k, matrix) - 2*(aprox_v(S[k], T[k], k, matrix) + V(s,t,S,matrix))

    :param t: the last item
    :param num_of_players: number of players
    :param S: a list such that S[i] == which item {0,...,(num_of_items - 1)} is the first item of player i
    :param T: a list such that T[i] == which item {0,...,(num_of_items - 1)} is the last item of player i
    :param matrix: all the valuations of the players
    :return: params k' and s' that maximize the expression

    #I dont have doctest because I dont know what the output should be
    """
    max = -sys.maxsize - 1
    k_tag = 0
    s_tag = 0
    for k in range(num_of_players):
        for s in range(t + 1):
            #the value of items s to t according to player k
            v1 = aprox_v(s,t,k,matrix)
            #the value of items player k currently own
            v2 = aprox_v(S[k], T[k], k, matrix)
            #the value of  all the parts from s to t that other players than k obtain
            v3 = V(s,t,S,T,matrix, k)
            #value = aprox_v(s, t, k, matrix) - 2*(aprox_v(S[k], T[k], k, matrix) + V(s,t,S,matrix))
            value = v1 - 2 * (v2 + v3)
            logging.info("in maximize_expression: v1: %f, v2: %f, v3: %f, s: %f, t: %f, k: %f\n", v1, v2, v3, s, t, k)
            if (value > max):
                max = value
                k_tag = k
                s_tag = s
    return [max, k_tag, s_tag]


def  discrete_utilitarian_welfare_approximation(matrix: List[List[float]], items):

    """
    :param matrix: row i is the valuations of player i of the items
    :param items: the cuts to create the items
    :return: [S,T] s.t.
    S is a list such that S[i] == which item {0,...,(num_of_items - 1)} is the first item of player i
    and T is a list such that current_t[i] == which item {0,...,(num_of_items - 1)} is the last item of player i
    """
    
    #we count the items from 0 so if there are 6 items, the first one is 0 and the last one is 5
    num_of_players = len(matrix)
    num_of_items = len(items) - 1
    S = [-1] * num_of_players #i think that this is like current s in the i'th cell there is the start of player i's start
    T = [-1] * num_of_players


    """
    the main loop.
    till t is less or equals to 3 everything is ok. where t equals 4 or more the maximize expression returns result
    smaller than 0.
    when t is 4 or more, the values of player 0 are bigger than those of player 1.
    when t is between 1 and 3 the values of player 1 are bigger than those of player 0.
    when t equals 0 (the first item), the value of player 0 is bigger than the value of player 1,
    """
    for t in range(0, num_of_items):
        logging.info("%d iteration",t)
        maximum = maximize_expression(t, num_of_players, S, T, matrix)
        logging.info("maximize values: maximum: %f, k': %f, s': %f\n", maximum[0], maximum[1], maximum[2])
        while maximum[0] >= 0:
            k_tag = maximum[1]
            s_tag = maximum[2]
            #S[k_tag] = s_tag
            #T[k_tag] = t
            for i in range(num_of_players):
                #if its equal it will put minus one in S[k_tag]
                if(S[i] >= s_tag):
                    S[i] = -1
                    T[i] = -1
            S[k_tag] = s_tag
            T[k_tag] = t
            for i in range(num_of_players):
                if (S[i] < s_tag and s_tag <= T[i]):
                    T[i] = s_tag - 1

            maximum = maximize_expression(t, num_of_players, S, T, matrix)

    return [S,T]



if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
    """
    my example. 
    the items are [0, 0.8, 1.22, 1.5057142857142858, 1.7914285714285716, 2.3828571428571435, 3]
    where 0 to 0.8 is item 0, 0.8 to 1.22 is item 1 and so on...
    there are 6 items, from 0 to 5.
    my code outputs [[0,1],[0,3]]
    that means that player 0 holds item 0 and player 1 holds items 1,2,3
    i think that the correct output is [[0,1],[0,5]]
    """
    a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    agents = [a, b]
    c = discretization_procedure(agents, 0.2)
    for i in range(6):
        print("part {}: {},{}: a {}, b {}\n".format(i, c[i], c[i + 1],a.eval(c[i], c[i + 1]), b.eval(c[i], c[i + 1])))
    matrix = get_players_valuation(agents, c)


    print(c)
    print('\n')
    #the problem is here
    x = discrete_utilitarian_welfare_approximation(matrix, c)
    print(x)
    print(agents[0].eval(c[0], c[1]))
    print(agents[1].eval(c[1], c[4]))

