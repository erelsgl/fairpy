#!python3
"""
Implementation of an Approximation Algorithm for computing continuous
division of a cake among n agents in order to maximize the welfare.

Reference:

    Yonatan Aumann, Yair Dombb, Avinatan Hassidim (2012). "Computing socially-efficient cake divisions".
    Proceedings of AAMAS 2013, 343--350. Algorithms 1 and 2.

Programmer: Jonathan Diamant
Since: 2019-12
"""

from fairpy import Allocation
from fairpy.cake.pieces import round_allocation
from fairpy.agents import Agent
from typing import List

import sys, logging
logger = logging.getLogger(__name__)

def discretization_procedure(agents: List[Agent], epsilon:float):
    """
    reduce the continuous cake into a sequence of discrete items.
    the algorithm below receives a list of agents and a parameter epsilon,
    and produces a set of cut positions that partition the cake into a
    set of items. each item's value is epsilon by any player.
    :param agents: List of agents. assumption: for each agent: agent.eval(0, agent.cake_length()) == 1
    :param epsilon: A bound
    :return: A discrete approximation version of the cake

    example for one player:

    >>> from fairpy.agents import PiecewiseConstantAgent
    >>> a = PiecewiseConstantAgent([0.2, 0.4, 0.4])
    >>> discretization_procedure([a], 0.2)
    [0, 1.0, 1.5, 2.0, 2.5, 3]

    example for 2 players:

    >>> a = PiecewiseConstantAgent([0.2, 0.3, 0.5])
    >>> b = PiecewiseConstantAgent([0.3, 0.4, 0.3])
    >>> list = [a,b]
    >>> [round(i,3) for i in discretization_procedure(list, 0.2)]
    [0, 0.667, 1.25, 1.75, 2.25, 2.65, 3]
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



def get_players_valuation(agents: List[Agent], c : List[float]):
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
    >>> from fairpy.agents import PiecewiseConstantAgent
    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    >>> agents = [a, b]
    >>> c = [0, 0.8, 1.22, 1.506, 1.791, 2.383, 3]
    >>> [round(i,3) for i in get_players_valuation(agents, c)[0]]
    [0.2, 0.16, 0.143, 0.142, 0.2, 0.154]
    >>> [round(i,3) for i in get_players_valuation(agents, c)[1]]
    [0.184, 0.2, 0.2, 0.199, 0.173, 0.043]

    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> b = PiecewiseConstantAgent([0.3, 0.5, 0.2])
    >>> c = [0,1,2,3]
    >>> get_players_valuation(agents, c)[0]
    [0.25, 0.5, 0.25]
    >>> get_players_valuation(agents, c)[1]
    [0.23, 0.7, 0.07]
    """


    matrix = []
    for agent in agents:
        valuations = [agent.eval(c[i], c[i + 1]) for i in range(len(c) - 1)]
        matrix.append(valuations)
    return matrix

def aprox_v(s:int ,t:int ,k:int,matrix: List[List[float]]):
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

    >>> from fairpy.agents import PiecewiseConstantAgent
    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    >>> agents = [a, b]
    >>> c = [0, 0.8, 1.22, 1.506, 1.791, 2.383, 3]
    >>> matrix = get_players_valuation(agents, c)
    >>> aprox_v(0,5,0,matrix) #all the items according to player 0
    1.0
    >>> aprox_v(0,0,0,matrix) #the first item according to player 0
    0.2
    >>> round(aprox_v(0,1,1,matrix),3) #the first and the second items according to player 1 -> = 0.18400000000000002 + 0.20000000000000007
    0.384



    >>> matrix = [[1,2,3,4,5,6], [4,5,1,2,3, 0]]
    >>> aprox_v(0,6,0,matrix) #all the items according to player 0 -> = 1+2+3+4+5+6 = 21
    21
    >>> aprox_v(0,0,1,matrix) #the first item according to player 1 -> 4
    4
    >>> aprox_v(0,1,1,matrix) #the first and the second items according to player 1 -> 4+5 = 9
    9
    """
    if (s == -1):
        return 0
    valuations = matrix[k]
    return sum(valuations[s:t+1])


def V_without_k(s:int ,t:int , current_s:List[int] , current_t:List[int], matrix : List[List[float]], k:int):
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
    that means items 0,1,2 so the sum is 1+2+3 = 6

    >>> from fairpy.agents import PiecewiseConstantAgent
    >>> matrix = [[1,2,3,4,5,6], [4,5,1,2,3, 0]]
    >>> V_without_k(0,3, [0,3], [2,5], matrix, k=1)
    6


    #2 items, 0 and 1, player 0 holds item 0, player 1 holds item 1 and we calculate the value of items 0 and 1 according to player 0
    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25])
    >>> b = PiecewiseConstantAgent([0.23, 0.7, 0.07])
    >>> agents = [a, b]
    >>> c = [0, 0.8, 1.22, 1.506, 1.791, 2.383, 3]
    >>> matrix = get_players_valuation(agents, c)
    >>> round(V_without_k(0,1,[0,1],[0,1],matrix,0),3) #2 items, 0 and 1, player 0 holds item 0, player 1 holds item 1 and we calculate the value of the items
    0.2

    """



    sum = 0
    for i in range(s, t + 1):
        for j in range(len(matrix)):
            if (i <= current_t[j] and i >= current_s[j]):
                if (j != k):
                    sum += matrix[j][i]
    return sum


def maximize_expression(t:int , num_of_players:int , S:List[int], T:List[int], matrix:List[List[float]]):
    """
    because of the factor 2, the algorithm gives only approximation
    this function maximizes the expression:
    aprox_v(s, t, k, matrix) - 2*(aprox_v(S[k], T[k], k, matrix) + V(s,t,S,matrix))

    :param t: the last item
    :param num_of_players: number of players
    :param S: a list such that S[i] == which item {0,...,(num_of_items - 1)} is the first item of player i
    :param T: a list such that T[i] == which item {0,...,(num_of_items - 1)} is the last item of player i
    :param matrix: all the valuations of the players
    :return: params k' and s' that maximize the expression

    """
    max = -sys.maxsize - 1
    k_tag = 0
    s_tag = 0
    for k in range(num_of_players):
        for s in range(t + 1):
            v1 = aprox_v(s,t,k,matrix)  #the value of items s to t according to player k
            v2 = aprox_v(S[k], T[k], k, matrix)   #the value of items player k currently own
            v3 = V_without_k(s,t,S,T,matrix, k)   #the value of  all the parts from s to t that other players than k obtain
            net_value = v1 - 2 * (v2 + v3)   #value = aprox_v(s, t, k, matrix) - 2*(aprox_v(S[k], T[k], k, matrix) + V(s,t,S,matrix))
            logger.debug("Moving items %d..%d to player %d gains %f but loses %f+%f. Value-2cost=%f", s,t,k, v1,v2,v3,net_value)
            # logger.debug("The value of items player {} currently own = {}".format(k,v2))
            # logger.debug("the value of  all the parts from {} to {} that other players than {} obtain = {}".format(s,t,k,v3))
            # logger.debug("Value minus twice the cost = {}".format(net_value))
            if (net_value > max):
                max = net_value
                k_tag = k
                s_tag = s
    return [max, k_tag, s_tag]


def  discrete_utilitarian_welfare_approximation(matrix: List[List[float]], items:List[float]):

    """
    :param matrix: row i is the valuations of player i of the items
    :param items: the cuts to create the items
    :return: [S,T] s.t.
    S is a list such that S[i] == which item {0,...,(num_of_items - 1)} is the first item of player i
    and T is a list such that current_t[i] == which item {0,...,(num_of_items - 1)} is the last item of player i

    >>> discrete_utilitarian_welfare_approximation([[0.25, 0.25, 0.25, 0.25]], [0, 1.0, 1.5, 2.0, 3])
    [[0], [3]]

    >>> discrete_utilitarian_welfare_approximation([[0.125, 0.125, 0.25, 0.25, 0.25], [0.25, 0.25, 0.2, 0.2, 0.1]], [0, 0.5, 1.0, 1.5, 2.0, 3])
    [[1, 0], [4, 0]]
    """
    
    #we count the items from 0 so if there are 6 items, the first one is 0 and the last one is 5
    num_of_players = len(matrix)
    num_of_items = len(items) - 1
    S = [-1] * num_of_players
    T = [-1] * num_of_players

    #the main loop of the algorithm
    for t in range(0, num_of_items):
        logger.debug("------Iteration %d------",t)
        maximum = maximize_expression(t, num_of_players, S, T, matrix)
        logger.debug("Max net value is %f, for player k'=%d, s'=%f.\n", maximum[0], maximum[1], maximum[2])
        while maximum[0] >= 0:
            k_tag = maximum[1]
            s_tag = maximum[2]
            for i in range(num_of_players):
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

def divide(agents: List[Agent], epsilon:float) -> Allocation:
    """
    this function gets a list of agents and epsilon and returns an approximation of the division
    :param agents: the players
    :param epsilon: a float
    :return: starting points and end points of the cuts

    >>> from fairpy.agents import PiecewiseConstantAgent
    >>> a = PiecewiseConstantAgent([0.25, 0.5, 0.25], name="Alice")
    >>> b = PiecewiseConstantAgent([0.23, 0.7, 0.07], name="Bob")
    >>> round_allocation(divide([a,b], 0.2))
    Alice gets {(0, 0.8)} with value 0.2.
    Bob gets {(0.8, 1.791)} with value 0.6.
    <BLANKLINE>
    """
    logger.info("\nStep 1: Discretizing the cake to parts with value at most epsilon=%f",epsilon)
    items = discretization_procedure(agents, epsilon)
    logger.info("  Discretized cake: ")
    logger.info(items)

    logger.info("\nStep 2: Evaluation")
    matrix = get_players_valuation(agents, items)
    logger.info("  Agents' values: ")
    for line in matrix:
        logger.info(line)

    logger.info("\nStep 3: Discrete allocation")
    result = discrete_utilitarian_welfare_approximation(matrix, items)

    num_of_players = len(result[0])
    pieces = num_of_players*[None]
    for j in range(num_of_players):
        pieces[j] = [(items[result[0][j]], items[result[1][j] + 1])]
    return Allocation(agents,pieces)

if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))


